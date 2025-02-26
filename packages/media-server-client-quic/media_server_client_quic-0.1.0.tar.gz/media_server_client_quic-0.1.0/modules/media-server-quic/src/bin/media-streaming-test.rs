use anyhow::Result;
use media_streaming::{
    common::TEST_CLIENT_COUNT,
    video::sink::TestSink,
    video::source::TestVideoSource,
    transport::{StreamClient, StreamServer},
};
use std::net::SocketAddr;
use std::time::Duration;
use tracing::{info, Level};
use tracing_subscriber::FmtSubscriber;

async fn run_client(server_addr: SocketAddr, client_id: u32) -> Result<()> {
    info!("Starting client {}", client_id);
    let mut client = StreamClient::new(Box::new(TestVideoSource::new()))?;
    client.connect(server_addr).await
}

async fn run_server(addr: SocketAddr) -> Result<()> {
    info!("Starting server");
    let mut server = StreamServer::new(addr, TestSink::new())?;
    server.run().await
}

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize logging
    FmtSubscriber::builder()
        .with_max_level(Level::INFO)
        .with_target(false)
        .with_thread_ids(true)
        .with_file(true)
        .with_line_number(true)
        .with_thread_names(true)
        .with_level(true)
        .with_ansi(true)
        .with_timer(tracing_subscriber::fmt::time::time())
        .compact()
        .try_init()
        .map_err(|e| anyhow::anyhow!("Failed to initialize logging: {}", e))?;

    let server_addr: SocketAddr = "127.0.0.1:4433".parse()?;
    
    // Start server in background task
    let server_handle = tokio::spawn(run_server(server_addr));
    
    // Give server a moment to start
    tokio::time::sleep(Duration::from_millis(100)).await;

    info!("Starting {} test clients", TEST_CLIENT_COUNT);
    let mut client_handles = Vec::new();

    // Start clients
    for i in 0..TEST_CLIENT_COUNT {
        let client_id = i;
        let handle = tokio::spawn(async move {
            if let Err(e) = run_client(server_addr, client_id).await {
                eprintln!("Client {} error: {}", client_id, e);
            }
        });
        client_handles.push(handle);
    }

    // Wait for server or any client to complete (they should run indefinitely)
    tokio::select! {
        res = server_handle => {
            if let Err(e) = res {
                eprintln!("Server error: {}", e);
            }
        }
        _ = async {
            for handle in client_handles {
                if let Err(e) = handle.await {
                    eprintln!("Client task error: {}", e);
                }
            }
        } => {}
    }

    Ok(())
} 