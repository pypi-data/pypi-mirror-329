#!/usr/bin/env python3
"""
Example script demonstrating how to use the media streaming module.
This example creates a streaming client that connects to a server and streams H264 video data.
"""

import os
import sys
import signal
import logging
import argparse
import tempfile
import requests
from time import sleep, time
from typing import Optional
from fractions import Fraction
from contextlib import contextmanager
from tqdm import tqdm

try:
    from media_streaming import MediaStreamingPy
except ImportError:
    print("Error: media_streaming module not found. Make sure to build the Rust library first.")
    print("Run: cargo build --release")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Default video URL and local path
VIDEO_URL = "https://www.dropbox.com/scl/fi/8b7hpxpv71lgj3ik6f2e4/Seg-Vid-Made-With-Clipchamp.mp4?rlkey=lxwrmcxhif0y0h6xoucehd132&st=lx38jn76&dl=1"
TEMP_DIR = tempfile.gettempdir()
VIDEO_PATH = os.path.join(TEMP_DIR, "demo.mp4")

def download_video(url: str = VIDEO_URL, path: str = VIDEO_PATH) -> str:
    """
    Download a video file with progress bar.
    
    Args:
        url: URL to download from
        path: Local path to save to
        
    Returns:
        str: Path to the downloaded file
    """
    if os.path.exists(path):
        logger.info(f"Video already exists at {path}")
        return path

    logger.info(f"Downloading video to {path}")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    with open(path, 'wb') as file, tqdm(
        desc="Downloading",
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            pbar.update(size)

    return path

class StreamingClient:
    """Wrapper class for MediaStreamingPy with proper resource management."""
    
    def __init__(self):
        self.client = MediaStreamingPy()
        self._running = False
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown."""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        self.stop()

    def start(self, host: str, port: int) -> bool:
        """
        Start the streaming client.
        
        Args:
            host: Server hostname or IP address
            port: Server port number
            
        Returns:
            bool: True if connection was successful, False otherwise
        """
        try:
            logger.info(f"Connecting to {host}:{port}")
            self.client.connect(host, port)
            self._running = True
            return True
        except Exception as e:
            logger.error(f"Failed to start streaming client: {e}")
            return False

    def stop(self):
        """Stop the streaming client."""
        if self._running:
            try:
                logger.info("Disconnecting streaming client")
                self.client.disconnect()
            except Exception as e:
                logger.error(f"Error during disconnect: {e}")
            finally:
                self._running = False

    def is_running(self) -> bool:
        """Check if the client is running."""
        try:
            return self.client.is_running()
        except Exception:
            return False

    def get_frame_count(self) -> Optional[int]:
        """Get the current frame count."""
        try:
            return self.client.frame_count()
        except Exception as e:
            logger.error(f"Failed to get frame count: {e}")
            return None

    def send_h264_frame(self, frame_data: bytes, is_keyframe: bool, width: int = 1920, height: int = 1080) -> bool:
        """Send an H264 encoded frame."""
        try:
            success = self.client.add_frame(
                frame_data,
                timestamp=None,  # Use automatic timestamp
                width=width,
                height=height,
                is_keyframe=is_keyframe
            )
            
            return success
        except Exception as e:
            logger.error(f"Error sending frame: {e}")
            
            return False
        
       

    @contextmanager
    def connect(self, host: str, port: int):
        """Context manager for connecting to the server."""
        try:
            if self.start(host, port):
                yield self
            else:
                raise RuntimeError("Failed to connect to server")
        finally:
            self.stop()

def stream_from_video(client: StreamingClient, video_path: str, fps: float = 30.0):
    """Stream H264 frames from a video file at the specified FPS."""
    import av
    frame_interval = 1.0 / fps
    frame_num = 0
    next_frame_time = time()

    try:
        # Open the video file with specific options for H264
        container = av.open(video_path, options={
            'codec': 'h264',
            'extract_extradata': 'true',  # Get SPS/PPS data
        })
        
        stream = container.streams.video[0]
        codec_context = stream.codec_context
        
        # Create H264 encoder with optimal settings
        encoder = av.CodecContext.create('libx264', 'w')
        encoder.width = codec_context.width
        encoder.height = codec_context.height
        encoder.pix_fmt = 'yuv420p'
        encoder.time_base = Fraction(1, 90000)  # 90kHz clock rate
        encoder.framerate = Fraction(int(fps), 1)
        
        # Configure for low latency
        encoder.options = {
            'preset': 'ultrafast',
            'tune': 'zerolatency',
            'crf': '18',
            'repeat-headers': '1'
        }

        logger.info(f"Streaming video: {video_path}")
        logger.info(f"Resolution: {codec_context.width}x{codec_context.height}")
        logger.info(f"Codec: {codec_context.name}")
        logger.info(f"Target FPS: {fps}")
        
        # Get codec extradata (SPS/PPS) and send it first if available
        extradata = codec_context.extradata
        if extradata:
            logger.info("Sending codec configuration data")
            client.send_h264_frame(extradata, True, codec_context.width, codec_context.height)

        # Stream each packet
        for frame in container.decode(video=0):
            if not client.is_running():
                break

            # Reset frame timing info
            frame.pts = None
            frame.time_base = encoder.time_base

            # Re-encode frame to ensure proper H264 format
            packages = encoder.encode(frame)
            for package in packages:
                # Get bytes directly from the package

                packet_view = memoryview(package)
                if client.send_h264_frame(packet_view, package.is_keyframe, 
                                        codec_context.width, codec_context.height):
                    frame_num += 1
                    if frame_num % int(fps) == 0:
                        logger.info(f"Sent {frame_num} frames")
                else:
                    logger.warning("Failed to send frame")

            # FPS control
            next_frame_time += frame_interval
            sleep_time = next_frame_time - time()
            if sleep_time > 0:
                sleep(sleep_time)

        # Flush encoder
        packages = encoder.encode(None)
        for package in packages:
            packet_bytes = memoryview(package)
            client.send_h264_frame(packet_bytes, package.is_keyframe, codec_context.width, codec_context.height)

    except KeyboardInterrupt:
        logger.info("Streaming stopped by user")
    except Exception as e:
        logger.error(f"Error streaming video: {e}")
        logger.error(f"Full error: {str(e)}")
        # Print more detailed exception info
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
    finally:
        container.close()

def main():
    parser = argparse.ArgumentParser(description="Media Streaming Example Client")
    parser.add_argument("--video", help="Path to H264 encoded video file or URL")
    parser.add_argument("--host", default="127.0.0.1", help="Server hostname or IP address")
    parser.add_argument("--port", type=int, default=25502, help="Server port number")
    parser.add_argument("--fps", type=float, default=30.0, help="Target frames per second")
    args = parser.parse_args()

    # Handle video source
    video_path = args.video if args.video else VIDEO_PATH
    if video_path.startswith(('http://', 'https://')):
        video_path = download_video(video_path)
    elif not args.video:
        video_path = download_video()  # Use default video

    # Create and run the streaming client
    client = StreamingClient()
    
    try:
        with client.connect(args.host, args.port) as stream:
            logger.info("Stream started successfully")
            stream_from_video(stream, video_path, args.fps)
    except Exception as e:
        logger.error(f"Streaming error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 