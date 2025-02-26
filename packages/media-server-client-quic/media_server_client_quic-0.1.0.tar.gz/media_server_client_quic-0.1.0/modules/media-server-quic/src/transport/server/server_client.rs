use anyhow::Result;
use std::sync::Arc;
use std::time::{Duration, Instant};
use std::sync::atomic::{AtomicU64, Ordering};
use tokio::sync::Mutex;
use tracing::info;
use protobuf_types::media_streaming::H264Message;

use crate::common::{MediaSink, StreamStats, AudioFrame};

// Common pattern for media frame handling
macro_rules! handle_video {
    ($self:ident, $frame:expr) => {
        {
            let mut inner = $self.inner.lock().await;
            let stream_id = inner.stream_id;
            inner.sink.handle_video($frame, stream_id).await
        }
    };
}

macro_rules! handle_audio {
    ($self:ident, $frame:expr) => {
        {
            let mut inner = $self.inner.lock().await;
            let stream_id = inner.stream_id;
            inner.sink.handle_audio($frame, stream_id).await
        }
    };
}

#[derive(Clone)]
pub struct ServerClient {
    pub(crate) client_id: u64,
    pub(crate) inner: Arc<Mutex<ServerClientInner>>,
    pub(crate) last_keep_alive: Arc<AtomicU64>,
}

pub(crate) struct ServerClientInner {
    sink: Box<dyn MediaSink>,
    stats: StreamStats,
    last_transit: Duration,
    stream_id: u64,
}

impl std::fmt::Debug for ServerClient {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ServerClient")
            .field("client_id", &self.client_id)
            .field("last_keep_alive", &self.last_keep_alive)
            .finish_non_exhaustive()
    }
}

impl ServerClient {
    pub fn new(client_id: u64, sink: Box<dyn MediaSink>) -> Self {
        Self {
            client_id,
            inner: Arc::new(Mutex::new(ServerClientInner {
                sink,
                stats: StreamStats::new(),
                last_transit: Duration::ZERO,
                stream_id: client_id,
            })),
            last_keep_alive: Arc::new(AtomicU64::new(Instant::now().elapsed().as_nanos() as u64)),
        }
    }

    #[inline]
    pub async fn handle_video(&self, frame: H264Message) -> Result<()> {
        handle_video!(self, frame)
    }

    #[inline]
    pub async fn handle_audio(&self, frame: AudioFrame) -> Result<()> {
        handle_audio!(self, frame)
    }

    #[inline]
    pub fn update_keep_alive(&self) {
        self.last_keep_alive.store(
            Instant::now().elapsed().as_nanos() as u64,
            Ordering::Release
        );
    }

    #[inline]
    pub fn get_elapsed_since_keep_alive(&self) -> Duration {
        let last = self.last_keep_alive.load(Ordering::Acquire);
        let now = Instant::now().elapsed().as_nanos() as u64;
        Duration::from_nanos(now.saturating_sub(last))
    }

    #[inline]
    pub async fn handle_ping(&self, sequence_number: u64, _timestamp: u64, total_size: usize) -> Result<()> {
        self.update_keep_alive();
        let mut inner = self.inner.lock().await;
        let stats = &mut inner.stats.network;
        stats.update_packet_loss(false);
        stats.update_throughput(total_size as f64);
        drop(inner);
        info!("Processed ping {} with size {} bytes", sequence_number, total_size);
        Ok(())
    }

    #[inline]
    pub async fn get_current_jitter(&self) -> Duration {
        self.inner.lock().await.stats.network.avg_jitter
    }

    #[inline]
    pub async fn update_network_stats(&self, rtt: Duration, jitter: Duration, total_size: usize) {
        let mut inner = self.inner.lock().await;
        let stats = &mut inner.stats.network;
        stats.update_rtt(rtt);
        stats.update_jitter(jitter);
        stats.update_packet_loss(false);
        stats.update_throughput(total_size as f64);
    }

    #[inline]
    pub async fn handle_pong(&self, sequence_number: u64, timestamp: u64, receive_timestamp: u64, total_size: usize) {
        let (now, rtt, transit) = self.calculate_timing(timestamp, receive_timestamp);
        
        // Single lock for all stats updates
        let mut inner = self.inner.lock().await;
        let last_transit = inner.last_transit;
        let current_jitter = inner.stats.network.avg_jitter;
        
        let new_jitter = crate::transport::calculate_rfc3550_jitter(
            transit, 
            last_transit,
            current_jitter
        );
        
        let stats = &mut inner.stats.network;
        stats.update_rtt(rtt);
        stats.update_jitter(new_jitter);
        stats.update_packet_loss(false);
        stats.update_throughput(total_size as f64);
        inner.last_transit = transit;
        drop(inner);
        
        info!(
            "Pong {} - size: {}B, rtt: {:?}, transit: {:?}, return: {:?}",
            sequence_number,
            total_size,
            rtt,
            transit,
            Duration::from_micros(now - receive_timestamp)
        );
    }

    #[inline]
    fn calculate_timing(&self, timestamp: u64, receive_timestamp: u64) -> (u64, Duration, Duration) {
        let now = crate::transport::current_timestamp_micros();
        let rtt = Duration::from_micros(now - timestamp);
        let transit = Duration::from_micros(receive_timestamp - timestamp);
        (now, rtt, transit)
    }

    #[inline]
    pub async fn get_stats(&self) -> StreamStats {
        self.inner.lock().await.stats.clone()
    }
} 