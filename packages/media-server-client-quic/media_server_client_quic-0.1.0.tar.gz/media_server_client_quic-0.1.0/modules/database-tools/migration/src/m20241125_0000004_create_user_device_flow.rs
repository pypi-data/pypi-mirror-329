use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .create_table(
                Table::create()
                    .table(DeviceFlow::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(DeviceFlow::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(ColumnDef::new(DeviceFlow::MachineId).string().not_null())
                    .col(
                        ColumnDef::new(DeviceFlow::VerificationUri)
                            .string()
                            .not_null(),
                    )
                    .col(ColumnDef::new(DeviceFlow::UserCode).string().not_null())
                    .col(ColumnDef::new(DeviceFlow::DeviceCode).string().not_null())
                    .col(
                        ColumnDef::new(DeviceFlow::VerificationUriComplete)
                            .string()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(DeviceFlow::CreatedAt)
                            .timestamp()
                            .not_null()
                            .default(SimpleExpr::Custom("CURRENT_TIMESTAMP".into())),
                    )
                    .col(
                        ColumnDef::new(DeviceFlow::UpdatedAt)
                            .timestamp()
                            .not_null()
                            .default(SimpleExpr::Custom("CURRENT_TIMESTAMP".into())),
                    )
                    .col(
                        ColumnDef::new(DeviceFlow::IsVerified)
                            .boolean()
                            .not_null()
                            .default(false),
                    )
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .drop_table(Table::drop().table(DeviceFlow::Table).to_owned())
            .await
    }
}

#[derive(Iden)]
enum DeviceFlow {
    Table,
    Id,
    MachineId,
    VerificationUri,
    UserCode,
    DeviceCode,
    VerificationUriComplete,
    CreatedAt,
    UpdatedAt,
    IsVerified,
}
