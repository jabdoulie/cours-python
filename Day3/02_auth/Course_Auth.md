# Day 3 — Authentication

#### API Key (Simple, Stateless)

Best for server-to-server communication where you control both sides. No token expiry, no refresh — just a shared secret in a header.

```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
import os

API_KEY = os.getenv("API_KEY", "dev-secret-change-in-prod")
api_key_scheme = APIKeyHeader(name="X-API-Key", auto_error=True)


def verify_api_key(key: str = Security(api_key_scheme)) -> str:
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return key


# Protect a route
@app.post("/servers", dependencies=[Depends(verify_api_key)])
async def register_server(server: ServerIn): ...

# Or inject and use it
@app.delete("/servers/{server_id}")
async def delete_server(server_id: int, _key: str = Depends(verify_api_key)): ...
```

Pass the key in requests:
```bash
curl -X POST http://localhost:8000/servers \
  -H "X-API-Key: dev-secret-change-in-prod" \
  -H "Content-Type: application/json" \
  -d '{"name": "api-1", "host": "10.0.0.1", "port": 8080}'
```

#### JWT — JSON Web Tokens

JWT is better for user-facing authentication. A token is issued at login and carries claims (user ID, role, expiry) — the server doesn't need a database lookup to validate it.

**Token structure:** `header.payload.signature` (base64-encoded, dot-separated)

```
eyJhbGciOiJIUzI1NiJ9
.eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTcxNzAwMDAwMH0
.abc123signature
```

```bash
pip install python-jose[cryptography]
```

```python
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("JWT_SECRET", "change-me-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def create_access_token(data: dict, expires_minutes: int = TOKEN_EXPIRE_MINUTES) -> str:
    """Create a signed JWT token."""
    payload = {
        **data,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid or expired")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    return decode_token(token)


# Login endpoint — issues a token
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

FAKE_USERS = {"admin": "password123"}   # replace with real DB lookup

@app.post("/auth/token")
async def login(credentials: LoginRequest):
    if FAKE_USERS.get(credentials.username) != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": credentials.username})
    return {"access_token": token, "token_type": "bearer"}


# Protected route
@app.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    return {"username": user["sub"]}
```

**API Key vs JWT — when to use each:**

| | API Key | JWT |
|---|---|---|
| Best for | Service-to-service | User login flows |
| Expiry | None (rotate manually) | Built-in (`exp` claim) |
| Revocation | Delete the key | Difficult (stateless) |
| Complexity | Low | Medium |
| Our capstone uses | ✓ API Key | Optional stretch |

---

### 3. Background Tasks

FastAPI can run work after sending a response, so the client doesn't wait.

#### FastAPI BackgroundTasks

```python
from fastapi import BackgroundTasks
import httpx

async def poll_server_health(server_id: int, url: str):
    """Check a server and update its status in the store."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{url}/health")
            status = "UP" if resp.status_code == 200 else "DEGRADED"
    except Exception:
        status = "DOWN"
    if server_id in _store:
        _store[server_id].status = status


@app.post("/servers/{server_id}/check")
async def trigger_check(server_id: int, background_tasks: BackgroundTasks):
    server = _store.get(server_id)
    if not server:
        raise HTTPException(404, "Server not found")
    background_tasks.add_task(
        poll_server_health,
        server_id,
        server.base_url(),
    )
    return {"message": f"Health check triggered for {server.name}"}
    # ↑ Response is sent immediately — check runs in the background
```

#### Scheduled Polling with Lifespan

For continuous background polling (every N seconds), use the FastAPI lifespan context manager:

```python
from contextlib import asynccontextmanager
import asyncio

POLL_INTERVAL_SECONDS = 10


async def periodic_health_poll():
    """Poll all registered servers every POLL_INTERVAL_SECONDS."""
    while True:
        if _store:
            tasks = [poll_server_health(sid, s.base_url()) for sid, s in _store.items()]
            await asyncio.gather(*tasks)
        await asyncio.sleep(POLL_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: launch the background polling task
    poll_task = asyncio.create_task(periodic_health_poll())
    yield
    # Shutdown: cancel the task cleanly
    poll_task.cancel()
    try:
        await poll_task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="DevOps Monitoring API", lifespan=lifespan)
```

> The lifespan pattern replaces the deprecated `@app.on_event("startup")` and `@app.on_event("shutdown")` decorators. Always prefer `lifespan`.
