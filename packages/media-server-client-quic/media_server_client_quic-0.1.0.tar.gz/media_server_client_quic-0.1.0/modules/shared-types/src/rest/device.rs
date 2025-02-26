use crate::types::{ComponentId, UnitId};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InitiateDeviceFlowRequest {
    pub scope: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CheckDeviceCodeRequest {
    pub device_code: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetOrCreateUnitRequest {
    pub component_id: ComponentId,
    pub unit_id: Option<UnitId>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CreateUnitRequest {
    pub name: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RemoveUnitRequest {
    pub unit_id: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeviceIdResponse {
    pub device_id: i32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StatusResponse {
    pub status: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetOrCreateUnitResponse {
    pub status: String,
    pub unit_id: i32,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct ComponentType {
    pub id: i32,
    pub name: String,
    pub description: String,
    pub battery: i32,
    pub scope: i32,
    pub recoil: i32,
    pub rate_of_fire: i32,
    pub model_url: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct ComponentCapability {
    pub id: i32,
    pub name: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct Component {
    pub id: i32,
    pub serial_number: String,
    #[serde(rename = "type")]
    pub component_type: ComponentType,
    pub capabilities: Vec<ComponentCapability>,
}

#[derive(Clone, Debug, Deserialize, Serialize)]
pub struct Unit {
    pub id: UnitId,
    pub components: Vec<Component>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct UnitWithComponents {
    pub id: i32,
    pub uuid: String,
    pub name: String,
    pub components: Vec<Component>,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct UserAndUnit {
    pub id: i32,
    pub auth0_id: String,
    pub name: String,
    pub avatar: String,
    pub unit: UnitWithComponents,
    pub stream_id: String, // Need to be string due to javascript limitation (u64 originally)
}
