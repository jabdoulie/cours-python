import asyncio
import logging
import time

import httpx
from dataclasses import dataclass, field as dc_field
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = FastAPI(title="DevOps Monitoring API", version="1.0")


# ─── Internal model ─────────────────────────────────────────────────────────

@dataclass
class Server:
    id: int
    name: str
    host: str
    port: int
    status: str = "unknown"
    tags: list[str] = dc_field(default_factory=list)

    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"


# ─── Pydantic schemas ────────────────────────────────────────────────────────

class ServerIn(BaseModel):
    name: str
    host: str
    port: int = Field(default=8080, ge=1, le=65535)
    tags: list[str] = []


class ServerOut(BaseModel):
    id: int
    name: str
    host: str
    port: int
    status: str
    tags: list[str] = []
    model_config = {"from_attributes": True}


# ─── HealthChecker ───────────────────────────────────────────────────────────

class HealthChecker:
    def __init__(self, timeout: float = 5.0, degraded_threshold_ms: float = 500.0):
        self.timeout = timeout
        self.degraded_threshold_ms = degraded_threshold_ms

    async def check(self, server: Server) -> Server:
        url = f"{server.base_url()}/health"
        start = time.time()
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.get(url)
            elapsed_ms = (time.time() - start) * 1000
            if resp.status_code == 200 and elapsed_ms <= self.degraded_threshold_ms:
                server.status = "UP"
            elif resp.status_code == 200:
                server.status = "DEGRADED"
            else:
                server.status = "DEGRADED"
        except (httpx.ConnectError, httpx.TimeoutException):
            server.status = "DOWN"
        return server

    async def check_all(self, servers: list[Server]) -> list[Server]:
        return await asyncio.gather(*[self.check(s) for s in servers])


# ─── In-memory store ─────────────────────────────────────────────────────────

_store: dict[int, Server] = {}
_counter = 0
checker = HealthChecker()


# ─── Endpoints ───────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "servers_monitored": len(_store)}


@app.post("/servers", response_model=ServerOut, status_code=201)
async def register_server(server: ServerIn):
    global _counter
    _counter += 1
    record = Server(
        id=_counter,
        name=server.name,
        host=server.host,
        port=server.port,
        tags=server.tags,
    )
    _store[_counter] = record
    return record


@app.get("/servers", response_model=list[ServerOut])
async def list_servers(status: str | None = None):
    servers = list(_store.values())
    if status:
        servers = [s for s in servers if s.status == status]
    return servers


@app.get("/servers/{server_id}", response_model=ServerOut)
async def get_server(server_id: int):
    if server_id not in _store:
        raise HTTPException(status_code=404, detail="Server not found")
    return _store[server_id]


@app.delete("/servers/{server_id}", status_code=204)
async def delete_server(server_id: int):
    if server_id not in _store:
        raise HTTPException(status_code=404, detail="Server not found")
    del _store[server_id]


@app.post("/servers/{server_id}/check", response_model=ServerOut)
async def trigger_check(server_id: int):
    if server_id not in _store:
        raise HTTPException(status_code=404, detail="Server not found")
    server = await checker.check(_store[server_id])
    return server
