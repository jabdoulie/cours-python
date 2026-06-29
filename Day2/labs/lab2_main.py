
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dataclasses import dataclass, field as dc_field

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


# ─── In-memory store ─────────────────────────────────────────────────────────

_store: dict[int, Server] = {}
_counter = 0


# ─── Endpoints ───────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "servers": len(_store)}


@app.post("/servers", response_model=ServerOut, status_code=201)
async def register_server(server: ServerIn):
    global _counter
    _counter += 1
    record = Server(id=_counter, name=server.name, host=server.host,
                    port=server.port, tags=server.tags)
    _store[_counter] = record
    return record


@app.get("/servers", response_model=list[ServerOut])
async def list_servers(status: str | None = None):
    # TODO: return all servers; filter by status if provided
    pass


@app.get("/servers/{server_id}", response_model=ServerOut)
async def get_server(server_id: int):
    # TODO: return server or raise 404
    pass


@app.delete("/servers/{server_id}", status_code=204)
async def delete_server(server_id: int):
    # TODO: delete server or raise 404
    pass


@app.post("/servers/{server_id}/check", response_model=ServerOut)
async def trigger_check(server_id: int):
    import httpx, asyncio
    if server_id not in _store:
        raise HTTPException(404, "Server not found")
    server = _store[server_id]
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{server.base_url()}/health")
            server.status = "UP" if resp.status_code == 200 else "DEGRADED"
    except Exception:
        server.status = "DOWN"
    return server
