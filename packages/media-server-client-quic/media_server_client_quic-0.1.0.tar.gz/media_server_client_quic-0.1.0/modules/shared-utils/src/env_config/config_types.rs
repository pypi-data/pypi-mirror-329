use crate::env_loader_2::deserialize_string;
use serde::{Deserialize, Serialize};
use validator::Validate;

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct GithubConfig {
    #[validate(length(min = 1))]
    pub token: String,
    #[validate(length(min = 1))]
    pub username: String,
    #[validate(length(min = 1))]
    pub email: String,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct TailscaleConfig {
    #[validate(length(min = 1))]
    pub network_id: String,
    #[validate(length(min = 1))]
    pub auth_key: String,
    #[validate(length(min = 1))]
    pub client_id: String,
    #[validate(length(min = 1))]
    pub client_secret: String,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct RabbitMQEndpoint {
    #[validate(length(min = 1))]
    pub host: String,
    #[validate(range(min = 1, max = 65535))]
    pub port: u16,
    pub vhost: String,
    #[validate(length(min = 1))]
    pub username: String,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct EndpointsConfig {
    #[validate(nested)]
    pub database: EndpointConfig,
    #[validate(nested)]
    pub redis: EndpointConfig,
    #[validate(nested)]
    pub web_backend: WebBackendEndpoint,
    #[validate(nested)]
    pub game_orchestrator: WebBackendEndpoint,
    #[validate(nested)]
    pub game_engine: GameEngineEndpoint,
    #[validate(nested)]
    pub socket_io_server: WebBackendEndpoint,
    #[validate(nested)]
    pub rabbitmq: RabbitMQEndpoint,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct EndpointConfig {
    #[validate(length(min = 1))]
    pub host: String,
    #[validate(range(min = 1, max = 65535))]
    pub port: u16,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct WebBackendEndpoint {
    #[validate(length(min = 1))]
    pub scheme: String,
    #[validate(length(min = 1))]
    pub host: String,
    #[validate(range(min = 1, max = 65535))]
    pub port: u16,
    #[validate(length(min = 1))]
    pub path: String,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct CommonConfig {
    #[validate(nested)]
    pub logging: LoggingConfig,
    #[validate(nested)]
    pub debug: DebugConfig,
    #[validate(nested)]
    pub input: InputConfig,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct LoggingConfig {
    #[validate(length(min = 1))]
    pub rust_level: String,
    pub spdlog_level: u32,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct DebugConfig {
    pub enable_render: bool,
    pub enable_nvidia: bool,
    #[validate(length(min = 1))]
    pub cuda_version: String,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct InputConfig {
    pub width: u32,
    pub height: u32,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct WebBackendConfig {
    #[validate(nested)]
    pub server: ServerConfig,
    #[validate(nested)]
    pub database: DatabaseConfig,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct ServerConfig {
    #[validate(length(min = 1))]
    pub bind_address: String,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct DatabaseConfig {
    #[validate(length(min = 1))]
    #[serde(rename = "type")]
    pub type_: String,
    #[validate(length(min = 1))]
    pub name: String,
    #[validate(length(min = 1))]
    pub user: String,
    #[validate(length(min = 1))]
    pub password: String,
    pub pool_size: u32,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct RedisConfig {
    pub verbose: bool,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct PaymentConfig {
    #[validate(nested)]
    pub stripe: StripeConfig,
    #[validate(nested)]
    pub vipps: VippsConfig,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct StripeConfig {
    #[validate(length(min = 1))]
    pub secret_key: String,
    #[validate(length(min = 1))]
    pub public_key: String,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct VippsConfig {
    #[validate(length(min = 1))]
    pub client_id: String,
    #[validate(length(min = 1))]
    pub client_secret: String,
    #[validate(length(min = 1))]
    pub subscription_key: String,
    #[validate(length(min = 1))]
    #[serde(deserialize_with = "deserialize_string")]
    pub merchant_serial_number: String,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct AuthConfig {
    #[validate(length(min = 1))]
    pub domain: String,
    #[validate(length(min = 1))]
    pub client_id: String,
    #[validate(length(min = 1))]
    pub audience: String,
    pub token_expiration_buffer: u32,
    #[validate(length(min = 1))]
    pub scope: String,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct AuthPrivilegedConfig {
    #[validate(length(min = 1))]
    pub client_id: String,
    #[validate(length(min = 1))]
    pub client_secret: String,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct GameEngineEndpoint {
    #[validate(length(min = 1))]
    pub host: String,
    #[validate(length(min = 1))]
    pub public_domain: String,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct MediaMTXConfig {
    #[validate(length(min = 1))]
    pub host: String,
    #[validate(range(min = 1, max = 65535))]
    pub webrtc_port: u16,
    #[validate(range(min = 1, max = 65535))]
    pub rtsp_port: u16,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct SegmentationConfig {
    #[validate(length(min = 1))]
    pub python_location: String,
    #[validate(range(min = 1))]
    pub batch_size: u32,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct GameEngineConfig {
    #[validate(range(min = 1, max = 65535))]
    pub websocket_port: u16,
    #[validate(range(min = 1, max = 65535))]
    pub stream_port: u16,
    #[validate(range(min = 1, max = 65535))]
    pub rest_port: u16,
    #[validate(length(min = 1))]
    pub bind_address: String,
    #[validate(length(min = 1))]
    pub game_engine_image: String,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct RabbitMQConfig {
    #[validate(length(min = 1))]
    pub oauth_audience: String,
    #[validate(length(min = 1))]
    pub oauth_scope: String,
}

#[derive(Debug, Deserialize, Serialize, Clone, Default, Validate, PartialEq)]
pub struct KubernetesConfig {
    pub enabled: bool,
    #[validate(length(min = 1))]
    pub namespace: String,
    #[validate(length(min = 1))]
    pub image_pull_secret: String,
}
