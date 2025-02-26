use serde::{Deserialize, Serialize};
use uuid::Uuid;

pub const PROTOCOL_VERSION: u32 = 1;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Capabilities {
    pub video_codecs: Vec<String>,
    pub audio_codecs: Vec<String>,
}

impl Default for Capabilities {
    fn default() -> Self {
        Self {
            video_codecs: vec!["h264".to_string()],
            audio_codecs: vec!["opus".to_string()],
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HelloMessage {
    pub version: u32,
    pub capabilities: Capabilities,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub nonce: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub client_id: Option<Uuid>,
}

impl HelloMessage {
    pub fn new_client() -> Self {
        Self {
            version: PROTOCOL_VERSION,
            capabilities: Capabilities::default(),
            nonce: None,
            client_id: None,
        }
    }

    pub fn new_server(nonce: String, client_id: Uuid) -> Self {
        Self {
            version: PROTOCOL_VERSION,
            capabilities: Capabilities::default(),
            nonce: Some(nonce),
            client_id: Some(client_id),
        }
    }

    pub fn verify_version(&self) -> bool {
        self.version == PROTOCOL_VERSION
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ProtocolMessage {
    Hello(HelloMessage),
} 