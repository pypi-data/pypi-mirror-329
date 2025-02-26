use log::{error, info, trace};
use std::future::Future;
use std::pin::Pin;
use std::sync::Arc;
use tokio::task::JoinHandle;
use tokio::time::Duration;

pub type ServiceFuture<'a> =
    Pin<Box<dyn Future<Output = Result<(), Box<dyn std::error::Error>>> + Send + 'a>>;
pub type CleanupFuture = Pin<Box<dyn Future<Output = ()> + Send>>;

/// Trait defining the interface for a background service
pub trait ServiceTask: Send + Sync + 'static {
    /// The name of the service for logging purposes
    fn name(&self) -> &str;
    /// The interval at which this service should run
    fn interval(&self) -> Duration;
    /// The actual work to be performed
    fn execute(&self) -> ServiceFuture<'_>;
    /// Optional cleanup to be performed when the service is stopping
    fn cleanup(&self) -> CleanupFuture {
        Box::pin(async {})
    }
}

/// Main service runner that manages background tasks
pub struct BackgroundService {
    tasks: Vec<Arc<dyn ServiceTask>>,
    handles: Vec<JoinHandle<()>>,
}

impl Default for BackgroundService {
    fn default() -> Self {
        Self::new()
    }
}

impl BackgroundService {
    pub fn new() -> Self {
        Self {
            tasks: Vec::new(),
            handles: Vec::new(),
        }
    }

    /// Add a new task to be run
    pub fn register_task(&mut self, task: impl ServiceTask) {
        self.tasks.push(Arc::new(task));
    }

    /// Start all registered tasks
    pub async fn start_all(&mut self) {
        for task in &self.tasks {
            let task = Arc::clone(task);
            let interval_duration = task.interval();

            info!(
                "Starting background service: {} with interval {:?}",
                task.name(),
                interval_duration
            );

            let handle = tokio::spawn(async move {
                // Initial run
                if let Err(e) = task.execute().await {
                    error!(
                        "Error in initial execution of service {}: {}",
                        task.name(),
                        e
                    );
                }

                let mut interval = tokio::time::interval(interval_duration);

                loop {
                    interval.tick().await;
                    match task.execute().await {
                        Ok(_) => {
                            trace!("Successfully executed task: {}", task.name());
                        }
                        Err(e) => {
                            error!("Error in background service {}: {}", task.name(), e);
                        }
                    }
                }
            });

            self.handles.push(handle);
        }
    }

    /// Gracefully stop all tasks
    pub async fn stop_all(&mut self) {
        info!("Stopping all background services...");

        // Execute cleanup for all tasks
        for task in &self.tasks {
            task.cleanup().await;
        }

        // Abort all running tasks
        for handle in self.handles.drain(..) {
            handle.abort();
        }

        info!("All background services stopped");
    }
}
