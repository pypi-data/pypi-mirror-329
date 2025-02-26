use num_enum::TryFromPrimitive;
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
pub struct ErrorMessage {
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub error_description: Option<String>,
    pub message: String,
}

#[derive(Clone, Debug, Deserialize, Serialize, TryFromPrimitive)]
#[serde(rename_all = "snake_case")]
#[repr(i32)]
pub enum ComponentRole {
    Unknown = 0,
    Camera = 1,
    Trigger = 2,
    Gps = 3,
    GpioHardware = 4,
    GpioRest = 5,
}

pub type ComponentId = String;
pub type UnitId = i32;
