use anyhow::Result;
use futures::future::select_all;
use std::net::SocketAddr;
use std::sync::Arc;
use std::time::Duration;
use tokio::sync::broadcast;
use tokio::sync::Mutex;
use tokio::task::JoinHandle;
use tokio::time::Instant;
use tracing::{error, info};

use crate::common::{MediaSource, StreamStats, StreamType};
use crate::transport::packet::{ControlPacket, MediaPacket};
use crate::transport::packet_io::PacketIO;

use super::config::configure_client;
use super::handlers::{handle_audio_stream, handle_keep_alive, handle_video_stream, monitor_stats};

const STREAM_SETUP_TIMEOUT: Duration = Duration::from_secs(5);

pub struct StreamClient {
    endpoint: quinn::Endpoint,
    client_id: u64,
    media_source: Option<Box<dyn MediaSource>>,
    stats: Arc<Mutex<StreamStats>>,
    shutdown: broadcast::Sender<()>,
}

pub struct ConnectionHandle {
    task: JoinHandle<Result<()>>,
    shutdown: broadcast::Sender<()>,
}

impl ConnectionHandle {
    pub async fn shutdown(self) -> Result<()> {
        let _ = self.shutdown.send(());
        self.task.await?
    }

    /// Wait for the connection to complete, either due to error or graceful shutdown
    pub async fn wait(&mut self) -> Result<Result<()>> {
        let task = std::mem::replace(&mut self.task, tokio::task::spawn(async { Ok(()) }));
        Ok(task.await?)
    }
}

impl StreamClient {
    pub fn new(media_source: Box<dyn MediaSource>) -> Result<Self> {
        let mut endpoint = quinn::Endpoint::client("0.0.0.0:0".parse()?)?;
        endpoint.set_default_client_config(configure_client()?);
        let (shutdown, _) = broadcast::channel(1);
        Ok(Self {
            endpoint,
            client_id: 0,
            media_source: Some(media_source),
            stats: Arc::new(Mutex::new(StreamStats::new())),
            shutdown,
        })
    }

    async fn wait_for_ack(recv: &mut quinn::RecvStream, expected_type: StreamType) -> Result<()> {
        let mut packet_io = PacketIO::new();
        match packet_io.read_packet(recv).await? {
            Some(MediaPacket::Control(ControlPacket::StartStream { stream_type }))
                if stream_type == expected_type =>
            {
                Ok(())
            }
            _ => anyhow::bail!("Invalid or missing ack packet"),
        }
    }

    async fn setup_stream(
        connection: &quinn::Connection,
        stream_type: StreamType,
    ) -> Result<(quinn::SendStream, quinn::RecvStream)> {
        let (mut send, mut recv) = connection.open_bi().await?;
        let mut packet_io = PacketIO::new();

        let start = MediaPacket::Control(ControlPacket::StartStream { stream_type });
        packet_io.write_packet(&mut send, &start).await?;

        tokio::time::timeout(
            STREAM_SETUP_TIMEOUT,
            Self::wait_for_ack(&mut recv, stream_type),
        )
        .await??;

        Ok((send, recv))
    }

    async fn perform_hello_handshake(
        connection: &quinn::Connection,
        _source: &mut Box<dyn MediaSource>,
    ) -> Result<String> {
        let (mut send, mut recv) = connection.open_bi().await?;
        let mut packet_io = PacketIO::new();

        // Send client hello
        let client_hello = MediaPacket::Control(ControlPacket::Hello {
            version: 1,
            nonce: None,
            capabilities: vec!["h264".to_string(), "opus".to_string()],
            client_id: None,
        });
        info!("Sending client hello");
        packet_io.write_packet(&mut send, &client_hello).await?;

        // Wait for server hello
        match packet_io.read_packet(&mut recv).await? {
            Some(MediaPacket::Control(ControlPacket::Hello {
                version,
                nonce,
                capabilities,
                client_id,
            })) => {
                info!("Received server hello - version: {}, nonce: {:?}, capabilities: {:?}, client_id: {:?}", 
                    version, nonce, capabilities, client_id);

                if version != 1 {
                    return Err(anyhow::anyhow!("Unsupported protocol version: {}", version));
                }

                Ok(nonce.unwrap_or_default())
            }
            _ => Err(anyhow::anyhow!("Invalid or missing server hello")),
        }
    }

