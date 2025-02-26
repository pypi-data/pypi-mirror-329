use std::path::PathBuf;

// Utility functions
pub fn get_home_dir() -> PathBuf {
    dirs::home_dir().unwrap_or_else(|| PathBuf::from("../.."))
}

pub fn get_newbringer_config_dir() -> PathBuf {
    get_home_dir().join(".config").join("newbringer")
}

pub fn get_newbringer_data_dir() -> PathBuf {
    get_newbringer_config_dir().join("data")
}

pub fn get_newbringer_cache_dir() -> PathBuf {
    get_newbringer_config_dir().join("cache")
}

pub fn get_cert_dir() -> PathBuf {
    get_newbringer_data_dir().join("certs")
}

pub fn auth_dir() -> PathBuf {
    get_newbringer_data_dir().join("auth")
}

pub fn auth_file() -> PathBuf {
    auth_dir().join("auth0_config.json")
}
