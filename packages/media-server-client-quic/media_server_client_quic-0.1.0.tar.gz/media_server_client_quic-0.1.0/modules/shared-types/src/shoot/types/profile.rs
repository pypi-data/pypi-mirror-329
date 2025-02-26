use crate::shoot::types::{FireMode, MechanismType, ReloadMechanism};
use serde::{Deserialize, Serialize};
use std::time::Duration;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GunProfile {
    pub name: String,
    pub max_ammo: u32,
    pub rate_of_fire: Duration,
    pub reload_time: Duration,
    pub supported_modes: Vec<FireMode>,
    pub burst_size: u32,
    pub reload_mechanism: ReloadMechanism,
    pub rounds_per_reload: u32,
    pub mechanism_type: MechanismType,
}

impl Default for GunProfile {
    fn default() -> Self {
        Self {
            name: "Standard".to_string(),
            max_ammo: 30,
            rate_of_fire: Duration::from_millis(100),
            reload_time: Duration::from_secs(2),
            supported_modes: vec![FireMode::Single, FireMode::Burst, FireMode::Automatic],
            burst_size: 3,
            reload_mechanism: ReloadMechanism::Magazine,
            rounds_per_reload: 30,
            mechanism_type: MechanismType::Magazine,
        }
    }
}

// Gun profile factory functions
pub fn create_kar98k() -> GunProfile {
    GunProfile {
        name: "Kar98k".to_string(),
        max_ammo: 5,
        rate_of_fire: Duration::from_millis(200),
        reload_time: Duration::from_millis(800),
        supported_modes: vec![FireMode::Single],
        burst_size: 0,
        mechanism_type: MechanismType::BoltAction { auto_reload: true },
        rounds_per_reload: 1,
        reload_mechanism: ReloadMechanism::Magazine,
    }
}

pub fn create_m1_garand() -> GunProfile {
    GunProfile {
        name: "M1 Garand".to_string(),
        max_ammo: 8,
        rate_of_fire: Duration::from_millis(150),
        reload_time: Duration::from_millis(500),
        supported_modes: vec![FireMode::Single],
        burst_size: 0,
        mechanism_type: MechanismType::BoltAction { auto_reload: true },
        rounds_per_reload: 1,
        reload_mechanism: ReloadMechanism::Magazine,
    }
}

// M1A1 Thompson
pub fn create_m1a1_thompson() -> GunProfile {
    GunProfile {
        name: "M1A1 Thompson".to_string(),
        max_ammo: 30,
        rate_of_fire: Duration::from_millis(100),
        reload_time: Duration::from_secs(2),
        supported_modes: vec![FireMode::Single, FireMode::Automatic],
        burst_size: 0,
        mechanism_type: MechanismType::Magazine,
        rounds_per_reload: 30,
        reload_mechanism: ReloadMechanism::Magazine,
    }
}

// MP40
pub fn create_mp40() -> GunProfile {
    GunProfile {
        name: "MP40".to_string(),
        max_ammo: 32,
        rate_of_fire: Duration::from_millis(100),
        reload_time: Duration::from_secs(2),
        supported_modes: vec![FireMode::Single, FireMode::Automatic],
        burst_size: 0,
        mechanism_type: MechanismType::Magazine,
        rounds_per_reload: 32,
        reload_mechanism: ReloadMechanism::Magazine,
    }
}

pub fn create_m16() -> GunProfile {
    GunProfile {
        name: "M16".to_string(),
        max_ammo: 30,
        rate_of_fire: Duration::from_millis(100),
        reload_time: Duration::from_secs(2),
        supported_modes: vec![FireMode::Single, FireMode::Burst, FireMode::Automatic],
        burst_size: 3,
        mechanism_type: MechanismType::Magazine,
        rounds_per_reload: 30,
        reload_mechanism: ReloadMechanism::Magazine,
    }
}
