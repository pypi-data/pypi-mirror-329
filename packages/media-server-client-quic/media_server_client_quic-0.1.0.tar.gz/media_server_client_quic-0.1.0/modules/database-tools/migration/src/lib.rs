use anyhow::{anyhow, Result};
use log::{error, info};
use sea_orm_migration::prelude::*;
use std::env;
use std::io::{BufRead, BufReader};
use std::process::{Command, Stdio};

pub mod m20220101_000001_create_table;
mod m20240808_151822_seed_database;

mod m20241125_0000002_create_payment;
mod m20241125_0000003_create_payment_data;

mod m20241125_0000004_create_user_device_flow;

pub mod entities;

pub struct Migrator;

#[async_trait::async_trait]
impl MigratorTrait for Migrator {
    fn migrations() -> Vec<Box<dyn MigrationTrait>> {
        vec![
            Box::new(m20220101_000001_create_table::Migration),
            Box::new(m20240808_151822_seed_database::Migration),
            Box::new(m20241125_0000002_create_payment::Migration),
            Box::new(m20241125_0000003_create_payment_data::Migration),
            Box::new(m20241125_0000004_create_user_device_flow::Migration),
        ]
    }
}

impl Migrator {
    pub async fn generate_entities(database_url: &str, entities_dir: &str) -> Result<()> {
        info!("Entities directory: {}", entities_dir);
        info!(
            "Current working directory: {}",
            env::current_dir()?.display()
        );

        let mut child = Command::new("/root/.cargo/bin/sea-orm-cli")
            .args([
                "generate",
                "entity",
                "--database-url",
                database_url,
                "--output-dir",
                entities_dir,
                "--with-serde",
                "both",
            ])
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .map_err(|e| anyhow!("Failed to execute sea-orm-cli: {}", e))?;

        // Capture and print stdout in real-time
        if let Some(stdout) = child.stdout.take() {
            let reader = BufReader::new(stdout);
            for line in reader.lines() {
                info!("sea-orm-cli stdout: {}", line?);
            }
        }

        // Capture and print stderr in real-time
        if let Some(stderr) = child.stderr.take() {
            let reader = BufReader::new(stderr);
            for line in reader.lines() {
                error!("sea-orm-cli stderr: {}", line?);
            }
        }

        // Wait for the command to finish and check the exit status
        let status = child
            .wait()
            .map_err(|e| anyhow!("Failed to wait for sea-orm-cli: {}", e))?;

        if status.success() {
            info!("Entities generated successfully.");
            Ok(())
        } else {
            Err(anyhow!(
                "sea-orm-cli failed with exit code: {:?}",
                status.code()
            ))
        }
    }
}
