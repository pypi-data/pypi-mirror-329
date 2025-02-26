use protobuf_types::newbringer::H264Message;

#[derive(Debug)]
pub struct InputVideoFrame {
    pub data: H264Message,
    pub stream_id: u64,
}
