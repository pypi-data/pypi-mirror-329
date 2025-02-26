#[derive(Debug)]
pub struct CycleState {
    pub in_progress: bool,
    pub locked: bool,
    pub needs_cycling: bool,
    pub auto_reload: bool, // If true, cycling will also trigger a reload
}

impl Default for CycleState {
    fn default() -> Self {
        Self {
            in_progress: false,
            locked: true,
            needs_cycling: false,
            auto_reload: true, // Default to true for hardware compatibility
        }
    }
}

impl CycleState {
    pub fn start_cycle(&mut self) {
        self.in_progress = true;
        self.locked = false;
    }

    pub fn complete_cycle(&mut self) {
        self.in_progress = false;
        self.locked = true;
        self.needs_cycling = false;
    }

    pub fn mark_needs_cycling(&mut self) {
        self.needs_cycling = true;
        self.locked = false;
    }
}
