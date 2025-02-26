#[derive(Debug)]
pub struct ReloadState {
    pub in_progress: bool,  // True when actively reloading
    pub locked: bool,       // True when ready to fire
    pub needs_reload: bool, // True when reload is required
}

impl Default for ReloadState {
    fn default() -> Self {
        Self {
            in_progress: false,
            locked: true,        // Start locked (ready to fire)
            needs_reload: false, // Start not needing reload
        }
    }
}

impl ReloadState {
    pub fn new() -> Self {
        Self {
            in_progress: false,
            locked: true,        // Start locked (ready to fire)
            needs_reload: false, // Start not needing reload
        }
    }

    pub fn start_reload(&mut self) {
        self.in_progress = true;
        self.locked = false;
    }

    pub fn complete_reload(&mut self, _rounds: u32) {
        self.in_progress = false;
        self.locked = true;
        self.needs_reload = false;
    }

    pub fn mark_needs_reload(&mut self) {
        self.needs_reload = true;
        self.locked = false;
    }
}
