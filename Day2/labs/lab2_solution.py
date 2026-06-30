from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dataclasses import dataclass, field as dc_field

app = FastAPI()

@dataclass
class Server:
    id: int
    name: str
    host: str
    port: int
    status: str = "unknown"
    tags: list[str] = dc_field(default_factory=list)

    def base_url(self):
        return f"http://{self.host}:{self.port}"


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


_store: dict[int, Server] = {}
_counter = 0


@app.get("/health")
async def health():
    return {"status": "ok", "servers_monitored": len(_store)}


@app.post("/servers", response_model=ServerOut, status_code=201)
async def register_server(server: ServerIn):
    global _counter
    _counter += 1
    rec = Server(
        id=_counter,
        name=server.name,
        host=server.host,
        port=server.port,
        tags=server.tags,
    )
    _store[_counter] = rec
    return rec


@app.get("/servers", response_model=list[ServerOut])
async def list_servers(status: str | None = None):
    svrs = list(_store.values())
    return [s for s in svrs if s.status == status] if status else svrs


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
