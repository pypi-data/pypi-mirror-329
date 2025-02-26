use crate::decoder::{
    DecodedFrameWithEncoded, DecoderCommand, DecoderResult, VideoDecoder,
};
use async_trait::async_trait;
use futures::{Stream, StreamExt};
use nvcodec::cuda_rs;
use nvcodec::npp::image::DeviceImage;
use std::error::Error;
use std::pin::Pin;
use std::sync::mpsc;
use tokio::sync::mpsc as tokio_mpsc;
use tokio_util::task::TaskTracker;
use tracing::{debug, info, trace, warn};

use nvcodec::input_video_frame::InputVideoFrame;
use nvcodec::npp::color::PixelFormat;

enum CudaCommand {
    Decode(Option<InputVideoFrame>),
    Stop,
}

pub struct NvidiaDecoder {
    cuda_tx: Option<std::sync::mpsc::Sender<CudaCommand>>,
    command_tx: Option<tokio_mpsc::Sender<DecoderCommand>>,
    device_thread: Option<std::thread::JoinHandle<()>>,
    tasks: TaskTracker,
}

impl NvidiaDecoder {
    pub fn new() -> Result<Self, Box<dyn Error + Send + Sync>> {
        Ok(Self {
            cuda_tx: None,
            command_tx: None,
            device_thread: None,
            tasks: TaskTracker::new(),
        })
    }
}

#[async_trait]
impl VideoDecoder for NvidiaDecoder {
    type Frame = DecodedFrameWithEncoded;

