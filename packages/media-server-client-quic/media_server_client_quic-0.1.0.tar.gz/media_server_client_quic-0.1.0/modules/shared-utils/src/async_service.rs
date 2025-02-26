use futures_util::future::BoxFuture;
use lazy_static::lazy_static;
use std::io;
use std::sync::{Arc, Mutex, Once};
use tokio::runtime::Runtime;
use tokio::sync::oneshot;

lazy_static! {
    static ref RUNTIME: Runtime = Runtime::new().expect("Failed to create runtime");
}

pub trait AsyncService: Send + Sync + 'static {
    fn run(&self, shutdown: oneshot::Receiver<()>) -> BoxFuture<'static, io::Result<()>>;
}

pub struct ServiceRunner<S: AsyncService> {
    service: Arc<S>,
    start_once: Once,
    shutdown_signal: Mutex<Option<oneshot::Sender<()>>>,
}

impl<S: AsyncService> ServiceRunner<S> {
    pub fn new(service: S) -> Self {
        Self {
            service: Arc::new(service),
            start_once: Once::new(),
            shutdown_signal: Mutex::new(None),
        }
    }

    pub fn start(&self) -> io::Result<()> {
        self.start_once.call_once(|| {
            let (shutdown_tx, shutdown_rx) = oneshot::channel();
            let service = self.service.clone();

            RUNTIME.spawn(async move {
                let _ = service.run(shutdown_rx).await;
            });

            let mut signal = self.shutdown_signal.lock().unwrap();
            *signal = Some(shutdown_tx);
        });

        Ok(())
    }

    pub fn stop(&self) -> io::Result<()> {
        let mut signal = self.shutdown_signal.lock().unwrap();
        if let Some(tx) = signal.take() {
            let _ = tx.send(());
        }
        Ok(())
    }
}

// Helper functions to simplify FFI
pub fn start_service<S: AsyncService>(runner: &ServiceRunner<S>) -> io::Result<()> {
    runner.start()
}

pub fn stop_service<S: AsyncService>(runner: &ServiceRunner<S>) -> io::Result<()> {
    runner.stop()
}
