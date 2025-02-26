use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ShootData {
    pub data: ShootDataContent,
    pub header: Header,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ShootDataContent {
    pub x: i32,
    pub y: i32,
    #[serde(default)]
    pub speed: f32,
    #[serde(default)]
    pub force: f32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Header {
    pub seq: u64,
    pub timestamp: u64,
    #[serde(rename = "type")]
    pub message_type: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ServoCommand {
    GPIO(ShootData),
}

impl ServoCommand {
    pub const PREFIX: &'static str = "servo:command:";

    pub fn to_redis_channel(&self) -> String {
        match self {
            Self::GPIO(_) => format!("{}gpio", Self::PREFIX),
        }
    }

    pub fn all_channels() -> Vec<String> {
        vec![format!("{}fire", Self::PREFIX)]
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ServoEvent {
    StateChanged {
        position: f32,
        is_firing: bool,
        fault: Option<String>,
        timestamp: u64,
    },
    FireConfirmation {
        position: f32,
        timestamp: u64,
    },
    Heartbeat {
        position: f32,
        timestamp: u64,
    },
    Status {
        position: f32,
        fault_count: u32,
        consecutive_errors: u32,
        last_signal: u64,
    },
    Error(String),
}

impl ServoEvent {
    pub const PREFIX: &'static str = "servo:event:";

    pub fn to_redis_channel(&self) -> String {
        match self {
            Self::StateChanged { .. } => format!("{}state", Self::PREFIX),
            Self::FireConfirmation { .. } => format!("{}fire_confirmation", Self::PREFIX),
            Self::Heartbeat { .. } => format!("{}heartbeat", Self::PREFIX),
            Self::Status { .. } => format!("{}status", Self::PREFIX),
            Self::Error(_) => format!("{}error", Self::PREFIX),
        }
    }

    pub fn all_channels() -> Vec<String> {
        vec![
            format!("{}state", Self::PREFIX),
            format!("{}fire_confirmation", Self::PREFIX),
            format!("{}heartbeat", Self::PREFIX),
            format!("{}status", Self::PREFIX),
            format!("{}error", Self::PREFIX),
        ]
    }

    pub fn to_redis_message(&self) -> Vec<u8> {
        serde_json::to_vec(self).expect("Failed to serialize event")
    }
}
