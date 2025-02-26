pub mod constants {
    pub const TICK_DURATION_MICROS: u64 = 100;
    pub const EVENT_CHANNEL_SIZE: usize = 1024;
}

#[derive(Debug, Clone, PartialEq)]
pub enum ShootEvent {
    Fire,
    Reload,
    Mode,
    Config,
    Cycle,
    Status,
    Heartbeat,
}

impl ShootEvent {
    pub const PREFIX: &'static str = "shoot:event:";

    pub fn to_redis_channel(&self) -> String {
        match self {
            Self::Fire => "shoot:event:fire",
            Self::Reload => "shoot:event:reload",
            Self::Mode => "shoot:event:mode",
            Self::Config => "shoot:event:config",
            Self::Cycle => "shoot:event:cycle",
            Self::Status => "shoot:event:status",
            Self::Heartbeat => "shoot:event:heartbeat",
        }
        .to_string()
    }

    pub fn all_channels() -> Vec<String> {
        [
            Self::Fire,
            Self::Reload,
            Self::Mode,
            Self::Config,
            Self::Cycle,
            Self::Status,
            Self::Heartbeat,
        ]
        .iter()
        .map(|cmd| cmd.to_redis_channel())
        .collect()
    }
}

#[derive(Debug, Clone, PartialEq)]
pub enum ShootCommand {
    Gpio,
    Config,
}

impl ShootCommand {
    pub fn to_redis_channel(&self) -> String {
        match self {
            Self::Gpio => "gpio:event:state",
            Self::Config => "shoot:input:config",
        }
        .to_string()
    }

    pub fn all_channels() -> Vec<String> {
        [Self::Gpio, Self::Config]
            .iter()
            .map(|evt| evt.to_redis_channel())
            .collect()
    }
}
