use anyhow::Result;
use crate::common::{AudioFrame, MediaSource, ConnectionEvents, StreamType};
use protobuf_types::media_streaming::H264Message;
use async_trait::async_trait;
use tracing::{warn, info};
use flume::{Sender, Receiver, bounded};
use std::collections::HashMap;
use std::sync::Arc;
use std::sync::atomic::{AtomicU64, AtomicBool, Ordering};

// Channel sizes (in number of frames)
const VIDEO_CHANNEL_SIZE: usize = 4; // Only keep last ~133ms of video (at 30fps)
const AUDIO_CHANNEL_SIZE: usize = 8; // Only keep last ~160ms of audio (at 50Hz)

pub struct VideoChannel {
    pub tx: Sender<H264Message>,
    pub rx: Receiver<H264Message>,
}

impl VideoChannel {
    pub fn new() -> Self {
        let (tx, rx) = bounded(VIDEO_CHANNEL_SIZE);
        Self { tx, rx }
    }

    pub fn clone_sender(&self) -> Sender<H264Message> {
        self.tx.clone()
    }

    pub fn subscribe(&self) -> Receiver<H264Message> {
        self.rx.clone()
    }
}

impl Default for VideoChannel {
    fn default() -> Self {
        Self::new()
    }
}

pub struct AudioChannel {
    pub tx: Sender<AudioFrame>,
    pub rx: Receiver<AudioFrame>,
}

impl AudioChannel {
    pub fn new() -> Self {
        let (tx, rx) = bounded(AUDIO_CHANNEL_SIZE);
        Self { tx, rx }
    }

    pub fn clone_sender(&self) -> Sender<AudioFrame> {
        self.tx.clone()
    }

    pub fn subscribe(&self) -> Receiver<AudioFrame> {
        self.rx.clone()
    }
}

impl Default for AudioChannel {
    fn default() -> Self {
        Self::new()
    }
}

pub struct SourceState {
    frame_count: AtomicU64,
    running: AtomicBool,
    connected: AtomicBool,
}

impl SourceState {
    pub fn new() -> Self {
        Self {
            frame_count: AtomicU64::new(0),
            running: AtomicBool::new(false),
            connected: AtomicBool::new(false),
        }
    }

    pub fn increment_frame_count(&self) -> u64 {
        self.frame_count.fetch_add(1, Ordering::SeqCst)
    }

    pub fn get_frame_count(&self) -> u64 {
        self.frame_count.load(Ordering::SeqCst)
    }

    pub fn set_running(&self, running: bool) {
        self.running.store(running, Ordering::SeqCst)
    }

    pub fn is_running(&self) -> bool {
        self.running.load(Ordering::SeqCst)
    }

    pub fn set_connected(&self, connected: bool) {
        self.connected.store(connected, Ordering::SeqCst)
    }

    pub fn is_connected(&self) -> bool {
        self.connected.load(Ordering::SeqCst)
    }
}

impl Default for SourceState {
    fn default() -> Self {
        Self::new()
    }
}

pub struct DummySource {
    state: Arc<SourceState>,
    video_channel: Arc<VideoChannel>,
    audio_channel: Arc<AudioChannel>,
    start_time: Option<std::time::Instant>,
    last_stats_time: Option<std::time::Instant>,
    bytes_sent: u64,
}

impl Default for DummySource {
    fn default() -> Self {
        Self::new()
    }
}

impl DummySource {
    pub fn new() -> Self {
        Self {
            state: Arc::new(SourceState::new()),
            video_channel: Arc::new(VideoChannel::new()),
            audio_channel: Arc::new(AudioChannel::new()),
            start_time: None,
            last_stats_time: None,
            bytes_sent: 0,
        }
    }

