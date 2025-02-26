use serde::{Deserialize, Serialize};
use std::sync::atomic::{AtomicU64, AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};
use std::time::Instant;

#[derive(Debug)]
pub struct CameraStatistics {
    frames_captured: AtomicUsize,
    frames_encoded: AtomicUsize,
    frames_dropped: AtomicUsize,
    bytes_processed: AtomicU64,
    start_time: Arc<Mutex<Instant>>,
    last_update: Arc<Mutex<Instant>>,
    last_bytes: AtomicU64,
    last_frames: AtomicUsize,
}

impl Default for CameraStatistics {
    fn default() -> Self {
        Self::new()
    }
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct CameraMetrics {
    pub frames_captured: usize,
    pub frames_encoded: usize,
    pub frames_dropped: usize,
    pub throughput_mbps: f64,
    pub fps: f64,
    pub total_data_mb: f64,
    pub uptime_seconds: u64,
}

impl CameraStatistics {
    pub fn new() -> Self {
        let now = Instant::now();
        Self {
            frames_captured: AtomicUsize::new(0),
            frames_encoded: AtomicUsize::new(0),
            frames_dropped: AtomicUsize::new(0),
            bytes_processed: AtomicU64::new(0),
            start_time: Arc::new(Mutex::new(now)),
            last_update: Arc::new(Mutex::new(now)),
            last_bytes: AtomicU64::new(0),
            last_frames: AtomicUsize::new(0),
        }
    }

    pub fn record_frame_captured(&self) {
        self.frames_captured.fetch_add(1, Ordering::Relaxed);
    }

    pub fn record_frame_encoded(&self, bytes: u64) {
        self.frames_encoded.fetch_add(1, Ordering::Relaxed);
        self.bytes_processed.fetch_add(bytes, Ordering::Relaxed);
    }

    pub fn record_frame_dropped(&self) {
        self.frames_dropped.fetch_add(1, Ordering::Relaxed);
    }

    pub fn reset(&self) {
        self.frames_captured.store(0, Ordering::Relaxed);
        self.frames_encoded.store(0, Ordering::Relaxed);
        self.frames_dropped.store(0, Ordering::Relaxed);
        self.bytes_processed.store(0, Ordering::Relaxed);
        let now = Instant::now();
        *self.start_time.lock().unwrap() = now;
        *self.last_update.lock().unwrap() = now;
        self.last_bytes.store(0, Ordering::Relaxed);
        self.last_frames.store(0, Ordering::Relaxed);
    }

    pub fn get_metrics(&self) -> CameraMetrics {
        let now = Instant::now();
        let duration = now.duration_since(*self.last_update.lock().unwrap());
        let total_duration = now.duration_since(*self.start_time.lock().unwrap());

        // Get current values
        let current_frames = self.frames_captured.load(Ordering::Relaxed);
        let current_bytes = self.bytes_processed.load(Ordering::Relaxed);

        // Calculate throughput and FPS over the last interval
        let frame_delta = current_frames - self.last_frames.load(Ordering::Relaxed);
        let byte_delta = current_bytes - self.last_bytes.load(Ordering::Relaxed);

        let fps = if duration.as_secs_f64() > 0.0 {
            frame_delta as f64 / duration.as_secs_f64()
        } else {
            0.0
        };

        let throughput_mbps = if duration.as_secs_f64() > 0.0 {
            (byte_delta as f64 * 8.0) / (duration.as_secs_f64() * 1_000_000.0)
        } else {
            0.0
        };

        // Update last values
        *self.last_update.lock().unwrap() = now;
        self.last_frames.store(current_frames, Ordering::Relaxed);
        self.last_bytes.store(current_bytes, Ordering::Relaxed);

        CameraMetrics {
            frames_captured: self.frames_captured.load(Ordering::Relaxed),
            frames_encoded: self.frames_encoded.load(Ordering::Relaxed),
            frames_dropped: self.frames_dropped.load(Ordering::Relaxed),
            throughput_mbps,
            fps,
            total_data_mb: current_bytes as f64 / 1_000_000.0,
            uptime_seconds: total_duration.as_secs(),
        }
    }
}
