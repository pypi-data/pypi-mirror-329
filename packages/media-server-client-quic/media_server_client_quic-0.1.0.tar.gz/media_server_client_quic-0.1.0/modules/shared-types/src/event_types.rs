use serde::{Deserialize, Serialize};

use crate::UnitId;

type BulletCount = i32;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum PlayerEvent {
    Shoot,
    ReloadStarted,
    Gyroscope,
    Accelerometer,
    GpsPosition,
    ShootNeedReload,
    ReloadDone(BulletCount),
    ShotHit(UnitId),
    ShotMiss,
}
