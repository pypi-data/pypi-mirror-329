use crate::rest::device::UserAndUnit;
use crate::types::UnitId;
use database_tools::entities::game_configurations;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
#[serde(default)]
pub struct CreateGame {
    pub game_feature_max_players: i32,
    pub game_duration: i32,
    pub latitude: f32,
    pub longitude: f32,
    pub min_radius: i32,
    pub start_radius: i32,
    pub persist_reboot: i8,
    pub self_join_game: bool,
    pub selected_unit_id: Option<i32>,
    pub start_immediately: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GameId {
    pub game_id: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StartGame {
    pub game_id: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StopGame {
    pub game_id: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JoinGame {
    pub game_id: i32,
    pub unit_id: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JoinGameDetailed {
    pub game_id: i32,
    pub user_and_unit: UserAndUnit,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JoinGameResponse {
    pub data: Option<JoinGameResponseData>,
    pub status: bool,
    pub error: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JoinGameResponseData {
    pub uid: String,
    pub participant: UserAndUnit,
    pub stream_id: u64,
    pub access_token: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LeaveGameRequest {
    pub game_id: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LeaveGameOrchestrator {
    pub game_id: i32,
    pub unit_id: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RequestConfiguration {
    pub unit_id: UnitId,
}

#[derive(Debug, Clone, Serialize, Deserialize, Default)]
pub struct GameConfigurationResponse {
    pub status: String,
    pub config: Option<GameConfiguration>,
    pub access_token: Option<String>,
    pub stream_id: Option<u64>,
    pub error: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GameConfiguration {
    pub game_id: i32,
    pub orchestrator_id: String,
    pub pod_address: String,
    pub vpn_address: String,
    pub ws_public_address: String,
    pub rest_public_address: String,
    pub stream_public_address: String,
    pub public_rest_port: i32,
    pub public_stream_port: i32,
    pub public_ws_port: i32,
    pub rest_port: i32,
    pub stream_port: i32,
    pub ws_port: i32,
}

// Conversion traits for the ORM model
impl From<game_configurations::Model> for GameConfiguration {
    fn from(model: game_configurations::Model) -> Self {
        Self {
            game_id: model.game_id,
            orchestrator_id: model.orchestrator_id,
            pod_address: model.pod_address,
            vpn_address: model.vpn_address,
            public_rest_port: model.public_rest_port,
            public_stream_port: model.public_stream_port,
            public_ws_port: model.public_ws_port,
            rest_port: model.rest_port,
            stream_port: model.stream_port,
            ws_port: model.ws_port,
            ws_public_address: model.ws_public_address,
            rest_public_address: model.rest_public_address,
            stream_public_address: model.stream_public_address,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RequestConfigurationFromGame {
    pub game_id: i32,
}

// Implement into for all structs
macro_rules! impl_json_conversion {
    ($($t:ty),*) => {
        $(
            impl From<$t> for serde_json::Value {
                fn from(val: $t) -> Self {
                    serde_json::to_value(val).unwrap()
                }
            }
        )*
    };
}

// Use it for all your structs
impl_json_conversion!(
    CreateGame,
    GameId,
    StartGame,
    StopGame,
    JoinGame,
    JoinGameDetailed,
    LeaveGameOrchestrator,
    RequestConfiguration,
    GameConfigurationResponse,
    GameConfiguration,
    RequestConfigurationFromGame
);
