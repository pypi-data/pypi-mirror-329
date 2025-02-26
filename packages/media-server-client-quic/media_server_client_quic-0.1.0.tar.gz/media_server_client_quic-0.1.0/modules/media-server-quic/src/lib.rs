pub mod common;
pub mod protocol;
pub mod transport;
pub mod video;

#[cfg(test)]
mod tests;

use crate::transport::{IntoMediaStreaming, StreamServer};
use crate::video::sink::DecoderSink;
pub use decoder_engine::decoder::DecodedFrame;
use shared_utils::env_config::game_engine::Settings;
use std::net::SocketAddr;
use std::sync::Arc;
use tokio::sync::mpsc;
use tokio_util::sync::CancellationToken;
use tracing::{info, warn};

use decoder_engine::decoder::VideoDecoder;
use decoder_engine::NvidiaDecoder;
use futures::StreamExt;

pub type StreamId = u64;

#[derive(Debug)]
pub struct FrameData {
    pub decoded: DecodedFrame,
    pub encoded: protobuf_types::media_streaming::H264Message,
    pub stream_id: StreamId,
}

#[derive(Debug)]
pub enum ServerCommand {
    DisconnectClient(StreamId),
}

#[derive(Debug)]
pub enum MediaEvent {
    Frame(FrameData),
    ClientConnected(StreamId),
    ClientDisconnected(StreamId),
    H264Frame(protobuf_types::media_streaming::H264Message, StreamId),
}

pub type MediaEventHandler = Box<dyn FnMut(MediaEvent) -> anyhow::Result<()> + Send>;

pub async fn run_server(
    settings: Arc<Settings>,
    event_handler: Option<MediaEventHandler>,
    command_rx: Option<mpsc::Receiver<ServerCommand>>,
    cancel_token: CancellationToken,
) -> anyhow::Result<()> {
    // Initialize logging with file and line numbers
    tracing_subscriber::fmt()
        .with_env_filter("debug,sqlx=warn,hyper=warn,reqwest=warn,tower=warn,h2=warn,rustls=warn")
        .with_file(true)
        .with_line_number(true)
        .with_thread_ids(true)
        .with_target(true)
        .try_init()
        .ok();

    // Create event channels
    let (event_tx, event_rx) = mpsc::channel(32);

    // Get port from settings and create address
    let port = settings.game_engine.stream_port;
    let addr: SocketAddr = format!("{}:{}", settings.game_engine.bind_address, port).parse()?;

    // Create and initialize decoder
    let mut decoder =
        NvidiaDecoder::new().map_err(|e| anyhow::anyhow!("Failed to initialize decoder: {}", e))?;
    let (_dec_cmd_tx, mut frame_stream) = decoder.start().await;
    let decoder = Arc::new(tokio::sync::Mutex::new(decoder));

    // Create media server with DecoderSink
    let sink = DecoderSink::new(decoder.clone(), event_tx.clone());
    let server = StreamServer::new(addr, sink)?;
    let server = Arc::new(tokio::sync::Mutex::new(server));

    // Process events from decoder and forward them to handler
    let event_handle = if let Some(mut handler) = event_handler {
        let mut event_rx = event_rx; // Move event_rx into the task
        Some(tokio::spawn(async move {
            while let Some(event) = event_rx.recv().await {
                if let Err(e) = handler(event) {
                    warn!("Event handler error: {}", e);
                }
            }
        }))
    } else {
        // If no handler provided, still need to drain the channel
        let mut event_rx = event_rx; // Move event_rx into the task
        Some(tokio::spawn(async move {
            while let Some(_) = event_rx.recv().await {
                // Drain events
            }
        }))
    };

    // Handle server commands
    if let Some(mut command_rx) = command_rx {
        let server_clone = Arc::clone(&server);
        tokio::spawn(async move {
            while let Some(command) = command_rx.recv().await {
                match command {
                    ServerCommand::DisconnectClient(stream_id) => {
                        if let Err(e) = server_clone.lock().await.disconnect_client(stream_id).await
                        {
                            warn!("Failed to disconnect client {}: {}", stream_id, e);
                        }
                    }
                }
            }
        });
    }

    // Process decoded frames
    let frame_handle = tokio::spawn(async move {
        while let Some(result) = frame_stream.next().await {
            match result {
                Ok(Some(frame)) => {
                    info!("Received decoded frame from stream {}", frame.stream_id);
                    let frame_data = FrameData {
                        decoded: DecodedFrame {
                            ticket: frame.ticket,
                            stream_id: frame.stream_id,
                            device_image: frame.device_image,
                        },
                        encoded: frame.encoded_frame.into_media_streaming(),
                        stream_id: frame.stream_id,
                    };

                    if let Err(e) = event_tx.send(MediaEvent::Frame(frame_data)).await {
                        warn!("Failed to send frame event: {}", e);
                    }
                }
                Ok(None) => break,
                Err(e) => warn!("Frame processing error: {}", e),
            }
        }
    });

    // Start server
    let server_handle = tokio::spawn({
        let server = Arc::clone(&server);
        async move {
            let mut server = server.lock().await;
            server.run().await
        }
    });

    // Wait for shutdown signal
    let _ = cancel_token.cancelled().await;

    // Wait for tasks to complete
    let _ = tokio::join!(frame_handle);
    if let Some(handle) = event_handle {
        let _ = handle.await;
    }

    // Stop server
    server_handle.abort();
    let _ = server_handle.await;

    Ok(())
}

pub use common::{
    AudioFrame, ControlPacket, MediaPacket, MediaSink, MediaSource, NetworkStats, StreamStats,
    StreamType, IDLE_TIMEOUT, KEYFRAME_INTERVAL, MAX_CONCURRENT_STREAMS, STATS_INTERVAL,
    STREAM_CHUNK_SIZE, TARGET_FPS, TEST_CLIENT_COUNT,
};

pub use transport::StreamClient;
