"""
01_websockets/client.py
───────────────────────
Async WebSocket client — connects to /ws/metrics and prints metrics for N seconds.

Run the server first:
    uvicorn server:app --reload --port 8000

Then:
    python client.py
"""

import asyncio
import json

import websockets


async def stream_metrics(uri: str = "ws://localhost:8000/ws/metrics", duration: int = 10):
    print(f"Connecting to {uri} …")
    async with websockets.connect(uri) as ws:
        print(f"Connected. Receiving metrics for {duration}s  (Ctrl-C to stop early)\n")
        deadline = asyncio.get_event_loop().time() + duration
        while asyncio.get_event_loop().time() < deadline:
            raw = await ws.recv()
            data = json.loads(raw)
            print(
                f"CPU: {data['cpu_percent']:5.1f}%  "
                f"RAM: {data['memory_percent']:5.1f}% ({data.get('memory_used_gb', '?')} GB)  "
                f"Disk: {data.get('disk_percent', '?'):5.1f}%"
            )


if __name__ == "__main__":
    asyncio.run(stream_metrics())
