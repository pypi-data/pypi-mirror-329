use sea_orm::entity::prelude::*;

#[derive(Clone, Debug, PartialEq, Eq, DeriveEntityModel)]
#[sea_orm(table_name = "device_flow")]
pub struct Model {
    #[sea_orm(primary_key)]
    pub id: i32,
    pub machine_id: String,
    pub verification_uri: String,
    pub user_code: String,
    pub device_code: String,
    pub verification_uri_complete: String,
    pub is_verified: bool,
    #[sea_orm(column_type = "Timestamp")] // Explicitly specify column type
    pub created_at: Option<DateTimeWithTimeZone>, // sea_orm's type for TIMESTAMP
    #[sea_orm(column_type = "Timestamp")]
    pub updated_at: Option<DateTimeWithTimeZone>,
}

#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}

impl ActiveModelBehavior for ActiveModel {}
