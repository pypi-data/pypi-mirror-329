use std::fs::{read_dir, File};
use std::io::{BufRead, BufReader};
use std::path::{Path, PathBuf};

pub struct SearchOptions {
    pub search_subdirs: bool,
    pub max_depth: usize,
}

pub fn find_env_file(variable: &str, options: SearchOptions) -> Option<PathBuf> {
    let current_dir = std::env::current_dir().ok()?;
    find_env_file_recursive(&current_dir, variable, &options, 0)
}

fn find_env_file_recursive(
    dir: &Path,
    variable: &str,
    options: &SearchOptions,
    current_depth: usize,
) -> Option<PathBuf> {
    let env_file_path = dir.join(".env");

    if env_file_path.exists() && file_contains_variable(&env_file_path, variable) {
        return Some(env_file_path);
    }

    if options.search_subdirs && current_depth < options.max_depth {
        if let Ok(entries) = read_dir(dir) {
            for entry in entries.flatten() {
                let path = entry.path();
                if path.is_dir() {
                    if let Some(found_path) =
                        find_env_file_recursive(&path, variable, options, current_depth + 1)
                    {
                        return Some(found_path);
                    }
                }
            }
        }
    }

    dir.parent()
        .and_then(|parent| find_env_file_recursive(parent, variable, options, current_depth))
}

fn file_contains_variable(file_path: &Path, variable: &str) -> bool {
    if let Ok(file) = File::open(file_path) {
        let reader = BufReader::new(file);
        reader
            .lines()
            .map_while(Result::ok)
            .any(|line| line.starts_with(variable) && line.contains('='))
    } else {
        false
    }
}
