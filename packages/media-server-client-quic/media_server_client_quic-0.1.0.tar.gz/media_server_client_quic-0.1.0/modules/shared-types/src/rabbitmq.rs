use serde::{Deserialize, Serialize};
use std::fmt;
pub use strum::IntoEnumIterator;
use strum_macros::EnumIter;
// Re-export strum traits that we want available to users of MessageType
pub mod strum {
    pub use ::strum::IntoEnumIterator;
    pub use ::strum_macros::{AsRefStr, EnumIter, EnumString};
}

#[derive(
    Debug,
    Clone,
    Copy,
    Eq,
    PartialEq,
    Hash,
    EnumIter,
    Serialize,
    Deserialize,
    strum_macros::AsRefStr,
    strum_macros::EnumString,
)]
#[strum(serialize_all = "kebab-case")]
pub enum MessageType {
    BehaviorTree,
    ServerCapacity,
}

impl fmt::Display for MessageType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.to_routing_key())
    }
}

impl MessageType {
    pub fn to_topic_name(&self) -> String {
        match self {
            MessageType::BehaviorTree => "behavior-tree",
            MessageType::ServerCapacity => "server-capacity",
        }
        .to_string()
    }

    pub fn to_routing_key(&self) -> String {
        match self {
            MessageType::BehaviorTree => "behavior.tree",
            MessageType::ServerCapacity => "server.capacity",
        }
        .to_string()
    }

    pub fn to_exchange(&self) -> String {
        match self {
            MessageType::BehaviorTree => "newbringer.events",
            MessageType::ServerCapacity => "newbringer.metrics",
        }
        .to_string()
    }
}
