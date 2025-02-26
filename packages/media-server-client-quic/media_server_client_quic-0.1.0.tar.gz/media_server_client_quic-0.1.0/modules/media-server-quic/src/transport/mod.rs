pub mod client;
pub mod server;
pub mod packet;
pub mod packet_io;
pub(crate) mod proto_conversion;

pub use client::StreamClient;
pub use server::StreamServer;
pub use packet::{MediaPacket, ControlPacket};

use std::time::{SystemTime, UNIX_EPOCH, Duration};

// Add conversion traits for H264Message
pub trait IntoMediaStreaming {
    type Output;
    fn into_media_streaming(self) -> Self::Output;
}

pub trait IntoNewbringer {
    type Output;
    fn into_newbringer(self) -> Self::Output;
}

impl IntoMediaStreaming for protobuf_types::newbringer::H264Message {
    type Output = protobuf_types::media_streaming::H264Message;

    fn into_media_streaming(self) -> Self::Output {
        protobuf_types::media_streaming::H264Message {
            data: self.data,
            timestamp: self.timestamp,
            frame_type: self.frame_type,
            metadata: self.metadata,
            width: self.width,
            height: self.height,
        }
    }
}

impl IntoNewbringer for protobuf_types::media_streaming::H264Message {
    type Output = protobuf_types::newbringer::H264Message;

    fn into_newbringer(self) -> Self::Output {
        protobuf_types::newbringer::H264Message {
            data: self.data,
            timestamp: self.timestamp,
            frame_type: self.frame_type,
            metadata: self.metadata,
            width: self.width,
            height: self.height,
        }
    }
}

// Helper function to get current timestamp in microseconds
pub(crate) fn current_timestamp_micros() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_micros() as u64
}

/// Calculate network jitter according to RFC 3550 section 6.4.1
/// 
/// The interarrival jitter is calculated continuously as specified by the following formula:
/// ```text
/// J(i) = J(i-1) + (|D(i-1,i)| - J(i-1))/16
/// ```
/// where:
/// - J(i) is the current jitter estimate
/// - J(i-1) is the previous jitter estimate
/// - D(i-1,i) is the difference between packet spacing at the receiver compared to sender
/// 
/// The RFC specifies using a weight of 1/16 to reduce noise in the estimate while
/// maintaining good responsiveness.
/// 
/// # Arguments
/// * `transit_time` - Current packet's transit time (receive_timestamp - send_timestamp)
/// * `last_transit` - Previous packet's transit time
/// * `last_jitter` - Previous jitter estimate
/// 
/// # Returns
/// The new jitter estimate as a Duration
#[inline]
pub(crate) fn calculate_rfc3550_jitter(
    transit_time: Duration,
    last_transit: Duration,
    last_jitter: Duration,
) -> Duration {
    // If this is the first packet, we can't calculate jitter yet
    if last_transit == Duration::ZERO {
        return Duration::ZERO;
    }

    // Calculate absolute difference in transit times
    let transit_delta = if transit_time > last_transit {
        transit_time - last_transit
    } else {
        last_transit - transit_time
    };

    // Apply the RFC 3550 jitter formula: J(i) = J(i-1) + (|D(i-1,i)| - J(i-1))/16
    let jitter_micros = last_jitter.as_micros() as i128;
    let delta_micros = transit_delta.as_micros() as i128;
    
    // Calculate (|D(i-1,i)| - J(i-1))/16 with integer arithmetic
    let adjustment = (delta_micros - jitter_micros) / 16;
    let new_jitter = jitter_micros + adjustment;
    
    // Ensure we never return zero jitter unless it's the first packet
    if new_jitter <= 0 {
        // Return a minimal jitter value (1 microsecond) to avoid zero
        Duration::from_micros(1)
    } else {
        Duration::from_micros(new_jitter as u64)
    }
}

// Re-export common types and constants
pub use crate::common::{
    STREAM_CHUNK_SIZE,
    MAX_CONCURRENT_STREAMS,
    IDLE_TIMEOUT,
    STATS_INTERVAL,
    StreamStats,
};

// Remove everything below this line 