use crate::{context::CuContext, error::CuResult, ffi};
use std::os::raw::c_int;

#[derive(Copy, Clone)]
pub struct CuDevice(ffi::CUdevice);

impl CuDevice {
    pub fn new(ordinal: u32) -> CuResult<Self> {
        let mut d = CuDevice(0);
        let res = unsafe { ffi::cuDeviceGet(&mut d.0 as *mut i32, ordinal as c_int) };

        wrap!(d, res)
    }

    pub fn get_device_count() -> CuResult<i32> {
        let mut count = 0;
        let res = unsafe { ffi::cuDeviceGetCount(&mut count as *mut i32) };

        wrap!(count, res)
    }

    pub fn retain_primary_context(&self) -> CuResult<CuContext> {
        CuContext::retain_primary_context(self)
    }

    pub fn total_memory(&self) -> CuResult<usize> {
        let mut nbytes = 0;
        let res = unsafe { ffi::cuDeviceTotalMem_v2(&mut nbytes as *mut usize, self.0) };

        wrap!(nbytes, res)
    }

    pub fn get_raw(&self) -> ffi::CUdevice {
        self.0
    }
}
