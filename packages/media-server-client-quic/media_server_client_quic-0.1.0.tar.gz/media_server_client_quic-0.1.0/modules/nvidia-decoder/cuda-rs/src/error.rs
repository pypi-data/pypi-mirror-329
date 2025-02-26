use crate::ffi;
use num_traits::FromPrimitive;
use thiserror::Error;

enum_from_primitive! {
    #[derive(Error, Debug, PartialEq)]
    pub enum CuError {
        #[error(" This indicates that one or more of the parameters passed to the API call\n is not within an acceptable range of values.")]
        InvalidValue = 1,
        #[error("The API call failed because it was unable to allocate enough memory to\n perform the requested operation.")]
        OutOfMemory = 2,
        #[error("This indicates that the CUDA driver has not been initialized with\n ::cuInit() or that initialization has failed.")]
        NotInitialized = 3,
        #[error("This indicates that the CUDA driver is in the process of shutting down.")]
        Deinitialized = 4,
        #[error("This indicates profiler is not initialized for this run. This can\n happen when the application is running with external profiling tools\n like visual profiler.")]
        ProfilerDisabled = 5,
        #[error("\\deprecated\n This error return is deprecated as of CUDA 5.0. It is no longer an error\n to attempt to enable/disable the profiling via ::cuProfilerStart or\n ::cuProfilerStop without initialization.")]
        ProfilerNotInitialized = 6,
        #[error("\\deprecated\n This error return is deprecated as of CUDA 5.0. It is no longer an error\n to call cuProfilerStart() when profiling is already enabled.")]
        ProfilerAlreadyStarted = 7,
        #[error("\\deprecated\n This error return is deprecated as of CUDA 5.0. It is no longer an error\n to call cuProfilerStop() when profiling is already disabled.")]
        ProfilerAlreadyStopped = 8,
        #[error("This indicates that the CUDA driver that the application has loaded is a\n stub library. Applications that run with the stub rather than a real\n driver loaded will result in CUDA API returning this error.")]
        StubLibrary = 34,
        #[error("This indicates that requested CUDA device is unavailable at the current\n time. Devices are often unavailable due to use of\n ::CU_COMPUTEMODE_EXCLUSIVE_PROCESS or ::CU_COMPUTEMODE_PROHIBITED.")]
        DeviceUnavailable = 46,
        #[error("This indicates that no CUDA-capable devices were detected by the installed\n CUDA driver.")]
        NoDevice = 100,
        #[error("This indicates that the device ordinal supplied by the user does not\n correspond to a valid CUDA device or that the action requested is\n invalid for the specified device.")]
        InvalidDevice = 101,
        #[error("This error indicates that the Grid license is not applied.")]
        DeviceNotLicensed = 102,
        #[error("This indicates that the device kernel image is invalid. This can also\n indicate an invalid CUDA module.")]
        InvalidImage = 200,
        #[error("This most frequently indicates that there is no context bound to the\n current thread. This can also be returned if the context passed to an\n API call is not a valid handle (such as a context that has had\n ::cuCtxDestroy() invoked on it). This can also be returned if a user\n mixes different API versions (i.e. 3010 context with 3020 API calls).\n See ::cuCtxGetApiVersion() for more details.")]
        InvalidContext = 201,
        #[error("This indicated that the context being supplied as a parameter to the\n API call was already the active context.\n \\deprecated\n This error return is deprecated as of CUDA 3.2. It is no longer an\n error to attempt to push the active context via ::cuCtxPushCurrent().")]
        ContextAlreadyCurrent = 202,
        #[error("This indicates that a map or register operation has failed.")]
        MapFailed = 205,
        #[error("This indicates that an unmap or unregister operation has failed.")]
        UnmapFailed = 206,
        #[error("This indicates that the specified array is currently mapped and thus\n cannot be destroyed.")]
        ArrayIsMapped = 207,
        #[error("This indicates that the resource is already mapped.")]
        AlreadyMapped = 208,
        #[error("This indicates that there is no kernel image available that is suitable\n for the device. This can occur when a user specifies code generation\n options for a particular CUDA source file that do not include the\n corresponding device configuration.")]
        NoBinaryForGpu = 209,
        #[error("This indicates that a resource has already been acquired.")]
        AlreadyAcquired = 210,
        #[error("This indicates that a resource is not mapped.")]
        NotMapped = 211,
        #[error("This indicates that a mapped resource is not available for access as an\n array.")]
        NotMappedAsArray = 212,
        #[error("This indicates that a mapped resource is not available for access as a\n pointer.")]
        NotMappedAsPointer = 213,
        #[error("This indicates that an uncorrectable ECC error was detected during\n execution.")]
        EccUncorrectable = 214,
        #[error("This indicates that the ::CUlimit passed to the API call is not\n supported by the active device.")]
        UnsupportedLimit = 215,
        #[error("This indicates that the ::CUcontext passed to the API call can\n only be bound to a single CPU thread at a time but is already\n bound to a CPU thread.")]
        ContextAlreadyInUse = 216,
        #[error("This indicates that peer access is not supported across the given\n devices.")]
        PeerAccessUnsupported = 217,
        #[error("A PTX JIT compilation failed.")]
        InvalidPtx = 218,
        #[error("This indicates an error with OpenGL or DirectX context.")]
        InvalidGraphicsContext = 219,
        #[error("This indicates that an uncorrectable NVLink error was detected during\n the execution.")]
        NvlinkUncorrectable = 220,
        #[error("This indicates that the PTX JIT compiler library was not found.")]
        JitCompilerNotFound = 221,
        #[error("This indicates that the provided PTX was compiled with an unsupported toolchain.")]
        UnsupportedPtxVersion = 222,
        #[error("This indicates that the PTX JIT compilation was disabled.")]
        JitCompilationDisabled = 223,
        #[error("This indicates that the ::CUexecAffinityType passed to the API call is not\n supported by the active device.")]
        UnsupportedExecAffinity = 224,
        #[error("This indicates that the code to be compiled by the PTX JIT contains\n unsupported call to cudaDeviceSynchronize.")]
        UnsupportedDevsideSync = 225,
        #[error("This indicates that the device kernel source is invalid. This includes\n compilation/linker errors encountered in device code or user error.")]
        InvalidSource = 300,
        #[error("This indicates that the file specified was not found.")]
        FileNotFound = 301,
        #[error("This indicates that a link to a shared object failed to resolve.")]
        SharedObjectSymbolNotFound = 302,
        #[error("This indicates that initialization of a shared object failed.")]
        SharedObjectInitFailed = 303,
        #[error("This indicates that an OS call failed.")]
        OperatingSystem = 304,
        #[error("This indicates that a resource handle passed to the API call was not\n valid. Resource handles are opaque types like ::CUstream and ::CUevent.")]
        InvalidHandle = 400,
        #[error("This indicates that a resource required by the API call is not in a\n valid state to perform the requested operation.")]
        IllegalState = 401,
        #[error("This indicates that a named symbol was not found. Examples of symbols\n are global/constant variable names, texture names, and surface names.")]
        NotFound = 500,
        #[error("This indicates that asynchronous operations issued previously have not\n completed yet. This result is not actually an error, but must be\n indicated differently than ::CUDA_SUCCESS (which indicates completion).\n Calls that may return this value include ::cuEventQuery() and\n ::cuStreamQuery().")]
        NotReady = 600,
        #[error("While executing a kernel, the device encountered a load or store\n instruction on an invalid memory address. This leaves the process in an\n inconsistent state and any further CUDA work will return the same error.\n To continue using CUDA, the process must be terminated and relaunched.")]
        IllegalAddress = 700,
        #[error("This indicates that a launch did not occur because it did not have\n appropriate resources. This error usually indicates that the user has\n attempted to pass too many arguments to the device kernel, or the\n kernel launch specifies too many threads for the kernel's register\n count. Passing arguments of the wrong size (i.e. a 64-bit pointer\n when a 32-bit int is expected) is equivalent to passing too many\n arguments and can also result in this error.")]
        LaunchOutOfResources = 701,
        #[error("This indicates that the device kernel took too long to execute. This can\n only occur if timeouts are enabled - see the device attribute\n ::CU_DEVICE_ATTRIBUTE_KERNEL_EXEC_TIMEOUT for more information.\n This leaves the process in an inconsistent state and any further CUDA work\n will return the same error. To continue using CUDA, the process must be terminated\n and relaunched.")]
        LaunchTimeout = 702,
        #[error("This error indicates a kernel launch that uses an incompatible texturing\n mode.")]
        LaunchIncompatibleTexturing = 703,
        #[error("This error indicates that a call to ::cuCtxEnablePeerAccess() is\n trying to re-enable peer access to a context which has already\n had peer access to it enabled.")]
        PeerAccessAlreadyEnabled = 704,
        #[error("This error indicates that ::cuCtxDisablePeerAccess() is trying to\n disable peer access which has not been enabled yet via\n ::cuCtxEnablePeerAccess().")]
        PeerAccessNotEnabled = 705,
        #[error("This error indicates that the primary context for the specified device\n has already been initialized.")]
        PrimaryContextActive = 708,
        #[error("This error indicates that the context current to the calling thread\n has been destroyed using ::cuCtxDestroy, or is a primary context which\n has not yet been initialized.")]
        ContextIsDestroyed = 709,
        #[error("A device-side assert triggered during kernel execution. The context\n cannot be used anymore, and must be destroyed. All existing device\n memory allocations from this context are invalid and must be\n reconstructed if the program is to continue using CUDA.")]
        Assert = 710,
        #[error("This error indicates that the hardware resources required to enable\n peer access have been exhausted for one or more of the devices\n passed to ::cuCtxEnablePeerAccess().")]
        TooManyPeers = 711,
        #[error("This error indicates that the memory range passed to ::cuMemHostRegister()\n has already been registered.")]
        HostMemoryAlreadyRegistered = 712,
        #[error("This error indicates that the pointer passed to ::cuMemHostUnregister()\n does not correspond to any currently registered memory region.")]
        HostMemoryNotRegistered = 713,
        #[error("While executing a kernel, the device encountered a stack error.\n This can be due to stack corruption or exceeding the stack size limit.\n This leaves the process in an inconsistent state and any further CUDA\n work will return the same error. To continue using CUDA, the process\n must be terminated and relaunched.")]
        HardwareStackError = 714,
        #[error("While executing a kernel, the device encountered an instruction\n which can only operate on memory locations in certain address spaces\n (global, shared, or local), but was supplied a memory address not\n belonging to an allowed address space. This leaves the process in an\n inconsistent state and any further CUDA work will return the same\n error. To continue using CUDA, the process must be terminated and\n relaunched.")]
        IllegalInstruction = 715,
        #[error("While executing a kernel, the device encountered an illegal address.\n This leaves the process in an inconsistent state and any further CUDA\n work will return the same error. To continue using CUDA, the process\n must be terminated and relaunched.")]
        MisalignedAddress = 716,
        #[error("While executing a kernel, the device encountered a load or store\n instruction on an invalid memory address. This leaves the process in an\n inconsistent state and any further CUDA work will return the same error.\n To continue using CUDA, the process must be terminated and relaunched.")]
        InvalidAddressSpace = 717,
        #[error("While executing a kernel, the device program counter wrapped its address\n space. This leaves the process in an inconsistent state and any further\n CUDA work will return the same error. To continue using CUDA, the\n process must be terminated and relaunched.")]
        InvalidPc = 718,
        #[error("An exception occurred on the device while executing a kernel. Common\n causes include dereferencing an invalid device pointer and accessing\n out of bounds shared memory. The context cannot be used, so it must\n be destroyed (and a new one should be created). All existing device\n memory allocations from this context are invalid and must be\n reconstructed if the program is to continue using CUDA.")]
        LaunchFailed = 719,
        #[error("This error indicates that the number of blocks launched per grid for a\n kernel that was launched via either ::cuLaunchCooperativeKernel or\n ::cuLaunchCooperativeKernelMultiDevice exceeds the maximum number of\n blocks as allowed by ::cuOccupancyMaxActiveBlocksPerMultiprocessor or\n ::cuOccupancyMaxActiveBlocksPerMultiprocessorWithFlags times the number\n of multiprocessors as specified by the device attribute\n ::CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT.")]
        CooperativeLaunchTooLarge = 720,
        #[error("This error indicates that the attempted operation is not permitted.")]
        NotPermitted = 800,
        #[error("This error indicates that the attempted operation is not supported\n on the current system or device.")]
        NotSupported = 801,
        #[error("This error indicates that the system is not yet ready to start any CUDA\n work.  To continue using CUDA, verify the system configuration is in a\n valid state and all required driver daemons are actively running.\n More information about this error can be found in the system specific\n user guide.")]
        SystemNotReady = 802,
        #[error("This error indicates that there is a mismatch between the versions of\n the display driver and the CUDA driver. Refer to the compatibility\n documentation for supported versions.")]
        SystemDriverMismatch = 803,
        #[error("This error indicates that the system was upgraded to run with forward\n compatibility but the visible hardware detected by CUDA does not support\n this configuration. Refer to the compatibility documentation for the\n supported hardware matrix or ensure that only supported hardware is\n visible during initialization via the CUDA_VISIBLE_DEVICES\n environment variable.")]
        CompatNotSupportedOnDevice = 804,
        #[error("This error indicates that the system was unable to initialize a\n connection to the target device requested by the application. The\n application should destroy and then re-create the CUDA context.")]
        MpsConnectionFailed = 805,
        #[error("This error indicates that a call to ::cuMultiGPUCooperativeGroupGetParams\n has failed because the CUDA runtime library's internal RPC subsystem\n has failed to initialize. This error can only occur if the CUDA\n runtime library was configured with the\n --disable-driver-rpc option.")]
        MpsRpcFailure = 806,
        #[error("This error indicates that the target device of a call to\n ::cuMultiGPUCooperativeGroupGetParams has not yet been initialized.\n The application should call ::cuMultiGPUCooperativeGroupGetParams again\n after the target device has been initialized.")]
        MpsServerNotReady = 807,
        #[error("This error indicates that the maximum number of clients (including this\n one) that can be supported by the device has been reached. The\n application should destroy and then re-create the CUDA context.")]
        MpsMaxClientsReached = 808,
        #[error("This error indicates that the maximum number of connections for a given\n client (including this one) has been reached. The application should\n destroy and then re-create the CUDA context.")]
        MpsMaxConnectionsReached = 809,
        #[error("This error indicates that the client's connection to the device has been\n lost and that the client must destroy its CUDA context and establish a\n new connection to the device before CUDA functions may be invoked on\n the context.")]
        MpsClientTerminated = 810,
        #[error("This error indicates that CDP can not be used in the system because it\n is not supported by the primary context's device. This can happen when\n the primary context's device is in WDDM mode.")]
        CdpNotSupported = 811,
        #[error("This error indicates that the CDP kernel image does not have a matching\n architecture version to the device.")]
        CdpVersionMismatch = 812,
        #[error("This error indicates that the operation is not permitted when the stream\n is capturing.")]
        StreamCaptureUnsupported = 900,
        #[error("This error indicates that the current capture sequence on the stream has\n been invalidated due to a previous error.")]
        StreamCaptureInvalidated = 901,
        #[error("This error indicates that the operation would have resulted in a merge\n of two independent capture sequences.")]
        StreamCaptureMerge = 902,
        #[error("This error indicates that the capture was not initiated in this stream.")]
        StreamCaptureUnmatched = 903,
        #[error("This error indicates that the capture sequence contains a fork that was\n not joined to the primary stream.")]
        StreamCaptureUnjoined = 904,
        #[error("This error indicates that a dependency would have been created which\n crosses the capture sequence boundary. Only implicit in-stream ordering\n dependencies are allowed to cross the boundary.")]
        StreamCaptureIsolation = 905,
        #[error("This error indicates a disallowed implicit dependency on a current capture\n sequence from cudaStreamLegacy.")]
        StreamCaptureImplicit = 906,
        #[error("This error indicates that the operation is not permitted on an event which\n was last recorded in a capturing stream.")]
        CapturedEvent = 907,
        #[error("A stream capture sequence not initiated with the ::CU_STREAM_CAPTURE_MODE_RELAXED\n argument to ::cuStreamBeginCapture was passed to ::cuStreamEndCapture in a different thread.")]
        StreamCaptureWrongThread = 908,
        #[error("This error indicates that the timeout specified for the wait operation has lapsed.")]
        Timeout = 909,
        #[error("This error indicates that the graph update was not performed because it included\n changes which violated constraints specific to instantiated graph update.")]
        GraphExecUpdateFailure = 910,
        #[error("This indicates that an async error has occurred in a device outside of CUDA.\n If CUDA was waiting for an external device's signal before consuming shared data,\n the external device signaled an error indicating that the data is not valid for\n consumption. This leaves the process in an inconsistent state and any further CUDA\n work will return the same error. To continue using CUDA, the process must be\n terminated and relaunched.")]
        ExternalDevice = 911,
        #[error("Indicates a kernel launch error due to cluster misconfiguration.")]
        InvalidClusterSize = 912,
        #[error("This indicates that an unknown internal error has occurred.")]
        Unknown = 999,
    }
}

impl From<CuError> for ffi::CUresult {
    fn from(err: CuError) -> Self {
        err as ffi::CUresult
    }
}

impl From<ffi::CUresult> for CuError {
    fn from(res: ffi::CUresult) -> Self {
        CuError::from_u64(res as u64).unwrap_or(CuError::Unknown)
    }
}

pub type CuResult<T> = Result<T, CuError>;

#[cfg(test)]
mod tests {
    #[test]
    fn enum_from_primitive() {
        use super::CuError;
        use num_traits::FromPrimitive;

        assert_eq!(CuError::from_i32(1), Some(CuError::InvalidValue));
        assert_eq!(CuError::from_i32(2), Some(CuError::OutOfMemory));
        assert_eq!(CuError::from_i32(3), Some(CuError::NotInitialized));
        assert_eq!(CuError::from_i32(4), Some(CuError::Deinitialized));
        assert_eq!(CuError::from_i32(1000), None);
    }
}
