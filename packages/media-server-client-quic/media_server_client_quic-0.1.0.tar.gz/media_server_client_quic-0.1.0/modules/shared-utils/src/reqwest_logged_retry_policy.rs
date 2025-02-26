use anyhow::Error as AnyhowError;
use http::Extensions;
use log::{info, warn};
use reqwest::Client;
use reqwest_middleware::{
    reqwest::Request, ClientBuilder, ClientWithMiddleware, Error as ClientError, Middleware, Next,
};
use std::future::Future;
use std::pin::Pin;
use std::time::Duration;

#[derive(Debug, Clone)]
pub struct RetryMiddleware {
    min_retry_delay: Duration,
    max_retry_delay: Duration,
    max_retries: u32,
    url: std::sync::Arc<std::sync::Mutex<String>>,
}

impl RetryMiddleware {
    pub fn new(min_retry_delay: Duration, max_retry_delay: Duration, max_retries: u32) -> Self {
        Self {
            min_retry_delay,
            max_retry_delay,
            max_retries,
            url: std::sync::Arc::new(std::sync::Mutex::new(String::new())),
        }
    }

    fn calculate_delay(&self, retry_count: u32) -> Duration {
        let base = 2_u32;
        let delay = self.min_retry_delay.as_millis() as u32 * base.pow(retry_count);
        let delay = delay as u64;

        Duration::from_millis(delay.min(self.max_retry_delay.as_millis() as u64))
    }

    fn retry_request<'a>(
        &'a self,
        req: Request,
        extensions: &'a mut Extensions,
        next: Next<'a>,
        retry_count: u32,
    ) -> Pin<Box<dyn Future<Output = reqwest_middleware::Result<reqwest::Response>> + Send + 'a>>
    {
        Box::pin(async move {
            let url = req.url().to_string();
            if let Ok(mut current_url) = self.url.lock() {
                *current_url = url;
            }

            // Clone the request before using it
            let req_clone = req.try_clone().ok_or_else(|| {
                ClientError::Middleware(AnyhowError::msg("Request cannot be cloned for retry"))
            })?;

            let result = next.clone().run(req, extensions).await;

            match result {
                Ok(response) => Ok(response),
                Err(err) => {
                    if retry_count >= self.max_retries {
                        warn!(
                            "Retry policy exhausted after {} attempts for endpoint {}",
                            retry_count,
                            self.url.lock().unwrap()
                        );
                        return Err(err);
                    }

                    let delay = self.calculate_delay(retry_count);
                    info!(
                        "Retry attempt #{} for endpoint {} - Sleeping for {:.3}ms before next attempt",
                        retry_count,
                        self.url.lock().unwrap(),
                        delay.as_millis() as f64
                    );

                    tokio::time::sleep(delay).await;

                    self.retry_request(req_clone, extensions, next, retry_count + 1)
                        .await
                }
            }
        })
    }
}

#[async_trait::async_trait]
impl Middleware for RetryMiddleware {
    async fn handle(
        &self,
        req: Request,
        extensions: &mut Extensions,
        next: Next<'_>,
    ) -> reqwest_middleware::Result<reqwest::Response> {
        self.retry_request(req, extensions, next, 0).await
    }
}

pub fn create_retry_client() -> ClientWithMiddleware {
    let retry_middleware =
        RetryMiddleware::new(Duration::from_millis(100), Duration::from_secs(30), 5);

    ClientBuilder::new(Client::new())
        .with(retry_middleware)
        .build()
}
