use std::sync::Arc;
use std::time::Duration;
use dashmap::DashMap;
use tokio::time::interval;
use tracing::info;

use crate::common::IDLE_TIMEOUT;
use super::ServerClient;

pub(crate) async fn monitor_keep_alive(clients: Arc<DashMap<u64, ServerClient>>) {
    let mut interval = interval(Duration::from_secs(1));

    loop {
        interval.tick().await;

        // Find and remove inactive clients
        let mut to_remove = Vec::new();
        for client in clients.iter() {
            if client.value().get_elapsed_since_keep_alive() > IDLE_TIMEOUT {
                info!("Client {} timed out", client.key());
                to_remove.push(*client.key());
            }
        }

        // Remove timed out clients
        for client_id in to_remove {
            if let Some((_, client)) = clients.remove(&client_id) {
                info!("Removing timed out client {}", client_id);
                drop(client); // Ensure client is dropped and cleanup is triggered
            }
        }
    }
} 