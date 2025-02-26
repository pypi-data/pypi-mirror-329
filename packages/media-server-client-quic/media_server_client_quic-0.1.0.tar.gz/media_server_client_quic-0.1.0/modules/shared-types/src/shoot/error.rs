use thiserror::Error;

#[derive(Error, Debug)]
pub enum ShootError {
    #[error("Redis error: {0}")]
    Redis(String),
    #[error("Serialization error: {0}")]
    Serde(#[from] serde_json::Error),
    #[error("No ammo remaining")]
    NoAmmo,
    #[error("Invalid mode")]
    InvalidMode,
    #[error("System time error")]
    Time(#[from] std::time::SystemTimeError),
    #[error("Channel error: {0}")]
    Channel(String),
    #[error("Unknown GPIO line: {0}")]
    UnknownGPIO(u32),
    #[error("Configuration error: {0}")]
    Config(String),
    #[error("Action not allowed: {0}")]
    ActionNotAllowed(String),
}
