use super::config_types::*;
use crate::{ConfigLoader, GenericLoader, ModuleIdentifier};
use config::ConfigError;
use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct PortRangeConfig {
    #[validate(range(min = 1, max = 65535))]
    pub start: u16,
    #[validate(range(min = 1, max = 65535))]
    pub end: u16,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct OrchestratorConfig {
    #[validate(length(min = 1))]
    pub identifier: String,
    #[validate(nested)]
    pub server: ServerConfig,
    #[validate(nested)]
    pub port_range: PortRangeConfig,
    #[validate(range(min = 1))]
    pub metrics_push_interval_seconds: u64,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct Settings {
    #[validate(nested)]
    pub common: CommonConfig,
    #[validate(nested)]
    pub game_orchestrator: OrchestratorConfig,
    #[validate(nested)]
    pub game_engine: GameEngineConfig,
    #[validate(nested)]
    pub kubernetes: KubernetesConfig,
    #[validate(nested)]
    pub endpoints: EndpointsConfig,
    #[validate(nested)]
    pub auth: AuthConfig,
    #[validate(nested)]
    pub auth_privileged: AuthPrivilegedConfig,
    #[validate(nested)]
    pub tailscale: TailscaleConfig,
    #[validate(nested)]
    pub github: GithubConfig,
    #[validate(nested)]
    pub rabbitmq: RabbitMQConfig,
}

impl Settings {
    pub fn get_bind_address(&self) -> String {
        format!(
            "{}:{}",
            self.game_orchestrator.server.bind_address, self.endpoints.game_orchestrator.port
        )
    }

    pub fn new() -> Result<Self, ConfigError> {
        let loader = GenericLoader::<Self>::new();
        loader.load()
    }
}

impl ModuleIdentifier for Settings {
    fn module_path() -> &'static str {
        "modules.game_orchestrator"
    }
}