    /// Add a video frame to the stream
    pub fn add_frame(&mut self, frame: H264Message, is_keyframe: bool) -> bool {
        if !self.state.is_running() {
            return false;
        }

        // Initialize timing if not done yet
        if self.start_time.is_none() {
            self.start_time = Some(std::time::Instant::now());
            self.last_stats_time = self.start_time;
        }

        let frame_size = frame.data.len();

        if is_keyframe {
            let frame_count = self.state.get_frame_count();
            info!("Sending keyframe {} - Size: {:.2}KB", frame_count, frame_size as f64 / 1024.0);
        }

        // Try to send frame, if channel is full it will drop oldest frame
        match self.video_channel.tx.try_send(frame) {
            Ok(_) => {
                self.bytes_sent += frame_size as u64;
                self.state.increment_frame_count();

                // Print statistics every 5 seconds
                let now = std::time::Instant::now();
                if let Some(last_stats) = self.last_stats_time {
                    if now.duration_since(last_stats).as_secs() >= 5 {
                        let elapsed = now.duration_since(self.start_time.unwrap()).as_secs_f64();
                        let frame_count = self.state.get_frame_count();
                        let actual_fps = frame_count as f64 / elapsed;
                        let mbps = (self.bytes_sent as f64 * 8.0) / (elapsed * 1_000_000.0);
                        
                        info!(
                            "Streaming stats - Frames: {}, Avg FPS: {:.2}, Bitrate: {:.2} Mbps",
                            frame_count, actual_fps, mbps
                        );
                        self.last_stats_time = Some(now);
                    }
                }
                true
            }
            Err(flume::TrySendError::Full(_)) => {
                // Channel full - frame dropped (expected in real-time streaming)
                self.state.increment_frame_count(); // Still increment to maintain timestamp sequence
                false
            }
            Err(e) => {
                warn!("Failed to send video frame: {}", e);
                false
            }
        }
    }

    /// Add an audio frame to the stream
    pub fn add_audio_frame(&mut self, frame: AudioFrame) -> bool {
        if !self.state.is_running() {
            return false;
        }

        // Try to send frame, if channel is full it will drop oldest frame
        match self.audio_channel.tx.try_send(frame) {
            Ok(_) => true,
            Err(flume::TrySendError::Full(_)) => false, // Frame dropped
            Err(e) => {
                warn!("Failed to send audio frame: {}", e);
                false
            }
        }
    }

    /// Get the current frame count
    pub fn frame_count(&self) -> u64 {
        self.state.get_frame_count()
    }

    /// Check if the source is running
    pub fn is_running(&self) -> bool {
        self.state.is_running()
    }

    /// Get a reference to the state
    pub fn state(&self) -> Arc<SourceState> {
        self.state.clone()
    }

    /// Get a clone of the video channel
    pub fn video_channel(&self) -> Arc<VideoChannel> {
        self.video_channel.clone()
    }

    /// Get a clone of the audio channel
    pub fn audio_channel(&self) -> Arc<AudioChannel> {
        self.audio_channel.clone()
    }
}

#[async_trait]
impl MediaSource for DummySource {
    fn video_channel(&self) -> &VideoChannel {
        &self.video_channel
    }

    fn audio_channel(&self) -> &AudioChannel {
        &self.audio_channel
    }

    async fn start(&mut self) -> Result<()> {
        self.state.set_running(true);
        Ok(())
    }

    async fn stop(&mut self) -> Result<()> {
        self.state.set_running(false);
        Ok(())
    }
}

#[async_trait]
impl ConnectionEvents for DummySource {
    async fn on_connect(&mut self) -> Result<()> {
        info!("DummySource connected");
        self.state.set_connected(true);
        Ok(())
    }

    async fn on_disconnect(&mut self) -> Result<()> {
        info!("DummySource disconnected");
        self.state.set_connected(false);
        Ok(())
    }

    async fn on_auth_success(&mut self, client_id: u64) -> Result<()> {
        info!("DummySource authenticated with client_id: {}", client_id);
        Ok(())
    }

    async fn on_auth_failure(&mut self, error: String) -> Result<()> {
        warn!("DummySource authentication failed: {}", error);
        Ok(())
    }

    async fn on_stream_ready(&mut self, stream_type: StreamType) -> Result<()> {
        info!("DummySource stream ready: {:?}", stream_type);
        Ok(())
    }

    async fn on_stream_error(&mut self, stream_type: StreamType, error: String) -> Result<()> {
        warn!("DummySource stream error for {:?}: {}", stream_type, error);
        Ok(())
    }
}

impl Clone for DummySource {
    fn clone(&self) -> Self {
        Self {
            state: self.state.clone(),
            video_channel: self.video_channel.clone(),
            audio_channel: self.audio_channel.clone(),
            start_time: self.start_time,
            last_stats_time: self.last_stats_time,
            bytes_sent: self.bytes_sent,
        }
    }
}

/// A video source that allows external frame injection
pub struct BufferedVideoSource {
    running: bool,
    frame_count: u64,
    video_channel: VideoChannel,
    audio_channel: AudioChannel,
}

impl Default for BufferedVideoSource {
    fn default() -> Self {
        Self::new()
    }
}

impl BufferedVideoSource {
    pub fn new() -> Self {
        Self {
            running: false,
            frame_count: 0,
            video_channel: VideoChannel::new(),
            audio_channel: AudioChannel::new(),
        }
    }

