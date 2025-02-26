// use crate::{H264Message};
// use std::error::Error;
// use std::sync::Arc;
// use tokio::sync::mpsc;
// use bytes::Bytes;
// use tracing::{info, error, debug};
// use thiserror::Error;
// use nvdec_rs::{DecoderConfig, Frame, NvDecoder};
//
// #[derive(Error, Debug)]
// pub enum DecoderError {
//     #[error("Failed to create decoder: {0}")]
//     Creation(String),
//     #[error("Decode error: {0}")]
//     Decode(String),
//     #[error("Frame error: {0}")]
//     Frame(String),
//     #[error("Channel error: {0}")]
//     Channel(String),
// }
//
// pub struct UnifiedDecoder {
//     decoder: Arc<NvDecoder>,
//     frame_tx: mpsc::Sender<Frame>,
//     frame_rx: mpsc::Receiver<Frame>,
// }
//
// impl UnifiedDecoder {
//     pub async fn new() -> Result<Self, DecoderError> {
//         let config = DecoderConfig {
//             max_width: 1920,
//             max_height: 1080,
//             num_decode_surfaces: 8,
//             ..Default::default()
//         };
//
//         let (frame_tx, frame_rx) = mpsc::channel(32);
//
//         let decoder = NvDecoder::new(config)
//             .map_err(|e| DecoderError::Creation(e.to_string()))?;
//
//         Ok(Self {
//             decoder: Arc::new(decoder),
//             frame_tx,
//             frame_rx,
//         })
//     }
//
//     pub async fn decode(&self, msg: H264Message) -> Result<(), DecoderError> {
//         let frame_data = Bytes::from(msg.data);
//         debug!("Starting decode for frame timestamp: {}", msg.timestamp);
//
//         // Decode frame
//         self.decoder.decode(frame_data, msg.timestamp as i64)
//             .map_err(|e| DecoderError::Decode(e.to_string()))?;
//
//         // Process any available decoded frames
//         while let Some(frame_result) = self.decoder.try_receive_frame().await {
//             match frame_result {
//                 Ok(frame) => {
//                     match self.frame_tx.try_send(frame) {
//                         Ok(_) => debug!("Sent decoded frame"),
//                         Err(e) => match e {
//                             mpsc::error::TrySendError::Full(_) => {
//                                 debug!("Frame channel full, skipping frame");
//                                 continue;
//                             }
//                             mpsc::error::TrySendError::Closed(_) => {
//                                 return Err(DecoderError::Channel("Frame channel closed".into()));
//                             }
//                         }
//                     }
//                 }
//                 Err(e) => {
//                     error!("Frame error: {}", e);
//                     // Continue processing other frames even if one fails
//                     continue;
//                 }
//             }
//         }
//
//         debug!("Completed decode for frame timestamp: {}", msg.timestamp);
//         Ok(())
//     }
//
//     pub async fn receive_frame(&mut self) -> Option<Frame> {
//         self.frame_rx.recv().await
//     }
// }
//
// pub async fn create_decoder_callback() -> Result<Box<dyn Fn(H264Message) -> Result<(), Box<dyn Error + Send + Sync>> + Send + Sync>, Box<dyn Error + Send + Sync>> {
//     let decoder = Arc::new(UnifiedDecoder::new().await?);
//     let callback_decoder = Arc::clone(&decoder);
//
//     Ok(Box::new(move |msg: H264Message| {
//         let decoder = Arc::clone(&callback_decoder);
//
//         // Fire and forget decode operation
//         tokio::spawn(async move {
//             if let Err(e) = decoder.decode(msg).await {
//                 error!("Decode error: {}", e);
//             }
//         });
//
//         Ok(())
//     }))
// }
