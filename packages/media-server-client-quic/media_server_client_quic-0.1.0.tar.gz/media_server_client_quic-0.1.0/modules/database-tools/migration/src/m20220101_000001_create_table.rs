use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Users Table
        manager
            .create_table(
                Table::create()
                    .table(Users::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(Users::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(Users::Auth0Id)
                            .string()
                            .not_null()
                            .unique_key(),
                    )
                    .col(ColumnDef::new(Users::Name).string().not_null())
                    .col(ColumnDef::new(Users::Avatar).string().not_null())
                    .to_owned(),
            )
            .await?;

        // Units Table
        manager
            .create_table(
                Table::create()
                    .table(Units::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(Units::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(ColumnDef::new(Units::Uuid).string().not_null())
                    .col(ColumnDef::new(Units::Name).string().not_null())
                    .col(ColumnDef::new(Units::CreatedAt).date_time().not_null())
                    .col(ColumnDef::new(Units::UpdatedAt).date_time().not_null())
                    .to_owned(),
            )
            .await?;

        // Games Table
        manager
            .create_table(
                Table::create()
                    .table(Games::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(Games::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(ColumnDef::new(Games::Uid).string().not_null())
                    .col(ColumnDef::new(Games::MaxPlayers).integer().not_null())
                    .col(ColumnDef::new(Games::Duration).integer().not_null())
                    .col(ColumnDef::new(Games::Latitude).float().not_null())
                    .col(ColumnDef::new(Games::Longitude).float().not_null())
                    .col(ColumnDef::new(Games::MinRadius).integer().not_null())
                    .col(ColumnDef::new(Games::StartRadius).integer().not_null())
                    .col(
                        ColumnDef::new(Games::PersistReboot)
                            .tiny_integer()
                            .not_null(),
                    )
                    .col(ColumnDef::new(Games::Status).string().not_null())
                    .col(ColumnDef::new(Games::OwnerId).integer().not_null())
                    .col(ColumnDef::new(Games::CreatedAt).date_time().not_null())
                    .col(ColumnDef::new(Games::UpdatedAt).date_time().not_null())
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-games-owner_id")
                            .from(Games::Table, Games::OwnerId)
                            .to(Users::Table, Users::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .to_owned(),
            )
            .await?;

        // GameParticipants Table
        manager
            .create_table(
                Table::create()
                    .table(GameParticipants::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(GameParticipants::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(GameParticipants::State)
                            .string()
                            .not_null()
                            .default("active"),
                    )
                    .col(
                        ColumnDef::new(GameParticipants::GameId)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameParticipants::UserId)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameParticipants::UnitId)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameParticipants::StreamId)
                            .big_unsigned()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameParticipants::CreatedAt)
                            .date_time()
                            .not_null()
                            .extra("DEFAULT CURRENT_TIMESTAMP".to_string()),
                    )
                    .col(
                        ColumnDef::new(GameParticipants::UpdatedAt)
                            .date_time()
                            .not_null()
                            .extra(
                                "DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP".to_string(),
                            ),
                    )
                    .col(
                        ColumnDef::new(GameParticipants::AccessToken)
                            .string_len(8192)
                            .not_null(),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-game_participants-game_id")
                            .from(GameParticipants::Table, GameParticipants::GameId)
                            .to(Games::Table, Games::Id)
                            .on_delete(ForeignKeyAction::Cascade)
                            .on_update(ForeignKeyAction::Cascade),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-game_participants-user_id")
                            .from(GameParticipants::Table, GameParticipants::UserId)
                            .to(Users::Table, Users::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Cascade),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-game_participants-unit_id")
                            .from(GameParticipants::Table, GameParticipants::UnitId)
                            .to(Units::Table, Units::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Cascade),
                    )
                    .index(
                        Index::create()
                            .name("idx-game_participants-game_unit")
                            .col(GameParticipants::GameId)
                            .col(GameParticipants::UnitId)
                            .unique(),
                    )
                    .to_owned(),
            )
            .await?;

        // ComponentTypes Table (renamed from UnitComponentTypes)
        manager
            .create_table(
                Table::create()
                    .table(ComponentTypes::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(ComponentTypes::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(ColumnDef::new(ComponentTypes::Name).string().not_null())
                    .col(
                        ColumnDef::new(ComponentTypes::Description)
                            .string()
                            .not_null(),
                    )
                    .col(ColumnDef::new(ComponentTypes::Battery).integer().not_null())
                    .col(ColumnDef::new(ComponentTypes::Scope).integer().not_null())
                    .col(ColumnDef::new(ComponentTypes::Recoil).integer().not_null())
                    .col(
                        ColumnDef::new(ComponentTypes::RateOfFire)
                            .integer()
                            .not_null(),
                    )
                    .col(ColumnDef::new(ComponentTypes::ModelUrl).string().not_null())
                    .to_owned(),
            )
            .await?;

        // ComponentCapabilities Table
        manager
            .create_table(
                Table::create()
                    .table(ComponentCapabilities::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(ComponentCapabilities::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(ComponentCapabilities::Name)
                            .string()
                            .not_null(),
                    )
                    .to_owned(),
            )
            .await?;

        // ComponentTypeCapabilities Table (renamed from UnitComponentTypeCapabilities)
        manager
            .create_table(
                Table::create()
                    .table(ComponentTypeCapabilities::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(ComponentTypeCapabilities::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(ComponentTypeCapabilities::CapabilityId)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(ComponentTypeCapabilities::ComponentTypeId)
                            .integer()
                            .not_null(),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-component_type_capabilities-component_type_id")
                            .from(
                                ComponentTypeCapabilities::Table,
                                ComponentTypeCapabilities::ComponentTypeId,
                            )
                            .to(ComponentTypes::Table, ComponentTypes::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-component_type_capabilities-capability_id")
                            .from(
                                ComponentTypeCapabilities::Table,
                                ComponentTypeCapabilities::CapabilityId,
                            )
                            .to(ComponentCapabilities::Table, ComponentCapabilities::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .to_owned(),
            )
            .await?;

        // Components Table
        manager
            .create_table(
                Table::create()
                    .table(Components::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(Components::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(Components::SerialNumber)
                            .string()
                            .not_null()
                            .unique_key(),
                    )
                    .col(
                        ColumnDef::new(Components::ComponentTypeId)
                            .integer()
                            .not_null(),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-components-component_type_id")
                            .from(Components::Table, Components::ComponentTypeId)
                            .to(ComponentTypes::Table, ComponentTypes::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .to_owned(),
            )
            .await?;

        // UserComponents Table
        // UserComponents Table
        manager
            .create_table(
                Table::create()
                    .table(UserComponents::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(UserComponents::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(ColumnDef::new(UserComponents::UserId).integer().not_null())
                    .col(
                        ColumnDef::new(UserComponents::ComponentId)
                            .integer()
                            .not_null(),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-user_components-user_id")
                            .from(UserComponents::Table, UserComponents::UserId)
                            .to(Users::Table, Users::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-user_components-component_id")
                            .from(UserComponents::Table, UserComponents::ComponentId)
                            .to(Components::Table, Components::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .to_owned(),
            )
            .await?;

        // UnitComponents Table (renamed from UnitsComponents)
        manager
            .create_table(
                Table::create()
                    .table(UnitComponents::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(UnitComponents::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(ColumnDef::new(UnitComponents::UnitId).integer().not_null())
                    .col(
                        ColumnDef::new(UnitComponents::ComponentId)
                            .integer()
                            .not_null(),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-unit_components-unit_id")
                            .from(UnitComponents::Table, UnitComponents::UnitId)
                            .to(Units::Table, Units::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-unit_components-user_components_id")
                            .from(UnitComponents::Table, UnitComponents::ComponentId)
                            .to(UserComponents::Table, UserComponents::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .to_owned(),
            )
            .await?;

        // UnitOwners Table (renamed from UnitsOwners)
        manager
            .create_table(
                Table::create()
                    .table(UnitOwners::Table)
                    .if_not_exists()
                    .col(ColumnDef::new(UnitOwners::UserId).integer().not_null())
                    .col(ColumnDef::new(UnitOwners::UnitId).integer().not_null())
                    .col(ColumnDef::new(UnitOwners::CreatedAt).date_time().not_null())
                    .col(ColumnDef::new(UnitOwners::UpdatedAt).date_time().not_null())
                    .primary_key(
                        Index::create()
                            .col(UnitOwners::UserId)
                            .col(UnitOwners::UnitId),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-unit_owners-user_id")
                            .from(UnitOwners::Table, UnitOwners::UserId)
                            .to(Users::Table, Users::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-unit_owners-unit_id")
                            .from(UnitOwners::Table, UnitOwners::UnitId)
                            .to(Units::Table, Units::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .to_owned(),
            )
            .await?;

        // UserConfigurations Table
        manager
            .create_table(
                Table::create()
                    .table(UserConfigurations::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(UserConfigurations::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(UserConfigurations::UserId)
                            .integer()
                            .not_null()
                            .unique_key(),
                    )
                    .col(
                        ColumnDef::new(UserConfigurations::DefaultUnitId)
                            .integer()
                            .null(),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-user_configurations-user_id")
                            .from(UserConfigurations::Table, UserConfigurations::UserId)
                            .to(Users::Table, Users::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-user_configurations-default_unit_id")
                            .from(UserConfigurations::Table, UserConfigurations::DefaultUnitId)
                            .to(Units::Table, Units::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .to_owned(),
            )
            .await?;

        // Orchestrators Table
        manager
            .create_table(
                Table::create()
                    .table(Orchestrators::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(Orchestrators::Id)
                            .string()
                            .not_null()
                            .primary_key(),
                    )
                    .col(ColumnDef::new(Orchestrators::Address).string().not_null())
                    .col(ColumnDef::new(Orchestrators::Port).integer().not_null())
                    .col(
                        ColumnDef::new(Orchestrators::CreatedAt)
                            .date_time()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(Orchestrators::UpdatedAt)
                            .date_time()
                            .not_null(),
                    )
                    .to_owned(),
            )
            .await?;

        manager
            .create_table(
                Table::create()
                    .table(OrchestratorMetrics::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(OrchestratorMetrics::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::OrchestratorId)
                            .string()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::CpuUsage)
                            .float()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::MemoryUsage)
                            .double()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::TotalGames)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::ActiveGames)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::PendingGames)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::FailedGames)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::GamesLastHour)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::AvgGameDuration)
                            .double()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::ClusterUsedCpuCores)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::ClusterUsedMemoryGb)
                            .double()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::ClusterUsedGpus)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::ClusterAvailableCpuCores)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::ClusterAvailableMemoryGb)
                            .double()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::ClusterAvailableGpus)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::IsHealthy)
                            .boolean()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(OrchestratorMetrics::RecordedAt)
                            .date_time()
                            .not_null(),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-orchestrator_metrics-orchestrator_id")
                            .from(
                                OrchestratorMetrics::Table,
                                OrchestratorMetrics::OrchestratorId,
                            )
                            .to(Orchestrators::Table, Orchestrators::Id)
                            .on_delete(ForeignKeyAction::Cascade)
                            .on_update(ForeignKeyAction::Cascade),
                    )
                    .to_owned(),
            )
            .await?;

        // GameConfigurations Table
        manager
            .create_table(
                Table::create()
                    .table(GameConfigurations::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(GameConfigurations::GameId)
                            .integer()
                            .not_null()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(GameConfigurations::PodAddress)
                            .string()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameConfigurations::VPNAddress)
                            .string()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameConfigurations::WsPublicAddress)
                            .string()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameConfigurations::RestPublicAddress)
                            .string()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameConfigurations::StreamPublicAddress)
                            .string()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameConfigurations::PublicRestPort)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameConfigurations::PublicStreamPort)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameConfigurations::PublicWsPort)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameConfigurations::RestPort)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameConfigurations::StreamPort)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameConfigurations::WsPort)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameConfigurations::GdbPort)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameConfigurations::OrchestratorId)
                            .string()
                            .not_null(),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-game_configurations-game_id")
                            .from(GameConfigurations::Table, GameConfigurations::GameId)
                            .to(Games::Table, Games::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-game_configurations-orchestrator_id")
                            .from(
                                GameConfigurations::Table,
                                GameConfigurations::OrchestratorId,
                            )
                            .to(Orchestrators::Table, Orchestrators::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .to_owned(),
            )
            .await?;

        // GameEvents Table
        manager
            .create_table(
                Table::create()
                    .table(GameEvents::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(GameEvents::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(ColumnDef::new(GameEvents::GameId).integer().not_null())
                    .col(ColumnDef::new(GameEvents::EventType).integer().not_null())
                    .col(
                        ColumnDef::new(GameEvents::OccurredAt)
                            .date_time()
                            .not_null(),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-game_events-game_id")
                            .from(GameEvents::Table, GameEvents::GameId)
                            .to(Games::Table, Games::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .to_owned(),
            )
            .await?;

        // CaCertificates Table
        manager
            .create_table(
                Table::create()
                    .table(CaCertificates::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(CaCertificates::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(CaCertificates::SerialNumber)
                            .string_len(64)
                            .not_null()
                            .unique_key(),
                    )
                    .col(
                        ColumnDef::new(CaCertificates::Subject)
                            .string_len(1024)
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(CaCertificates::Issuer)
                            .string_len(1024)
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(CaCertificates::PublicKey)
                            .string_len(2048)
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(CaCertificates::ValidFrom)
                            .date_time()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(CaCertificates::ValidTo)
                            .date_time()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(CaCertificates::CertificateData)
                            .string_len(4096)
                            .not_null(),
                    )
                    .to_owned(),
            )
            .await?;

        // CaAuditLogs Table
        manager
            .create_table(
                Table::create()
                    .table(CaAuditLogs::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(CaAuditLogs::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(ColumnDef::new(CaAuditLogs::EventDate).date_time().null())
                    .col(ColumnDef::new(CaAuditLogs::EventType).string().not_null())
                    .col(ColumnDef::new(CaAuditLogs::CertificateId).integer().null())
                    .col(
                        ColumnDef::new(CaAuditLogs::Description)
                            .string_len(2048)
                            .not_null(),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-ca_audit_logs-certificate_id")
                            .from(CaAuditLogs::Table, CaAuditLogs::CertificateId)
                            .to(CaCertificates::Table, CaCertificates::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .to_owned(),
            )
            .await?;

        // CaRevocations Table
        manager
            .create_table(
                Table::create()
                    .table(CaRevocations::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(CaRevocations::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(CaRevocations::CertificateId)
                            .integer()
                            .null(),
                    )
                    .col(
                        ColumnDef::new(CaRevocations::RevocationPem)
                            .string_len(2048)
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(CaRevocations::RevocationDate)
                            .date_time()
                            .null(),
                    )
                    .col(ColumnDef::new(CaRevocations::Reason).string().not_null())
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-ca_revocations-certificate_id")
                            .from(CaRevocations::Table, CaRevocations::CertificateId)
                            .to(CaCertificates::Table, CaCertificates::Id)
                            .on_delete(ForeignKeyAction::Restrict)
                            .on_update(ForeignKeyAction::Restrict),
                    )
                    .to_owned(),
            )
            .await?;

        manager
            .create_table(
                Table::create()
                    .table(GamesHistory::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(GamesHistory::Id)
                            .string()
                            .not_null()
                            .primary_key(),
                    )
                    .col(ColumnDef::new(GamesHistory::Status).string().not_null())
                    .col(
                        ColumnDef::new(GamesHistory::CreatedAt)
                            .timestamp()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GamesHistory::UpdatedAt)
                            .timestamp()
                            .not_null(),
                    )
                    .to_owned(),
            )
            .await?;

        manager
            .create_table(
                Table::create()
                    .table(GameParticipantsHistory::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(GameParticipantsHistory::UnitId)
                            .integer()
                            .not_null()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(GameParticipantsHistory::GameId)
                            .string()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameParticipantsHistory::Health)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameParticipantsHistory::Ammo)
                            .integer()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameParticipantsHistory::PositionX)
                            .float()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameParticipantsHistory::PositionY)
                            .float()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameParticipantsHistory::PositionZ)
                            .float()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameParticipantsHistory::OrientationX)
                            .float()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameParticipantsHistory::OrientationY)
                            .float()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameParticipantsHistory::OrientationZ)
                            .float()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GameParticipantsHistory::UpdatedAt)
                            .timestamp()
                            .not_null(),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-player-game")
                            .from(
                                GameParticipantsHistory::Table,
                                GameParticipantsHistory::GameId,
                            )
                            .to(GamesHistory::Table, GamesHistory::Id)
                            .on_delete(ForeignKeyAction::Cascade)
                            .on_update(ForeignKeyAction::Cascade),
                    )
                    .to_owned(),
            )
            .await?;

        manager
            .create_table(
                Table::create()
                    .table(GamesStateHistory::Table)
                    .if_not_exists()
                    .col(
                        ColumnDef::new(GamesStateHistory::Id)
                            .integer()
                            .not_null()
                            .auto_increment()
                            .primary_key(),
                    )
                    .col(
                        ColumnDef::new(GamesStateHistory::GameId)
                            .string()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GamesStateHistory::EditType)
                            .string()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GamesStateHistory::EditData)
                            .json()
                            .not_null(),
                    )
                    .col(
                        ColumnDef::new(GamesStateHistory::CreatedAt)
                            .timestamp()
                            .not_null(),
                    )
                    .foreign_key(
                        ForeignKey::create()
                            .name("fk-edit-game")
                            .from(GamesStateHistory::Table, GamesStateHistory::GameId)
                            .to(GamesHistory::Table, GamesHistory::Id)
                            .on_delete(ForeignKeyAction::Cascade)
                            .on_update(ForeignKeyAction::Cascade),
                    )
                    .to_owned(),
            )
            .await?;

        Ok(())
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        // Drop tables in reverse order of creation
        manager
            .drop_table(Table::drop().table(CaRevocations::Table).to_owned())
            .await
            .ok();
        manager
            .drop_table(Table::drop().table(CaAuditLogs::Table).to_owned())
            .await
            .ok();
        manager
            .drop_table(Table::drop().table(CaCertificates::Table).to_owned())
            .await
            .ok();
        manager
            .drop_table(Table::drop().table(GameEvents::Table).to_owned())
            .await
            .ok();
        manager
            .drop_table(Table::drop().table(GameConfigurations::Table).to_owned())
            .await
            .ok();
        manager
            .drop_table(Table::drop().table(OrchestratorMetrics::Table).to_owned())
            .await?;
        manager
            .drop_table(Table::drop().table(Orchestrators::Table).to_owned())
            .await?;
        manager
            .drop_table(Table::drop().table(UserConfigurations::Table).to_owned())
            .await?;
        manager
            .drop_table(Table::drop().table(UnitOwners::Table).to_owned())
            .await?;
        manager
            .drop_table(Table::drop().table(UnitComponents::Table).to_owned())
            .await?;
        manager
            .drop_table(Table::drop().table(UserComponents::Table).to_owned())
            .await?;
        manager
            .drop_table(Table::drop().table(Components::Table).to_owned())
            .await?;
        manager
            .drop_table(Table::drop().table(ComponentTypes::Table).to_owned())
            .await?;
        manager
            .drop_table(
                Table::drop()
                    .table(ComponentTypeCapabilities::Table)
                    .to_owned(),
            )
            .await?;
        manager
            .drop_table(Table::drop().table(ComponentCapabilities::Table).to_owned())
            .await?;
        manager
            .drop_table(Table::drop().table(GameParticipants::Table).to_owned())
            .await?;
        manager
            .drop_table(Table::drop().table(Games::Table).to_owned())
            .await?;
        manager
            .drop_table(Table::drop().table(Units::Table).to_owned())
            .await?;
        manager
            .drop_table(Table::drop().table(Users::Table).to_owned())
            .await?;
        manager
            .drop_table(Table::drop().table(GamesStateHistory::Table).to_owned())
            .await?;
        manager
            .drop_table(
                Table::drop()
                    .table(GameParticipantsHistory::Table)
                    .to_owned(),
            )
            .await?;
        manager
            .drop_table(Table::drop().table(GamesHistory::Table).to_owned())
            .await?;

        Ok(())
    }
}

#[derive(Iden)]
enum Components {
    Table,
    Id,
    SerialNumber,
    ComponentTypeId,
}

#[derive(Iden)]
pub(crate) enum Users {
    Table,
    Id,
    Auth0Id,
    Name,
    Avatar,
}

#[derive(Iden)]
enum Units {
    Table,
    Id,
    Uuid,
    Name,
    CreatedAt,
    UpdatedAt,
}

#[derive(Iden)]
pub enum Games {
    Table,
    Id,
    Uid,
    MaxPlayers,
    Duration,
    Latitude,
    Longitude,
    MinRadius,
    StartRadius,
    PersistReboot,
    Status,
    OwnerId,
    CreatedAt,
    UpdatedAt,
}

#[derive(Iden)]
enum GameParticipants {
    Table,
    Id,
    State,
    GameId,
    UserId,
    UnitId,
    StreamId,
    CreatedAt,
    UpdatedAt,
    AccessToken,
}

#[derive(Iden)]
enum ComponentTypes {
    Table,
    Id,
    Name,
    Description,
    Battery,
    Scope,
    Recoil,
    RateOfFire,
    ModelUrl,
}
#[derive(Iden)]
enum ComponentCapabilities {
    Table,
    Id,
    Name,
}

#[derive(Iden)]
enum ComponentTypeCapabilities {
    Table,
    Id,
    CapabilityId,
    ComponentTypeId,
}

#[derive(Iden)]
enum UnitComponents {
    Table,
    Id,
    UnitId,
    ComponentId,
}

#[derive(Iden)]
enum UserComponents {
    Table,
    Id,
    UserId,
    ComponentId,
}

#[derive(Iden)]
enum UnitOwners {
    Table,
    UserId,
    UnitId,
    CreatedAt,
    UpdatedAt,
}

#[derive(Iden)]
enum UserConfigurations {
    Table,
    Id,
    UserId,
    DefaultUnitId,
}

#[derive(Iden)]
enum Orchestrators {
    Table,
    Id,
    Address,
    Port,
    CreatedAt,
    UpdatedAt,
}

#[derive(Iden)]
enum GameConfigurations {
    Table,
    GameId,
    PodAddress,
    VPNAddress,
    WsPublicAddress,
    RestPublicAddress,
    StreamPublicAddress,
    PublicRestPort,
    PublicStreamPort,
    PublicWsPort,
    RestPort,
    StreamPort,
    WsPort,
    GdbPort,
    OrchestratorId,
}

#[derive(Iden)]
enum GameEvents {
    Table,
    Id,
    GameId,
    EventType,
    OccurredAt,
}

#[derive(Iden)]
enum CaCertificates {
    Table,
    Id,
    SerialNumber,
    Subject,
    Issuer,
    PublicKey,
    ValidFrom,
    ValidTo,
    CertificateData,
}

#[derive(Iden)]
enum CaAuditLogs {
    Table,
    Id,
    EventDate,
    EventType,
    CertificateId,
    Description,
}

#[derive(Iden)]
enum CaRevocations {
    Table,
    Id,
    CertificateId,
    RevocationPem,
    RevocationDate,
    Reason,
}

#[derive(Iden)]
enum GamesHistory {
    Table,
    Id,
    Status,
    CreatedAt,
    UpdatedAt,
}

#[derive(Iden)]
enum GameParticipantsHistory {
    Table,
    UnitId,
    GameId,
    Health,
    Ammo,
    PositionX,
    PositionY,
    PositionZ,
    OrientationX,
    OrientationY,
    OrientationZ,
    UpdatedAt,
}

#[derive(Iden)]
enum GamesStateHistory {
    Table,
    Id,
    GameId,
    EditType,
    EditData,
    CreatedAt,
}

#[derive(Iden)]
enum OrchestratorMetrics {
    Table,
    Id,
    OrchestratorId,
    CpuUsage,
    MemoryUsage,
    TotalGames,
    ActiveGames,
    PendingGames,
    FailedGames,
    GamesLastHour,
    AvgGameDuration,
    ClusterUsedCpuCores,
    ClusterUsedMemoryGb,
    ClusterUsedGpus,
    ClusterAvailableCpuCores,
    ClusterAvailableMemoryGb,
    ClusterAvailableGpus,
    IsHealthy,
    RecordedAt,
}
