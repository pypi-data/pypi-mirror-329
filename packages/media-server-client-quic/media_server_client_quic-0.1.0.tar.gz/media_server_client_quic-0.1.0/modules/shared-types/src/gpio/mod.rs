use crate::shoot::types::profile::GunProfile;
use crate::shoot::types::Action;
use log::info;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::env;

#[derive(Serialize, Deserialize, Debug, Clone, Copy, PartialEq)]
pub enum GPIOEventType {
    Press,
    Release,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct GPIOEvent {
    pub line: u32,
    pub event_type: GPIOEventType,
    pub timestamp: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum GpioCommand {
    SetState {
        line: u32,
        event_type: GPIOEventType,
    },
    GetStatus,
    Reset,
}

impl GpioCommand {
    pub const PREFIX: &'static str = "gpio:command:";

    pub fn from_redis_message(channel: &str, payload: &str) -> Option<Self> {
        match channel {
            ch if ch.ends_with("set") => {
                // Expects payload to be JSON with line and event_type
                serde_json::from_str(payload).ok()
            }
            ch if ch.ends_with("status") => Some(Self::GetStatus),
            ch if ch.ends_with("reset") => Some(Self::Reset),
            _ => None,
        }
    }

    pub fn to_redis_channel(&self) -> String {
        match self {
            Self::SetState { .. } => "gpio:command:set",
            Self::GetStatus => "gpio:command:status",
            Self::Reset => "gpio:command:reset",
        }
        .to_string()
    }

    pub fn all_channels() -> Vec<String> {
        [
            "gpio:command:set",
            "gpio:command:status",
            "gpio:command:reset",
        ]
        .iter()
        .map(|&s| s.to_string())
        .collect()
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum GpioEvent {
    StateChanged(GPIOEvent),
    Status(HashMap<u32, bool>),
    Heartbeat,
    Config(ConfigurationUpdate),
}

impl GpioEvent {
    pub const PREFIX: &'static str = "gpio:event:";

    pub fn to_redis_channel(&self) -> String {
        match self {
            Self::StateChanged(_) => "gpio:event:state",
            Self::Status(_) => "gpio:event:status",
            Self::Heartbeat => "gpio:event:heartbeat",
            Self::Config(_) => "gpio:event:config",
        }
        .to_string()
    }

    pub fn channel_name(event: GpioEvent) -> String {
        match event {
            GpioEvent::StateChanged(_) => "gpio:event:state",
            GpioEvent::Status(_) => "gpio:event:status",
            GpioEvent::Heartbeat => "gpio:event:heartbeat",
            GpioEvent::Config(_) => "gpio:event:config",
        }
        .to_string()
    }

    pub fn all_channels() -> Vec<String> {
        [
            "gpio:event:state",
            "gpio:event:status",
            "gpio:event:heartbeat",
        ]
        .iter()
        .map(|&s| s.to_string())
        .collect()
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConfigurationUpdate {
    pub profile: Option<GunProfile>,
    pub gpio_config: Option<GPIOConfig>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GPIOConfig {
    pub action_mappings: HashMap<u32, Action>,
}

impl GPIOConfig {
    pub fn from_env() -> Self {
        info!("Loading GPIO configuration from environment");

        const ENV_PREFIX: &str = "GPIO_";
        let action_map = [
            ("SHOOT", Action::Shoot),
            ("RELOAD", Action::Reload),
            ("MODE1", Action::SwitchMode1),
            ("MODE2", Action::SwitchMode2),
            ("MODE3", Action::SwitchMode3),
            ("MODE", Action::SwitchMode),
        ];

        let default_config = Self::default();
        let mut mappings = HashMap::new();

        for (action_name, action) in action_map {
            let env_var_name = format!("{}{}", ENV_PREFIX, action_name);

            if let Ok(pin_str) = env::var(&env_var_name) {
                if let Ok(pin) = pin_str.parse::<u32>() {
                    // Parse directly to u32
                    info!("Configured {} on GPIO pin {}", action_name, pin);
                    mappings.insert(pin, action);
                } else if let Some((&default_pin, _)) = default_config
                    .action_mappings
                    .iter()
                    .find(|(_, &act)| act == action)
                {
                    info!(
                        "Invalid {} pin configuration, using default pin {}",
                        action_name, default_pin
                    );
                    mappings.insert(default_pin, action); // default_pin is already u32
                }
            } else if let Some((&default_pin, _)) = default_config
                .action_mappings
                .iter()
                .find(|(_, &act)| act == action)
            {
                info!("Using default pin {} for {}", default_pin, action_name);
                mappings.insert(default_pin, action); // default_pin is already u32
            }
        }

        info!("Final GPIO configuration:");
        for (pin, action) in &mappings {
            info!("  Pin {}: {:?}", pin, action);
        }

        Self {
            action_mappings: mappings,
        }
    }
}

impl Default for GPIOConfig {
    fn default() -> Self {
        let mut mappings = HashMap::new();
        mappings.insert(22, Action::Shoot);
        mappings.insert(23, Action::Reload);
        mappings.insert(17, Action::SwitchMode1);
        mappings.insert(16, Action::SwitchMode2);
        mappings.insert(20, Action::SwitchMode3);
        mappings.insert(24, Action::SwitchMode);
        Self {
            action_mappings: mappings,
        }
    }
}