    /// Add a video frame to the stream
    /// 
    /// # Arguments
    /// * `data` - Raw H264 frame data
    /// * `timestamp` - Optional timestamp in microseconds. If None, will use frame_count
    /// * `width` - Optional frame width. If None, defaults to 1920
    /// * `height` - Optional frame height. If None, defaults to 1080
    /// * `is_keyframe` - Whether this frame is a keyframe. If None, defaults to false
    /// * `metadata` - Optional metadata to attach to the frame
    pub fn add_frame(
        &mut self,
        data: Vec<u8>,
        timestamp: Option<u64>,
        width: Option<u32>,
        height: Option<u32>,
        is_keyframe: Option<bool>,
        metadata: Option<HashMap<String, String>>,
    ) -> bool {
        if !self.running {
            return false;
        }

        let frame = H264Message {
            data,
            timestamp: timestamp.unwrap_or(self.frame_count),
            frame_type: if is_keyframe.unwrap_or(false) { 1 } else { 2 },
            metadata: metadata.unwrap_or_default(),
            width: Some(width.unwrap_or(1920)),
            height: Some(height.unwrap_or(1080)),
        };

        // Try to send frame, if channel is full it will drop oldest frame
        match self.video_channel.tx.try_send(frame) {
            Ok(_) => {
                self.frame_count += 1;
                true
            }
            Err(flume::TrySendError::Full(_)) => {
                // Channel full - frame dropped (expected in real-time streaming)
                self.frame_count += 1; // Still increment to maintain timestamp sequence
                false
            }
            Err(e) => {
                warn!("Failed to send video frame: {}", e);
                false
            }
        }
    }

    /// Add an audio frame to the stream
    pub fn add_audio_frame(&mut self, data: Vec<u8>, timestamp: Option<u64>) -> bool {
        if !self.running {
            return false;
        }

        let frame = AudioFrame {
            data,
            timestamp: timestamp.unwrap_or(self.frame_count * 1000),
        };

        // Try to send frame, if channel is full it will drop oldest frame
        match self.audio_channel.tx.try_send(frame) {
            Ok(_) => true,
            Err(flume::TrySendError::Full(_)) => false, // Frame dropped
            Err(e) => {
                warn!("Failed to send audio frame: {}", e);
                false
            }
        }
    }

    /// Get the current frame count
    pub fn frame_count(&self) -> u64 {
        self.frame_count
    }

    /// Check if the source is running
    pub fn is_running(&self) -> bool {
        self.running
    }
}

#[async_trait]
impl MediaSource for BufferedVideoSource {
    fn video_channel(&self) -> &VideoChannel {
        &self.video_channel
    }

    fn audio_channel(&self) -> &AudioChannel {
        &self.audio_channel
    }

    async fn start(&mut self) -> Result<()> {
        self.running = true;
        Ok(())
    }

    async fn stop(&mut self) -> Result<()> {
        self.running = false;
        Ok(())
    }
}

#[async_trait]
impl ConnectionEvents for BufferedVideoSource {
    async fn on_connect(&mut self) -> Result<()> {
        info!("BufferedVideoSource connected");
        Ok(())
    }

    async fn on_disconnect(&mut self) -> Result<()> {
        info!("BufferedVideoSource disconnected");
        self.running = false;
        Ok(())
    }

    async fn on_auth_success(&mut self, client_id: u64) -> Result<()> {
        info!("BufferedVideoSource authenticated with client_id: {}", client_id);
        Ok(())
    }

    async fn on_auth_failure(&mut self, error: String) -> Result<()> {
        warn!("BufferedVideoSource authentication failed: {}", error);
        Ok(())
    }

    async fn on_stream_ready(&mut self, stream_type: StreamType) -> Result<()> {
        info!("BufferedVideoSource stream ready: {:?}", stream_type);
        Ok(())
    }

    async fn on_stream_error(&mut self, stream_type: StreamType, error: String) -> Result<()> {
        warn!("BufferedVideoSource stream error for {:?}: {}", stream_type, error);
        Ok(())
    }
}

impl Clone for BufferedVideoSource {
    fn clone(&self) -> Self {
        Self {
            running: self.running,
            frame_count: self.frame_count,
            video_channel: VideoChannel {
                tx: self.video_channel.clone_sender(),
                rx: self.video_channel.subscribe(),
            },
            audio_channel: AudioChannel {
                tx: self.audio_channel.clone_sender(),
                rx: self.audio_channel.subscribe(),
            },
        }
    }
} 