use serde::{Deserialize, Serialize};

// In a new file called websocket_types.rs
#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum OpCode {
    Empty = 0,
    Text = 1,
    Binary = 2,
    Close = 8,
    Ping = 9,
    Pong = 10,
    NewConnection = 100,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WebSocketMessage {
    pub client_id: i32,
    pub op_code: OpCode,
    pub content: String,
    pub serial_number: String,
}

impl WebSocketMessage {
    pub fn new(client_id: i32, op_code: OpCode, content: String, serial_number: String) -> Self {
        Self {
            client_id,
            op_code,
            content,
            serial_number,
        }
    }

    pub fn ping(client_id: i32, serial_number: String) -> Self {
        Self::new(client_id, OpCode::Ping, String::new(), serial_number)
    }

    pub fn pong(client_id: i32, serial_number: String) -> Self {
        Self::new(client_id, OpCode::Pong, String::new(), serial_number)
    }
}
