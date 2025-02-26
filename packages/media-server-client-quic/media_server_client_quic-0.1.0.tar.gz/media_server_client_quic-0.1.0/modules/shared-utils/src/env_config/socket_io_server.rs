use crate::env_config::config_types::EndpointsConfig;
use crate::env_loader_2::ModuleIdentifier;
use crate::{ConfigLoader, GenericLoader};
use config::ConfigError;
use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct SocketIOServerConfig {
    #[validate(length(min = 1))]
    pub bind_address: String,
    #[validate(range(min = 1))]
    pub redis_channel_buffer: usize,
    #[validate(range(min = 1))]
    pub redis_connection_timeout_secs: u64,
    #[validate(range(min = 1))]
    pub redis_operation_timeout_ms: u64,
    #[validate(range(min = 1))]
    pub redis_keepalive_interval_secs: u64,

    #[validate(length(min = 1))]
    pub socket_cors_origin: String,
    #[validate(range(min = 1))]
    pub socket_ping_interval_secs: u64,
    #[validate(range(min = 1))]
    pub socket_ping_timeout_secs: u64,
    #[validate(length(min = 1))]
    pub log_level: String,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct Settings {
    #[validate(nested)]
    pub endpoints: EndpointsConfig,

    #[validate(nested)]
    pub socket_io_server: SocketIOServerConfig,
}

impl ModuleIdentifier for Settings {
    fn module_path() -> &'static str {
        "modules.socket_io_server"
    }
}

impl Settings {
    pub fn new() -> Result<Self, ConfigError> {
        let loader = GenericLoader::<Self>::new();
        loader.load()
    }
}
