use once_cell::sync::Lazy;
use std::sync::Mutex;
use tracing_subscriber::util::SubscriberInitExt;
use tracing_subscriber::{fmt, prelude::*, reload, EnvFilter, Registry}; // removed Layer // added import

// change FilterHandle to use Registry
type FilterHandle = reload::Handle<EnvFilter, Registry>;
static FILTER_HANDLE: Lazy<Mutex<Option<FilterHandle>>> = Lazy::new(|| Mutex::new(None));

pub fn init_logger_with_level(log_level: &str) -> Result<(), String> {
    // Set the environment variable
    std::env::set_var("RUST_LOG", log_level);

    // Try to get the handle if we already have one
    if let Ok(handle_lock) = FILTER_HANDLE.lock() {
        if let Some(handle) = handle_lock.as_ref() {
            let new_filter = EnvFilter::from_default_env();
            handle
                .reload(new_filter)
                .map_err(|e| format!("Failed to update log level: {}", e))?;
            println!("Logger level updated to: {}", log_level);
            return Ok(());
        }
    }

    // First time initialization
    let env_filter = EnvFilter::from_default_env();
    let (filter_layer, reload_handle) = reload::Layer::new(env_filter);

    // Store the handle for future reloads
    if let Ok(mut handle_lock) = FILTER_HANDLE.lock() {
        *handle_lock = Some(reload_handle);
    } else {
        return Err("Failed to acquire lock for filter handle".to_string());
    }

    // Create the formatting layer
    let fmt_layer = fmt::layer()
        .with_file(true)
        .with_line_number(true)
        .with_target(false);

    // Compose the layers
    let subscriber = Registry::default().with(filter_layer).with(fmt_layer);

    // Use try_init() and log an info-level message when already initialized
    match subscriber.try_init() {
        Ok(()) => println!("Logger initialized with level: {}", log_level),
        Err(e) => println!("Unable to initialize logger: {}", e),
    }
    Ok(())
}

pub fn init_logger_from_env() -> Result<(), String> {
    println!("Initializing logger from environment variables");
    let log_level = std::env::var("NB_COMMON__LOGGING__RUST_LEVEL")
        .or_else(|_| std::env::var("RUST_LOG"))
        .unwrap_or_else(|_| {
            println!("No log level found in environment variables, defaulting to 'debug'");
            "debug".to_string()
        });

    init_logger_with_level(&log_level)
}
