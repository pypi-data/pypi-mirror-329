use std::env;
use std::fs;
use std::path::{Path, PathBuf};

fn find_latest_cuda_version(base_path: &Path) -> Option<PathBuf> {
    if let Ok(entries) = fs::read_dir(base_path) {
        return entries
            .filter_map(|entry| entry.ok())
            .filter(|entry| {
                entry.path().is_dir() && entry.file_name().to_string_lossy().starts_with("cuda-")
            })
            .max_by(|a, b| {
                let name_a = a.file_name();
                let name_b = b.file_name();
                let ver_a = name_a.to_string_lossy();
                let ver_b = name_b.to_string_lossy();
                ver_a.cmp(&ver_b)
            })
            .map(|entry| entry.path());
    }
    None
}

fn find_dir(cuda_env_vars: &[&'static str]) -> Option<PathBuf> {
    let mut set_variables = std::collections::HashMap::new();
    let mut set_paths = std::collections::HashSet::new();

    // First check environment variables
    for env_var in cuda_env_vars {
        if let Some(cand_cuda_path) = env::var_os(env_var) {
            set_variables.insert(env_var, cand_cuda_path.clone());
            set_paths.insert(cand_cuda_path);
        }
    }

    match set_paths.len() {
        0 => {
            // No environment variables set, try to find CUDA installation
            let base_paths = ["/usr/local", "/opt"];
            for base in base_paths.iter() {
                let base_path = Path::new(base);

                // First try versioned CUDA directory
                if let Some(cuda_path) = find_latest_cuda_version(base_path) {
                    println!(
                        "Using latest CUDA installation found at: {}",
                        cuda_path.to_str().unwrap()
                    );
                    return Some(cuda_path);
                }

                // Fallback to unversioned cuda directory
                let cuda_path = base_path.join("cuda");
                if cuda_path.is_dir() {
                    println!(
                        "Using CUDA installation found at: {}",
                        cuda_path.to_str().unwrap()
                    );
                    return Some(cuda_path);
                }
            }
            None
        }
        1 => {
            let (env_var, cuda_path) = set_variables.drain().next().unwrap();
            println!(
                "Using CUDA path: {} from environment variable {}",
                cuda_path.to_str().unwrap(),
                env_var
            );
            Some(PathBuf::from(cuda_path))
        }
        _ => {
            panic!(
                "ERROR: npp-rs-sys: Multiple CUDA paths set: {:?}",
                set_variables
            );
        }
    }
}

fn validate_and_link_npp_install(cuda_home: &Path, npplibs: &[&str]) -> PathBuf {
    let cuda_include_dir = cuda_home.join("include");
    let npp_h = cuda_include_dir.join("npp.h");
    if !npp_h.is_file() {
        panic!(
            "ERROR: npp-rs-sys: Could not find npp.h include directory: {}",
            npp_h.to_string_lossy()
        );
    }

    // Try various lib directory locations
    let lib_paths = [
        cuda_home.join("targets").join("x86_64-linux").join("lib"),
        cuda_home.join("lib64"),
        cuda_home.join("lib"),
    ];

    let libdir = lib_paths
        .iter()
        .find(|&path| path.is_dir())
        .unwrap_or_else(|| {
            panic!(
                "ERROR: npp-rs-sys: Could not find CUDA lib directory in any of: {:?}",
                lib_paths
            )
        });

    println!("cargo:rustc-link-search={}", libdir.to_string_lossy());

    for npplib in npplibs {
        // Special case for culibos which doesn't follow the _static pattern
        if *npplib == "culibos" {
            let culibos_path = libdir.join("libculibos.a");
            if culibos_path.is_file() {
                println!("Using static library for culibos");
                println!("cargo:rustc-link-lib=static=culibos");
                continue;
            }
        }

        // Regular case for other libraries
        let static_path = libdir.join(format!("lib{}_static.a", npplib));
        let dynamic_path = libdir.join(format!("lib{}.so", npplib));

        if static_path.is_file() {
            println!("Using static library for {}", npplib);
            println!("cargo:rustc-link-lib=static={}_static", npplib);
        } else if dynamic_path.is_file() {
            println!("Using dynamic library for {}", npplib);
            println!("cargo:rustc-link-lib=dylib={}", npplib);
        } else {
            panic!(
                "ERROR: npp-rs-sys: Could not find neither static ({}) nor dynamic ({}) library for {}",
                static_path.to_string_lossy(),
                dynamic_path.to_string_lossy(),
                npplib
            );
        }
    }

    cuda_include_dir
}

fn main() {
    let cuda_path_vars = ["CUDA_PATH", "CUDA_HOME", "CUDA_ROOT", "CUDA_TOOLKIT_ROOT"];

    let npplibs = vec![
        "cudart", "nppc", "nppial", "nppicc", "nppidei", "nppif", "nppig", "nppim", "nppist",
        "nppisu", "nppitc", "npps", "culibos",
    ];
    println!("cargo:rustc-link-lib=stdc++");
    // change detection
    println!("cargo:rerun-if-changed=wrapper.h");
    for var in cuda_path_vars {
        println!("cargo:rerun-if-env-changed={}", var);
    }

    let cuda_home = find_dir(&cuda_path_vars).expect("Could not find CUDA installation");

    let cuda_include = validate_and_link_npp_install(&cuda_home, &npplibs);

    // Setup bindgen to scan correct folders
    let bindings = bindgen::Builder::default()
        .clang_arg(format!("-I{}", cuda_include.to_string_lossy()))
        .header("wrapper.h")
        .blocklist_function("strtold")
        .blocklist_function("qecvt")
        .blocklist_function("qfcvt")
        .blocklist_function("qgcvt")
        .blocklist_function("qecvt_r")
        .blocklist_function("qfcvt_r")
        .generate_comments(false)
        .generate()
        .expect("Unable to generate bindings");

    let out_path = PathBuf::from(env::var("OUT_DIR").unwrap());
    bindings
        .write_to_file(out_path.join("bindings.rs"))
        .expect("Couldn't write bindings!");
}
