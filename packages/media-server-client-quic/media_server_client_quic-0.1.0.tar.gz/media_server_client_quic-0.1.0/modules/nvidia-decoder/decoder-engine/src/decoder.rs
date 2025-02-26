
use async_trait::async_trait;
use futures::Stream;
use nvcodec::input_video_frame::InputVideoFrame;
use nvcodec::npp::image::DeviceImage;
use protobuf_types::newbringer::H264Message;
use std::error::Error;
use std::pin::Pin;
use std::sync::mpsc::Sender;

#[derive(Debug)]
pub enum DecoderBackend {
    X264,
    NVDEC,
}

// Dont CLONE!
#[derive(Debug)]
pub struct DecodedFrame {
    pub ticket: i64,
    pub device_image: DeviceImage,
    pub stream_id: u64,
}

#[derive(Debug)]
pub struct DecodedFrameWithEncoded {
    pub ticket: i64,
    pub encoded_frame: H264Message,
    pub device_image: DeviceImage,
    pub stream_id: u64,
}

/// Commands that can be sent to the decoder
pub enum DecoderCommand {
    Decode { input_frame: InputVideoFrame },
    Flush,
    Reset,
    Stop,
}

/// Results from the decoder
pub type DecoderResult<T> = Result<Option<T>, Box<dyn Error + Send + Sync>>;
#[async_trait]
pub trait VideoDecoder: Send + Sync {
    type Frame;

    /// Start the decoder and return a sender for commands and implement Stream for frames
    async fn start(
        &mut self,
    ) -> (
        Sender<DecoderCommand>,
        Pin<Box<dyn Stream<Item = DecoderResult<Self::Frame>> + Send>>,
    );

    /// Decode a frame
    async fn decode(
        &mut self,
        input_frame: InputVideoFrame,
    ) -> Result<(), Box<dyn Error + Send + Sync>>;
}
