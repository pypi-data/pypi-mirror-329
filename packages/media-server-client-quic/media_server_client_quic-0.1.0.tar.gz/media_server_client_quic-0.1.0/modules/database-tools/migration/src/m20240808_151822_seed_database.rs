use crate::entities::{prelude::*, *};
use sea_orm::entity::*;
use sea_orm::QueryFilter;
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        // Insert predefined component capabilities
        let capabilities = vec![(1, "camera"), (2, "gpio"), (3, "gps")];

        for (id, name) in capabilities {
            let capability = component_capabilities::ActiveModel {
                id: Set(id),
                name: Set(name.to_string()),
            };
            ComponentCapabilities::insert(capability).exec(db).await?;
        }

        // Insert PerGun-v3 into component_types
        let pergun_v3 = component_types::ActiveModel {
            id: Set(1),
            name: Set("PerGun-v3".to_string()),
            description: Set("PerGun-v3".to_string()),
            battery: Set(99),
            scope: Set(50),
            recoil: Set(20),
            rate_of_fire: Set(100),
            model_url: Set("https://raw.githubusercontent.com/perara-libs/3d-models/refs/heads/main/TAGTWO_Single.gltf".to_string())
        };
        let pergun_v3 = ComponentTypes::insert(pergun_v3).exec(db).await?;

        // Associate PerGun-v3 with camera and gpio capabilities
        let pergun_capabilities = [1, 2]; // IDs for camera and gpio
        for (index, capability_id) in pergun_capabilities.iter().enumerate() {
            let type_capability = component_type_capabilities::ActiveModel {
                id: Set((index + 1) as i32),
                capability_id: Set(*capability_id),
                component_type_id: Set(pergun_v3.last_insert_id),
            };
            ComponentTypeCapabilities::insert(type_capability)
                .exec(db)
                .await?;
        }

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        // Remove the PerGun-v3 component type and its associated capabilities
        ComponentTypeCapabilities::delete_many()
            .filter(component_type_capabilities::Column::ComponentTypeId.eq(1))
            .exec(db)
            .await?;

        ComponentTypes::delete_by_id(1).exec(db).await?;

        // Remove all predefined component capabilities
        ComponentCapabilities::delete_many()
            .filter(component_capabilities::Column::Id.is_in(vec![1, 2, 3]))
            .exec(db)
            .await?;

        Ok(())
    }
}