    async fn perform_auth(connection: &quinn::Connection, nonce: &str) -> Result<()> {
        let (mut send, mut recv) = connection.open_bi().await?;
        let mut packet_io = PacketIO::new();

        // Send auth
        let auth = MediaPacket::Control(ControlPacket::Auth {
            auth: "test-auth".to_string(),
            serial: "test-serial".to_string(),
            sign: nonce.as_bytes().to_vec(),
            stream_id: 1,
        });
        info!("Sending auth request");
        packet_io.write_packet(&mut send, &auth).await?;

        // Wait for auth response
        match packet_io.read_packet(&mut recv).await? {
            Some(MediaPacket::Control(ControlPacket::AuthResponse {
                success, message, ..
            })) => {
                if success {
                    info!("Auth successful");
                    Ok(())
                } else {
                    Err(anyhow::anyhow!(
                        "Auth failed: {}",
                        message.unwrap_or_default()
                    ))
                }
            }
            _ => Err(anyhow::anyhow!("Invalid or missing auth response")),
        }
    }

    pub async fn connect(&mut self, server_addr: SocketAddr) -> Result<ConnectionHandle> {
        info!("Starting connection to server at {}", server_addr);

        // Take ownership of the media source
        let mut source = self
            .media_source
            .take()
            .ok_or_else(|| anyhow::anyhow!("No media source available"))?;

        // Start the media source immediately
        source.start().await?;
        source.on_connect().await?;

        // Clone necessary components for the connection task
        let endpoint = self.endpoint.clone();
        let stats = self.stats.clone();
        let shutdown = self.shutdown.clone();
        let client_id = self.client_id;

        // Spawn the connection handling task
        let task = tokio::spawn(async move {
            let result: Result<()> = async {
                let connection = endpoint.connect(server_addr, "localhost")?.await?;

                // Perform hello handshake first
                let nonce = Self::perform_hello_handshake(&connection, &mut source).await?;

                // Perform auth
                Self::perform_auth(&connection, &nonce).await?;
                source.on_auth_success(client_id).await?;

                // Setup streams
                let (video_send, _) = Self::setup_stream(&connection, StreamType::Video).await?;
                source.on_stream_ready(StreamType::Video).await?;

                let (audio_send, _) = Self::setup_stream(&connection, StreamType::Audio).await?;
                source.on_stream_ready(StreamType::Audio).await?;

                let (keep_alive_send, keep_alive_recv) =
                    Self::setup_stream(&connection, StreamType::KeepAlive).await?;
                source.on_stream_ready(StreamType::KeepAlive).await?;

                // Get channels for streaming
                let video_rx = source.video_channel().subscribe();
                let audio_rx = source.audio_channel().subscribe();

                let mut shutdown_rx = shutdown.subscribe();
                let start = Instant::now();

                let mut handles = vec![
                    tokio::spawn(handle_video_stream(
                        video_send,
                        video_rx,
                        stats.clone(),
                        start,
                    )),
                    tokio::spawn(handle_audio_stream(
                        audio_send,
                        audio_rx,
                        stats.clone(),
                        start,
                    )),
                    tokio::spawn(handle_keep_alive(
                        client_id,
                        keep_alive_send,
                        keep_alive_recv,
                        stats.clone(),
                    )),
                    tokio::spawn(monitor_stats(stats.clone(), client_id)),
                ];

                tokio::select! {
                    result = select_all(handles.split_off(0)) => {
                        let (result, _, remaining) = result;
                        if let Err(e) = result {
                            error!("Task failed: {}", e);
                        }
                        // Abort all remaining tasks
                        for task in remaining {
                            task.abort();
                            let _ = task.await;
                        }
                    }
                    _ = shutdown_rx.recv() => {
                        info!("Shutdown signal received");
                        // Abort all tasks
                        for task in handles {
                            task.abort();
                            let _ = task.await;
                        }
                    }
                }

                source.on_disconnect().await?;
                Ok(())
            }
            .await;

            match result {
                Ok(_) => {
                    info!("Connection closed gracefully");
                    Ok(())
                }
                Err(e) => {
                    error!("Connection failed: {}", e);
                    source
                        .on_stream_error(StreamType::Video, e.to_string())
                        .await?;
                    source.on_disconnect().await?;
                    Err(e)
                }
            }
        });

        Ok(ConnectionHandle {
            task,
            shutdown: self.shutdown.clone(),
        })
    }

    pub async fn shutdown(&self) {
        let _ = self.shutdown.send(());
    }
}

impl Clone for StreamClient {
    fn clone(&self) -> Self {
        Self {
            endpoint: self.endpoint.clone(),
            client_id: self.client_id,
            media_source: None,
            stats: self.stats.clone(),
            shutdown: self.shutdown.clone(),
        }
    }
}
