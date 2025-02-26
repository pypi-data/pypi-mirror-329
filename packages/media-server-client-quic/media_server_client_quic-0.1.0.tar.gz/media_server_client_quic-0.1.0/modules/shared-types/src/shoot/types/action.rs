use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, Serialize, Deserialize, PartialEq, Eq, Hash)]
pub enum Action {
    Shoot,
    Reload,
    Cycle,
    SwitchMode,  // Switch to the next mode in the list
    SwitchMode1, // Switch to the first mode in the list
    SwitchMode2, // Switch to the second mode in the list
    SwitchMode3, // Switch to the third mode in the list
    None,
}
