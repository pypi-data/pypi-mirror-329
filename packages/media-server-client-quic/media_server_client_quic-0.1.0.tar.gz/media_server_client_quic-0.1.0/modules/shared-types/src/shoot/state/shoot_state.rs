use crate::shoot::types::profile::GunProfile;
use crate::shoot::types::reload::ReloadState;
use crate::shoot::types::FireMode;
use std::time::Instant;

#[derive(Debug)]
pub struct GunState {
    pub current_mode: FireMode,
    pub is_trigger_pressed: bool,
    pub last_shot_time: Instant,
    pub burst_shots_remaining: u32,
    pub sequence: u64,
    pub reload_state: ReloadState,
}

impl GunState {
    pub fn new(profile: &GunProfile) -> Self {
        Self {
            current_mode: profile.supported_modes[0],
            is_trigger_pressed: false,
            last_shot_time: Instant::now(),
            burst_shots_remaining: 0,
            sequence: 0,
            reload_state: ReloadState::default(),
        }
    }
}
