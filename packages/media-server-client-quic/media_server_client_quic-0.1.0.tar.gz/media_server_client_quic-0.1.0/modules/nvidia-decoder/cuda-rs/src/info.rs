use crate::device::CuDevice;
use crate::ffi::{self};
use crate::ffi::{
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_ASYNC_ENGINE_COUNT,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CAN_MAP_HOST_MEMORY,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CAN_USE_64_BIT_STREAM_MEM_OPS,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CAN_USE_HOST_POINTER_FOR_REGISTERED_MEM,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CAN_USE_STREAM_WAIT_VALUE_NOR,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CLOCK_RATE,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CLUSTER_LAUNCH,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MAJOR,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MINOR,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_COMPUTE_MODE,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_COMPUTE_PREEMPTION_SUPPORTED,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CONCURRENT_KERNELS,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CONCURRENT_MANAGED_ACCESS,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_DEFERRED_MAPPING_CUDA_ARRAY_SUPPORTED,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_DIRECT_MANAGED_MEM_ACCESS_FROM_HOST,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_DMA_BUF_SUPPORTED,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_ECC_ENABLED,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_GENERIC_COMPRESSION_SUPPORTED,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_GLOBAL_L1_CACHE_SUPPORTED,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_GLOBAL_MEMORY_BUS_WIDTH,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_GPU_DIRECT_RDMA_FLUSH_WRITES_OPTIONS,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_GPU_DIRECT_RDMA_SUPPORTED,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_GPU_DIRECT_RDMA_WRITES_ORDERING,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_GPU_OVERLAP,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_HOST_NATIVE_ATOMIC_SUPPORTED,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_INTEGRATED,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_IPC_EVENT_SUPPORTED,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_KERNEL_EXEC_TIMEOUT,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_L2_CACHE_SIZE,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_LOCAL_L1_CACHE_SUPPORTED,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MANAGED_MEMORY,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAXIMUM_TEXTURE1D_WIDTH,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAXIMUM_TEXTURE2D_HEIGHT,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAXIMUM_TEXTURE2D_WIDTH,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAXIMUM_TEXTURE3D_DEPTH,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAXIMUM_TEXTURE3D_HEIGHT,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAXIMUM_TEXTURE3D_WIDTH,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_ACCESS_POLICY_WINDOW_SIZE,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_BLOCKS_PER_MULTIPROCESSOR,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_BLOCK_DIM_X,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_BLOCK_DIM_Y,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_BLOCK_DIM_Z,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_GRID_DIM_X,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_GRID_DIM_Y,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_GRID_DIM_Z,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_PERSISTING_L2_CACHE_SIZE,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_PITCH,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_REGISTERS_PER_BLOCK,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_REGISTERS_PER_MULTIPROCESSOR,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_SHARED_MEMORY_PER_BLOCK,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_SHARED_MEMORY_PER_BLOCK_OPTIN,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_SHARED_MEMORY_PER_MULTIPROCESSOR,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_THREADS_PER_BLOCK,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_THREADS_PER_MULTIPROCESSOR,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MEMORY_CLOCK_RATE,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MEMORY_POOLS_SUPPORTED,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MEMPOOL_SUPPORTED_HANDLE_TYPES,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MPS_ENABLED,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MULTICAST_SUPPORTED,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MULTI_GPU_BOARD,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MULTI_GPU_BOARD_GROUP_ID,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_PAGEABLE_MEMORY_ACCESS,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_PAGEABLE_MEMORY_ACCESS_USES_HOST_PAGE_TABLES,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_PCI_BUS_ID,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_PCI_DEVICE_ID,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_SURFACE_ALIGNMENT,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_TCC_DRIVER,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_TEXTURE_ALIGNMENT,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_TOTAL_CONSTANT_MEMORY,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_UNIFIED_ADDRESSING,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_UNIFIED_FUNCTION_POINTERS,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_VIRTUAL_MEMORY_MANAGEMENT_SUPPORTED,
    CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_WARP_SIZE,
};
use log::debug;
use std::ffi::CStr;

