use crate::m20220101_000001_create_table::{Games, Users};
use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .create_table(
                Table::create()
                    .table(PaymentMethods::Table)
                    .col(
                        ColumnDef::new(PaymentMethods::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(ColumnDef::new(PaymentMethods::Name).string().not_null())
                    .col(
                        ColumnDef::new(PaymentMethods::Code)
                            .string()
                            .not_null()
                            .unique_key(),
                    )
                    .col(
                        ColumnDef::new(PaymentMethods::IsActive)
                            .boolean()
                            .not_null()
                            .default(true),
                    )
                    .to_owned(),
            )
            .await?;

        manager
            .create_table(
                Table::create()
                    .table(PaymentTransactions::Table)
                    .col(
                        ColumnDef::new(PaymentTransactions::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(PaymentTransactions::UserId)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(PaymentTransactions::GameId)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(PaymentTransactions::PaymentMethodId)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(PaymentTransactions::ExternalId)
                            .string()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(PaymentTransactions::Amount)
                            .decimal()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(PaymentTransactions::Currency)
                            .string()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(PaymentTransactions::Status)
                            .string()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(PaymentTransactions::CreatedAt)
                            .date_time()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(PaymentTransactions::UpdatedAt)
                            .date_time()
                            .not_null(),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-payment_transactions-user_id")
                            .from(PaymentTransactions::Table, PaymentTransactions::UserId)
                            .to(Users::Table, Users::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Cascade),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-payment_transactions-payment_method_id")
                            .from(
                                PaymentTransactions::Table,
                                PaymentTransactions::PaymentMethodId,
                            )
                            .to(PaymentMethods::Table, PaymentMethods::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Cascade),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-payment_transactions-game_id")
                            .from(PaymentTransactions::Table, PaymentTransactions::GameId)
                            .to(Games::Table, Games::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Cascade),
                    )
                    .to_owned(),
            )
            .await?;

        manager
            .create_table(
                Table::create()
                    .table(PaymentDetails::Table)
                    .col(
                        ColumnDef::new(PaymentDetails::TransactionId)
                            .integer()
                            .not_null()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(PaymentDetails::RedirectUrl)
                            .string_len(2000)
                            .null(),
                    )
                    .col(ColumnDef::new(PaymentDetails::ClientSecret).string().null())
                    .col(ColumnDef::new(PaymentDetails::MetaData).json().null())
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-payment_details-transaction_id")
                            .from(PaymentDetails::Table, PaymentDetails::TransactionId)
                            .to(PaymentTransactions::Table, PaymentTransactions::Id)
                            .on_delete(ForeignKeyAction::Cascade)
                            .on_update(ForeignKeyAction::Cascade),
                    )
                    .to_owned(),
            )
            .await?;

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .drop_table(Table::drop().table(PaymentDetails::Table).to_owned())
            .await?;
        manager
            .drop_table(Table::drop().table(PaymentTransactions::Table).to_owned())
            .await?;
        manager
            .drop_table(Table::drop().table(PaymentMethods::Table).to_owned())
            .await?;
        Ok(())
    }
}

#[derive(Iden)]
enum PaymentMethods {
    Table,
    Id,
    Name,
    Code,
    IsActive,
}

#[derive(Iden)]
enum PaymentTransactions {
    Table,
    Id,
    UserId,
    GameId,
    PaymentMethodId,
    ExternalId,
    Amount,
    Currency,
    Status,
    CreatedAt,
    UpdatedAt,
}

#[derive(Iden)]
enum PaymentDetails {
    Table,
    TransactionId,
    RedirectUrl,
    ClientSecret,
    MetaData,
}
