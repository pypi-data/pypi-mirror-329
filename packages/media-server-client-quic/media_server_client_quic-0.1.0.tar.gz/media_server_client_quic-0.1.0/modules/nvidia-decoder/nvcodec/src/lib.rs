pub extern crate nvcodec_sys as ffi;

pub mod codec;
pub mod decoder;
pub mod error;
pub mod input_video_frame;
pub mod surface;
pub use {
    codec::CuVideoCodecType,
    decoder::NVDecoder,
    error::{NVCodecError, NVCodecResult},
    surface::VideoSurfaceFormat,
};

pub use cuda_rs;
pub use npp;
pub use npp::image;
