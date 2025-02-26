use super::config_types::*;
use crate::{ConfigLoader, GenericLoader, ModuleIdentifier};
use config::ConfigError;
use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct Settings {
    #[validate(nested)]
    pub common: CommonConfig,
    #[validate(nested)]
    pub web_backend: WebBackendConfig,
    #[validate(nested)]
    pub auth: AuthConfig,
    #[validate(nested)]
    pub auth_privileged: AuthPrivilegedConfig,
    #[validate(nested)]
    pub payment: PaymentConfig,
    #[validate(nested)]
    pub redis: RedisConfig,
    #[validate(nested)]
    pub endpoints: EndpointsConfig,
    #[validate(nested)]
    pub rabbitmq: RabbitMQConfig,
}

impl Settings {
    pub fn new() -> Result<Self, ConfigError> {
        let loader = GenericLoader::<Self>::new();
        loader.load()
    }

    pub fn get_database_url(&self) -> String {
        format!(
            "{}://{}:{}@{}:{}/{}",
            self.web_backend.database.type_,
            self.web_backend.database.user,
            self.web_backend.database.password,
            self.endpoints.database.host,
            self.endpoints.database.port,
            self.web_backend.database.name
        )
    }

    pub fn get_bind_address(&self) -> String {
        format!(
            "{}:{}",
            self.web_backend.server.bind_address, self.endpoints.web_backend.port
        )
    }
}

impl ModuleIdentifier for Settings {
    fn module_path() -> &'static str {
        "modules.web_backend"
    }
}
