use serde::{Deserialize, Serialize};
use serde_json::Value;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TaskInfo {
    pub id: String,
    pub status: TaskStatusEnum,
    pub created_at: TaskTimestamp,
    pub updated_at: TaskTimestamp,
    pub task_type: String,
    pub start_time: Option<f64>, // Timestamp when task started
    pub end_time: Option<f64>,   // Timestamp when task completed/failed
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TaskTimestamp {
    pub secs_since_epoch: u64,
    pub nanos_since_epoch: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "status", content = "value")]
pub enum TaskStatusEnum {
    Completed(Value),
    Failed {
        error: String,
        details: Option<Value>,
    },
    Pending,
    InProgress,
}

#[derive(Clone, Serialize, Deserialize, Debug)]
pub enum TaskStatus {
    Pending,
    InProgress,
    Completed(serde_json::Value),
    Failed {
        error: String,
        details: Option<serde_json::Value>,
    },
}

#[derive(Debug, Serialize, Deserialize)]
pub struct TaskResponse {
    pub task_id: String,
}
