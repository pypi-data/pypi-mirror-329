use crate::env_config::config_types::AuthConfig;
use crate::env_config::config_types::CommonConfig;
use crate::env_config::config_types::EndpointsConfig;
use crate::env_config::config_types::GameEngineConfig;
use crate::env_config::config_types::MediaMTXConfig;
use crate::env_config::config_types::SegmentationConfig;
use crate::env_loader_2::{ConfigLoader, GenericLoader, ModuleIdentifier};
use config::ConfigError;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use validator::Validate;

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct Settings {
    #[validate(nested)]
    pub common: CommonConfig,
    #[validate(nested)]
    pub mediamtx: MediaMTXConfig,
    #[validate(nested)]
    pub segmentation: SegmentationConfig,
    #[validate(nested)]
    pub game_engine: GameEngineConfig,
    #[validate(nested)]
    pub auth: AuthConfig,
    #[validate(nested)]
    pub endpoints: EndpointsConfig,
}

impl ModuleIdentifier for Settings {
    fn module_path() -> &'static str {
        "modules.game_engine"
    }
}

impl Settings {
    pub fn new() -> Result<Self, ConfigError> {
        let loader = GenericLoader::<Self>::new();
        loader.load()
    }

    pub fn get_bind_address(&self) -> String {
        format!(
            "{}:{}",
            self.game_engine.bind_address, self.game_engine.rest_port
        )
    }

    /// Convert settings into environment variables format
    /// Returns a BTreeMap where keys are environment variable names (e.g. "NB_GAME_ENGINE_PORTS_WEBSOCKET")
    /// and values are their string representations
    pub fn to_env_vars(&self) -> BTreeMap<String, String> {
        crate::to_env_vars(self, "NB")
    }
}
