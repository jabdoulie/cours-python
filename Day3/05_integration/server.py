"""
05_integration/server.py
─────────────────────────
A single FastAPI app that combines every Day 3 feature:

  • WebSocket endpoint (/ws/metrics)
  • API Key authentication
  • JWT login + protected routes
  • BackgroundTasks (fire-and-forget checks)
  • Lifespan background polling loop
  • Pydantic models with validation
  • /health liveness probe

Run:
    uvicorn server:app --reload --port 8005

Then run the integration tests:
    python test_integration.py
"""

import asyncio
import logging
import time
from collections import deque
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import Annotated

import psutil
from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    HTTPException,
    Security,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ─── Configuration ────────────────────────────────────────────────────────────

API_KEY = "integration-key"
JWT_SECRET = "integration-jwt-secret"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 30

FAKE_USERS = {
    "admin": {"password": "admin123", "role": "admin"},
    "viewer": {"password": "viewer123", "role": "viewer"},
}


# ─── Shared state ─────────────────────────────────────────────────────────────

metrics_history: deque[dict] = deque(maxlen=60)
check_results: list[dict] = []


# ─── Lifespan ─────────────────────────────────────────────────────────────────

async def _poll_metrics():
    logger.info("Background metrics loop started")
    while True:
        metrics_history.append({
            "ts":  time.time(),
            "cpu": psutil.cpu_percent(interval=None),
            "mem": psutil.virtual_memory().percent,
        })
        await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(_poll_metrics())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="Integration Server", lifespan=lifespan)


# ─── Auth helpers ─────────────────────────────────────────────────────────────

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def require_api_key(key: str = Security(api_key_header)) -> str:
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return key


def _make_token(username: str, role: str) -> str:
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    if not username or username not in FAKE_USERS:
        raise HTTPException(status_code=401, detail="Unknown user")
    return {"username": username, "role": payload.get("role")}


# ─── Models ───────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ServerIn(BaseModel):
    name: str = Field(..., min_length=1)
    host: str
    port: int = Field(8080, ge=1, le=65535)


class ServerOut(ServerIn):
    id: int


class CheckRequest(BaseModel):
    host: str
    check_type: str = "ping"


# ─── In-memory server store ───────────────────────────────────────────────────

_servers: list[ServerOut] = []
_next_id = 1


# ─── Background task ──────────────────────────────────────────────────────────

async def _run_check(host: str, check_type: str):
    await asyncio.sleep(1.5)
    check_results.append({
        "host": host,
        "check_type": check_type,
        "status": "ok",
        "ts": time.time(),
    })
    logger.info("Check complete: %s %s", check_type, host)


# ─── Routes ───────────────────────────────────────────────────────────────────

# Auth
@app.post("/auth/token", response_model=TokenResponse)
async def login(creds: LoginRequest):
    user = FAKE_USERS.get(creds.username)
    if not user or user["password"] != creds.password:
        raise HTTPException(status_code=401, detail="Bad credentials")
    return TokenResponse(access_token=_make_token(creds.username, user["role"]))


# Servers (API key protected)
@app.get("/servers", response_model=list[ServerOut])
async def list_servers(_: Annotated[str, Depends(require_api_key)]):
    return _servers


@app.post("/servers", response_model=ServerOut, status_code=201)
async def add_server(server: ServerIn, _: Annotated[str, Depends(require_api_key)]):
    global _next_id
    out = ServerOut(**server.model_dump(), id=_next_id)
    _servers.append(out)
    _next_id += 1
    return out


# Checks (JWT protected)
@app.post("/checks", status_code=202)
async def trigger_check(
    req: CheckRequest,
    bg: BackgroundTasks,
    user: Annotated[dict, Depends(get_current_user)],
):
    bg.add_task(_run_check, req.host, req.check_type)
    return {"accepted": True, "triggered_by": user["username"]}


@app.get("/checks/results")
async def get_check_results(_: Annotated[dict, Depends(get_current_user)]):
    return check_results


# Metrics (public)
@app.get("/metrics/history")
async def get_metrics_history():
    return list(metrics_history)


# WebSocket
@app.websocket("/ws/metrics")
async def ws_metrics(websocket: WebSocket):
    import json
    await websocket.accept()
    try:
        while True:
            await websocket.send_text(json.dumps({
                "cpu":  psutil.cpu_percent(interval=None),
                "mem":  psutil.virtual_memory().percent,
                "ts":   time.time(),
            }))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "servers": len(_servers),
        "checks": len(check_results),
        "metrics_snapshots": len(metrics_history),
    }
