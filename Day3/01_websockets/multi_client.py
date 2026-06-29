"""
01_websockets/multi_client.py
──────────────────────────────
Spawns N concurrent WebSocket clients against /ws/broadcast.
Each client runs for `duration` seconds and prints its own line.

Demonstrates that the server handles many simultaneous connections.

Run the server first:
    uvicorn server:app --reload --port 8000

Then:
    python multi_client.py              # 5 clients, 10 seconds
    python multi_client.py --clients 10 --duration 20
"""

import argparse
import asyncio
import json

import websockets


async def single_client(client_id: int, uri: str, duration: int):
    """One client: connects, receives frames until timeout, then exits."""
    try:
        async with websockets.connect(uri) as ws:
            deadline = asyncio.get_event_loop().time() + duration
            frames = 0
            while asyncio.get_event_loop().time() < deadline:
                raw = await ws.recv()
                data = json.loads(raw)
                frames += 1
                # Print only every 3 frames to avoid flooding the terminal
                if frames % 3 == 1:
                    print(
                        f"[Client {client_id:02d}] "
                        f"CPU {data['cpu_percent']:5.1f}%  "
                        f"RAM {data['memory_percent']:5.1f}%  "
                        f"clients={data.get('clients', '?')}"
                    )
    except Exception as e:
        print(f"[Client {client_id:02d}] Error: {e}")


async def main(n_clients: int, duration: int, uri: str):
    print(f"Launching {n_clients} clients → {uri}  ({duration}s)\n")
    tasks = [
        asyncio.create_task(single_client(i + 1, uri, duration))
        for i in range(n_clients)
    ]
    await asyncio.gather(*tasks)
    print(f"\nAll {n_clients} clients finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--clients", type=int, default=5, help="Number of concurrent clients")
    parser.add_argument("--duration", type=int, default=10, help="Duration in seconds")
    parser.add_argument("--uri", default="ws://localhost:8000/ws/broadcast")
    args = parser.parse_args()

    asyncio.run(main(args.clients, args.duration, args.uri))
