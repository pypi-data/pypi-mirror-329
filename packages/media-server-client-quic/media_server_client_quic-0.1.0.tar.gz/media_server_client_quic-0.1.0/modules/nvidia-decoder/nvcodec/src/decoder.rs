use crate::input_video_frame::InputVideoFrame;
use crate::{
    codec::CuVideoCodecType,
    error::{NVCodecError, NVCodecResult},
    ffi,
    surface::VideoSurfaceFormat,
};
use cuda_rs::{context::CuContext, memory::PitchedDeviceMemory, stream::CuStream};
use dashmap::DashMap;
use futures::{stream::Stream, task::AtomicWaker};
use npp::{
    color::{ColorRange, ColorSpace, PixelFormat},
    image::DeviceImage,
};
use std::{
    pin::Pin,
    sync::Arc,
    task::{Context, Poll},
};

static CUVID: std::sync::OnceLock<ffi::CuvidLibrary> = std::sync::OnceLock::new();

#[allow(dead_code)] // Library API
struct Inner {
    ctx: CuContext,
    stream: CuStream,
    display_area: DisplayArea,
    target_size: Size,
    keyframe_only: bool,

    waker: Arc<AtomicWaker>,

    ctx_lock: ffi::CUvideoctxlock,
    parser: ffi::CUvideoparser,

    decoder: ffi::CUvideodecoder,
    video_fmt: Option<ffi::CUVIDEOFORMAT>,
    surface_fmt: VideoSurfaceFormat,
    bpp: u32,
    num_chroma_planes: u32,
    width: u32,
    luma_height: u32,
    chroma_height: u32,
    max_width: u32,
    max_height: u32,

    packet_map: DashMap<i64, PacketData>,

    sender: Option<flume::Sender<NVCodecResult<DecodedFrame>>>,

    color_space: Option<ColorSpace>,
    color_range: Option<ColorRange>,
}

pub struct NVDecoder {
    inner: Box<Inner>,
    eos: bool,
    pub receiver: flume::Receiver<NVCodecResult<DecodedFrame>>,
    pub time_key_value: i64,
}

#[derive(Debug)]
pub struct PacketData {
    pub input_frame: InputVideoFrame,
    pub color_space: Option<ColorSpace>,
    pub color_range: Option<ColorRange>,
}

pub struct DecodedFrame {
    pub buf: PitchedDeviceMemory,
    pub width: usize,
    pub height: usize,
    pub packet_data: PacketData,
    pub surface_format: VideoSurfaceFormat,
}

impl From<DecodedFrame> for DeviceImage {
    fn from(frame: DecodedFrame) -> Self {
        let pixel_format = match frame.surface_format {
            VideoSurfaceFormat::NV12 => PixelFormat::NV12,
            VideoSurfaceFormat::P016 => PixelFormat::P016,
            VideoSurfaceFormat::YUV444 => PixelFormat::YUV444,
            VideoSurfaceFormat::YUV444_16Bit => PixelFormat::YUV444_16Bit,
        };

        let color_space = frame.packet_data.color_space.unwrap_or(ColorSpace::UNSPEC);
        let color_range = frame.packet_data.color_range.unwrap_or(ColorRange::UDEF);

        Self {
            mem: frame.buf,
            width: frame.width,
            height: frame.height,
            pixel_format,
            color_space,
            color_range,
        }
    }
}

