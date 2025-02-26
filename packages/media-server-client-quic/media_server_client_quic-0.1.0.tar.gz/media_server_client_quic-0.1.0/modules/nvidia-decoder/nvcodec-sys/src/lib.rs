#![allow(dead_code)]
#![allow(non_snake_case)]
#![allow(non_camel_case_types)]
#![allow(non_upper_case_globals)]
#![allow(clippy::all)] // Disable all clippy warnings as we are using bindgen

include!(concat!(env!("OUT_DIR"), "/bindings.rs"));

use libloading::{Library, Symbol};
use std::sync::Arc;
use std::sync::OnceLock;

// Function types (same as before)
type CuvidCreateVideoParserFn =
    unsafe extern "C" fn(*mut CUvideoparser, *mut CUVIDPARSERPARAMS) -> CUresult;
type CuvidParseVideoDataFn =
    unsafe extern "C" fn(CUvideoparser, *mut CUVIDSOURCEDATAPACKET) -> CUresult;
type CuvidDestroyVideoParserFn = unsafe extern "C" fn(CUvideoparser) -> CUresult;
type CuvidDestroyDecoderFn = unsafe extern "C" fn(CUvideodecoder) -> CUresult;
type CuvidCtxLockDestroyFn = unsafe extern "C" fn(CUvideoctxlock) -> CUresult;
type CuvidGetDecoderCapsFn = unsafe extern "C" fn(*mut CUVIDDECODECAPS) -> CUresult;
type CuvidCreateDecoderFn =
    unsafe extern "C" fn(*mut CUvideodecoder, *mut CUVIDDECODECREATEINFO) -> CUresult;
type CuvidReconfigureDecoderFn =
    unsafe extern "C" fn(CUvideodecoder, *mut CUVIDRECONFIGUREDECODERINFO) -> CUresult;
type CuvidDecodePictureFn = unsafe extern "C" fn(CUvideodecoder, *mut CUVIDPICPARAMS) -> CUresult;
type CuvidMapVideoFrame64Fn = unsafe extern "C" fn(
    CUvideodecoder,
    ::std::os::raw::c_int,
    *mut ::std::os::raw::c_ulonglong,
    *mut ::std::os::raw::c_uint,
    *mut CUVIDPROCPARAMS,
) -> CUresult;
type CuvidGetDecodeStatusFn = unsafe extern "C" fn(
    CUvideodecoder,
    ::std::os::raw::c_int,
    *mut CUVIDGETDECODESTATUS,
) -> CUresult;
type CuvidUnmapVideoFrame64Fn =
    unsafe extern "C" fn(CUvideodecoder, ::std::os::raw::c_ulonglong) -> CUresult;
type CuvidCtxLockCreateFn = unsafe extern "C" fn(*mut CUvideoctxlock, CUcontext) -> CUresult;

static CUVID: OnceLock<CuvidLibrary> = OnceLock::new();

type StoredFn<T> = Box<T>;

pub struct CuvidLibrary {
    _lib: Arc<Library>,
    create_video_parser_fn: StoredFn<CuvidCreateVideoParserFn>,
    parse_video_data_fn: StoredFn<CuvidParseVideoDataFn>,
    destroy_video_parser_fn: StoredFn<CuvidDestroyVideoParserFn>,
    destroy_decoder_fn: StoredFn<CuvidDestroyDecoderFn>,
    ctx_lock_destroy_fn: StoredFn<CuvidCtxLockDestroyFn>,
    get_decoder_caps_fn: StoredFn<CuvidGetDecoderCapsFn>,
    create_decoder_fn: StoredFn<CuvidCreateDecoderFn>,
    reconfigure_decoder_fn: StoredFn<CuvidReconfigureDecoderFn>,
    decode_picture_fn: StoredFn<CuvidDecodePictureFn>,
    map_video_frame64_fn: StoredFn<CuvidMapVideoFrame64Fn>,
    get_decode_status_fn: StoredFn<CuvidGetDecodeStatusFn>,
    unmap_video_frame64_fn: StoredFn<CuvidUnmapVideoFrame64Fn>,
    ctx_lock_create_fn: StoredFn<CuvidCtxLockCreateFn>,
}

