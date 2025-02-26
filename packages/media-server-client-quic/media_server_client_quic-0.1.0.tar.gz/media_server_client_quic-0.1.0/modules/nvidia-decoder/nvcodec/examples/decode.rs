mod demuxer;

// THIS IS THE EXAMPLE CODE FOR DECODING VIDEO USING NVDECODER
use crate::demuxer::ffmpeg::FFmpegDemuxStream;
use cuda_rs::{context::CuContext, device::CuDevice, stream::CuStream};
use futures::StreamExt;
use indicatif::ProgressBar;
use npp::{color::PixelFormat, image::DeviceImage};
use nvcodec::decoder::NVDecoder;
use nvcodec::input_video_frame::InputVideoFrame;
use protobuf_types::H264Message;
use std::path::Path;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let input_video = "/root/test.mp4".to_string();
    let output_dir = "/workspace/decoding_test".to_string();

    // --input-video /root/test.mp4 --output-dir /tmp

    let output_dir = Path::new(&output_dir);
    if !output_dir.exists() {
        std::fs::create_dir_all(output_dir)?;
    }

    cuda_rs::init().unwrap();

    let device = CuDevice::new(0).unwrap();
    let ctx = CuContext::retain_primary_context(&device).unwrap();
    let _guard = ctx.guard().unwrap();

    let mut demuxer = FFmpegDemuxStream::new(&input_video).unwrap();

    let bar = ProgressBar::new(demuxer.total_frames as u64);

    let stream = CuStream::new().unwrap();

    let mut decoder = NVDecoder::new(&stream, demuxer.codec_id.into(), None, None, false).unwrap();

    let mut i = 0;
    loop {
        tokio::select! {
            res = demuxer.next() => {
            match res {
                Some(res) => {
                    match res {
                        Ok(packet) => {
                            let msg: H264Message = (&packet).into();
                            decoder.decode(Some(InputVideoFrame {
                                data: msg, // Convert Vec<u8> to Bytes directly
                                stream_id: 51019231
                            })).unwrap();
                        },
                        Err(e) => {
                            eprintln!("demux error: {:?}", e);
                            break;
                        }
                    }
                }
                None => {
                    decoder.decode(None).unwrap();
                    break;
                }
            }
        }
            Some(res) = decoder.next() => {
                match res {
                    Ok(frame) => {
                        let device_image: DeviceImage = frame.into();

                        let device_image = device_image.convert_pixel_format(
                            PixelFormat::RGB, &stream
                        ).unwrap();

                         let host_mem = device_image.mem.to_host().unwrap();
                        //
                         stream.synchronize().unwrap();
                        //
                         image::save_buffer(
                             output_dir.join(format!("frame_{}.jpg", i)),
                             host_mem.as_slice(),
                             device_image.width as _,
                             device_image.height as _,
                             image::ColorType::Rgb8,
                         ).unwrap();

                        bar.inc(1);
                        i += 1;
                    },
                    Err(e) => {
                        eprintln!("decode error: {:?}", e);
                        continue;
                    }
                }
            }
            else => break,
        }
    }

    while let Some(res) = decoder.next().await {
        match res {
            Ok(_frame) => {
                bar.inc(1);
                i += 1;
            }
            Err(e) => {
                eprintln!("decode error: {:?}", e);
                break;
            }
        }
    }

    bar.finish();

    println!("done");
    Ok(())
}
