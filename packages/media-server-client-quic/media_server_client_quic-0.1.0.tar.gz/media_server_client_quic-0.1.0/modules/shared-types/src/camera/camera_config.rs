use crate::camera::statistics::CameraMetrics;
use bytes::Bytes;
use serde::{Deserialize, Serialize};

// Input channels (commands received from Redis)
#[derive(Debug, Clone)]
pub enum RedisCommandChannel {
    Start,
    Stop,
    Restart,
    Shutdown,
    EncoderStart,
    EncoderStop,
    EncoderConfigure(EncoderConfig),
    OutputStart(OutputStreamConfig),
    OutputStop,
    QrStart,
    QrStop,
    JsonEvent,
}

impl RedisCommandChannel {
    pub fn to_channel(&self) -> &'static str {
        match self {
            Self::Start => "camera::command::start",
            Self::Stop => "camera::command::stop",
            Self::Restart => "camera::command::restart",
            Self::Shutdown => "camera::command::shutdown",
            Self::EncoderStart => "camera::command::encoder.start",
            Self::EncoderStop => "camera::command::encoder.stop",
            Self::EncoderConfigure(_) => "camera::command::encoder.configure",
            Self::OutputStart(_) => "camera::command::output.start",
            Self::OutputStop => "camera::command::output.stop",
            Self::QrStart => "camera::command::qr.start",
            Self::QrStop => "camera::command::qr.stop",
            Self::JsonEvent => "camera::command::json.event",
        }
    }

    pub fn all_channels() -> Vec<String> {
        use RedisCommandChannel::*;
        // Create default/placeholder configs for demonstration
        let default_encoder_config = EncoderConfig {
            pixel_format: PixelTypes::YUV420,
            bitrate: 0,
            keyframe_interval: 0,
        };
        let default_output_config = OutputStreamConfig::File {
            identifier: String::new(),
            path: String::new(),
            append: false,
        };

        [
            Start,
            Stop,
            Restart,
            Shutdown,
            EncoderStart,
            EncoderStop,
            EncoderConfigure(default_encoder_config),
            OutputStart(default_output_config),
            OutputStop,
            QrStart,
            QrStop,
        ]
        .iter()
        .map(|cmd| cmd.to_channel().to_string())
        .collect()
    }

    pub fn from_channel(channel: &str) -> Option<Self> {
        match channel {
            "camera::command::start" => Some(Self::Start),
            "camera::command::stop" => Some(Self::Stop),
            "camera::command::restart" => Some(Self::Restart),
            "camera::command::shutdown" => Some(Self::Shutdown),
            "camera::command::encoder.start" => Some(Self::EncoderStart),
            "camera::command::encoder.stop" => Some(Self::EncoderStop),
            "camera::command::encoder.configure" => Some(Self::EncoderConfigure(EncoderConfig {
                pixel_format: PixelTypes::YUV420,
                bitrate: 0,
                keyframe_interval: 0,
            })),
            "camera::command::output.start" => Some(Self::OutputStart(OutputStreamConfig::File {
                identifier: String::new(),
                path: String::new(),
                append: false,
            })),
            "camera::command::output.stop" => Some(Self::OutputStop),
            "camera::command::qr.start" => Some(Self::QrStart),
            "camera::command::qr.stop" => Some(Self::QrStop),
            _ => None,
        }
    }
}

// Output channels (events published to Redis)
#[derive(Debug, Clone)]
pub enum RedisEventChannel {
    CaptureStarted,
    CaptureStopped,
    CaptureFrame,
    QRCodeDetected,
    Error,
    EncoderStatus,
    StreamStatus,
    Statistics,
    Heartbeat,
    Announce,
    EncoderStart,
    EncoderStop,
    EncoderConfigure,
    OutputStart,
    OutputStop,
    QrStart,
    QrStop,
}

