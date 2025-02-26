# Media Streaming

Python bindings for the media streaming server that handles H264 video streaming over QUIC.

## Prerequisites

- Python 3.7 or higher
- Rust toolchain (cargo, rustc)
- NVIDIA drivers (for hardware decoding)
- maturin (for building Python package)

## Installation

1. Install maturin (Python package builder for Rust):
```bash
pip install maturin
```

2. Build and install the package:
```bash
# From the media-streaming directory
maturin develop
```

For development with hot-reload:
```bash
maturin develop --release
```

## Usage

Here's a simple example of how to use the media streaming server:

```python
import time
from media_streaming import MediaStreamingPy

# Create a new media streaming instance
streaming = MediaStreamingPy()

# Start the server
streaming.start("127.0.0.1", 12345)

try:
    # Send H264 encoded frames
    frame_data = get_h264_frame()  # Your frame source
    streaming.add_frame(frame_data)
    
finally:
    # Clean shutdown
    streaming.shutdown()
```

See the `examples` directory for more detailed examples.

## API Reference

### MediaStreamingPy

#### `start(bind_address: str, port: int)`
Starts the media streaming server on the specified address and port.

#### `add_frame(frame_data: bytes)`
Adds an H264 encoded frame to be streamed. The frame should be a complete H264 NAL unit.

#### `shutdown()`
Gracefully shuts down the streaming server.

## Development

To run the example:
```bash
python examples/stream_example.py
``` 