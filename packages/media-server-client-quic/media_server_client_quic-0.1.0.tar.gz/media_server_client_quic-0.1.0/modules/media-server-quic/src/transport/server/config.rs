use anyhow::Result;
use std::sync::Arc;
use std::time::Duration;
use quinn::ServerConfig;

pub(crate) fn configure_server() -> Result<ServerConfig> {
    let cert = rcgen::generate_simple_self_signed(vec!["localhost".to_string()])?;
    let key = rustls::PrivateKey(cert.serialize_private_key_der());
    let cert = rustls::Certificate(cert.serialize_der()?);

    let mut server_config = ServerConfig::with_single_cert(vec![cert], key)?;
    let mut transport = quinn::TransportConfig::default();
    // Increase limits for 32 clients (32 * 3 streams each = 96)
    transport.max_concurrent_uni_streams(200u32.into());
    transport.max_concurrent_bidi_streams(200u32.into());
    transport.keep_alive_interval(Some(Duration::from_secs(5)));
    server_config.transport = Arc::new(transport);

    Ok(server_config)
} 