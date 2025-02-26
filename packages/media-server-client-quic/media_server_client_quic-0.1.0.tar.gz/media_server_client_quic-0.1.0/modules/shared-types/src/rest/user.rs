use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UpdateUserName {
    pub name: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CreateUser {
    pub username: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UserResponse {
    pub message: String,
    pub text: UserData,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UserData {
    pub id: i32,
    pub name: String,
    pub auth0_id: String,
}
