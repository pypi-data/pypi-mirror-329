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

        // Define payment methods
        let payment_methods = vec![
            (1, "Vipps/MobilePay", "VIPPSMOBILEPAY", 1),
            (2, "Stripe", "STRIPE", 1),
            (3, "Development", "DEV_PAYMENT", 1),
        ];

        // Insert payment methods
        for (id, name, code, is_active) in payment_methods {
            let payment_method = payment_methods::ActiveModel {
                id: Set(id),
                name: Set(name.to_string()),
                code: Set(code.to_string()),
                is_active: Set(is_active), // Now using i8 (1 for true, 0 for false)
            };
            PaymentMethods::insert(payment_method).exec(db).await?;
        }

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        let db = manager.get_connection();

        // Remove all seeded payment methods
        PaymentMethods::delete_many()
            .filter(payment_methods::Column::Id.is_in(vec![1, 2, 3]))
            .exec(db)
            .await?;

        Ok(())
    }
}
