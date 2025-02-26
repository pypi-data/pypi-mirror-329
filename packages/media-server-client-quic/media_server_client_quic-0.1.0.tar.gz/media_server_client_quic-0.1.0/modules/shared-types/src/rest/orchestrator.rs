use chrono::{DateTime, Utc};
use database_tools::entities::{game_configurations, games};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OrchestratorCreate {
    pub identifier: String,
    pub orchestrator_address: String,
    pub orchestrator_port: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OrchestratorGet {
    pub identifier: String,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct OrchestratorHeartbeat {
    pub identifier: String,
    pub game_ids: Vec<i32>,
}

////////// Orchestrator Get games
#[derive(Debug, Serialize)]
pub struct GameResponse {
    // Game core information
    pub id: i32,
    pub uid: String,
    pub status: String,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,

    // Game configuration
    pub max_players: i32,
    pub duration: i32,
    pub location: GameLocation,
    pub radius: GameRadius,

    // Network configuration
    pub network: NetworkConfig,

    // Additional metadata
    pub persist_reboot: bool,
    pub owner_id: i32,
}

#[derive(Debug, Serialize)]
pub struct GameLocation {
    pub latitude: f32,
    pub longitude: f32,
}

#[derive(Debug, Serialize)]
pub struct GameRadius {
    pub min: i32,
    pub start: i32,
}

#[derive(Debug, Serialize)]
pub struct NetworkConfig {
    pub pod_address: String,
    pub vpn_address: String,
    pub websocket: EndpointConfig,
    pub rest: EndpointConfig,
    pub stream: EndpointConfig,
    pub gdb_port: i32,
}

#[derive(Debug, Serialize)]
pub struct EndpointConfig {
    pub public_address: String,
    pub public_port: i32,
    pub internal_port: i32,
}

impl From<(games::Model, game_configurations::Model)> for GameResponse {
    fn from((game, config): (games::Model, game_configurations::Model)) -> Self {
        GameResponse {
            id: game.id,
            uid: game.uid,
            status: game.status,
            created_at: DateTime::<Utc>::from_naive_utc_and_offset(game.created_at, Utc),
            updated_at: DateTime::<Utc>::from_naive_utc_and_offset(game.updated_at, Utc),
            max_players: game.max_players,
            duration: game.duration,
            location: GameLocation {
                latitude: game.latitude,
                longitude: game.longitude,
            },
            radius: GameRadius {
                min: game.min_radius,
                start: game.start_radius,
            },
            network: NetworkConfig {
                pod_address: config.pod_address,
                vpn_address: config.vpn_address,
                websocket: EndpointConfig {
                    public_address: config.ws_public_address,
                    public_port: config.public_ws_port,
                    internal_port: config.ws_port,
                },
                rest: EndpointConfig {
                    public_address: config.rest_public_address,
                    public_port: config.public_rest_port,
                    internal_port: config.rest_port,
                },
                stream: EndpointConfig {
                    public_address: config.stream_public_address,
                    public_port: config.public_stream_port,
                    internal_port: config.stream_port,
                },
                gdb_port: config.gdb_port,
            },
            persist_reboot: game.persist_reboot != 0,
            owner_id: game.owner_id,
        }
    }
}
