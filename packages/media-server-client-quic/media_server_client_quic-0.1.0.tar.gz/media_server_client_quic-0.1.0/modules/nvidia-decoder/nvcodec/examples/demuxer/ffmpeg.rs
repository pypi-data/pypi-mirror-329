use ffmpeg_next::codec::Id as CodecId;
use futures::{task::AtomicWaker, Stream};
use protobuf_types::H264Message;
use std::collections::HashMap;
use std::io::Read;
use std::path::Path;
use std::pin::Pin;
use std::process::{Command, Stdio};
use std::sync::{
    mpsc::{self, Receiver},
    Arc,
};
use std::task::{Context, Poll};
use std::thread;

pub struct Packet {
    pub data: Vec<u8>,
    pub is_keyframe: bool,
}

impl From<&Packet> for H264Message {
    fn from(packet: &Packet) -> Self {
        H264Message {
            data: packet.data.clone(),
            timestamp: 0, // You might want to get this from ffmpeg
            frame_type: if packet.is_keyframe { 1 } else { 2 }, // 1 for I-Frame, 2 for P-Frame
            metadata: HashMap::new(),
            width: None,  // Could be added from ffprobe
            height: None, // Could be added from ffprobe
        }
    }
}

pub struct FFmpegDemuxStream {
    pub codec_id: CodecId,
    pub total_frames: i64,
    waker: Arc<AtomicWaker>,
    rx: Receiver<Result<Packet, std::io::Error>>,
}

impl FFmpegDemuxStream {
    pub fn new<P: AsRef<Path>>(path: &P) -> Result<Self, std::io::Error> {
        let path_str = path.as_ref().to_string_lossy();

        // Get video info using ffprobe
        let probe = Command::new("ffprobe")
            .args([
                "-v",
                "error",
                "-select_streams",
                "v:0",
                "-show_entries",
                "stream=codec_name,nb_frames",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                path_str.as_ref(),
            ])
            .output()?;

        let info = String::from_utf8_lossy(&probe.stdout);
        let mut lines = info.lines();
        let codec_name = lines.next().unwrap_or("h264").trim();
        let total_frames = lines
            .next()
            .and_then(|f| f.parse::<i64>().ok())
            .unwrap_or(0);

        let codec_id = match codec_name {
            "h264" => CodecId::H264,
            "hevc" => CodecId::HEVC,
            _ => CodecId::H264,
        };

        let waker = Arc::new(AtomicWaker::new());
        let (tx, rx) = mpsc::sync_channel(8);

        // Start ffmpeg process with frame type info
        let mut child = Command::new("ffmpeg")
            .args([
                "-i",
                path_str.as_ref(),
                "-c:v",
                "copy",
                "-bsf:v",
                "h264_mp4toannexb", // Add bitstream filter
                "-f",
                "h264",
                "-",
            ])
            .stdout(Stdio::piped())
            .stderr(Stdio::null())
            .spawn()?;

        let mut stdout = child.stdout.take().unwrap();
        let waker_clone = waker.clone();

        thread::spawn(move || {
            let mut buffer = vec![0u8; 65536];
            let mut nal_buffer = Vec::new();

            loop {
                match stdout.read(&mut buffer) {
                    Ok(n) if n > 0 => {
                        // Look for NAL unit markers (0x00000001)
                        let mut i = 0;
                        while i < n {
                            if i + 4 <= n
                                && buffer[i] == 0
                                && buffer[i + 1] == 0
                                && buffer[i + 2] == 0
                                && buffer[i + 3] == 1
                            {
                                // Found a NAL unit
                                if !nal_buffer.is_empty() {
                                    let is_keyframe =
                                        !nal_buffer.is_empty() && (nal_buffer[4] & 0x1F) == 5; // IDR frame
                                    let packet = Packet {
                                        data: nal_buffer.clone(),
                                        is_keyframe,
                                    };
                                    if tx.send(Ok(packet)).is_err() {
                                        return;
                                    }
                                    waker_clone.wake();
                                }
                                nal_buffer.clear();
                            }
                            nal_buffer.push(buffer[i]);
                            i += 1;
                        }
                    }
                    Ok(0) => break, // EOF
                    Err(e) => {
                        let _ = tx.send(Err(e));
                        waker_clone.wake();
                        break;
                    }
                    _ => {}
                }
            }

            // Send final NAL unit if any
            if !nal_buffer.is_empty() {
                let is_keyframe = !nal_buffer.is_empty() && (nal_buffer[4] & 0x1F) == 5;
                let packet = Packet {
                    data: nal_buffer,
                    is_keyframe,
                };
                let _ = tx.send(Ok(packet));
                waker_clone.wake();
            }
        });

        Ok(Self {
            codec_id,
            total_frames,
            waker,
            rx,
        })
    }
}

impl Stream for FFmpegDemuxStream {
    type Item = Result<Packet, std::io::Error>;

    fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<Self::Item>> {
        self.waker.register(cx.waker());

        match self.rx.try_recv() {
            Ok(v) => Poll::Ready(Some(v)),
            Err(mpsc::TryRecvError::Empty) => Poll::Pending,
            Err(mpsc::TryRecvError::Disconnected) => Poll::Ready(None),
        }
    }
}
