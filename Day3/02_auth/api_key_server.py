"""
02_auth/api_key_server.py
──────────────────────────
FastAPI server protected by an API Key sent in the X-API-Key header.

Run:
    uvicorn api_key_server:app --reload --port 8001

Test with:
    # No key → 403
    curl http://localhost:8001/servers

    # Valid key → 200
    curl -H "X-API-Key: secret-key-123" http://localhost:8001/servers

    # Or use the test client:
    python client.py --mode apikey
"""

import logging
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="API Key Auth Demo")

# ─── Configuration ────────────────────────────────────────────────────────────

VALID_API_KEYS = {
    "secret-key-123": "team-a",
    "another-key-456": "team-b",
}

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


# ─── Dependency ───────────────────────────────────────────────────────────────

async def verify_api_key(key: str = Security(api_key_header)) -> str:
    """
    Raise 403 if the key is missing or unknown.
    Returns the team name associated with the key.
    """
    if key is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Missing X-API-Key header",
        )
    team = VALID_API_KEYS.get(key)
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
    logger.info("Authenticated request from team: %s", team)
    return team


# ─── Models ───────────────────────────────────────────────────────────────────

class ServerIn(BaseModel):
    name: str = Field(..., min_length=1)
    host: str
    port: int = Field(default=8080, ge=1, le=65535)
    environment: str = "prod"


class ServerOut(ServerIn):
    id: int
    registered_by: str   # team that registered it


# ─── In-memory store ──────────────────────────────────────────────────────────

_servers: list[ServerOut] = []
_next_id = 1


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/servers", response_model=list[ServerOut])
async def list_servers(_team: Annotated[str, Depends(verify_api_key)]):
    """List all registered servers. Requires a valid API key."""
    return _servers


@app.post("/servers", response_model=ServerOut, status_code=status.HTTP_201_CREATED)
async def register_server(
    server: ServerIn,
    team: Annotated[str, Depends(verify_api_key)],
):
    """Register a new server. The key determines which team owns it."""
    global _next_id
    out = ServerOut(**server.model_dump(), id=_next_id, registered_by=team)
    _servers.append(out)
    _next_id += 1
    logger.info("Server '%s' registered by %s", out.name, team)
    return out


@app.delete("/servers/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_server(
    server_id: int,
    team: Annotated[str, Depends(verify_api_key)],
):
    """Delete a server. Only the team that registered it can delete it."""
    for i, s in enumerate(_servers):
        if s.id == server_id:
            if s.registered_by != team:
                raise HTTPException(status_code=403, detail="Not your server")
            _servers.pop(i)
            return
    raise HTTPException(status_code=404, detail="Server not found")


@app.get("/health")
async def health():
    return {"status": "ok"}