impl NVDecoder {
    pub fn new(
        stream: &CuStream,
        codec_type: CuVideoCodecType,
        display_area: Option<DisplayArea>,
        target_size: Option<Size>,
        keyframe_only: bool,
    ) -> NVCodecResult<Self> {
        tracing::trace!("Creating new NVDecoder - codec: {:?}, keyframe_only: {}", codec_type, keyframe_only);
        let ctx = stream.get_context()?;

        let mut parser = std::ptr::null_mut();
        let mut ctx_lock = std::ptr::null_mut();

        let cuvid = CUVID
            .get_or_init(|| ffi::CuvidLibrary::new().expect("Failed to initialize CUVID library"));

        unsafe {
            cuvid.ctx_lock_create(&mut ctx_lock, ctx.get_raw() as _);
        }
        tracing::trace!("Created CUDA context lock");

        let (tx, rx) = flume::unbounded::<NVCodecResult<DecodedFrame>>();

        let waker = Arc::new(AtomicWaker::new());
        let mut inner = Box::new(Inner {
            ctx,
            stream: stream.clone(),
            display_area: display_area.unwrap_or_default(),
            target_size: target_size.unwrap_or_default(),
            keyframe_only,
            waker,
            ctx_lock,
            parser,
            decoder: std::ptr::null_mut(),
            video_fmt: None,
            surface_fmt: VideoSurfaceFormat::NV12,
            bpp: 1,
            num_chroma_planes: 0,
            width: 0,
            luma_height: 0,
            chroma_height: 0,
            max_width: 0,
            max_height: 0,
            packet_map: DashMap::new(),
            sender: Some(tx),
            color_space: None,
            color_range: None,
        });

        let mut params: ffi::CUVIDPARSERPARAMS = unsafe { std::mem::zeroed() };
        params.CodecType = codec_type as _;
        params.ulMaxNumDecodeSurfaces = 20; // Absolute minimum
        params.ulMaxDisplayDelay = 0; // No display delay
        params.ulClockRate = 1000; // Millisecond timestamps
        params.uReserved1[0] = 1; // Low latency mode

        // Skip any buffering or reordering
        params.pUserData = (&mut *inner as *mut Inner) as *mut std::os::raw::c_void;
        params.pfnSequenceCallback = Some(handle_video_sequence_proc);
        params.pfnDecodePicture = Some(handle_picture_decode_proc);
        params.pfnDisplayPicture = Some(handle_picture_display_proc);

        unsafe {
            cuvid.create_video_parser(&mut parser, &mut params);
        }
        tracing::trace!("Created video parser");
        inner.parser = parser;

        Ok(Self {
            inner,
            eos: false,
            receiver: rx,
            time_key_value: 1,
        })
    }

    pub fn time_key(&mut self) -> i64 {
        self.time_key_value
    }

    pub fn time_key_increment(&mut self) {
        self.time_key_value += 1;
    }

    pub fn decode(&mut self, packet: Option<InputVideoFrame>) -> NVCodecResult<()> {
        let mut params: ffi::CUVIDSOURCEDATAPACKET = unsafe { std::mem::zeroed() };

        // Set timestamp and end-of-picture flags to ensure immediate processing
        params.flags = (ffi::CUvideopacketflags_CUVID_PKT_TIMESTAMP as u64)
            | (ffi::CUvideopacketflags_CUVID_PKT_ENDOFPICTURE as u64);

        match packet {
            Some(input_frame) => {
                tracing::trace!("Decoding frame for stream {}", input_frame.stream_id);
                params.payload_size = input_frame.data.data.len() as _;
                params.payload = input_frame.data.data.as_ptr() as _;

                // Use current time for timestamp to track actual latency
                let timestamp = std::time::SystemTime::now()
                    .duration_since(std::time::UNIX_EPOCH)
                    .unwrap()
                    .as_millis() as i64;

                params.timestamp = timestamp;

                self.inner.packet_map.insert(
                    timestamp,
                    PacketData {
                        input_frame,
                        color_space: Some(ColorSpace::BT601),
                        color_range: Some(ColorRange::JPEG),
                    },
                );
                tracing::trace!("Added packet to map with timestamp {}", timestamp);
            }
            None => {
                tracing::trace!("Received end of stream");
                params.flags |= (ffi::CUvideopacketflags_CUVID_PKT_ENDOFSTREAM as u64)
                    | (ffi::CUvideopacketflags_CUVID_PKT_NOTIFY_EOS as u64);
                self.eos = true;
            }
        };

        let cuvid = CUVID.get().unwrap();
        unsafe {
            cuvid.parse_video_data(self.inner.parser, &mut params);
        }
        tracing::trace!("Video data parsed successfully");

        Ok(())
    }
}

