use anyhow::Result;
use std::sync::Arc;
use std::time::Duration;
use dashmap::DashMap;
use tracing::{error, info, debug};
use tokio::io::AsyncWriteExt;
use crate::common::{MediaSink, StreamType};
use crate::transport::packet::{MediaPacket, ControlPacket};
use crate::transport::packet_io::PacketIO;
use super::ServerClient;

// Helper function to get or create client
fn get_or_create_client<S: MediaSink + Send + Sync + Clone + 'static>(
    clients: &DashMap<u64, ServerClient>,
    client_id: u64,
    sink_factory: &S,
) -> ServerClient {
    clients.entry(client_id)
        .or_insert_with(|| {
            info!("New client {} connected", client_id);
            ServerClient::new(client_id, Box::new(sink_factory.clone()))
        })
        .clone()
}

async fn handle_hello_handshake(connection: &quinn::Connection) -> Result<u64> {
    let (mut send, mut recv) = connection.accept_bi().await?;
    let mut packet_io = PacketIO::new();

    // Wait for client hello
    match packet_io.read_packet(&mut recv).await? {
        Some(MediaPacket::Control(ControlPacket::Hello { version, nonce: _, capabilities, client_id: _ })) => {
            info!("Received client hello - version: {}, capabilities: {:?}", version, capabilities);
            
            if version != 1 {
                return Err(anyhow::anyhow!("Unsupported protocol version: {}", version));
            }

            // Generate server nonce
            use rand::RngCore;
            let mut nonce = vec![0u8; 32];
            rand::thread_rng().fill_bytes(&mut nonce);
            let nonce = String::from_utf8_lossy(&nonce).to_string();

            // Generate client ID
            let client_id = rand::random::<u64>();

            // Send server hello with client ID
            let server_hello = MediaPacket::Control(ControlPacket::Hello {
                version: 1,
                nonce: Some(nonce),
                capabilities: vec!["h264".to_string(), "opus".to_string()],
                client_id: Some(client_id),
            });

            info!("Sending server hello with client_id: {}", client_id);
            packet_io.write_packet(&mut send, &server_hello).await?;
            Ok(client_id)
        }
        _ => Err(anyhow::anyhow!("Invalid or missing client hello"))
    }
}

async fn handle_auth<S: MediaSink + Send + Sync + Clone + 'static>(
    connection: &quinn::Connection,
    sink_factory: &S,
    client_id: u64,
) -> Result<()> {
    let (mut send, mut recv) = connection.accept_bi().await?;
    let mut packet_io = PacketIO::new();

    match packet_io.read_packet(&mut recv).await? {
        Some(MediaPacket::Control(ControlPacket::Auth { auth, serial, sign, stream_id })) => {
            info!("Received auth request from client {}", client_id);
            
            // Create a sink instance to handle auth
            let mut sink = sink_factory.clone();
            let auth_result = sink.on_auth(auth, serial, sign, stream_id).await?;

            let response = MediaPacket::Control(ControlPacket::AuthResponse {
                success: auth_result,
                message: if auth_result { None } else { Some("Auth failed".to_string()) },
            });

            info!("Sending auth response - success: {}", auth_result);
            packet_io.write_packet(&mut send, &response).await?;

            if auth_result {
                Ok(())
            } else {
                Err(anyhow::anyhow!("Auth failed"))
            }
        }
        _ => Err(anyhow::anyhow!("Invalid or missing auth request"))
    }
}

// Helper to validate stream setup
fn validate_streams(
    streams: Vec<(StreamType, quinn::SendStream, quinn::RecvStream)>,
) -> Result<(quinn::RecvStream, quinn::RecvStream, (quinn::SendStream, quinn::RecvStream))> {
    let mut stream_map: std::collections::HashMap<_, _> = streams.into_iter()
        .map(|(ty, send, recv)| (ty, (send, recv)))
        .collect();

    // Verify all required streams are present
    for stream_type in [StreamType::Video, StreamType::Audio, StreamType::KeepAlive] {
        if !stream_map.contains_key(&stream_type) {
            return Err(anyhow::anyhow!("Missing required stream: {:?}", stream_type));
        }
    }

    let (_, video_recv) = stream_map.remove(&StreamType::Video).unwrap();
    let (_, audio_recv) = stream_map.remove(&StreamType::Audio).unwrap();
    let keep_alive = stream_map.remove(&StreamType::KeepAlive).unwrap();

    Ok((video_recv, audio_recv, keep_alive))
}

async fn setup_stream<S: MediaSink + Send + Sync + Clone + 'static>(
    connection: &quinn::Connection,
    _clients: &DashMap<u64, ServerClient>,
    _sink_factory: &S,
    _client_id: &mut Option<u64>,
) -> Result<Option<(StreamType, quinn::SendStream, quinn::RecvStream)>> {
    let (mut send, mut recv) = connection.accept_bi().await?;
    let mut packet_io = PacketIO::new();
    
    match packet_io.read_packet(&mut recv).await? {
        Some(MediaPacket::Control(ControlPacket::StartStream { stream_type })) => {
            let response = MediaPacket::Control(ControlPacket::StartStream { stream_type });
            packet_io.write_packet(&mut send, &response).await?;
            Ok(Some((stream_type, send, recv)))
        }
        _ => Ok(None)
    }
}

