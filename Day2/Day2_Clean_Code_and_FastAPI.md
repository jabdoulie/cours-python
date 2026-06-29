# Day 2 — FastAPI Introduction 

---

### 1. Why FastAPI?

FastAPI is the framework we use for the entire course capstone. Here's how it compares:

| Feature | Flask | FastAPI |
|---|---|---|
| Type safety | Manual | Built-in via Pydantic |
| Async support | Extension needed | Native (`async def`) |
| Auto API docs | Manual | Swagger UI at `/docs`, ReDoc at `/redoc` |
| Performance | Synchronous (WSGI) | Async (ASGI) — near Go-level |
| Request validation | Manual | Automatic via Pydantic models |
| IDE autocomplete | Limited | Full — thanks to type hints |

---

### 2. Your First FastAPI Application

#### Project Structure

```
my_api/
├── __init__.py
├── main.py
└── models.py
```

#### Install and Run

```bash
pip install fastapi uvicorn[standard]
uvicorn my_api.main:app --reload --port 8000
```

- `--reload` watches for file changes and restarts automatically (development only)
- Visit `http://localhost:8000/docs` for the interactive Swagger UI

#### main.py — minimal example

```python
from fastapi import FastAPI

app = FastAPI(title="Monitoring API", version="1.0")


@app.get("/health")
async def health():
    return {"status": "ok"}
```

---

### 3. Pydantic Models — Request & Response Validation

Pydantic validates incoming data automatically and serialises responses. No manual validation code needed.

```python
from pydantic import BaseModel, Field


class ServerIn(BaseModel):
    """Schema for creating a server."""
    host: str
    port: int = Field(default=8080, ge=1, le=65535)   # 1 ≤ port ≤ 65535
    name: str


class ServerOut(ServerIn):
    """Schema returned to the client — extends ServerIn."""
    id: int
    status: str = "unknown"
```

**What Pydantic does automatically:**
- Rejects requests where `port` is not an integer
- Rejects requests where `port` is outside 1–65535
- Generates the JSON Schema used by Swagger UI
- Serialises Python objects to JSON in responses

---

### 4. Path, Query & Body Parameters

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI()

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
```

**HTTP method conventions:**

| Method | Use for | Success code |
|---|---|---|
| `GET` | Retrieve data | 200 |
| `POST` | Create a resource | 201 |
| `PUT` | Replace a resource | 200 |
| `PATCH` | Update part of a resource | 200 |
| `DELETE` | Remove a resource | 204 (no content) |

---

### 5. HTTPException

Use `HTTPException` to return a meaningful error response:

```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Server not found")
raise HTTPException(status_code=400, detail="Port must be between 1 and 65535")
raise HTTPException(status_code=403, detail="Invalid API key")
raise HTTPException(status_code=422, detail="Validation failed")   # auto-raised by Pydantic
raise HTTPException(status_code=500, detail="Internal error")
```

FastAPI serialises these to:
```json
{
  "detail": "Server not found"
}
```

---

### 6. Dependency Injection with Depends

`Depends` lets you declare reusable logic (auth checks, DB sessions, config loading) that FastAPI resolves automatically:

```python
from fastapi import Depends, HTTPException, Header

def get_api_key(x_api_key: str = Header(...)):
    """Validate the X-API-Key header."""
    if x_api_key != "super-secret-ops-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key


# Inject into a single route
@app.post("/servers", dependencies=[Depends(get_api_key)])
async def register_server(server: ServerIn): ...

# Or inject and use the return value
@app.get("/servers/me")
async def get_my_servers(api_key: str = Depends(get_api_key)):
    return {"key": api_key, "servers": []}
```

---

### 7. Async Basics

FastAPI is built on `asyncio` — Python's built-in event loop for concurrent I/O.

#### sync vs async

```python
import time
import asyncio
import httpx

# ❌ Synchronous — blocks the entire event loop while waiting
def check_health_sync(url: str) -> dict:
    import requests
    resp = requests.get(url, timeout=5)
    return resp.json()

# ✓ Async — yields control while waiting for the network
async def check_health_async(url: str) -> dict:
    async with httpx.AsyncClient(timeout=5.0) as client:
        resp = await client.get(url)
        return resp.json()
```

#### Running Multiple Requests Concurrently

```python
import asyncio
import httpx

urls = [
    "http://10.0.0.1:8080/health",
    "http://10.0.0.2:8080/health",
    "http://10.0.0.3:8080/health",
]

async def check_all(urls: list[str]) -> list[dict]:
    async with httpx.AsyncClient(timeout=5.0) as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        results = []
        for url, resp in zip(urls, responses):
            if isinstance(resp, Exception):
                results.append({"url": url, "status": "DOWN"})
            else:
                results.append({"url": url, "status": "UP" if resp.status_code == 200 else "DEGRADED"})
        return results

# Run 3 requests in parallel — takes ~1 network RTT instead of 3×
asyncio.run(check_all(urls))
```

#### Rules

- Use `async def` for FastAPI route handlers and anything that does I/O (HTTP, DB, file)
- Use `await` to call other async functions
- Use `asyncio.gather()` to run multiple coroutines concurrently
- **Never** call `time.sleep()` inside async code — use `await asyncio.sleep()` instead

---

### 8. Auto-Generated API Documentation

FastAPI generates interactive docs from your code with zero configuration.

| URL | Tool | Use |
|---|---|---|
| `/docs` | Swagger UI | Interactive — test endpoints in the browser |
| `/redoc` | ReDoc | Read-only — clean reference documentation |
| `/openapi.json` | OpenAPI spec | Machine-readable — can generate client SDKs |

Enhance your docs with metadata:

```python
app = FastAPI(
    title="DevOps Monitoring API",
    description="Real-time server health monitoring and metrics streaming.",
    version="1.0.0",
    contact={"name": "SupdeVinci", "email": "devops@supdevinci.fr"},
)


@app.post(
    "/servers",
    response_model=ServerOut,
    status_code=201,
    summary="Register a new server",
    description="Add a server to the monitoring pool. Requires a valid API key.",
    tags=["Servers"],
)
async def register_server(server: ServerIn): ...
```
