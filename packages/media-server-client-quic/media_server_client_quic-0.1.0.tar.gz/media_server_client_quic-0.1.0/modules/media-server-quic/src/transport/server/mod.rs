mod server_client;
mod handlers;
mod config;
mod stats;

pub use server_client::ServerClient;
use handlers::handle_connection;
use config::configure_server;
use stats::monitor_keep_alive;

use anyhow::Result;
use std::net::SocketAddr;
use std::sync::Arc;
use dashmap::DashMap;
use quinn::Endpoint;
use crate::common::MediaSink;
use tracing::{error, info};
use tokio::task::JoinHandle;

pub struct StreamServer<S: MediaSink  + Send + Sync + Clone + 'static> {
    endpoint: Endpoint,
    clients: Arc<DashMap<u64, ServerClient>>,
    sink_factory: S,
    background_tasks: Vec<JoinHandle<()>>,
}

impl<S: MediaSink  + Send + Sync + Clone + 'static> StreamServer<S> {
    pub fn new(addr: SocketAddr, sink_factory: S) -> Result<Self> {
        let config = configure_server()?;
        let endpoint = Endpoint::server(config, addr)?;
        let clients = Arc::new(DashMap::new());

        Ok(Self {
            endpoint,
            clients: clients.clone(),
            sink_factory,
            background_tasks: vec![tokio::spawn(monitor_keep_alive(clients))],
        })
    }

    pub fn get_clients(&self) -> &Arc<DashMap<u64, ServerClient>> {
        &self.clients
    }

    pub async fn disconnect_client(&self, stream_id: u64) -> Result<()> {
        if let Some((_, client)) = self.clients.remove(&stream_id) {
            info!("Disconnecting client {}", stream_id);
            // Client will be dropped here, triggering cleanup
            drop(client);
        }
        Ok(())
    }

    pub async fn run(&mut self) -> Result<()> {
        info!("Server listening on {}", self.endpoint.local_addr()?);

        while let Some(connecting) = self.endpoint.accept().await {
            let clients = Arc::clone(&self.clients);
            let sink_factory = self.sink_factory.clone();

            let handle = tokio::spawn(handle_connection(connecting, clients, sink_factory));

            tokio::spawn(async move {
                if let Err(e) = handle.await {
                    error!("Connection handler failed: {}", e);
                }
            });
        }

        for task in self.background_tasks.drain(..) {
            if let Err(e) = task.await {
                error!("Task failed during shutdown: {}", e);
            }
        }

        Ok(())
    }
}

impl<S: MediaSink  + Send + Sync + Clone + 'static> Drop for StreamServer<S> {
    fn drop(&mut self) {
        for task in self.background_tasks.drain(..) {
            task.abort();
        }
    }
} 