pub(crate) async fn handle_connection<S: MediaSink + Send + Sync + Clone + 'static>(
    connecting: quinn::Connecting,
    clients: Arc<DashMap<u64, ServerClient>>,
    sink_factory: S,
) -> Result<()> {
    let connection = connecting.await?;
    info!("Client connected from {}", connection.remote_address());

    // Perform hello handshake first
    let client_id = match handle_hello_handshake(&connection).await {
        Ok(id) => id,
        Err(e) => {
            error!("Hello handshake failed: {}", e);
            return Ok(());
        }
    };

    // Perform auth
    if let Err(e) = handle_auth(&connection, &sink_factory, client_id).await {
        error!("Auth failed: {}", e);
        return Ok(());
    }

    // Create client immediately after successful auth
    let client = Arc::new(get_or_create_client(&clients, client_id, &sink_factory));
    info!("Client {} authenticated and registered", client_id);

    // Setup phase
    let mut streams = Vec::new();
    let mut client_id_opt = Some(client_id);

    for _ in 0..3 {
        match setup_stream(&connection, &clients, &sink_factory, &mut client_id_opt).await {
            Ok(Some(stream)) => streams.push(stream),
            Ok(None) => break,
            Err(e) => {
                error!("Stream setup failed: {}", e);
                return Ok(());
            }
        }
    }

    // Validate and extract streams
    let (video_recv, audio_recv, (keep_alive_send, keep_alive_recv)) = match validate_streams(streams) {
        Ok(streams) => streams,
        Err(e) => {
            error!("Stream validation failed: {}", e);
            return Ok(());
        }
    };

    // Start handlers
    let handles = vec![
        tokio::spawn(handle_media_stream(video_recv, client.clone(), StreamType::Video)),
        tokio::spawn(handle_media_stream(audio_recv, client.clone(), StreamType::Audio)),
        tokio::spawn(handle_keep_alive_stream(keep_alive_recv, keep_alive_send, client.clone())),
    ];

    // Wait for completion
    let (result, _, remaining) = futures::future::select_all(handles).await;
    remaining.into_iter().for_each(|h| h.abort());

    clients.remove(&client_id);
    info!("Client {} disconnected", client_id);

    result.map_err(|e| anyhow::anyhow!("Task failed: {}", e))??;
    Ok(())
}

// Generic handler for media streams
async fn handle_media_stream(
    mut recv: quinn::RecvStream,
    client: Arc<ServerClient>,
    stream_type: StreamType,
) -> Result<()> {
    debug!("{:?} stream handler started for client {}", stream_type, client.client_id);
    let mut packet_io = PacketIO::new();
    
    while let Ok(Some(packet)) = packet_io.read_packet(&mut recv).await {
        match (packet, stream_type) {
            (MediaPacket::Video(frame), StreamType::Video) => {
                client.update_keep_alive();
                if let Err(e) = client.handle_video(frame).await {
                    error!("Error handling video for client {}: {}", client.client_id, e);
                    break;
                }
            },
            (MediaPacket::Audio(frame), StreamType::Audio) => {
                client.update_keep_alive();
                if let Err(e) = client.handle_audio(frame).await {
                    error!("Error handling audio for client {}: {}", client.client_id, e);
                    break;
                }
            },
            (MediaPacket::Control(ControlPacket::StopStream), _) => break,
            _ => debug!("Ignoring non-{:?} packet on {:?} stream", stream_type, stream_type),
        }
    }
    
    debug!("{:?} stream handler exiting for client {}", stream_type, client.client_id);
    Ok(())
}

async fn handle_keep_alive_stream(
    mut recv: quinn::RecvStream,
    mut send: quinn::SendStream,
    client: Arc<ServerClient>,
) -> Result<()> {
    debug!("Keep-alive stream handler started for client {}", client.client_id);
    let mut last_transit = Duration::ZERO;
    let mut packet_io = PacketIO::new();
    
    while let Ok(Some(packet)) = packet_io.read_packet(&mut recv).await {
        match packet {
            MediaPacket::Control(ControlPacket::Ping { sequence_number, timestamp }) => {
                client.update_keep_alive();
                let receive_timestamp = crate::transport::current_timestamp_micros();
                
                let pong = MediaPacket::Control(ControlPacket::Pong {
                    sequence_number,
                    timestamp,
                    receive_timestamp,
                });
                
                let transit = Duration::from_micros(receive_timestamp - timestamp);
                let rtt = Duration::from_micros(crate::transport::current_timestamp_micros() - timestamp);
                let new_jitter = crate::transport::calculate_rfc3550_jitter(
                    transit,
                    last_transit,
                    client.get_current_jitter().await
                );
                
                let size = packet_io.write_packet(&mut send, &pong).await?;
                client.update_network_stats(rtt, new_jitter, size).await;
                send.flush().await?;
                
                debug!("Ping {} processed - size: {}B, RTT: {:?}, transit: {:?}, jitter: {:?}", 
                    sequence_number, size, rtt, transit, new_jitter);
                
                last_transit = transit;
            },
            MediaPacket::Control(ControlPacket::StopStream) => break,
            _ => (),
        }
    }
    debug!("Keep-alive stream handler exiting for client {}", client.client_id);
    Ok(())
} 