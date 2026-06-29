"""
04_streamlit/api.py
────────────────────
Minimal FastAPI backend that the Streamlit dashboard connects to.

Endpoints:
  GET  /metrics          — live CPU/memory/disk snapshot
  GET  /servers          — list registered servers  (requires X-API-Key)
  POST /servers          — register a server        (requires X-API-Key)
  DELETE /servers/{id}   — remove a server          (requires X-API-Key)
  GET  /health           — liveness probe

Run:
    uvicorn api:app --reload --port 8004

Then launch the dashboard:
    streamlit run app.py
"""

import time
from collections import deque
from typing import Annotated

import psutil
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

app = FastAPI(title="Dashboard Backend")

# ─── Auth ─────────────────────────────────────────────────────────────────────

API_KEY = "demo-key"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
    return key


# ─── Models ───────────────────────────────────────────────────────────────────

class ServerIn(BaseModel):
    name: str = Field(..., min_length=1)
    host: str
    port: int = Field(8080, ge=1, le=65535)
    environment: str = "prod"


class ServerOut(ServerIn):
    id: int
    registered_at: float


# ─── In-memory store ──────────────────────────────────────────────────────────

_servers: list[ServerOut] = [
    ServerOut(id=1, name="api-prod",      host="10.0.0.1", port=8080, environment="prod",    registered_at=time.time() - 3600),
    ServerOut(id=2, name="api-staging",   host="10.0.1.1", port=8080, environment="staging", registered_at=time.time() - 1800),
    ServerOut(id=3, name="db-prod",       host="10.0.0.5", port=5432, environment="prod",    registered_at=time.time() - 7200),
]
_next_id = 4

# Keep a small history of metric snapshots for sparklines
_metrics_history: deque[dict] = deque(maxlen=60)


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/metrics")
async def get_metrics():
    """Live system metrics snapshot."""
    mem = psutil.virtual_memory()
    snapshot = {
        "ts":             time.time(),
        "cpu_percent":    psutil.cpu_percent(interval=None),
        "memory_percent": mem.percent,
        "memory_used_gb": round(mem.used / 1e9, 2),
        "memory_total_gb": round(mem.total / 1e9, 2),
        "disk_percent":   psutil.disk_usage("/").percent,
    }
    _metrics_history.append(snapshot)
    return snapshot


@app.get("/metrics/history")
async def get_metrics_history():
    return list(_metrics_history)


@app.get("/servers", response_model=list[ServerOut])
async def list_servers(_: Annotated[str, Depends(verify_key)]):
    return _servers


@app.post("/servers", response_model=ServerOut, status_code=201)
async def add_server(
    server: ServerIn,
    _: Annotated[str, Depends(verify_key)],
):
    global _next_id
    out = ServerOut(**server.model_dump(), id=_next_id, registered_at=time.time())
    _servers.append(out)
    _next_id += 1
    return out


@app.delete("/servers/{server_id}", status_code=204)
async def remove_server(
    server_id: int,
    _: Annotated[str, Depends(verify_key)],
):
    for i, s in enumerate(_servers):
        if s.id == server_id:
            _servers.pop(i)
            return
    raise HTTPException(status_code=404, detail="Not found")


@app.get("/health")
async def health():
    return {"status": "ok", "servers": len(_servers)}
