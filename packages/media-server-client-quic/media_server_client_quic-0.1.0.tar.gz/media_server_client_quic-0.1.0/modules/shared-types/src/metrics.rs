use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OrchestratorMetrics {
    pub orchestrator_id: String,
    pub cluster_used: ClusterResources,
    pub cluster_available: ClusterResources,
    pub games: GameMetrics,
    pub system: SystemMetrics,
    pub status: ServerStatus,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ClusterResources {
    pub cpu_cores: i32,
    pub memory_gb: f64,
    pub gpus: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GameMetrics {
    pub total_games: i32,
    pub active_games: i32,
    pub pending_games: i32,
    pub failed_games: i32,
    pub games_created_last_hour: i32,
    pub average_game_duration: f64, // in minutes
    pub games_by_status: HashMap<String, i32>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SystemMetrics {
    pub cpu_usage: f32,         // percentage
    pub memory_usage: f64,      // GB
    pub memory_available: f64,  // GB
    pub uptime: u64,            // seconds
    pub load_average: Vec<f32>, // 1, 5, 15 minute averages
    pub network_connections: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ServerStatus {
    pub version: String,
    pub start_time: u64,
    pub healthy: bool,
}