impl CuvidLibrary {
    pub fn instance() -> &'static CuvidLibrary {
        CUVID.get_or_init(|| Self::new().expect("Failed to initialize CUVID library"))
    }

    pub fn new() -> Result<Self, Box<dyn std::error::Error>> {
        let library_paths = [
            "libnvcuvid.so.1",
            "libnvcuvid.so",
            "/usr/lib/x86_64-linux-gnu/libnvcuvid.so.1",
            "/usr/local/cuda/lib64/libnvcuvid.so.1",
        ];

        let lib = library_paths
            .iter()
            .find_map(|path| unsafe { Library::new(*path).ok() })
            .ok_or("Failed to load CUVID library")?;

        let lib = Arc::new(lib);

        // Load all symbols once and store them as function pointers
        unsafe {
            Ok(Self {
                create_video_parser_fn: Box::new(
                    **lib
                        .get::<Symbol<CuvidCreateVideoParserFn>>(b"cuvidCreateVideoParser")?
                        .into_raw(),
                ),
                parse_video_data_fn: Box::new(
                    **lib
                        .get::<Symbol<CuvidParseVideoDataFn>>(b"cuvidParseVideoData")?
                        .into_raw(),
                ),
                destroy_video_parser_fn: Box::new(
                    **lib
                        .get::<Symbol<CuvidDestroyVideoParserFn>>(b"cuvidDestroyVideoParser")?
                        .into_raw(),
                ),
                destroy_decoder_fn: Box::new(
                    **lib
                        .get::<Symbol<CuvidDestroyDecoderFn>>(b"cuvidDestroyDecoder")?
                        .into_raw(),
                ),
                ctx_lock_destroy_fn: Box::new(
                    **lib
                        .get::<Symbol<CuvidCtxLockDestroyFn>>(b"cuvidCtxLockDestroy")?
                        .into_raw(),
                ),
                get_decoder_caps_fn: Box::new(
                    **lib
                        .get::<Symbol<CuvidGetDecoderCapsFn>>(b"cuvidGetDecoderCaps")?
                        .into_raw(),
                ),
                create_decoder_fn: Box::new(
                    **lib
                        .get::<Symbol<CuvidCreateDecoderFn>>(b"cuvidCreateDecoder")?
                        .into_raw(),
                ),
                reconfigure_decoder_fn: Box::new(
                    **lib
                        .get::<Symbol<CuvidReconfigureDecoderFn>>(b"cuvidReconfigureDecoder")?
                        .into_raw(),
                ),
                decode_picture_fn: Box::new(
                    **lib
                        .get::<Symbol<CuvidDecodePictureFn>>(b"cuvidDecodePicture")?
                        .into_raw(),
                ),
                map_video_frame64_fn: Box::new(
                    **lib
                        .get::<Symbol<CuvidMapVideoFrame64Fn>>(b"cuvidMapVideoFrame64")?
                        .into_raw(),
                ),
                get_decode_status_fn: Box::new(
                    **lib
                        .get::<Symbol<CuvidGetDecodeStatusFn>>(b"cuvidGetDecodeStatus")?
                        .into_raw(),
                ),
                unmap_video_frame64_fn: Box::new(
                    **lib
                        .get::<Symbol<CuvidUnmapVideoFrame64Fn>>(b"cuvidUnmapVideoFrame64")?
                        .into_raw(),
                ),
                ctx_lock_create_fn: Box::new(
                    **lib
                        .get::<Symbol<CuvidCtxLockCreateFn>>(b"cuvidCtxLockCreate")?
                        .into_raw(),
                ),
                _lib: lib,
            })
        }
    }

    /// # Safety
    /// Caller must ensure:
    /// - `pObj` and `pParams` are valid pointers
    /// - The CUDA context is initialized and current
    #[inline(always)]
    pub unsafe fn create_video_parser(
        &self,
        pObj: *mut CUvideoparser,
        pParams: *mut CUVIDPARSERPARAMS,
    ) -> CUresult {
        (self.create_video_parser_fn)(pObj, pParams)
    }

    /// # Safety
    /// Caller must ensure:
    /// - `obj` is a valid video parser handle
    /// - `pPacket` points to valid packet data
    #[inline(always)]
    pub unsafe fn parse_video_data(
        &self,
        obj: CUvideoparser,
        pPacket: *mut CUVIDSOURCEDATAPACKET,
    ) -> CUresult {
        (self.parse_video_data_fn)(obj, pPacket)
    }

    /// # Safety
    /// Caller must ensure `obj` is a valid video parser handle
    #[inline(always)]
    pub unsafe fn destroy_video_parser(&self, obj: CUvideoparser) -> CUresult {
        (self.destroy_video_parser_fn)(obj)
    }

    /// # Safety
    /// Caller must ensure `decoder` is a valid decoder handle
    #[inline(always)]
    pub unsafe fn destroy_decoder(&self, decoder: CUvideodecoder) -> CUresult {
        (self.destroy_decoder_fn)(decoder)
    }

    /// # Safety
    /// Caller must ensure `lock` is a valid context lock handle
    #[inline(always)]
    pub unsafe fn ctx_lock_destroy(&self, lock: CUvideoctxlock) -> CUresult {
        (self.ctx_lock_destroy_fn)(lock)
    }

    /// # Safety
    /// Caller must ensure `pdc` points to valid decoder caps structure
    #[inline(always)]
    pub unsafe fn get_decoder_caps(&self, pdc: *mut CUVIDDECODECAPS) -> CUresult {
        (self.get_decoder_caps_fn)(pdc)
    }

    /// # Safety
    /// Caller must ensure:
    /// - `phDecoder` and `pdci` are valid pointers
    /// - The CUDA context is initialized and current
    #[inline(always)]
    pub unsafe fn create_decoder(
        &self,
        phDecoder: *mut CUvideodecoder,
        pdci: *mut CUVIDDECODECREATEINFO,
    ) -> CUresult {
        (self.create_decoder_fn)(phDecoder, pdci)
    }

    /// # Safety
    /// Caller must ensure:
    /// - `hDecoder` is a valid decoder handle
    /// - `pDecReconfigParams` points to valid reconfiguration parameters
    #[inline(always)]
    pub unsafe fn reconfigure_decoder(
        &self,
        hDecoder: CUvideodecoder,
        pDecReconfigParams: *mut CUVIDRECONFIGUREDECODERINFO,
    ) -> CUresult {
        (self.reconfigure_decoder_fn)(hDecoder, pDecReconfigParams)
    }

    /// # Safety
    /// Caller must ensure:
    /// - `hDecoder` is a valid decoder handle
    /// - `pPicParams` points to valid picture parameters
    #[inline(always)]
    pub unsafe fn decode_picture(
        &self,
        hDecoder: CUvideodecoder,
        pPicParams: *mut CUVIDPICPARAMS,
    ) -> CUresult {
        (self.decode_picture_fn)(hDecoder, pPicParams)
    }

    /// # Safety
    /// Caller must ensure:
    /// - `hDecoder` is a valid decoder handle
    /// - `pDevPtr`, `pPitch`, and `pVPP` are valid pointers
    /// - `nPicIdx` is a valid picture index
    #[inline(always)]
    pub unsafe fn map_video_frame64(
        &self,
        hDecoder: CUvideodecoder,
        nPicIdx: ::std::os::raw::c_int,
        pDevPtr: *mut ::std::os::raw::c_ulonglong,
        pPitch: *mut ::std::os::raw::c_uint,
        pVPP: *mut CUVIDPROCPARAMS,
    ) -> CUresult {
        (self.map_video_frame64_fn)(hDecoder, nPicIdx, pDevPtr, pPitch, pVPP)
    }

    /// # Safety
    /// Caller must ensure:
    /// - `hDecoder` is a valid decoder handle
    /// - `pDecodeStatus` is a valid pointer
    /// - `nPicIdx` is a valid picture index
    #[inline(always)]
    pub unsafe fn get_decode_status(
        &self,
        hDecoder: CUvideodecoder,
        nPicIdx: ::std::os::raw::c_int,
        pDecodeStatus: *mut CUVIDGETDECODESTATUS,
    ) -> CUresult {
        (self.get_decode_status_fn)(hDecoder, nPicIdx, pDecodeStatus)
    }

    /// # Safety
    /// Caller must ensure:
    /// - `hDecoder` is a valid decoder handle
    /// - `DevPtr` is a valid device pointer obtained from map_video_frame64
    #[inline(always)]
    pub unsafe fn unmap_video_frame64(
        &self,
        hDecoder: CUvideodecoder,
        DevPtr: ::std::os::raw::c_ulonglong,
    ) -> CUresult {
        (self.unmap_video_frame64_fn)(hDecoder, DevPtr)
    }

    /// # Safety
    /// Caller must ensure:
    /// - `pLock` is a valid pointer
    /// - `ctx` is a valid CUDA context
    #[inline(always)]
    pub unsafe fn ctx_lock_create(&self, pLock: *mut CUvideoctxlock, ctx: CUcontext) -> CUresult {
        (self.ctx_lock_create_fn)(pLock, ctx)
    }
}
