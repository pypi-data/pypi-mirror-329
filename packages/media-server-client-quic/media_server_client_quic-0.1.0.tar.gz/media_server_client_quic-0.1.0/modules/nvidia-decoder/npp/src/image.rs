use crate::{
    color::{ColorRange, ColorSpace, PixelFormat},
    cvt_color::convert_pixel_format,
    error::NppResult,
};
use cuda_rs::{
    cuda_rs_sys::cuDeviceGetAttribute, cuda_rs_sys::cuIpcGetMemHandle, cuda_rs_sys::CUdeviceptr,
    error::CuError, error::CuResult, memory::PitchedDeviceMemory, stream::CuStream,
};

use log::{debug, warn};
use std::sync::Arc;

#[derive(Clone, Debug)]
pub struct CudaIpcHandle {
    data: Arc<Vec<u8>>,
}

impl CudaIpcHandle {
    pub fn new(device_ptr: CUdeviceptr) -> CuResult<Self> {
        unsafe {
            debug!("Creating IPC handle for CUDA memory at {:#x}", device_ptr);

            // Check if device supports IPC
            let mut ipc_supported: i32 = 0;
            let dev_result = cuDeviceGetAttribute(
                &mut ipc_supported,
                125, // CU_DEVICE_ATTRIBUTE_IPC_EVENT_SUPPORTED
                0,   // Assuming device 0
            );
            debug!(
                "IPC support check result: {}, supported: {}",
                dev_result, ipc_supported
            );

            // Create a properly aligned CUipcMemHandle
            #[repr(C, align(64))]
            struct AlignedHandle {
                data: [u8; 64],
            }
            let mut handle = AlignedHandle { data: [0; 64] };

            let result = cuIpcGetMemHandle(&mut handle as *mut AlignedHandle as *mut _, device_ptr);
            debug!("cuIpcGetMemHandle result: {}", result);

            if result != 0 {
                warn!("Failed to get IPC handle: CUDA_ERROR_INVALID_VALUE");
                return Err(CuError::from(result));
            }

            debug!("Handle size: {} bytes", handle.data.len());
            debug!(
                "Handle bytes: {:02x?}",
                &handle.data[..std::cmp::min(32, handle.data.len())]
            );

            Ok(Self {
                data: Arc::new(handle.data.to_vec()),
            })
        }
    }

    pub fn as_bytes(&self) -> &[u8] {
        &self.data
    }

    pub fn into_vec(self) -> Vec<u8> {
        Arc::try_unwrap(self.data).unwrap_or_else(|arc| (*arc).clone())
    }
}

#[derive(Debug)]
pub struct DeviceImage {
    pub mem: PitchedDeviceMemory,
    pub width: usize,
    pub height: usize,
    pub pixel_format: PixelFormat,
    pub color_space: ColorSpace,
    pub color_range: ColorRange,
}

impl DeviceImage {
    pub fn new(
        width: usize,
        height: usize,
        pixel_format: PixelFormat,
        color_space: ColorSpace,
        color_range: ColorRange,
        stream: &CuStream,
    ) -> NppResult<Self> {
        let (mem_width, mem_height) = get_memory_size(width, height, pixel_format);
        let mem = PitchedDeviceMemory::new(mem_width, mem_height, stream)?;
        Ok(Self {
            mem,
            width,
            height,
            pixel_format,
            color_space,
            color_range,
        })
    }

    pub fn from_memory(
        mem: PitchedDeviceMemory,
        width: usize,
        height: usize,
        pixel_format: PixelFormat,
        color_space: ColorSpace,
        color_range: ColorRange,
    ) -> Self {
        Self {
            mem,
            width,
            height,
            pixel_format,
            color_space,
            color_range,
        }
    }

    pub fn convert_pixel_format(
        &self,
        dst_pixel_format: PixelFormat,
        stream: &CuStream,
    ) -> NppResult<DeviceImage> {
        let mut dst = DeviceImage::new(
            self.width,
            self.height,
            dst_pixel_format,
            self.color_space,
            self.color_range,
            stream,
        )?;

        convert_pixel_format(self, &mut dst)?;

        Ok(dst)
    }

    pub fn pitch(&self) -> usize {
        self.mem.pitch
    }

    pub fn get_raw(&self) -> *mut u8 {
        unsafe { self.mem.get_raw() as *mut u8 }
    }
}

pub fn get_memory_size(width: usize, height: usize, pixel_format: PixelFormat) -> (usize, usize) {
    match pixel_format {
        PixelFormat::RGB | PixelFormat::BGR | PixelFormat::HSV => (width * 3, height),
        PixelFormat::NV12 => (width, height * 3 / 2),
        _ => unimplemented!(),
    }
}
