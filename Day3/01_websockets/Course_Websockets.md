# Day 3 —  WebSockets — Streaming Live Data

REST endpoints follow a request-response cycle: the client asks, the server answers, connection closes. This is fine for CRUD operations but terrible for live data — you'd have to poll every second and waste bandwidth on empty responses.

**WebSockets** open a persistent, bidirectional channel. The server can push data to the client at any time without a new request. This is exactly what we need for a live metrics dashboard.

```
Client                          Server
  │──── HTTP Upgrade ──────────▶│
  │◀─── 101 Switching Protocols ─│
  │                              │  (connection stays open)
  │◀─── {"cpu": 45.2} ───────────│  (server pushes every 1s)
  │◀─── {"cpu": 47.8} ───────────│
  │◀─── {"cpu": 43.1} ───────────│
  │──── close ──────────────────▶│
```

#### Basic WebSocket Endpoint

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import json
import psutil

app = FastAPI()


@app.websocket("/ws/metrics")
async def metrics_stream(websocket: WebSocket):
    await websocket.accept()   # complete the handshake
    try:
        while True:
            payload = {
                "cpu_percent": psutil.cpu_percent(interval=None),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage("/").percent,
            }
            await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass   # client closed the tab — this is normal, not an error
```

#### Testing a WebSocket

**Option 1 — Swagger UI:** FastAPI's `/docs` does not support WebSocket testing. Use a dedicated tool.

**Option 2 — Python script:**

```python
import asyncio
import json
import websockets   # pip install websockets

async def watch():
    async with websockets.connect("ws://localhost:8000/ws/metrics") as ws:
        for _ in range(5):   # receive 5 frames
            data = json.loads(await ws.recv())
            print(f"CPU: {data['cpu_percent']}%  MEM: {data['memory_percent']}%")

asyncio.run(watch())
```

**Option 3 — Browser console:**

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/metrics");
ws.onmessage = (e) => console.log(JSON.parse(e.data));
```

#### Managing Multiple WebSocket Clients

When more than one dashboard is open, you need a connection manager:

```python
class ConnectionManager:
    """Tracks all active WebSocket connections."""

    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active.remove(ws)

    async def broadcast(self, message: str):
        """Send a message to every connected client."""
        dead = []
        for ws in self.active:
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.active.remove(ws)


manager = ConnectionManager()


@app.websocket("/ws/metrics")
async def metrics_stream(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            payload = {
                "cpu_percent": psutil.cpu_percent(interval=None),
                "memory_percent": psutil.virtual_memory().percent,
            }
            await manager.broadcast(json.dumps(payload))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```
