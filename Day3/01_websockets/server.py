"""
01_websockets/server.py
───────────────────────
FastAPI WebSocket server that streams live system metrics every second.

Run:
    uvicorn server:app --reload --port 8000

Then test with:
    python client.py          # Python client
    python multi_client.py    # multiple clients at once
"""

import asyncio
import json
import logging

import psutil
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="WebSocket Demo")


# ─────────────────────────────────────────────────────────────────────────────
# 1. Simplest possible WebSocket — one client, streams metrics every 1s
# ─────────────────────────────────────────────────────────────────────────────

@app.websocket("/ws/metrics")
async def stream_metrics(websocket: WebSocket):
    """
    Accept a WebSocket connection and push live CPU/memory/disk data every second.
    Handles disconnects gracefully — closing a browser tab is NOT an error.
    """
    await websocket.accept()
    logger.info("Client connected → /ws/metrics")
    try:
        while True:
            payload = {
                "cpu_percent":    psutil.cpu_percent(interval=None),   # non-blocking
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent":   psutil.disk_usage("/").percent,
                "memory_used_gb": round(psutil.virtual_memory().used / 1e9, 2),
            }
            await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(1)          # yield to event loop — never use time.sleep here
    except WebSocketDisconnect:
        logger.info("Client disconnected — WebSocketDisconnect (normal)")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Connection manager — broadcast to MULTIPLE clients at once
# ─────────────────────────────────────────────────────────────────────────────

class ConnectionManager:
    """Tracks all open WebSocket connections and handles broadcast."""

    def __init__(self):
        self.active: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)
        logger.info("Client connected. Total connections: %d", len(self.active))

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)
        logger.info("Client disconnected. Total connections: %d", len(self.active))

    async def broadcast(self, message: str):
        """Send a message to every connected client. Remove dead connections."""
        dead = []
        for ws in self.active:
            try:
                await ws.send_text(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.active.remove(ws)


manager = ConnectionManager()


@app.websocket("/ws/broadcast")
async def broadcast_metrics(websocket: WebSocket):
    """
    Multiple clients connect here. The server broadcasts the same
    metrics payload to ALL of them every second.

    Try opening two browser tabs to ws://localhost:8000/ws/broadcast
    and see them both receive the same data.
    """
    await manager.connect(websocket)
    try:
        # This loop drives the broadcast for this connection.
        # In a real app you'd have a single background task broadcasting
        # and clients just listen — see server_with_background.py for that pattern.
        while True:
            payload = {
                "cpu_percent":    psutil.cpu_percent(interval=None),
                "memory_percent": psutil.virtual_memory().percent,
                "clients":        len(manager.active),
            }
            await manager.broadcast(json.dumps(payload))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# ─────────────────────────────────────────────────────────────────────────────
# 3. Bidirectional — server sends metrics, client can send commands back
# ─────────────────────────────────────────────────────────────────────────────

@app.websocket("/ws/bidirectional")
async def bidirectional(websocket: WebSocket):
    """
    Client can send JSON commands:
        {"action": "pause"}   — stop streaming
        {"action": "resume"}  — restart streaming
        {"action": "ping"}    — server replies with pong

    Server streams metrics while not paused.
    """
    await websocket.accept()
    paused = False

    async def receive_commands():
        nonlocal paused
        while True:
            try:
                raw = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
                cmd = json.loads(raw)
                if cmd.get("action") == "pause":
                    paused = True
                    await websocket.send_text(json.dumps({"event": "paused"}))
                elif cmd.get("action") == "resume":
                    paused = False
                    await websocket.send_text(json.dumps({"event": "resumed"}))
                elif cmd.get("action") == "ping":
                    await websocket.send_text(json.dumps({"event": "pong"}))
            except asyncio.TimeoutError:
                pass    # no command this tick — fine

    try:
        while True:
            await receive_commands()
            if not paused:
                payload = {
                    "cpu_percent":    psutil.cpu_percent(interval=None),
                    "memory_percent": psutil.virtual_memory().percent,
                }
                await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        logger.info("Bidirectional client disconnected")


@app.get("/health")
async def health():
    return {"status": "ok", "active_clients": len(manager.active)}
