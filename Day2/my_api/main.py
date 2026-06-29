from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from models import ServerIn, ServerOut
app = FastAPI(
    title="DevOps Monitoring API",
    description="Real-time server health monitoring and metrics streaming.",
    version="1.0.0",
    contact={"name": "SupdeVinci", "email": "devops@supdevinci.fr"},
)

_store: dict[int, ServerOut] = {}
_counter = 0


# --- POST — body parameter (JSON) ---
@app.post("/servers", response_model=ServerOut, status_code=201)
async def register_server(server: ServerIn):
    global _counter
    _counter += 1
    record = ServerOut(id=_counter, **server.model_dump())
    _store[_counter] = record
    return record


# --- GET all — query parameter ---
@app.get("/servers", response_model=list[ServerOut])
async def list_servers(status: str | None = Query(default=None)):
    servers = list(_store.values())
    if status:
        servers = [s for s in servers if s.status == status]
    return servers


# --- GET one — path parameter ---
@app.get("/servers/{server_id}", response_model=ServerOut)
async def get_server(server_id: int):
    if server_id not in _store:
        raise HTTPException(status_code=404, detail="Server not found")
    return _store[server_id]


# --- DELETE ---
@app.delete("/servers/{server_id}", status_code=204)
async def delete_server(server_id: int):
    if server_id not in _store:
        raise HTTPException(status_code=404, detail="Server not found")
    del _store[server_id]