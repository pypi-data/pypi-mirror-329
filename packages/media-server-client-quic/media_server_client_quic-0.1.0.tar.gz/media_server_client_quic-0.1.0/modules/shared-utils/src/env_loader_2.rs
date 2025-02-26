use config::{Config, ConfigError, Environment, File};
use log::{error, trace, warn};
use serde::{Deserialize, Deserializer, Serialize};
use serde_json;
use std::path::PathBuf;
use std::{collections::BTreeMap, env};
use validator::{Validate, ValidationError};

pub fn validate_optional_component<T>(component: &T) -> Result<(), ValidationError>
where
    T: Validate + Default + PartialEq,
{
    if component != &T::default() {
        component
            .validate()
            .map_err(|_| ValidationError::new("validation failed"))?;
    }
    Ok(())
}

pub trait ModuleIdentifier {
    fn module_path() -> &'static str;
}

pub trait ConfigLoader: Sized {
    type Settings: Default + Validate + Serialize + for<'de> Deserialize<'de> + ModuleIdentifier;

    fn find_config_file() -> Option<PathBuf>;
    fn load_module_config(
        config: &Config,
        module_name: &str,
        settings: &mut Self::Settings,
    ) -> Result<(), ConfigError>;
    fn merge_module_config(
        config: &Config,
        run_mode: &str,
        module_name: &str,
        settings: &mut Self::Settings,
    ) -> Result<(), ConfigError>;
    fn load(&self) -> Result<Self::Settings, ConfigError>;
}

pub struct GenericLoader<T>(std::marker::PhantomData<T>);

impl<T> Default for GenericLoader<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T> GenericLoader<T> {
    pub fn new() -> Self {
        Self(std::marker::PhantomData)
    }
}

