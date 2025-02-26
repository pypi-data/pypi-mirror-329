use crate::{context::CuContext, error::CuError, error::CuResult, ffi};
use std::ptr::NonNull;
use std::sync::Arc;

/// A CUDA stream object that can be either owned or borrowed.
/// Owned streams are reference counted and automatically destroyed when the last reference is dropped.
/// Borrowed streams are not destroyed when dropped.
#[derive(Debug)]
pub struct CUstream {
    stream: NonNull<ffi::CUstream_st>,
}

// CUDA streams are thread-safe according to NVIDIA's documentation
unsafe impl Send for CUstream {}
unsafe impl Sync for CUstream {}

impl CUstream {
    /// Creates a new CUDA stream
    pub fn new() -> Result<Self, CuError> {
        let mut stream = std::ptr::null_mut();
        unsafe {
            let res = ffi::cuStreamCreate(&mut stream, 0);
            if res != ffi::cudaError_enum_CUDA_SUCCESS {
                return Err(CuError::from(res));
            }
            let stream = NonNull::new(stream)
                .expect("CUDA stream creation returned null despite success status");
            Ok(Self { stream })
        }
    }

    /// Returns the underlying CUDA stream pointer
    pub fn as_ptr(&self) -> *mut ffi::CUstream_st {
        self.stream.as_ptr()
    }
}

impl Drop for CUstream {
    fn drop(&mut self) {
        unsafe {
            ffi::cuStreamDestroy_v2(self.stream.as_ptr());
        }
    }
}

/// Internal representation of a stream that can be either owned or borrowed
#[derive(Clone, Debug)]
enum Inner {
    Owned(Arc<CUstream>),
    Borrowed(ffi::CUstream),
}

// Implement Send and Sync for Inner
unsafe impl Send for Inner {}
unsafe impl Sync for Inner {}

/// High-level wrapper around a CUDA stream
#[derive(Debug)]
pub struct CuStream(Inner);

// Implement Send and Sync for CuStream
unsafe impl Send for CuStream {}
unsafe impl Sync for CuStream {}

impl CuStream {
    /// Creates a new CUDA stream with default flags
    pub fn new() -> CuResult<Self> {
        let mut s = std::ptr::null_mut();
        let res =
            unsafe { ffi::cuStreamCreate(&mut s, ffi::CUstream_flags_enum_CU_STREAM_DEFAULT) };

        if res != ffi::cudaError_enum_CUDA_SUCCESS {
            return Err(CuError::from(res));
        }

        // Safe because we just created the stream and checked for errors
        let stream = unsafe {
            CUstream {
                stream: NonNull::new_unchecked(s),
            }
        };

        let stream = CuStream(Inner::Owned(Arc::new(stream)));
        Ok(stream)
    }

    /// Creates a new stream wrapper from a raw CUDA stream pointer.
    /// The stream will not be destroyed when dropped.
    ///
    /// # Safety
    /// The caller must ensure that the stream pointer is valid and outlives this object
    pub unsafe fn from_raw(s: ffi::CUstream) -> Self {
        CuStream(Inner::Borrowed(s))
    }

    /// Waits for all work in the stream to complete
    pub fn synchronize(&self) -> CuResult<()> {
        let res = unsafe { ffi::cuStreamSynchronize(self.get_raw()) };
        wrap!((), res)
    }

    /// Gets the CUDA context associated with this stream
    pub fn get_context(&self) -> CuResult<CuContext> {
        let mut ctx = std::ptr::null_mut();
        let (ctx, res) = unsafe {
            let raw_stream = self.get_raw();
            let res = ffi::cuStreamGetCtx(raw_stream, &mut ctx);
            let ctx = CuContext::from_raw(ctx);
            (ctx, res)
        };
        wrap!(ctx, res)
    }

    /// Gets the underlying CUDA stream pointer
    ///
    /// # Safety
    /// The caller must ensure that the pointer is not used after the stream is destroyed
    pub unsafe fn get_raw(&self) -> ffi::CUstream {
        match self.0 {
            Inner::Owned(ref s) => s.stream.as_ptr(),
            Inner::Borrowed(s) => s,
        }
    }
}

impl Clone for CuStream {
    fn clone(&self) -> Self {
        match self.0 {
            Inner::Owned(ref s) => CuStream(Inner::Owned(s.clone())),
            Inner::Borrowed(s) => CuStream(Inner::Borrowed(s)),
        }
    }
}
