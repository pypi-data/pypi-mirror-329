use media_server_quic::common::AudioFrame;
use media_server_quic::transport::StreamClient;
use media_server_quic::video::source::{AudioChannel, DummySource, SourceState, VideoChannel};
use protobuf_types::media_streaming::H264Message;
use pyo3::prelude::*;
use pyo3_bytes::PyBytes;
use std::collections::HashMap;
use std::net::SocketAddr;
use std::sync::Arc;
use tokio::runtime::Runtime;
use tracing::{debug, error, info};

/// Initialize logging with debug level
fn init_logging() {
    use tracing_subscriber::{fmt, EnvFilter};
    let _ = fmt()
        .with_env_filter(
            EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| EnvFilter::new("media_streaming=debug,info")),
        )
        .with_thread_ids(true)
        .with_thread_names(true)
        .with_file(true)
        .with_line_number(true)
        .with_target(false)
        .try_init();
}

/// Python class for media streaming
#[pyclass]
struct MediaStreamingPy {
    runtime: Option<Runtime>,
    state: Option<Arc<SourceState>>,
    video_channel: Option<Arc<VideoChannel>>,
    audio_channel: Option<Arc<AudioChannel>>,
}

#[pymethods]
impl MediaStreamingPy {
    #[new]
    fn new() -> Self {
        debug!("Creating new MediaStreamingPy instance");
        init_logging();
        Self {
            runtime: None,
            state: None,
            video_channel: None,
            audio_channel: None,
        }
    }

    fn connect(&mut self, host: String, port: u16) -> PyResult<()> {
        debug!("Connecting to {}:{}", host, port);
        let runtime = Runtime::new().unwrap();

        // Move the runtime into the block_on closure
        let result = runtime.block_on(async {
            let addr: SocketAddr = format!("{}:{}", host, port).parse().map_err(|e| {
                error!("Failed to parse address: {}", e);
                PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Invalid address: {}", e))
            })?;

            // Create source and get state/channels
            let source = DummySource::new();
            let state = source.state();
            let video_channel = source.video_channel();
            let audio_channel = source.audio_channel();

            // Store state and channels
            self.state = Some(state.clone());
            self.video_channel = Some(video_channel.clone());
            self.audio_channel = Some(audio_channel.clone());

            // Create client with source
            let mut client = StreamClient::new(Box::new(source)).map_err(|e| {
                error!("Failed to create client: {}", e);
                PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!(
                    "Failed to create client: {}",
                    e
                ))
            })?;

            // Start client connection
            let state_clone = state.clone();
            tokio::spawn(async move {
                if let Err(e) = client.connect(addr).await {
                    error!("Connection failed: {}", e);
                }
                state_clone.set_running(false);
            });

            // Start the source
            state.set_running(true);

            info!("Successfully connected and started media source");
            Ok::<(), PyErr>(())
        });

        // Store the runtime after successful connection setup
        self.runtime = Some(runtime);
        result
    }

    #[pyo3(signature = (data, timestamp=None, width=None, height=None, is_keyframe=None, metadata=None))]
    fn add_frame(
        &self,
        _py: Python<'_>,
        data: PyBytes,
        timestamp: Option<u64>,
        width: Option<u32>,
        height: Option<u32>,
        is_keyframe: Option<bool>,
        metadata: Option<HashMap<String, String>>,
    ) -> PyResult<bool> {
        let state = self.state.as_ref().ok_or_else(|| {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Not connected to server")
        })?;

        if !state.is_running() {
            return Ok(false);
        }

        // Get the underlying bytes without copying
        let bytes = data.into_inner();

        // Create H264Message with data from buffer
        let frame = H264Message {
            data: bytes.to_vec(), // Still need one copy for protobuf
            timestamp: timestamp.unwrap_or_else(|| state.get_frame_count()),
            frame_type: if is_keyframe.unwrap_or(false) { 1 } else { 2 },
            metadata: metadata.unwrap_or_default(),
            width: Some(width.unwrap_or(1920)),
            height: Some(height.unwrap_or(1080)),
        };

        // Try to send frame
        if let Some(video_channel) = &self.video_channel {
            match video_channel.tx.try_send(frame) {
                Ok(_) => {
                    state.increment_frame_count();
                    Ok(true)
                }
                Err(_) => Ok(false),
            }
        } else {
            Ok(false)
        }
    }

    #[pyo3(signature = (data, timestamp=None))]
    fn add_audio_frame(&self, data: &[u8], timestamp: Option<u64>) -> PyResult<bool> {
        let state = self.state.as_ref().ok_or_else(|| {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Not connected to server")
        })?;

        if !state.is_running() {
            return Ok(false);
        }

        let frame = AudioFrame {
            data: data.to_vec(),
            timestamp: timestamp.unwrap_or_else(|| state.get_frame_count() * 1000),
        };

        // Try to send frame
        if let Some(audio_channel) = &self.audio_channel {
            match audio_channel.tx.try_send(frame) {
                Ok(_) => Ok(true),
                Err(_) => Ok(false),
            }
        } else {
            Ok(false)
        }
    }

    fn disconnect(&mut self) -> PyResult<()> {
        debug!("Disconnecting media streaming client");
        if let Some(runtime) = &self.runtime {
            runtime.block_on(async {
                // Stop the source
                if let Some(state) = &self.state {
                    state.set_running(false);
                }

                debug!("Successfully stopped media source");
                Ok::<(), PyErr>(())
            })?;
        }
        self.state = None;
        self.video_channel = None;
        self.audio_channel = None;
        self.runtime = None;
        info!("Successfully disconnected media streaming client");
        Ok(())
    }

    /// Get the current frame count
    fn frame_count(&self) -> PyResult<u64> {
        let state = self.state.as_ref().ok_or_else(|| {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Not connected to server")
        })?;
        Ok(state.get_frame_count())
    }

    /// Check if the source is running
    fn is_running(&self) -> PyResult<bool> {
        let state = self.state.as_ref().ok_or_else(|| {
            PyErr::new::<pyo3::exceptions::PyRuntimeError, _>("Not connected to server")
        })?;
        Ok(state.is_running())
    }
}

/// This module provides Python bindings for the media streaming client.
/// It allows streaming H264-encoded video frames over QUIC.
#[pymodule]
fn media_server_client_quic(m: &Bound<'_, PyModule>) -> PyResult<()> {
    debug!("Initializing media_streaming Python module");
    m.add_class::<MediaStreamingPy>()?;
    Ok(())
}