impl Stream for NVDecoder {
    type Item = NVCodecResult<DecodedFrame>;

    fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
        self.inner.waker.register(cx.waker());

        match self.receiver.try_recv() {
            Ok(v) => Poll::Ready(Some(v)),
            Err(flume::TryRecvError::Empty) => {
                if self.eos {
                    Poll::Ready(None)
                } else {
                    Poll::Pending
                }
            }
            Err(flume::TryRecvError::Disconnected) => Poll::Ready(None),
        }
    }
}

impl Drop for NVDecoder {
    fn drop(&mut self) {
        let cuvid = CUVID.get().unwrap();

        unsafe {
            if !self.inner.parser.is_null() {
                cuvid.destroy_video_parser(self.inner.parser);
            }

            if !self.inner.decoder.is_null() {
                cuvid.destroy_decoder(self.inner.decoder);
            }

            cuvid.ctx_lock_destroy(self.inner.ctx_lock);
        }
    }
}

impl Inner {
    fn sequence_callback(&mut self, video_format: *mut ffi::CUVIDEOFORMAT) -> i32 {
        tracing::trace!("Sequence callback triggered");
        match self.sequence_callback_impl(video_format) {
            Ok(num_decode_surfaces) => {
                tracing::trace!("Sequence callback successful, num_decode_surfaces: {}", num_decode_surfaces);
                num_decode_surfaces
            }
            Err(err) => {
                tracing::error!("Error in sequence callback: {:?}", err);

                if let Some(sender) = self.sender.as_ref() {
                    if sender.send(Err(err)).is_ok() {
                        self.waker.wake();
                    }
                }

                0
            }
        }
    }

