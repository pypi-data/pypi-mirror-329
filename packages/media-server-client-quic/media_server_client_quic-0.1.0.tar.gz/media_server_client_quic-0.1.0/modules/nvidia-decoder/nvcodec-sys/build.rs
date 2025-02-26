use std::env;
use std::path::PathBuf;

fn find_dir(env_key: &'static str, candidates: Vec<&'static str>) -> Option<PathBuf> {
    match env::var_os(env_key) {
        Some(val) => Some(PathBuf::from(&val)),
        _ => {
            for candidate in candidates {
                let path = PathBuf::from(candidate);
                if path.exists() {
                    return Some(path);
                }
            }
            None
        }
    }
}

fn main() {
    println!("cargo:rerun-if-changed=wrapper.h");
    println!("cargo:rerun-if-changed=include/nvcuvid.h");
    println!("cargo:rerun-if-changed=build.rs");
    println!("cargo:rerun-if-env-changed=CUDA_INCLUDE_PATH");

    let cuda_include = find_dir(
        "CUDA_INCLUDE_PATH",
        vec!["/opt/cuda/include", "/usr/local/cuda/include"],
    )
    .expect("Could not find CUDA include path");

    // Generate bindings...
    let out_dir = PathBuf::from(env::var("OUT_DIR").expect("OUT_DIR not set"));
    let include_dir = out_dir.join("include");
    std::fs::create_dir_all(&include_dir).expect("Failed to create include directory");

    std::fs::copy("include/nvcuvid.h", include_dir.join("nvcuvid.h"))
        .expect("Failed to copy nvcuvid.h");

    // Generate bindings
    let bindings = bindgen::Builder::default()
        .header("wrapper.h")
        .clang_arg(format!("-I{}", include_dir.display()))
        .clang_arg(format!("-I{}", cuda_include.display()))
        // Types
        .allowlist_type("CUvideoparser")
        .allowlist_type("CUvideodecoder")
        .allowlist_type("CUdeviceptr")
        .allowlist_type("CUresult")
        .allowlist_type("CUcontext")
        .allowlist_type("CUVIDEOFORMAT")
        .allowlist_type("CUVIDPICPARAMS")
        .allowlist_type("CUVIDPARSERDISPINFO")
        .allowlist_type("CUVIDSOURCEDATAPACKET")
        .allowlist_type("CUVIDDECODECAPS")
        .allowlist_type("CUVIDPARSERPARAMS")
        .allowlist_type("CUVIDDECODECREATEINFO")
        .allowlist_type("CUVIDPROCPARAMS")
        .allowlist_type("CUVIDGETDECODESTATUS")
        .allowlist_type("CUVIDRECONFIGUREDECODERINFO")
        // Enums
        .allowlist_type("CUvideopacketflags.*")
        .allowlist_type("cudaVideoCodec_enum")
        .allowlist_type("cudaVideoChromaFormat_enum")
        .allowlist_type("cudaVideoCreateFlags_enum")
        .allowlist_type("cudaError_enum")
        // Settings
        .generate_comments(true)
        .derive_debug(true)
        .derive_default(true)
        .derive_copy(true)
        .derive_eq(true)
        .derive_hash(true)
        .size_t_is_usize(true)
        .layout_tests(true)
        .formatter(bindgen::Formatter::Rustfmt)
        .generate()
        .expect("Unable to generate bindings");

    bindings
        .write_to_file(out_dir.join("bindings.rs"))
        .expect("Couldn't write bindings!");
}