pub fn query_device_attributes(device: CuDevice) -> Result<(), String> {
    let attributes = [
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_THREADS_PER_BLOCK, "Max Threads per Block"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_BLOCK_DIM_X, "Max Block Dimension X"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_BLOCK_DIM_Y, "Max Block Dimension Y"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_BLOCK_DIM_Z, "Max Block Dimension Z"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_GRID_DIM_X, "Max Grid Dimension X"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_GRID_DIM_Y, "Max Grid Dimension Y"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_GRID_DIM_Z, "Max Grid Dimension Z"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_SHARED_MEMORY_PER_BLOCK, "Max Shared Memory per Block"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_TOTAL_CONSTANT_MEMORY, "Total Constant Memory"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_WARP_SIZE, "Warp Size"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_PITCH, "Max Pitch"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_REGISTERS_PER_BLOCK, "Max Registers per Block"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CLOCK_RATE, "Clock Rate"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_TEXTURE_ALIGNMENT, "Texture Alignment"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_GPU_OVERLAP, "GPU Overlap"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT, "Multiprocessor Count"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_KERNEL_EXEC_TIMEOUT, "Kernel Execution Timeout"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_INTEGRATED, "Integrated GPU"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CAN_MAP_HOST_MEMORY, "Can Map Host Memory"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_COMPUTE_MODE, "Compute Mode"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAXIMUM_TEXTURE1D_WIDTH, "Max Texture1D Width"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAXIMUM_TEXTURE2D_WIDTH, "Max Texture2D Width"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAXIMUM_TEXTURE2D_HEIGHT, "Max Texture2D Height"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAXIMUM_TEXTURE3D_WIDTH, "Max Texture3D Width"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAXIMUM_TEXTURE3D_HEIGHT, "Max Texture3D Height"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAXIMUM_TEXTURE3D_DEPTH, "Max Texture3D Depth"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_SURFACE_ALIGNMENT, "Surface Alignment"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CONCURRENT_KERNELS, "Concurrent Kernels"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_ECC_ENABLED, "ECC Enabled"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_PCI_BUS_ID, "PCI Bus ID"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_PCI_DEVICE_ID, "PCI Device ID"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_TCC_DRIVER, "TCC Driver"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MEMORY_CLOCK_RATE, "Memory Clock Rate"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_GLOBAL_MEMORY_BUS_WIDTH, "Global Memory Bus Width"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_L2_CACHE_SIZE, "L2 Cache Size"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_THREADS_PER_MULTIPROCESSOR, "Max Threads per MP"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_ASYNC_ENGINE_COUNT, "Async Engine Count"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_UNIFIED_ADDRESSING, "Unified Addressing"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MAJOR, "Compute Capability Major"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MINOR, "Compute Capability Minor"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_GLOBAL_L1_CACHE_SUPPORTED, "Global L1 Cache Supported"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_LOCAL_L1_CACHE_SUPPORTED, "Local L1 Cache Supported"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_SHARED_MEMORY_PER_MULTIPROCESSOR, "Max Shared Memory per MP"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_REGISTERS_PER_MULTIPROCESSOR, "Max Registers per MP"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MANAGED_MEMORY, "Managed Memory"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MULTI_GPU_BOARD, "Multi-GPU Board"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MULTI_GPU_BOARD_GROUP_ID, "Multi-GPU Board Group ID"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_HOST_NATIVE_ATOMIC_SUPPORTED, "Host Native Atomic"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_PAGEABLE_MEMORY_ACCESS, "Pageable Memory Access"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CONCURRENT_MANAGED_ACCESS, "Concurrent Managed Access"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_COMPUTE_PREEMPTION_SUPPORTED, "Compute Preemption"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CAN_USE_HOST_POINTER_FOR_REGISTERED_MEM, "Can Use Host Pointer for Registered Mem"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_SHARED_MEMORY_PER_BLOCK_OPTIN, "Max Shared Memory per Block Opt-in"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_PAGEABLE_MEMORY_ACCESS_USES_HOST_PAGE_TABLES, "Pageable Memory Uses Host Page Tables"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_DIRECT_MANAGED_MEM_ACCESS_FROM_HOST, "Direct Managed Mem Access from Host"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_VIRTUAL_MEMORY_MANAGEMENT_SUPPORTED, "Virtual Memory Management"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_BLOCKS_PER_MULTIPROCESSOR, "Max Blocks per MP"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_GENERIC_COMPRESSION_SUPPORTED, "Generic Compression"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_PERSISTING_L2_CACHE_SIZE, "Max Persisting L2 Cache Size"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_ACCESS_POLICY_WINDOW_SIZE, "Max Access Policy Window Size"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MEMORY_POOLS_SUPPORTED, "Memory Pools"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_GPU_DIRECT_RDMA_SUPPORTED, "GPUDirect RDMA"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_GPU_DIRECT_RDMA_FLUSH_WRITES_OPTIONS, "GPUDirect RDMA Flush Options"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_GPU_DIRECT_RDMA_WRITES_ORDERING, "GPUDirect RDMA Write Ordering"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MEMPOOL_SUPPORTED_HANDLE_TYPES, "Mempool Supported Handle Types"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CLUSTER_LAUNCH, "Cluster Launch"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_DEFERRED_MAPPING_CUDA_ARRAY_SUPPORTED, "Deferred Mapping CUDA Array"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CAN_USE_64_BIT_STREAM_MEM_OPS, "64-bit Stream MemOps"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CAN_USE_STREAM_WAIT_VALUE_NOR, "Stream Wait Value NOR"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_DMA_BUF_SUPPORTED, "DMA Buffer"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_IPC_EVENT_SUPPORTED, "IPC Event"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_UNIFIED_FUNCTION_POINTERS, "Unified Function Pointers"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MULTICAST_SUPPORTED, "Multicast"),
        (CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MPS_ENABLED, "MPS Enabled"),
    ];

    debug!("Querying attributes for device {}", device.get_raw());

    for (attr, name) in attributes.iter() {
        let mut value = 0;
        unsafe {
            let result = ffi::cuDeviceGetAttribute(&mut value, *attr, device.get_raw());
            if result != 0 {
                let mut error_str: *const i8 = std::ptr::null();
                ffi::cuGetErrorString(result, &mut error_str);
                let error = if !error_str.is_null() {
                    CStr::from_ptr(error_str).to_string_lossy().into_owned()
                } else {
                    format!("Unknown error: {}", result)
                };
                return Err(format!("Failed to get attribute {}: {}", name, error));
            }

            // Format special values
            #[allow(non_upper_case_globals)]
            let display_value = match *attr {
                CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_COMPUTE_MODE => match value {
                    0 => "Default".to_string(),
                    1 => "Exclusive".to_string(),
                    2 => "Prohibited".to_string(),
                    3 => "Exclusive Process".to_string(),
                    _ => format!("Unknown ({})", value),
                },
                CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_SHARED_MEMORY_PER_BLOCK
                | CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_TOTAL_CONSTANT_MEMORY
                | CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_L2_CACHE_SIZE
                | CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_SHARED_MEMORY_PER_MULTIPROCESSOR
                | CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MAX_PERSISTING_L2_CACHE_SIZE => {
                    format!("{} bytes", value)
                }
                CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_CLOCK_RATE
                | CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_MEMORY_CLOCK_RATE => {
                    format!("{} MHz", value / 1000)
                }
                CUdevice_attribute_enum_CU_DEVICE_ATTRIBUTE_GLOBAL_MEMORY_BUS_WIDTH => {
                    format!("{} bits", value)
                }
                _ if name.contains("Supported") || name.contains("Enabled") => {
                    if value == 0 {
                        "No".to_string()
                    } else {
                        "Yes".to_string()
                    }
                }
                _ => value.to_string(),
            };

            debug!("  {}: {}", name, display_value);
        }
    }

    Ok(())
}