    #[inline]
    fn sequence_callback_impl(
        &mut self,
        video_format: *mut ffi::CUVIDEOFORMAT,
    ) -> NVCodecResult<i32> {
        let fmt = unsafe { &*video_format };

        let cuvid = CUVID.get().unwrap();

        tracing::debug!(
            "Video Input Information
            Codec: {}
            Frame Rate : {}/{}
            Sequence: {}
            Coded Size {}x{}
            Display Area: {}x{}x{}x{}
            Chroma :{}
            Bit Depth: {}
            Minimum Surfaces: {}",
            fmt.codec,
            fmt.frame_rate.numerator,
            fmt.frame_rate.denominator,
            fmt.progressive_sequence,
            fmt.coded_width,
            fmt.coded_height,
            fmt.display_area.top,
            fmt.display_area.left,
            fmt.display_area.bottom,
            fmt.display_area.right,
            fmt.chroma_format,
            fmt.bit_depth_chroma_minus8,
            fmt.min_num_decode_surfaces,
        );

        let mut decode_caps: ffi::CUVIDDECODECAPS = unsafe { std::mem::zeroed() };
        decode_caps.eCodecType = fmt.codec;
        decode_caps.eChromaFormat = fmt.chroma_format;
        decode_caps.nBitDepthMinus8 = fmt.bit_depth_chroma_minus8 as _;

        unsafe {
            cuvid.get_decoder_caps(&mut decode_caps);
        }

        if decode_caps.bIsSupported == 0 {
            let msg = format!("Codec {} not supported for this GPU", fmt.codec);
            return Err(NVCodecError::NotSupported(msg));
        }

        if decode_caps.nMaxWidth < fmt.coded_width || decode_caps.nMaxHeight < fmt.coded_height {
            let msg = format!(
                "Resolution (wxh) {}x{} if greater than max resolution {}x{} for this GPU",
                fmt.coded_width, fmt.coded_height, decode_caps.nMaxWidth, decode_caps.nMaxHeight
            );
            return Err(NVCodecError::NotSupported(msg));
        }

        if decode_caps.nMaxMBCount < (fmt.coded_width >> 4) * (fmt.coded_height >> 4) {
            let msg = format!(
                "bitrate {} if greater than max bitrate {} for the GPU",
                (fmt.coded_width >> 4) * (fmt.coded_height >> 4),
                decode_caps.nMaxMBCount
            );
            return Err(NVCodecError::NotSupported(msg));
        }

        if self.video_fmt.is_some() {
            match self.reconfigure_decoder(fmt) {
                Ok(num_decode_surfaces) => {
                    self.video_fmt = Some(*fmt);
                    return Ok(num_decode_surfaces);
                }
                Err(err) => match err {
                    NVCodecError::ReconfigureFailed => {
                        let cuvid = CUVID.get().unwrap();
                        unsafe {
                            cuvid.destroy_decoder(self.decoder);
                            self.decoder = std::ptr::null_mut();
                        }
                    }
                    _ => {
                        tracing::error!("Error in reconfigure decoder: {:?}", err);
                        return Err(err);
                    }
                },
            }
        }

        let mut output_format = match fmt.chroma_format {
            ffi::cudaVideoChromaFormat_enum_cudaVideoChromaFormat_420 => {
                if fmt.bit_depth_luma_minus8 > 0 {
                    VideoSurfaceFormat::P016
                } else {
                    VideoSurfaceFormat::NV12
                }
            }
            ffi::cudaVideoChromaFormat_enum_cudaVideoChromaFormat_444 => {
                if fmt.bit_depth_luma_minus8 > 0 {
                    VideoSurfaceFormat::YUV444_16Bit
                } else {
                    VideoSurfaceFormat::YUV444
                }
            }
            _ => VideoSurfaceFormat::NV12,
        };

        // Check if output format supported. If not, check falback options
        if decode_caps.nOutputFormatMask & (1 << (output_format as u16)) == 0 {
            if decode_caps.nOutputFormatMask & (1 << (VideoSurfaceFormat::NV12 as u16)) != 0 {
                output_format = VideoSurfaceFormat::NV12;
            } else if decode_caps.nOutputFormatMask & (1 << (VideoSurfaceFormat::P016 as u16)) != 0
            {
                output_format = VideoSurfaceFormat::P016;
            } else if decode_caps.nOutputFormatMask & (1 << (VideoSurfaceFormat::YUV444 as u16))
                != 0
            {
                output_format = VideoSurfaceFormat::YUV444;
            } else if decode_caps.nOutputFormatMask
                & (1 << (VideoSurfaceFormat::YUV444_16Bit as u16))
                != 0
            {
                output_format = VideoSurfaceFormat::YUV444_16Bit;
            } else {
                let msg = format!(
                    "No supported output format found. Supported formats: {}",
                    decode_caps.nOutputFormatMask
                );
                return Err(NVCodecError::NotSupported(msg));
            }
        }

        self.surface_fmt = output_format;
        self.video_fmt = Some(*fmt);

        // Shall be enough according to NVIDIA Nvdec mem optimization blog article
        // (https://developer.nvidia.com/blog/optimizing-video-memory-usage-with-the-nvdecode-api-and-nvidia-video-codec-sdk/)
        let num_decode_surfaces = fmt.min_num_decode_surfaces as i32 + 4;

        let mut video_decode_create_info: ffi::CUVIDDECODECREATEINFO =
            unsafe { std::mem::zeroed() };
        video_decode_create_info.ulIntraDecodeOnly = if self.keyframe_only { 1 } else { 0 };
        video_decode_create_info.CodecType = fmt.codec;
        video_decode_create_info.ChromaFormat = fmt.chroma_format;
        video_decode_create_info.OutputFormat = output_format as _;
        video_decode_create_info.bitDepthMinus8 = fmt.bit_depth_chroma_minus8 as _;
        video_decode_create_info.DeinterlaceMode = if fmt.progressive_sequence != 0 {
            ffi::cudaVideoDeinterlaceMode_enum_cudaVideoDeinterlaceMode_Weave
        } else {
            ffi::cudaVideoDeinterlaceMode_enum_cudaVideoDeinterlaceMode_Adaptive
        };
        video_decode_create_info.ulNumOutputSurfaces = 2; // TODO: find out optimal value
        video_decode_create_info.ulCreationFlags =
            ffi::cudaVideoCreateFlags_enum_cudaVideoCreate_PreferCUVID as _;
        video_decode_create_info.ulNumDecodeSurfaces = num_decode_surfaces as _;
        video_decode_create_info.vidLock = self.ctx_lock as _;
        video_decode_create_info.ulWidth = fmt.coded_width as _;
        video_decode_create_info.ulHeight = fmt.coded_height as _;

        if fmt.coded_width > self.max_width as _ {
            self.max_width = fmt.coded_width as _;
        }

        if fmt.coded_height > self.max_height as _ {
            self.max_height = fmt.coded_height as _;
        }

        video_decode_create_info.ulMaxWidth = self.max_width as _;
        video_decode_create_info.ulMaxHeight = self.max_height as _;

        if (self.display_area.right == 0 || self.display_area.bottom == 0)
            && (self.target_size.width == 0 || self.target_size.height == 0)
        {
            self.width = (fmt.display_area.right - fmt.display_area.left) as _;
            self.luma_height = (fmt.display_area.bottom - fmt.display_area.top) as _;
        } else {
            if self.target_size.width != 0 && self.target_size.height != 0 {
                video_decode_create_info.display_area.left = fmt.display_area.left as _;
                video_decode_create_info.display_area.top = fmt.display_area.top as _;
                video_decode_create_info.display_area.right = fmt.display_area.right as _;
                video_decode_create_info.display_area.bottom = fmt.display_area.bottom as _;
                self.width = self.target_size.width as _;
                self.luma_height = self.target_size.height as _;
            }

            if self.display_area.right != 0 && self.display_area.bottom != 0 {
                video_decode_create_info.display_area.left = self.display_area.left as _;
                video_decode_create_info.display_area.top = self.display_area.top as _;
                video_decode_create_info.display_area.right = self.display_area.right as _;
                video_decode_create_info.display_area.bottom = self.display_area.bottom as _;
                self.width = (self.display_area.right - self.display_area.left) as _;
                self.luma_height = (self.display_area.bottom - self.display_area.top) as _;
            }
        }

        video_decode_create_info.ulTargetWidth = self.width as _;
        video_decode_create_info.ulTargetHeight = self.luma_height as _;

        self.bpp = if fmt.bit_depth_luma_minus8 > 0 { 2 } else { 1 };
        self.chroma_height =
            (self.luma_height as f32 * get_chroma_height_factor(fmt.chroma_format)) as u32;
        self.num_chroma_planes = get_chroma_plane_count(fmt.chroma_format);
        self.display_area.left = video_decode_create_info.display_area.left as _;
        self.display_area.top = video_decode_create_info.display_area.top as _;
        self.display_area.right = video_decode_create_info.display_area.right as _;
        self.display_area.bottom = video_decode_create_info.display_area.bottom as _;

        // self.color_space = match fmt.video_signal_description.matrix_coefficients {
        //     1 => Some(ColorSpace::BT709),
        //     5 | 6 => Some(ColorSpace::BT601),
        //     // Add other mappings as needed
        //     _ => Some(ColorSpace::UNSPEC),
        // };
        //
        // self.color_range = if fmt.video_signal_description.video_full_range_flag() != 0 {
        //     Some(ColorRange::JPEG)
        // } else {
        //     Some(ColorRange::MPEG)
        // };

        unsafe {
            cuvid.create_decoder(&mut self.decoder, &mut video_decode_create_info);
        }

        Ok(num_decode_surfaces)
    }

