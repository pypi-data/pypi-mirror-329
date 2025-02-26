use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub enum MechanismType {
    Magazine,                         // Standard magazine reload
    BoltAction { auto_reload: bool }, // Bolt action requiring cycling, optionally auto-reloads
    Pump { auto_reload: bool },       // Pump action requiring cycling, optionally auto-reloads
    Break,                            // Break action
}

impl MechanismType {
    pub fn requires_cycling(&self) -> bool {
        matches!(
            self,
            MechanismType::BoltAction { .. } | MechanismType::Pump { .. }
        )
    }

    pub fn auto_reloads(&self) -> bool {
        match self {
            MechanismType::BoltAction { auto_reload } | MechanismType::Pump { auto_reload } => {
                *auto_reload
            }
            _ => false,
        }
    }
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub enum ReloadMechanism {
    Magazine,   // Single press to reload fully
    BoltAction, // Press + release for each round
    Pump,       // Press + release for each round
    Break,      // Press to open, release to close and load
}
