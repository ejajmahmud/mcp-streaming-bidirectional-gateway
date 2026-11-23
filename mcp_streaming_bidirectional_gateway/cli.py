"""CLI for MCP Streaming Bidirectional Gateway."""
import argparse
from .core import MCPStreamingGateway

def main():
    parser = argparse.ArgumentParser(description="MCP Streaming Bidirectional Gateway CLI")
    parser.add_argument("--demo", action="store_true", help="Run streaming gateway demo")
    args = parser.parse_args()

    gw = MCPStreamingGateway()
    stream_id = "call-1049"
    gw.open_stream(stream_id)

    gw.send_progress(stream_id, 25.0, "Parsing repository...")
    gw.send_chunk(stream_id, "Found 12 source files.")
    gw.send_progress(stream_id, 75.0, "Synthesizing documentation...")
    gw.send_chunk(stream_id, "Documentation generated successfully.")
    gw.complete(stream_id)

    ch = gw.channels[stream_id]
    print(f"Stream {stream_id} finished with {len(ch.frames)} frames:")
    for f in ch.frames:
        print(f"  Seq {f.seq}: [{f.frame_type.upper()}] {f.payload}")

if __name__ == "__main__":
    main()
