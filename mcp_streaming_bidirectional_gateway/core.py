"""Core MCP Streaming Bidirectional Gateway implementation."""
import time
from typing import Dict, List, Optional, Any

class FrameType:
    CHUNK = "chunk"
    PROGRESS = "progress"
    INTERRUPT = "interrupt"
    COMPLETE = "complete"
    ERROR = "error"

class StreamFrame:
    def __init__(self, stream_id: str, frame_type: str, payload: Any, seq: int):
        self.stream_id = stream_id
        self.frame_type = frame_type
        self.payload = payload
        self.seq = seq
        self.timestamp = time.time()

class StreamChannel:
    def __init__(self, stream_id: str):
        self.stream_id = stream_id
        self.frames: List[StreamFrame] = []
        self.interrupted = False
        self.completed = False
        self.seq_counter = 0

    def push(self, frame_type: str, payload: Any) -> StreamFrame:
        if self.completed and frame_type != FrameType.COMPLETE:
            raise RuntimeError("Cannot push frames to completed stream")
        self.seq_counter += 1
        frame = StreamFrame(self.stream_id, frame_type, payload, self.seq_counter)
        self.frames.append(frame)
        return frame

class MCPStreamingGateway:
    def __init__(self):
        self.channels: Dict[str, StreamChannel] = {}

    def open_stream(self, stream_id: str) -> StreamChannel:
        if stream_id in self.channels:
            raise KeyError(f"Stream {stream_id} already exists")
        ch = StreamChannel(stream_id)
        self.channels[stream_id] = ch
        return ch

    def send_chunk(self, stream_id: str, chunk: str) -> StreamFrame:
        ch = self._get_channel(stream_id)
        if ch.interrupted:
            raise InterruptedError(f"Stream {stream_id} was interrupted")
        return ch.push(FrameType.CHUNK, chunk)

    def send_progress(self, stream_id: str, percentage: float, message: str) -> StreamFrame:
        ch = self._get_channel(stream_id)
        return ch.push(FrameType.PROGRESS, {"percent": percentage, "message": message})

    def interrupt(self, stream_id: str, reason: str = "User requested cancellation") -> StreamFrame:
        ch = self._get_channel(stream_id)
        ch.interrupted = True
        return ch.push(FrameType.INTERRUPT, {"reason": reason})

    def complete(self, stream_id: str) -> StreamFrame:
        ch = self._get_channel(stream_id)
        ch.completed = True
        return ch.push(FrameType.COMPLETE, {"status": "ok"})

    def _get_channel(self, stream_id: str) -> StreamChannel:
        if stream_id not in self.channels:
            raise KeyError(f"Stream {stream_id} not found")
        return self.channels[stream_id]
