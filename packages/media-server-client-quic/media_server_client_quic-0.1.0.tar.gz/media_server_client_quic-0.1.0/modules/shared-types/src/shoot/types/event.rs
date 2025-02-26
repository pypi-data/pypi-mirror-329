use super::FireMode;
use crate::shoot::error::ShootError;
use serde::{Deserialize, Serialize};
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Clone, Debug, Serialize, Deserialize)]
pub enum ShootMessageType {
    Fire,
    Reload,
    ReloadStart,
    ReloadComplete,
    MagazineRefill,
    OutOfAmmo,
    NoRoundChambered,
    NeedsCycling,
    CyclingStart,
    CyclingInProgress,
    CyclingComplete,
    ModeChange,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ShootEventMessage {
    pub event_type: ShootMessageType,
    pub timestamp: u64,
    pub mode: FireMode,
    pub ammo_remaining: u32,
    pub sequence: u64,
    pub details: Option<String>,
}

impl ShootEventMessage {
    pub fn new(
        event_type: ShootMessageType,
        mode: FireMode,
        ammo: u32,
        sequence: u64,
        details: Option<String>,
    ) -> Result<Self, ShootError> {
        Ok(Self {
            event_type,
            timestamp: SystemTime::now().duration_since(UNIX_EPOCH)?.as_secs(),
            mode,
            ammo_remaining: ammo,
            sequence,
            details,
        })
    }
}
