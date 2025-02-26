use crate::common::{AudioFrame, MediaSink};
use crate::MediaEvent;
use protobuf_types::media_streaming::H264Message;
use anyhow::Result;
use tracing::{info, trace};
use async_trait::async_trait;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;
use tokio::sync::mpsc::Sender;
use decoder_engine::nvdec::NvidiaDecoder;
use decoder_engine::decoder::VideoDecoder;
use crate::transport::IntoNewbringer;

#[derive(Debug, Default, Clone)]
pub struct NullSink;

#[async_trait]
impl MediaSink for NullSink {
    async fn handle_video(&mut self, _frame: H264Message, _stream_id: u64) -> Result<()> {
        Ok(())
    }

    async fn handle_audio(&mut self, _frame: AudioFrame, _stream_id: u64) -> Result<()> {
        Ok(())
    }

    async fn on_auth(&mut self, _: String, _: String, _: Vec<u8>, _: u64) -> Result<bool> {
        info!("NullSink on_auth");
        Ok(true) // Always accept auth in null sink
    }

    async fn on_client_disconnect(&mut self, stream_id: u64) -> Result<()> {
        info!("NullSink client {} disconnected", stream_id);
        Ok(())
    }
}

#[derive(Default, Clone)]
pub struct TestSink {
    video_frames: Arc<AtomicU64>,
    audio_frames: Arc<AtomicU64>,
}

impl TestSink {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn video_frames(&self) -> u64 {
        self.video_frames.load(Ordering::Relaxed)
    }

    pub fn audio_frames(&self) -> u64 {
        self.audio_frames.load(Ordering::Relaxed)
    }
}

#[async_trait]
impl MediaSink for TestSink {
    async fn handle_video(&mut self, frame: H264Message, stream_id: u64) -> Result<()> {
        let count = self.video_frames.fetch_add(1, Ordering::Relaxed);
        trace!(
            "Received video frame {} from stream {}: {}x{}, type={}, size={}",
            count,
            stream_id,
            frame.width.unwrap_or(0),
            frame.height.unwrap_or(0),
            frame.frame_type,
            frame.data.len()
        );
        Ok(())
    }

    async fn handle_audio(&mut self, frame: AudioFrame, stream_id: u64) -> Result<()> {
        let count = self.audio_frames.fetch_add(1, Ordering::Relaxed);
        trace!(
            "Received audio frame {} from stream {}: size={}",
            count,
            stream_id,
            frame.data.len()
        );
        Ok(())
    }

    async fn on_auth(&mut self, auth: String, serial: String, sign: Vec<u8>, stream_id: u64) -> Result<bool> {
        info!(
            "Auth request - auth: {}, serial: {}, sign: {} bytes, stream_id: {}",
            auth,
            serial,
            sign.len(),
            stream_id
        );
        // Accept all auth requests in test sink
        Ok(true)
    }

    async fn on_client_disconnect(&mut self, stream_id: u64) -> Result<()> {
        info!("TestSink client {} disconnected", stream_id);
        Ok(())
    }
}

 pub struct DecoderSink {
    decoder: Arc<tokio::sync::Mutex<NvidiaDecoder>>,
    event_tx: Sender<MediaEvent>,
}

impl DecoderSink {
    pub fn new(decoder: Arc<tokio::sync::Mutex<NvidiaDecoder>>, event_tx: Sender<MediaEvent>) -> Self {
        Self {
            decoder,
            event_tx,
        }
    }
}

#[async_trait]
impl MediaSink for DecoderSink {
    async fn handle_video(&mut self, frame: H264Message, stream_id: u64) -> Result<()> {
        // Forward the H264 frame to event handler first
        trace!("Received H264 frame from stream {}", stream_id);

        // print first 16 bytes of frame.data
        trace!("First 16 bytes of frame.data: {:?}", &frame.data[..16]);

        self.event_tx.send(MediaEvent::H264Frame(frame.clone(), stream_id)).await
            .map_err(|e| anyhow::anyhow!("Failed to send H264 frame event: {}", e))?;

        // Send frame to decoder
        let mut decoder = self.decoder.lock().await;
        decoder.decode(nvcodec::input_video_frame::InputVideoFrame {
            data: frame.into_newbringer(),
            stream_id,
        }).await.map_err(|e| anyhow::anyhow!("Failed to decode frame: {}", e))?;

        Ok(())
    }

    async fn handle_audio(&mut self, _frame: AudioFrame, _stream_id: u64) -> Result<()> {
        // For now, we just ignore audio frames since we're focusing on video
        Ok(())
    }

    async fn on_auth(&mut self, auth: String, serial: String, sign: Vec<u8>, stream_id: u64) -> Result<bool> {
        info!(
            "Auth request - auth: {}, serial: {}, sign: {} bytes, stream_id: {}",
            auth,
            serial,
            sign.len(),
            stream_id
        );

        // Send client connected event
        self.event_tx.send(MediaEvent::ClientConnected(stream_id)).await
            .map_err(|e| anyhow::anyhow!("Failed to send client connected event: {}", e))?;

        Ok(true)
    }

    async fn on_client_disconnect(&mut self, stream_id: u64) -> Result<()> {
        // Send client disconnected event
        self.event_tx.send(MediaEvent::ClientDisconnected(stream_id)).await
            .map_err(|e| anyhow::anyhow!("Failed to send client disconnected event: {}", e))?;
        
        info!("Client {} disconnected", stream_id);
        Ok(())
    }
}

impl Clone for DecoderSink {
    fn clone(&self) -> Self {
        Self {
            decoder: Arc::clone(&self.decoder),
            event_tx: self.event_tx.clone(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_null_sink() {
        let mut sink = NullSink::default();
        let video_frame = H264Message {
            data: vec![0; 320 * 240 * 3 / 2],
            timestamp: 0,
            frame_type: 1,
            metadata: Default::default(),
            width: Some(320),
            height: Some(240),
        };
        let audio_frame = AudioFrame {
            timestamp: 0,
            data: vec![0; 1024],
        };
        assert!(sink.handle_video(video_frame, 1).await.is_ok());
        assert!(sink.handle_audio(audio_frame, 1).await.is_ok());
        assert!(sink.on_client_disconnect(1).await.is_ok());
    }

    #[tokio::test]
    async fn test_test_sink() {
        let mut sink = TestSink::default();
        
        // Test video frame handling
        let video_frame = H264Message {
            data: vec![0; 320 * 240 * 3 / 2],
            timestamp: 0,
            frame_type: 1,
            metadata: Default::default(),
            width: Some(320),
            height: Some(240),
        };
        assert!(sink.handle_video(video_frame, 1).await.is_ok());
        assert_eq!(sink.video_frames(), 1);

        // Test audio frame handling
        let audio_frame = AudioFrame {
            timestamp: 0,
            data: vec![0; 1024],
        };
        assert!(sink.handle_audio(audio_frame, 1).await.is_ok());
        assert_eq!(sink.audio_frames(), 1);
        assert!(sink.on_client_disconnect(1).await.is_ok());
    }
} 