    fn reconfigure_decoder(&mut self, fmt: &ffi::CUVIDEOFORMAT) -> NVCodecResult<i32> {
        let old_fmt = self.video_fmt.as_ref().unwrap();

        let is_bit_depth_change = old_fmt.bit_depth_chroma_minus8 != fmt.bit_depth_chroma_minus8
            || old_fmt.bit_depth_luma_minus8 != fmt.bit_depth_luma_minus8;
        if is_bit_depth_change {
            tracing::debug!("Reconfigure Not supported for bit depth change. Re-creating decoder.");
            return Err(NVCodecError::ReconfigureFailed);
        }

        let is_chroma_format_change = old_fmt.chroma_format != fmt.chroma_format;
        if is_chroma_format_change {
            tracing::debug!(
                "Reconfigure Not supported for chroma format change. Re-creating decoder."
            );
            return Err(NVCodecError::ReconfigureFailed);
        }

        let num_decode_surfaces = fmt.min_num_decode_surfaces as i32 + 4;

        if fmt.coded_width > self.max_width || fmt.coded_height > self.max_height {
            // For VP9, let driver  handle the change if new width/height > maxwidth/maxheight
            if old_fmt.codec != ffi::cudaVideoCodec_enum_cudaVideoCodec_VP9 {
                tracing::debug!("Reconfigure Not supported for downscaling. Re-creating decoder.");
                return Err(NVCodecError::ReconfigureFailed);
            }
            return Ok(num_decode_surfaces);
        }

        let is_decode_res_change =
            old_fmt.coded_width != fmt.coded_width || old_fmt.coded_height != fmt.coded_height;
        let is_display_area_change = old_fmt.display_area.top != fmt.display_area.top
            || old_fmt.display_area.left != fmt.display_area.left
            || old_fmt.display_area.bottom != fmt.display_area.bottom
            || old_fmt.display_area.right != fmt.display_area.right;

        if !is_decode_res_change {
            // if the coded_width/coded_height hasn't changed but display resolution has
            // changed, then need to update width/height for correct output without
            // cropping. Example : 1920x1080 vs 1920x1088
            if is_display_area_change {
                self.width = (fmt.display_area.right - fmt.display_area.left) as _;
                self.luma_height = (fmt.display_area.bottom - fmt.display_area.top) as _;
                self.chroma_height =
                    (self.luma_height as f32 * get_chroma_height_factor(fmt.chroma_format)) as u32;
            }

            return Ok(num_decode_surfaces);
        }

        let mut params: ffi::CUVIDRECONFIGUREDECODERINFO = unsafe { std::mem::zeroed() };
        params.ulWidth = fmt.coded_width as _;
        params.ulHeight = fmt.coded_height as _;
        params.ulTargetWidth = self.width as _;
        params.ulTargetHeight = self.luma_height as _;

        if is_decode_res_change {
            self.width = (fmt.display_area.right - fmt.display_area.left) as _;
            self.luma_height = (fmt.display_area.bottom - fmt.display_area.top) as _;
            self.chroma_height =
                (self.luma_height as f32 * get_chroma_height_factor(fmt.chroma_format)) as u32;
        }

        params.ulNumDecodeSurfaces = num_decode_surfaces as _;

        let cuvid = CUVID.get().unwrap();
        unsafe {
            cuvid.reconfigure_decoder(self.decoder, &mut params);
        }

        Ok(num_decode_surfaces)
    }