impl<T> ConfigLoader for GenericLoader<T>
where
    T: Default + Validate + Serialize + for<'de> Deserialize<'de> + ModuleIdentifier,
{
    type Settings = T;

    fn find_config_file() -> Option<PathBuf> {
        let mut current_dir = env::current_dir().ok()?;
        let config_names = ["environment.yaml", "environment.yml"];
        trace!(
            "Searching for config file from directory: {}",
            current_dir.display()
        );

        loop {
            for name in &config_names {
                let config_path = current_dir.join(name);
                trace!("Checking for config file at: {}", config_path.display());
                if config_path.exists() {
                    return Some(config_path);
                }
            }

            if !current_dir.pop() {
                warn!("No config file found in directory tree");
                break;
            }
        }

        None
    }

    fn load_module_config(
        config: &Config,
        module_name: &str,
        settings: &mut Self::Settings,
    ) -> Result<(), ConfigError> {
        let path = format!("profiles.base.{}", module_name);
        trace!("Loading module '{}' from path: {}", module_name, path);

        if let Ok(raw) = config.get_table(&path) {
            trace!("Found raw {} config: {:#?}", module_name, raw);
        }

        if let Ok(config_value) = config.get::<serde_json::Value>(&path) {
            let settings_ref = &*settings;
            let mut settings_value = serde_json::to_value(settings_ref).map_err(|e| {
                ConfigError::Message(format!("Failed to serialize settings: {}", e))
            })?;

            if let serde_json::Value::Object(ref mut map) = settings_value {
                let field_name = module_name.replace("-", "_");

                // Check if the struct has this field before trying to insert
                let settings_type =
                    serde_json::to_value(Self::Settings::default()).map_err(|e| {
                        ConfigError::Message(format!("Failed to get settings type: {}", e))
                    })?;
                if let serde_json::Value::Object(type_map) = settings_type {
                    if !type_map.contains_key(&field_name) {
                        return Err(ConfigError::Message(format!(
                            "Settings struct is missing field for required module: {}",
                            module_name
                        )));
                    }
                }

                map.insert(field_name.clone(), config_value);
                trace!("Successfully loaded {} config", module_name);
            }

            *settings = serde_json::from_value(settings_value).map_err(|e| {
                ConfigError::Message(format!("Failed to deserialize settings: {}", e))
            })?;
        }

        Ok(())
    }

    fn merge_module_config(
        config: &Config,
        run_mode: &str,
        module_name: &str,
        settings: &mut Self::Settings,
    ) -> Result<(), ConfigError> {
        let path = format!("profiles.{}.{}", run_mode, module_name);
        trace!("Checking for overrides at path: {}", path);

        let field_name = module_name.replace("-", "_");

        if let Ok(override_value) = config.get::<serde_json::Value>(&path) {
            let settings_ref = &*settings;
            let mut settings_value = serde_json::to_value(settings_ref).map_err(|e| {
                ConfigError::Message(format!("Failed to serialize settings: {}", e))
            })?;

            if let serde_json::Value::Object(ref mut map) = settings_value {
                if let Some(current) = map.get(&field_name) {
                    let merged = merge_json_values(current, &override_value);
                    map.insert(field_name.clone(), merged);
                    trace!("Successfully merged {} config override", module_name);
                }
            }

            *settings = serde_json::from_value(settings_value).map_err(|e| {
                ConfigError::Message(format!("Failed to deserialize settings: {}", e))
            })?;
        }

        Ok(())
    }

    fn load(&self) -> Result<Self::Settings, ConfigError> {
        // Load only relevant environment variables from .env file
            let mut use_env_vars = env::var("NB_USE_ENV_VARS")
        .map(|v| v.parse().unwrap_or(false))
        .unwrap_or(false);
    
        let mut run_mode = env::var("RUN_MODE").unwrap_or_default();
        let mut env_file = env::var("NB_ENV_FILE").unwrap_or_default();

        // Then allow .env to override if present
        if let Ok(iter) = dotenvy::dotenv_iter() {
            for item in iter {
                match item {
                    Err(e) => {
                        warn!("Illegal environment variable: {:?}", e);
                        continue;
                    }
                    Ok((key, value)) => match key.as_str() {
                        "NB_USE_ENV_VARS" => {
                            use_env_vars = value.parse().unwrap_or(false);
                        }
                        "RUN_MODE" => {
                            run_mode = value;
                        }
                        "NB_ENV_FILE" => {
                            env_file = value;
                        }
                        _ => {}
                    },
                }
            }
        }

        let mut settings = Self::Settings::default();

        // Create our own environment store
        let mut env_store = BTreeMap::new();

        // Always try to load .env file if specified
        if !&env_file.is_empty() {
            trace!("Using environment file from NB_ENV_FILE: {}", &env_file);
            if let Ok(metadata) = std::fs::metadata(&env_file) {
                if metadata.is_file() {
                    trace!("Found .env file, will load as environment variables");
                    let content = std::fs::read_to_string(&env_file).map_err(|e| {
                        ConfigError::Message(format!("Failed to read .env file: {}", e))
                    })?;

                    for line in content.lines() {
                        let line = line.trim();
                        if line.is_empty() || line.starts_with('#') {
                            continue;
                        }

                        if let Some((key, value)) = line.split_once('=') {
                            let key = key.trim();
                            let value = value.trim_start();
                            env_store.insert(key.to_string(), value.to_string());
                            trace!("Set environment variable: {}={}", key, value);
                        }
                    }
                }
            }
        }

        // Add system environment variables to store
        for (key, value) in env::vars() {
            if key.starts_with("NB_") {
                env_store.insert(key, value);
            }
        }

        if use_env_vars || Self::find_config_file().is_none() {
            trace!("Loading configuration from environment variables");

            // Create root object
            let mut root = serde_json::Map::new();

            fn parse_value(value: &str) -> serde_json::Value {
                trace!("Parsing value: {:?}", value);

                // First handle array-like strings
                if value.trim().starts_with('[') && value.trim().ends_with(']') {
                    trace!("Attempting to parse array value");

                    // Clean the value of any outer quotes
                    let clean_value = value.trim().trim_matches('"').trim_matches('\'');

                    // Try to parse as a JSON array
                    if let Ok(json_value) = serde_json::from_str(clean_value) {
                        trace!("Successfully parsed JSON array: {:?}", json_value);
                        return json_value;
                    }

                    // If JSON parsing fails, try comma-separated format
                    let items: Vec<String> = clean_value[1..clean_value.len() - 1]
                        .split(',')
                        .map(|s| s.trim().to_string())
                        .collect();

                    trace!("Parsed as comma-separated array: {:?}", items);
                    return serde_json::Value::Array(
                        items.into_iter().map(serde_json::Value::String).collect(),
                    );
                }

                // Check if the value is quoted
                let is_quoted = (value.starts_with('"') && value.ends_with('"'))
                    || (value.starts_with('\'') && value.ends_with('\''));

                if is_quoted {
                    let unquoted = &value[1..value.len() - 1];
                    trace!("Value is quoted, treating as string: {:?}", unquoted);

                    // Check if the unquoted value might be an array
                    if unquoted.starts_with('[') && unquoted.ends_with(']') {
                        if let Ok(json_value) = serde_json::from_str(unquoted) {
                            trace!("Found array in quoted string: {:?}", json_value);
                            return json_value;
                        }
                    }

                    return serde_json::Value::String(unquoted.to_string());
                }

                // Handle unquoted values
                let trimmed = value.trim();
                trace!("Processing unquoted value: {:?}", trimmed);

                // Try boolean first
                match trimmed.to_lowercase().as_str() {
                    "true" | "yes" | "1" => {
                        trace!("Parsed as boolean true");
                        return serde_json::Value::Bool(true);
                    }
                    "false" | "no" | "0" => {
                        trace!("Parsed as boolean false");
                        return serde_json::Value::Bool(false);
                    }
                    _ => trace!("Not a boolean value"),
                }

                // Try integers first (before float)
                if let Ok(num) = trimmed.parse::<i64>() {
                    trace!("Successfully parsed as integer: {}", num);
                    return serde_json::Value::Number(num.into());
                }
                trace!("Integer parsing failed");

                // Try float next
                if let Ok(num) = trimmed.parse::<f64>() {
                    if let Some(num) = serde_json::Number::from_f64(num) {
                        trace!("Successfully parsed as float: {}", num);
                        return serde_json::Value::Number(num);
                    }
                }
                trace!("Float parsing failed");

                // If all parsing attempts fail, return as string
                trace!("Defaulting to string: {:?}", trimmed);
                serde_json::Value::String(trimmed.to_string())
            }

            fn insert_value(
                map: &mut serde_json::Map<String, serde_json::Value>,
                parts: &[&str],
                value: &str,
            ) {
                if parts.is_empty() {
                    return;
                }

                if parts.len() == 1 {
                    let parsed_value = parse_value(value);
                    trace!("Inserting value for key '{}': {:?}", parts[0], parsed_value);
                    map.insert(parts[0].to_string(), parsed_value);
                    return;
                }

                let current_key = parts[0].to_string();
                let next = map
                    .entry(current_key)
                    .or_insert_with(|| serde_json::Value::Object(serde_json::Map::new()));

                if let serde_json::Value::Object(next_map) = next {
                    insert_value(next_map, &parts[1..], value);
                }
            }

            // First pass: collect all variables by their full path
            let mut vars: Vec<(String, String)> = Vec::new();

            for (key, value) in env_store.iter().filter(|(k, _)| k.starts_with("NB_")) {
                trace!("Processing env var: {} = {}", key, value);

                // Skip the NB_ prefix and convert to lowercase
                let key = key.strip_prefix("NB_").unwrap_or("").to_lowercase();
                vars.push((key, value.clone()));
            }

            // Build the structure
            for (key, value) in vars {
                // Split by double underscore to get the nested levels
                let parts: Vec<&str> = key.split("__").collect();
                if parts.is_empty() {
                    continue;
                }

                // First part is the section (common, auth, etc)
                let section = parts[0];

                // Get or create the section object
                let section_obj = root
                    .entry(section.to_string())
                    .or_insert_with(|| serde_json::Value::Object(serde_json::Map::new()));

                if let serde_json::Value::Object(section_map) = section_obj {
                    insert_value(section_map, &parts[1..], &value);
                }
            }

            trace!("Built configuration structure: {:#?}", root);

            // Deserialize into settings
            match serde_json::from_value(serde_json::Value::Object(root)) {
                Ok(s) => settings = s,
                Err(e) => {
                    error!("Failed to deserialize environment variables: {}", e);
                    return Err(ConfigError::Message(format!(
                        "Failed to load environment variables: {}",
                        e
                    )));
                }
            }
        } else if let Some(config_path) = Self::find_config_file() {
            // Original YAML config loading logic
            trace!("Loading config from: {}", config_path.display());
            let config = Config::builder()
                .add_source(File::from(config_path))
                .build()
                .map_err(|e| ConfigError::Message(format!("Failed to load config: {}", e)))?;

            // Load base profile from includes
            let module_path = Self::Settings::module_path();
            trace!("Loading config for module path: {}", module_path);

            let includes = config
                .get::<Vec<String>>(&format!("{}.include", module_path))
                .map_err(|e| {
                    ConfigError::Message(format!(
                        "Failed to get includes for {}: {}",
                        module_path, e
                    ))
                })?;

            trace!("Found includes for {}: {:?}", module_path, includes);

            // First validate that all included modules have config sections
            for module_name in &includes {
                let path = format!("profiles.base.{}", module_name);
                if config.get::<serde_json::Value>(&path).is_err() {
                    error!(
                        "Missing configuration for module '{}' at path '{}'",
                        module_name, path
                    );
                    return Err(ConfigError::Message(format!(
                        "Missing configuration for required module '{}' at path '{}'",
                        module_name, path
                    )));
                }
                trace!(
                    "Found config for module '{}' at path '{}'",
                    module_name,
                    path
                );
            }

            // Then validate that the settings struct doesn't have extra fields
            let settings_type = serde_json::to_value(Self::Settings::default())
                .map_err(|e| ConfigError::Message(format!("Failed to get settings type: {}", e)))?;

            if let serde_json::Value::Object(type_map) = settings_type {
                for field_name in type_map.keys() {
                    if field_name != "common" {
                        // Skip common as it's always allowed
                        let module_name = field_name;
                        if !includes.contains(module_name) {
                            error!("Settings struct contains field '{}' but module '{}' is not in includes list", field_name, module_name);
                            return Err(ConfigError::Message(format!(
                                "Settings struct contains field '{}' but module '{}' is not in includes list", 
                                field_name, module_name
                            )));
                        }
                    }
                }
            }

            // Then load the configs
            for module_name in includes {
                trace!("Loading config for module '{}'", module_name);
                if let Err(e) = Self::load_module_config(&config, &module_name, &mut settings) {
                    error!("Failed to load config for module '{}': {}", module_name, e);
                    return Err(e);
                }
            }

            // Apply profile-specific overrides from includes
            if !run_mode.is_empty() {
                trace!("Applying overrides for run mode: {}", run_mode);
                if let Ok(includes) = config.get::<Vec<String>>(&format!("{}.include", module_path))
                {
                    for module_name in includes {
                        if let Err(e) = Self::merge_module_config(
                            &config,
                            &run_mode,
                            &module_name,
                            &mut settings,
                        ) {
                            error!("Failed to merge config override for module '{}' in run mode '{}': {}", module_name, run_mode, e);
                            return Err(e);
                        }
                    }
                }
            } else {
                warn!("RUN_MODE is not set, using base profile");
            }
        } else {
            // Fallback to environment variables if no config file found
            trace!("No config file found, falling back to environment variables");
            let env_prefix = "NB";
            if let Ok(env_settings) = Config::builder()
                .add_source(Environment::with_prefix(env_prefix).separator("_"))
                .build()
            {
                match env_settings.try_deserialize() {
                    Ok(s) => settings = s,
                    Err(e) => {
                        error!("Failed to deserialize environment variables: {}", e);
                        return Err(ConfigError::Message(format!(
                            "Failed to load environment variables: {}",
                            e
                        )));
                    }
                }
            }
        }

        // Validate final settings
        if let Err(errors) = settings.validate() {
            error!("Configuration validation failed:");
            for (field, error) in errors.field_errors() {
                error!(
                    "  {}: {}",
                    field,
                    error[0].message.as_ref().unwrap_or(&"Unknown error".into())
                );
            }
            return Err(ConfigError::Message(
                "Configuration validation failed".to_string(),
            ));
        }

        Ok(settings)
    }
}

