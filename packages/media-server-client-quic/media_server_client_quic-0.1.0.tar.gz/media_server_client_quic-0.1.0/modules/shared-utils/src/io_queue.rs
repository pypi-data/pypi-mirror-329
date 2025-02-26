use anyhow::{anyhow, Result};
use crossbeam_queue::ArrayQueue;
use log::{error, warn};
use std::sync::Arc;
use tokio::sync::Notify;

pub trait QueueItem: Send + Sync {}

pub struct IOQueue<I: QueueItem, O: QueueItem = I> {
    input_queue: Arc<ArrayQueue<I>>,
    output_queue: Arc<ArrayQueue<O>>,
    input_notify: Arc<Notify>,
    output_notify: Arc<Notify>,
}

impl<I: QueueItem, O: QueueItem> IOQueue<I, O> {
    pub fn new(input_capacity: usize, output_capacity: usize) -> Self {
        Self {
            input_queue: Arc::new(ArrayQueue::new(input_capacity)),
            output_queue: Arc::new(ArrayQueue::new(output_capacity)),
            input_notify: Arc::new(Notify::new()),
            output_notify: Arc::new(Notify::new()),
        }
    }

    pub fn push_input(&self, item: I) -> Result<()> {
        match self.input_queue.push(item) {
            Ok(()) => {
                self.input_notify.notify_one();
                Ok(())
            }
            Err(rejected_item) => {
                warn!("Input Queue Full, popping oldest item");
                self.input_queue.pop();
                self.input_queue
                    .push(rejected_item)
                    .map(|_| self.input_notify.notify_one())
                    .map_err(|_| {
                        error!("Input Queue is still full after cleanup");
                        anyhow!("Input Queue is still full after cleanup")
                    })
            }
        }
    }

    pub fn pop_input(&self) -> Option<I> {
        self.input_queue.pop()
    }

    pub fn push_output(&self, item: O) -> Result<()> {
        match self.output_queue.push(item) {
            Ok(()) => {
                self.output_notify.notify_one();
                Ok(())
            }
            Err(rejected_item) => {
                warn!("Output Queue Full, popping oldest item");
                self.output_queue.pop();
                self.output_queue
                    .push(rejected_item)
                    .map(|_| self.output_notify.notify_one())
                    .map_err(|_| {
                        error!("Output Queue is still full after cleanup");
                        anyhow!("Output Queue is still full after cleanup")
                    })
            }
        }
    }

    pub fn pop_output(&self) -> Option<O> {
        self.output_queue.pop()
    }

    pub async fn pop_input_async(&self) -> I {
        loop {
            if let Some(item) = self.pop_input() {
                return item;
            }
            self.input_notify.notified().await;
        }
    }

    pub async fn pop_output_async(&self) -> O {
        loop {
            if let Some(item) = self.pop_output() {
                return item;
            }
            self.output_notify.notified().await;
        }
    }

    pub fn process_all<F>(&self, mut processor: F) -> Result<()>
    where
        F: FnMut(I) -> Result<O>,
    {
        while let Some(item) = self.pop_input() {
            let output = processor(item)?;
            self.push_output(output)?;
        }
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[derive(Debug)]
    struct InputItem {
        value: i32,
    }

    impl QueueItem for InputItem {}

    #[derive(Debug)]
    struct OutputItem {
        processed_value: String,
    }

    impl QueueItem for OutputItem {}

    #[tokio::test]
    async fn test_generic_queue() {
        let queue: IOQueue<InputItem, OutputItem> = IOQueue::new(10, 10);
        let item1 = InputItem { value: 1 };
        let item2 = InputItem { value: 2 };

        queue.push_input(item1).unwrap();
        queue.push_input(item2).unwrap();

        queue
            .process_all(|input| {
                Ok(OutputItem {
                    processed_value: format!("Processed: {}", input.value),
                })
            })
            .unwrap();

        assert_eq!(queue.pop_output().unwrap().processed_value, "Processed: 1");
        assert_eq!(queue.pop_output().unwrap().processed_value, "Processed: 2");
        assert!(queue.pop_output().is_none());
    }

    #[tokio::test]
    async fn test_async_pop() {
        let queue: IOQueue<InputItem, OutputItem> = IOQueue::new(10, 10);

        // Spawn a task that will push an item after a delay
        let queue_clone = Arc::new(queue);
        let push_queue = queue_clone.clone();

        tokio::spawn(async move {
            tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
            push_queue.push_input(InputItem { value: 42 }).unwrap();
        });

        // This should wait until the item is pushed
        let item = queue_clone.pop_input_async().await;
        assert_eq!(item.value, 42);
    }
}