    fn picture_decode_callback(&mut self, pic_params: *mut ffi::CUVIDPICPARAMS) -> i32 {
        tracing::trace!("Picture decode callback triggered");
        match self.picture_decode_callback_impl(pic_params) {
            Ok(res) => {
                tracing::trace!("Picture decode successful");
                res
            }
            Err(err) => {
                tracing::error!("Error in picture decode callback: {:?}", err);

                if let Some(sender) = self.sender.as_ref() {
                    if sender.send(Err(err)).is_ok() {
                        self.waker.wake();
                    }
                }

                0
            }
        }
    }

    fn picture_decode_callback_impl(
        &mut self,
        pic_params: *mut ffi::CUVIDPICPARAMS,
    ) -> NVCodecResult<i32> {
        if self.decoder.is_null() {
            return Err(NVCodecError::DecoderNotInitialized);
        }

        let cuvid = CUVID.get().unwrap();

        unsafe {
            cuvid.decode_picture(self.decoder, pic_params);
        }

        Ok(1)
    }

    fn picture_display_callback(&mut self, display_info: *mut ffi::CUVIDPARSERDISPINFO) -> i32 {
        tracing::trace!("Picture display callback triggered");
        match self.picture_display_callback_impl(display_info) {
            Ok(res) => {
                tracing::trace!("Picture display successful");
                res
            }
            Err(err) => {
                tracing::error!("Error in picture display callback: {:?}", err);

                if let Some(sender) = self.sender.as_ref() {
                    if sender.send(Err(err)).is_ok() {
                        self.waker.wake();
                    }
                }

                0
            }
        }
    }

