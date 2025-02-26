#[cfg(test)]
mod tests {
    use super::*;
    use tokio_test::assert_ok;

    #[tokio::test]
    async fn test_client_server_connection() {
        let server_addr: SocketAddr = "127.0.0.1:4434".parse().unwrap();

        // Start server
        let mut server = MediaServer::new(server_addr, Box::new(DummyMediaSource)).unwrap();
        tokio::spawn(async move {
            assert_ok!(server.run().await);
        });

        tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;

        // Connect client
        let (mut client, _) = MediaClient::new(server_addr, Box::new(DummyMediaSink)).unwrap();
        assert_ok!(client.connect(server_addr).await);
    }

    #[tokio::test]
    async fn test_media_streaming() {
        let server_addr: SocketAddr = "127.0.0.1:4435".parse().unwrap();

        // Start server
        let mut server = MediaServer::new(server_addr, Box::new(DummyMediaSource)).unwrap();
        tokio::spawn(async move {
            assert_ok!(server.run().await);
        });

        tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;

        // Connect client
        let (mut client, _) = MediaClient::new(server_addr, Box::new(DummyMediaSink)).unwrap();
        assert_ok!(client.connect(server_addr).await);

        // Let it stream for a while
        tokio::time::sleep(tokio::time::Duration::from_secs(2)).await;
    }
} 