    async fn start(
        &mut self,
    ) -> (
        mpsc::Sender<DecoderCommand>,
        Pin<Box<dyn Stream<Item = DecoderResult<Self::Frame>> + Send>>,
    ) {
        let (frame_tx, frame_rx) = tokio_mpsc::channel(32);
        let (cuda_tx, cuda_rx) = std::sync::mpsc::channel();
        let (command_tx, mut command_rx) = tokio_mpsc::channel(32);

        self.cuda_tx = Some(cuda_tx.clone());
        self.command_tx = Some(command_tx.clone());

        // Create a dedicated thread for CUDA operations
        let handle = std::thread::spawn(move || {
            info!("Starting CUDA thread");
            // Initialize CUDA in the dedicated thread
            cuda_rs::init().unwrap();
            let device = cuda_rs::device::CuDevice::new(0).unwrap();
            let ctx = cuda_rs::context::CuContext::retain_primary_context(&device).unwrap();
            let _guard = ctx.guard().unwrap();

            let stream = cuda_rs::stream::CuStream::new().unwrap();

            let mut decoder = nvcodec::decoder::NVDecoder::new(
                &stream,
                nvcodec::CuVideoCodecType::H264,
                None,
                None,
                false,
            )
            .unwrap();

            let runtime = tokio::runtime::Builder::new_current_thread()
                .enable_all()
                .build()
                .unwrap();

            runtime.block_on(async {
                debug!("CUDA thread runtime started");
                let mut next_ticket = 1;

                // Create an async channel for the bridge
                let (bridge_tx, mut bridge_rx) = tokio_mpsc::channel(32);

                // Spawn a task to bridge the sync channel to async
                let _bridge_handle = std::thread::spawn(move || {
                    let bridge_runtime = tokio::runtime::Builder::new_current_thread()
                        .enable_all()
                        .build()
                        .unwrap();

                    while let Ok(cmd) = cuda_rx.recv() {
                        if bridge_runtime.block_on(bridge_tx.send(cmd)).is_err() {
                            break;
                        }
                    }
                });

                loop {
                    tokio::select! {
                        // Check for incoming commands through the bridge
                        Some(cmd) = bridge_rx.recv() => {
                            match cmd {
                                CudaCommand::Decode(packet) => {
                                    trace!("CUDA thread processing decode command");
                                    if let Err(e) = decoder.decode(packet) {
                                        warn!("Decode error: {:?}", e);
                                        let boxed_err: Box<dyn Error + Send + Sync> = Box::new(e);
                                        let _ = frame_tx.send(Err(boxed_err)).await;
                                    }
                                    trace!("Decode command processed successfully");
                                }
                                CudaCommand::Stop => {
                                    debug!("CUDA thread received stop command");
                                    break;
                                }

                            }
                        }

                        // Process decoded frames
                        Some(frame_result) = decoder.next() => {
                            match frame_result {
                                Ok(frame) => {
                                    trace!("Processing decoded frame");
                                    let stream_id = frame.packet_data.input_frame.stream_id;
                                    let encoded_frame_data = frame.packet_data.input_frame.data.clone();  // Clone the data before move
                                    let device_image: DeviceImage = frame.into();

                                    let device_image = device_image.convert_pixel_format(
                                        PixelFormat::RGB,
                                        &stream
                                    ).unwrap();

                                    let ticket = next_ticket;
                                    next_ticket += 1;

                                    let decoded_frame = DecodedFrameWithEncoded {
                                        device_image,
                                        encoded_frame: encoded_frame_data,  // Use the saved data
                                        stream_id,
                                        ticket,
                                    };

                                    if frame_tx.send(Ok(Some(decoded_frame))).await.is_err() {
                                        warn!("Failed to send decoded frame");
                                        break;
                                    }
                                    trace!("Frame {} sent successfully", ticket);

                                    // let host_mem = device_image.mem.to_host().unwrap();
                                    // let output_dir = std::path::Path::new("/workspace/decoding_test");
                                    // image::save_buffer(
                                    //     output_dir.join(format!("frame_{}.jpg", ticket)),
                                    //     host_mem.as_slice(),
                                    //     device_image.width as _,
                                    //     device_image.height as _,
                                    //     image::ColorType::Rgb8,
                                    // ).unwrap();

                                }
                                Err(e) => {
                                    warn!("Frame decode error: {:?}", e);
                                    let boxed_err: Box<dyn Error + Send + Sync> = Box::new(e);
                                    if frame_tx.send(Err(boxed_err)).await.is_err() {
                                        break;
                                    }
                                }
                            }
                        }
                        else => break,
                    }
                }

                // Process any remaining frames
                while let Some(frame_result) = decoder.next().await {
                    match frame_result {
                        Ok(frame) => {
                            let stream_id = frame.packet_data.input_frame.stream_id;
                            let encoded_frame_data = frame.packet_data.input_frame.data.clone(); // Clone the data before move
                            let device_image: DeviceImage = frame.into();

                            let device_image = device_image
                                .convert_pixel_format(PixelFormat::RGB, &stream)
                                .unwrap();

                            let ticket = next_ticket;
                            next_ticket += 1;

                            let decoded_frame = DecodedFrameWithEncoded {
                                device_image,
                                encoded_frame: encoded_frame_data, // Use the saved data
                                stream_id,
                                ticket,
                            };
                            if frame_tx.send(Ok(Some(decoded_frame))).await.is_err() {
                                break;
                            }
                        }
                        Err(e) => {
                            let boxed_err: Box<dyn Error + Send + Sync> = Box::new(e);
                            let _ = frame_tx.send(Err(boxed_err)).await;
                            break;
                        }
                    }
                }

                info!("CUDA thread loop ended");
            });
        });

        self.device_thread = Some(handle);

        // Spawn command handling task
        let cuda_tx_for_task = cuda_tx.clone();
        self.tasks.spawn(async move {
            debug!("Starting command handling task");
            while let Some(cmd) = command_rx.recv().await {
                trace!("Received command in handler");
                match cmd {
                    DecoderCommand::Decode { input_frame } => {
                        trace!("Sending decode command to CUDA thread");
                        if let Err(e) =
                            cuda_tx_for_task.send(CudaCommand::Decode(Some(input_frame)))
                        {
                            warn!("Failed to send to CUDA thread: {}", e);
                        }
                    }
                    DecoderCommand::Flush => {
                        let _ = cuda_tx_for_task.send(CudaCommand::Decode(None));
                    }
                    DecoderCommand::Reset => {
                        // Handle reset if needed
                    }
                    DecoderCommand::Stop => {
                        let _ = cuda_tx_for_task.send(CudaCommand::Stop);
                        break;
                    }
                }
            }
            debug!("Command handling task ended");
        });

        let (sync_tx, sync_rx) = mpsc::channel();

        // Bridge between sync and async channels
        let command_tx_clone = command_tx.clone();
        self.tasks.spawn(async move {
            while let Ok(cmd) = sync_rx.recv() {
                if command_tx_clone.send(cmd).await.is_err() {
                    break;
                }
            }
        });

        // Convert the receiver into a Stream
        let stream = Box::pin(async_stream::stream! {
            let mut rx = frame_rx;
            while let Some(frame) = rx.recv().await {
                yield frame;
            }
        });

        (sync_tx, stream)
    }

    async fn decode(
        &mut self,
        input_frame: InputVideoFrame,
    ) -> Result<(), Box<dyn Error + Send + Sync>> {
        if let Some(ref tx) = self.command_tx {
            tx.send(DecoderCommand::Decode { input_frame }).await?;
            trace!("Sent decode command through async channel");
        }
        Ok(())
    }
}

impl Drop for NvidiaDecoder {
    fn drop(&mut self) {
        if let Some(tx) = self.cuda_tx.take() {
            let _ = tx.send(CudaCommand::Stop);
        }
        if let Some(handle) = self.device_thread.take() {
            handle.join().unwrap();
        }
    }
}
