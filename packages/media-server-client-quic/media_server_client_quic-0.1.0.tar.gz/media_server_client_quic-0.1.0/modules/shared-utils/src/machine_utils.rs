// In machine_utils.rs
use std::{fs, io};

// Original functions remain unchanged
pub fn get_machine_id() -> io::Result<String> {
    let machine_id = fs::read_to_string("/etc/machine-id")?;
    Ok(machine_id.trim().to_string())
}

pub fn get_machine_id_trimmed() -> io::Result<String> {
    let machine_id = get_machine_id()?;
    Ok(machine_id[..6].to_string())
}
