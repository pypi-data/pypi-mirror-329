use crate::shoot::state::CycleState;
use crate::shoot::types::profile::GunProfile;

#[derive(Debug)]
pub struct WeaponState {
    pub cycle_state: CycleState,
    pub current_magazine: u32, // Rounds in the magazine
    pub loaded_round: bool,    // Whether a round is chambered
    pub max_magazine: u32,     // Magazine capacity
}

impl WeaponState {
    pub fn new(profile: &GunProfile) -> Self {
        let initial_magazine = profile.max_ammo - 1; // Subtract one for the chambered round
        Self {
            cycle_state: CycleState::default(),
            current_magazine: initial_magazine,
            loaded_round: true, // Start with a round chambered
            max_magazine: profile.max_ammo,
        }
    }

    pub fn total_ammo(&self) -> u32 {
        self.current_magazine + if self.loaded_round { 1 } else { 0 }
    }
}
