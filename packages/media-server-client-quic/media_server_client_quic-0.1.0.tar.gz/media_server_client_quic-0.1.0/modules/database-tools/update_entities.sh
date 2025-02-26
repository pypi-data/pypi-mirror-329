#!/bin/bash

cargo install sea-orm-cli
cargo add sea-orm sqlx



sea-orm-cli generate entity -o ./migration/src/entities --with-serde both --database-url mysql://tagtwo:tagtwo@db/tagtwo?charset=utf8mb4