#[macro_use]
extern crate enum_primitive;

pub extern crate cuda_rs_sys as ffi;

#[macro_use]
mod macros;

pub mod context;
pub mod device;
pub mod error;
pub mod event;
pub mod info;
pub mod memory;
pub mod stream;

// export the ffi module
pub use ffi as cuda_rs_sys;

pub fn init() -> Result<(), error::CuError> {
    let res = unsafe { ffi::cuInit(0) };
    wrap!((), res)
}