    fn picture_display_callback_impl(
        &mut self,
        display_info: *mut ffi::CUVIDPARSERDISPINFO,
    ) -> NVCodecResult<i32> {
        if display_info.is_null() {
            tracing::trace!("Display info is null, ending display callback");
            if let Some(sender) = self.sender.take() {
                std::mem::drop(sender);
                self.waker.wake();
            }
            return Ok(1);
        }

        let display_info = unsafe { &*display_info };
        tracing::trace!("Processing frame with picture index: {}", display_info.picture_index);

        // Early sender check to avoid unnecessary work
        if self.sender.as_ref().map_or(true, |s| s.is_disconnected()) {
            tracing::trace!("Sender disconnected, skipping frame processing");
            return Ok(1);
        }

        let mut params: ffi::CUVIDPROCPARAMS = unsafe { std::mem::zeroed() };
        params.progressive_frame = display_info.progressive_frame;
        params.second_field = 0;
        params.top_field_first = display_info.top_field_first;
        params.unpaired_field = 0;
        unsafe {
            params.output_stream = self.stream.get_raw() as _;
        }

        let mut src_ptr: ffi::CUdeviceptr = 0;
        let mut src_pitch: u32 = 0;

        unsafe {
            let cuvid = CUVID.get().unwrap();
            cuvid.map_video_frame64(
                self.decoder,
                display_info.picture_index,
                &mut src_ptr,
                &mut src_pitch,
                &mut params,
            );
            tracing::trace!("Mapped video frame with pitch: {}", src_pitch);

            let mut decode_status: ffi::CUVIDGETDECODESTATUS = std::mem::zeroed();
            cuvid.get_decode_status(self.decoder, display_info.picture_index, &mut decode_status);
            if decode_status.decodeStatus == ffi::cuvidDecodeStatus_enum_cuvidDecodeStatus_Error {
                tracing::error!("Decode error detected for picture index: {}", display_info.picture_index);
                cuvid.unmap_video_frame64(self.decoder, src_ptr);
                return Err(NVCodecError::DecodeError);
            }
        }

        let buffer_height = self.luma_height + self.chroma_height * self.num_chroma_planes;
        tracing::trace!("Creating surface buffer with dimensions: {}x{}", self.width * self.bpp, buffer_height);

        let surface_buffer = PitchedDeviceMemory::new(
            (self.width * self.bpp) as _,
            buffer_height as _,
            &self.stream,
        )?;

        surface_buffer.copy_from_raw(
            src_ptr,
            src_pitch as _,
            self.width as _,
            buffer_height as _,
            false,
            Some(&self.stream),
        )?;
        tracing::trace!("Copied frame data to surface buffer");

        if let Some(sender) = self.sender.as_ref() {
            if let Some((_, packet_data)) = self.packet_map.remove(&display_info.timestamp) {
                tracing::trace!("Found matching packet data for timestamp: {}", display_info.timestamp);

                let frame = DecodedFrame {
                    buf: surface_buffer,
                    width: self.width as _,
                    height: self.luma_height as _,
                    packet_data,
                    surface_format: self.surface_fmt,
                };

                if sender.send(Ok(frame)).is_ok() {
                    tracing::trace!("Successfully sent decoded frame");
                    self.waker.wake();
                }
            } else {
                tracing::trace!("No matching packet found for timestamp: {}", display_info.timestamp);
            }
        }

        unsafe {
            CUVID.get().unwrap().unmap_video_frame64(self.decoder, src_ptr);
        }
        tracing::trace!("Unmapped video frame");

        Ok(1)
    }
}

