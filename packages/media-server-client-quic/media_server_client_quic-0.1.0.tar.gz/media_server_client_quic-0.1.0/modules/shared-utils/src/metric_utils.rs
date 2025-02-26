// metrics_utils.rs
use shared_types::metrics::{
    ClusterResources, GameMetrics, OrchestratorMetrics, ServerStatus, SystemMetrics,
};
use std::collections::HashMap;
use std::env;
use sysinfo::System;

#[async_trait::async_trait]
pub trait GameMetricsProvider {
    async fn get_total_games(&self) -> Result<i32, String>;
    async fn get_games_by_status(&self) -> Result<HashMap<String, i32>, String>;
    async fn get_games_created_last_hour(&self) -> Result<i32, String>;
    async fn get_average_game_duration(&self) -> Result<f64, String>;
}

#[async_trait::async_trait]
pub trait ClusterMetricsProvider {
    async fn get_cluster_resources(&self) -> Result<(ClusterResources, ClusterResources), String>;
}

pub struct MetricsCollector<G, C>
where
    G: GameMetricsProvider,
    C: ClusterMetricsProvider,
{
    game_metrics_provider: G,
    cluster_metrics_provider: C,
    orchestrator_identifier: String,
}

#[cfg(target_os = "linux")]
fn get_load_average() -> Vec<f32> {
    match std::fs::read_to_string("/proc/loadavg") {
        Ok(contents) => contents
            .split_whitespace()
            .take(3)
            .filter_map(|s| s.parse::<f32>().ok())
            .collect(),
        Err(_) => vec![0.0, 0.0, 0.0],
    }
}

#[cfg(not(target_os = "linux"))]
fn get_load_average() -> Vec<f32> {
    vec![0.0, 0.0, 0.0]
}

#[cfg(target_os = "linux")]
fn get_uptime() -> u64 {
    match std::fs::read_to_string("/proc/uptime") {
        Ok(contents) => contents
            .split_whitespace()
            .next()
            .and_then(|s| s.parse::<f64>().ok())
            .map(|secs| secs as u64)
            .unwrap_or(0),
        Err(_) => 0,
    }
}

#[cfg(not(target_os = "linux"))]
fn get_uptime() -> u64 {
    match SystemTime::now().duration_since(UNIX_EPOCH) {
        Ok(duration) => duration.as_secs(),
        Err(_) => 0,
    }
}

impl<G, C> MetricsCollector<G, C>
where
    G: GameMetricsProvider,
    C: ClusterMetricsProvider,
{
    pub fn new(
        game_metrics_provider: G,
        cluster_metrics_provider: C,
        orchestrator_identifier: String,
    ) -> Self {
        Self {
            game_metrics_provider,
            cluster_metrics_provider,
            orchestrator_identifier,
        }
    }

    pub async fn collect_metrics(&self) -> Result<OrchestratorMetrics, String> {
        let cluster_resources = self
            .cluster_metrics_provider
            .get_cluster_resources()
            .await?;
        let system_metrics = Self::collect_system_metrics()?;
        let game_metrics = self.collect_game_metrics().await?;
        let server_status = Self::collect_server_status();

        Ok(OrchestratorMetrics {
            orchestrator_id: self.orchestrator_identifier.clone(),
            cluster_used: cluster_resources.0,
            cluster_available: cluster_resources.1,
            games: game_metrics,
            system: system_metrics,
            status: server_status,
        })
    }

    fn collect_system_metrics() -> Result<SystemMetrics, String> {
        let mut sys = System::new();
        sys.refresh_all();

        let cpu_usage = if !sys.cpus().is_empty() {
            sys.cpus().iter().map(|cpu| cpu.cpu_usage()).sum::<f32>() / sys.cpus().len() as f32
        } else {
            0.0
        };

        let total_memory = sys.total_memory() as f64 / (1024.0 * 1024.0 * 1024.0);
        let available_memory = sys.available_memory() as f64 / (1024.0 * 1024.0 * 1024.0);
        let used_memory = total_memory - available_memory;

        Ok(SystemMetrics {
            cpu_usage,
            memory_usage: used_memory,
            memory_available: available_memory,
            uptime: get_uptime(),
            load_average: get_load_average(),
            network_connections: Self::count_network_connections(),
        })
    }

    async fn collect_game_metrics(&self) -> Result<GameMetrics, String> {
        let games_by_status = self.game_metrics_provider.get_games_by_status().await?;

        let active_count = *games_by_status.get("Running").unwrap_or(&0);
        let pending_count = *games_by_status.get("Pending").unwrap_or(&0);
        let failed_count = *games_by_status.get("Failed").unwrap_or(&0);

        Ok(GameMetrics {
            total_games: self.game_metrics_provider.get_total_games().await?,
            active_games: active_count,
            pending_games: pending_count,
            failed_games: failed_count,
            games_created_last_hour: self
                .game_metrics_provider
                .get_games_created_last_hour()
                .await?,
            average_game_duration: self
                .game_metrics_provider
                .get_average_game_duration()
                .await?,
            games_by_status,
        })
    }

    fn collect_server_status() -> ServerStatus {
        ServerStatus {
            version: env!("CARGO_PKG_VERSION").to_string(),
            start_time: std::env::var("SERVER_START_TIME")
                .unwrap_or_default()
                .parse()
                .unwrap_or_default(),
            healthy: true,
        }
    }

    fn count_network_connections() -> i32 {
        match std::process::Command::new("netstat").arg("-n").output() {
            Ok(output) => String::from_utf8_lossy(&output.stdout)
                .lines()
                .filter(|line| line.contains("ESTABLISHED"))
                .count() as i32,
            Err(_) => 0,
        }
    }
}