fn merge_json_values(base: &serde_json::Value, other: &serde_json::Value) -> serde_json::Value {
    match (base, other) {
        (serde_json::Value::Object(base_map), serde_json::Value::Object(other_map)) => {
            let mut result = base_map.clone();
            for (key, value) in other_map {
                if !value.is_null() && value.as_str() != Some("") && value.as_str() != Some("0") {
                    match (result.get(key), value) {
                        (Some(base_val), other_val)
                            if base_val.is_object() && other_val.is_object() =>
                        {
                            result.insert(key.clone(), merge_json_values(base_val, other_val));
                        }
                        _ => {
                            result.insert(key.clone(), value.clone());
                        }
                    }
                }
            }
            serde_json::Value::Object(result)
        }
        (_, other) => other.clone(),
    }
}

/// Convert any serializable struct into environment variables format
pub fn to_env_vars<T: Serialize>(value: &T, prefix: &str) -> BTreeMap<String, String> {
    let mut env_vars = BTreeMap::new();

    fn flatten_to_env_vars(
        map: &mut BTreeMap<String, String>,
        prefix: &str,
        value: &serde_json::Value,
        current_path: &str,
    ) {
        match value {
            serde_json::Value::Object(obj) => {
                for (key, val) in obj {
                    let new_path = if current_path.is_empty() {
                        key.to_string()
                    } else {
                        format!("{}__{}", current_path, key)
                    };
                    flatten_to_env_vars(map, prefix, val, &new_path);
                }
            }
            serde_json::Value::Array(arr) => {
                // Note: prefix already includes the underscore
                let key = format!("{}{}", prefix, current_path).to_uppercase();
                let value = serde_json::to_string(arr).unwrap_or_else(|_| "[]".to_string());
                trace!("Setting array env var: {} = {}", key, value);
                map.insert(key, value);
            }
            serde_json::Value::String(s) => {
                let key = format!("{}{}", prefix, current_path).to_uppercase();
                trace!("Setting string env var: {} = \"{}\"", key, s);
                map.insert(key, format!("\"{}\"", s));
            }
            serde_json::Value::Number(n) => {
                let key = format!("{}{}", prefix, current_path).to_uppercase();
                trace!("Setting number env var: {} = {}", key, n);
                map.insert(key, n.to_string());
            }
            serde_json::Value::Bool(b) => {
                let key = format!("{}{}", prefix, current_path).to_uppercase();
                let value = if *b { "True" } else { "False" };
                trace!("Setting boolean env var: {} = {}", key, value);
                map.insert(key, value.to_string());
            }
            serde_json::Value::Null => {
                let key = format!("{}{}", prefix, current_path).to_uppercase();
                trace!("Setting null env var: {} = \"\"", key);
                map.insert(key, "\"\"".to_string());
            }
        }
    }

    if let Ok(json_value) = serde_json::to_value(value) {
        // Ensure prefix includes the underscore
        let prefix = if prefix.ends_with('_') {
            prefix.to_string()
        } else {
            format!("{}_", prefix)
        };

        flatten_to_env_vars(&mut env_vars, &prefix, &json_value, "");
        trace!("Generated {} environment variables", env_vars.len());
    } else {
        trace!("Failed to serialize value to JSON");
    }

    env_vars
}
// Add helper function for string deserialization
pub fn deserialize_string<'de, D>(deserializer: D) -> Result<String, D::Error>
where
    D: Deserializer<'de>,
{
    use serde::de::Error;

    // Try to deserialize into a Value first
    let value = serde_json::Value::deserialize(deserializer)?;

    match value {
        serde_json::Value::String(s) => Ok(s),
        serde_json::Value::Number(n) => Ok(n.to_string()),
        serde_json::Value::Bool(b) => Ok(b.to_string()),
        serde_json::Value::Null => Ok(String::new()),
        _ => Err(Error::custom("Expected string, number, bool, or null")),
    }
}

// Export the macro for use in other modules
#[macro_export]
macro_rules! string_from_any {
    () => {
        #[serde(deserialize_with = "shared_utils::env_loader_2::deserialize_string")]
    };
}
