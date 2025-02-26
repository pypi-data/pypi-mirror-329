use anyhow::Result;
use tracing::info;
use tokio::sync::broadcast;
use tracing_subscriber;
use std::sync::Arc;

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize logging with file and line numbers
    tracing_subscriber::fmt()
        .with_env_filter("info,sqlx=warn,hyper=warn,reqwest=warn,tower=warn,h2=warn,rustls=warn")
        .with_file(true)
        .with_line_number(true)
        .with_thread_ids(true)
        .with_target(true)
        .init();

    info!("Logger initialized with enhanced format including file and line numbers");

    let (_shutdown_tx, shutdown_rx) = broadcast::channel(1);

    // Create default settings with valid address
    let settings = {
        let mut s = shared_utils::env_config::game_engine::Settings::default();
        s.game_engine.bind_address = "127.0.0.1".to_string();
        s.game_engine.stream_port = 25502;
        Arc::new(s)
    };

    // Run server
    media_streaming::run_server(
        settings,
        None,
        None,
        shutdown_rx,
    ).await
} 