impl RedisEventChannel {
    pub fn to_channel(&self) -> &'static str {
        match self {
            Self::CaptureStarted => "camera::event::capture.started",
            Self::CaptureStopped => "camera::event::capture.stopped",
            Self::CaptureFrame => "camera::event::capture.frame",
            Self::QRCodeDetected => "camera::event::qr.detected",
            Self::Error => "camera::event::error",
            Self::EncoderStatus => "camera::event::encoder.status",
            Self::StreamStatus => "camera::event::stream.status",
            Self::Statistics => "camera::event::statistics",
            Self::Heartbeat => "camera::event::heartbeat",
            Self::Announce => "camera::event::announce",
            Self::EncoderStart => "camera::event::encoder.start",
            Self::EncoderStop => "camera::event::encoder.stop",
            Self::EncoderConfigure => "camera::event::encoder.configure",
            Self::OutputStart => "camera::event::output.start",
            Self::OutputStop => "camera::event::output.stop",
            Self::QrStart => "camera::event::qr.start",
            Self::QrStop => "camera::event::qr.stop",
        }
    }
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Heartbeat {
    pub unique_id: String,
    pub timestamp: u64,
    pub ready: bool,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Announce {
    pub unique_id: String,
    pub timestamp: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum CameraEvent {
    CaptureStarted,
    CaptureStopped,
    CaptureFrame(u32),
    QRCodeDetected(String),
    Error(String),
    EncoderStatus(bool),
    StreamStatus { identifier: String, connected: bool },
    Statistics(CameraMetrics),
    Heartbeat(Heartbeat),
    Announce(Heartbeat),
    EncoderStart,
    EncoderStop,
    EncoderConfigure,
    OutputStart,
    OutputStop,
    QrStart,
    QrStop,
}

impl CameraEvent {
    pub fn channel(&self) -> RedisEventChannel {
        match self {
            Self::CaptureStarted => RedisEventChannel::CaptureStarted,
            Self::CaptureStopped => RedisEventChannel::CaptureStopped,
            Self::CaptureFrame(_) => RedisEventChannel::CaptureFrame,
            Self::QRCodeDetected(_) => RedisEventChannel::QRCodeDetected,
            Self::Error(_) => RedisEventChannel::Error,
            Self::EncoderStatus(_) => RedisEventChannel::EncoderStatus,
            Self::StreamStatus { .. } => RedisEventChannel::StreamStatus,
            Self::Statistics(_) => RedisEventChannel::Statistics,
            Self::Heartbeat(_) => RedisEventChannel::Heartbeat,
            Self::Announce(_) => RedisEventChannel::Announce,
            Self::EncoderStart => RedisEventChannel::EncoderStart,
            Self::EncoderStop => RedisEventChannel::EncoderStop,
            Self::EncoderConfigure => RedisEventChannel::EncoderConfigure,
            Self::OutputStart => RedisEventChannel::OutputStart,
            Self::OutputStop => RedisEventChannel::OutputStop,
            Self::QrStart => RedisEventChannel::QrStart,
            Self::QrStop => RedisEventChannel::QrStop,
        }
    }

    pub fn to_redis_payload(&self) -> Bytes {
        match self {
            Self::CaptureStarted | Self::CaptureStopped => Bytes::from("true"),
            Self::QRCodeDetected(code) => Bytes::from(code.clone()),
            Self::Error(err) => Bytes::from(err.clone()),
            Self::CaptureFrame(frame) => Bytes::from(frame.to_string()),
            Self::EncoderStatus(status) => Bytes::from(if *status { "active" } else { "inactive" }),
            Self::StreamStatus {
                identifier,
                connected,
            } => {
                let payload = StreamStatusPayload {
                    identifier: identifier.clone(),
                    connected: *connected,
                };
                Bytes::from(serde_json::to_string(&payload).unwrap_or_default())
            }
            Self::Statistics(stats) => {
                Bytes::from(serde_json::to_string(&stats).unwrap_or_default())
            }
            Self::Heartbeat(_) => Bytes::from("true"),
            Self::Announce(_) => Bytes::from("true"),
            _ => Bytes::new(),
        }
    }
}

// Helper trait for Redis channel operations
pub trait RedisChannel {
    fn channel_name(&self) -> String;
}

impl RedisChannel for CameraEvent {
    fn channel_name(&self) -> String {
        self.channel().to_channel().to_string()
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EncoderConfig {
    pub pixel_format: PixelTypes,
    pub bitrate: u32,
    pub keyframe_interval: u32,
}

#[derive(Serialize, Deserialize)]
pub struct StreamStatusPayload {
    identifier: String,
    connected: bool,
}

#[derive(Copy, Clone, PartialEq, Debug, Serialize, Deserialize)]
pub enum PixelTypes {
    YUV420,
    YUV422,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct StreamAddress {
    pub host: String,
    pub port: u16,
    pub ssl: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub enum OutputStreamConfig {
    File {
        identifier: String,
        path: String,
        append: bool,
    },
    Tcp {
        identifier: String,
        addresses: Vec<StreamAddress>,
        reconnect_attempts: u32,
        auth: String,
        serial: String,
        sign: String,
        stream_id: u64,
    },
}

impl OutputStreamConfig {
    pub fn identifier(&self) -> &str {
        match self {
            OutputStreamConfig::File { identifier, .. } => identifier,
            OutputStreamConfig::Tcp { identifier, .. } => identifier,
        }
    }
}

#[derive(Debug, Clone)]
pub struct CameraConfig {
    pub width: u32,
    pub height: u32,
    pub framerate: i32,
}

impl Default for CameraConfig {
    fn default() -> Self {
        Self {
            width: 1280,
            height: 720,
            framerate: 30,
        }
    }
}