fn get_chroma_height_factor(chroma_format: ffi::cudaVideoChromaFormat) -> f32 {
    match chroma_format {
        ffi::cudaVideoChromaFormat_enum_cudaVideoChromaFormat_Monochrome => 0.,
        ffi::cudaVideoChromaFormat_enum_cudaVideoChromaFormat_420 => 0.5,
        ffi::cudaVideoChromaFormat_enum_cudaVideoChromaFormat_422 => 1.,
        ffi::cudaVideoChromaFormat_enum_cudaVideoChromaFormat_444 => 1.,
        _ => 0.5,
    }
}

fn get_chroma_plane_count(chroma_format: ffi::cudaVideoChromaFormat) -> u32 {
    match chroma_format {
        ffi::cudaVideoChromaFormat_enum_cudaVideoChromaFormat_420 => 1,
        ffi::cudaVideoChromaFormat_enum_cudaVideoChromaFormat_444 => 2,
        _ => 0,
    }
}

/// # Safety
/// This function is called by CUDA video parser and expects:
/// - `user_data` points to a valid Inner instance
/// - `video_format` points to a valid CUVIDEOFORMAT structure
pub unsafe extern "C" fn handle_video_sequence_proc(
    user_data: *mut std::os::raw::c_void,
    video_format: *mut ffi::CUVIDEOFORMAT,
) -> i32 {
    let decoder = user_data as *mut Inner;
    let decoder = &mut *decoder;

    decoder.sequence_callback(video_format)
}

/// # Safety
/// This function is called by CUDA video parser and expects:
/// - `user_data` points to a valid Inner instance
/// - `pic_params` points to a valid CUVIDPICPARAMS structure
pub unsafe extern "C" fn handle_picture_decode_proc(
    user_data: *mut std::os::raw::c_void,
    pic_params: *mut ffi::CUVIDPICPARAMS,
) -> i32 {
    let decoder = user_data as *mut Inner;
    let decoder = &mut *decoder;
    decoder.picture_decode_callback(pic_params)
}

/// # Safety
/// This function is called by CUDA video parser and expects:
/// - `user_data` points to a valid Inner instance
/// - `display_info` points to a valid CUVIDPARSERDISPINFO structure or is null
pub unsafe extern "C" fn handle_picture_display_proc(
    user_data: *mut std::os::raw::c_void,
    display_info: *mut ffi::CUVIDPARSERDISPINFO,
) -> i32 {
    let decoder = user_data as *mut Inner;
    let decoder = &mut *decoder;

    decoder.picture_display_callback(display_info)
}

#[derive(Clone, Copy, Debug, Default)]
pub struct DisplayArea {
    pub top: i32,
    pub left: i32,
    pub bottom: i32,
    pub right: i32,
}

#[derive(Clone, Copy, Debug, Default)]
pub struct Size {
    pub width: i32,
    pub height: i32,
}
