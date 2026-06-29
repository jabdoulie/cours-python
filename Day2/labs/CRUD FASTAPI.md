## Lab 2.3 —  FastAPI CRUD API (3.5 h)

### Goal

Refactor the Day 1 `server_health.py` CLI tool into a proper OOP structure, then expose it as a FastAPI REST API with full CRUD operations.
---

### Project Structure

```
day2-lab/
├── __init__.py
├── main.py          # FastAPI app
├── models.py        # Pydantic schemas
├── health.py        # HealthChecker class
├── config.py        # ConfigLoader class
└── requirements.txt
```

---

### Setup

```bash
mkdir day2-lab && cd day2-lab
python -m venv .venv
source .venv/bin/activate

pip install fastapi uvicorn[standard] httpx
pip freeze > requirements.txt
```

---

### Task 1 — Model the Server with a Dataclass

Create `models.py` with:
- A `Server` dataclass for internal use (host, port, name, status, id)
- A `ServerIn` Pydantic model for incoming POST requests
- A `ServerOut` Pydantic model for API responses

```python
# models.py
from dataclasses import dataclass, field
from pydantic import BaseModel, Field


@dataclass
class Server:
    """Internal server representation."""
    id: int
    name: str
    host: str
    port: int
    status: str = "unknown"
    tags: list[str] = field(default_factory=list)

    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"


class ServerIn(BaseModel):
    """Schema for registering a new server."""
    name: str
    host: str
    port: int = Field(default=8080, ge=1, le=65535)

    # TODO: add an optional list of tags (default empty list)


class ServerOut(BaseModel):
    """Schema returned to the API client."""
    id: int
    name: str
    host: str
    port: int
    status: str

    # TODO: add tags field
    
    model_config = {"from_attributes": True}
```

---

### Task 2 — ConfigLoader Class

Create `config.py` with a `ConfigLoader` class that:
- Accepts a file path on construction
- Has a `load() -> list[Server]` method that reads JSON and returns `Server` objects
- Logs info on success and raises `ConfigError` on failure

```python
# config.py
import json
import logging
import pathlib
from models import Server

logger = logging.getLogger(__name__)


class ConfigError(ValueError):
    """Raised when configuration loading fails."""
    pass


class ConfigLoader:
    """Loads server configuration from a JSON file."""

    def __init__(self, path: str):
        self.path = pathlib.Path(path)

    def load(self) -> list[Server]:
        """Load and return servers from the config file.
        
        Raises:
            ConfigError: If the file is missing or contains invalid JSON.
        """
        # TODO: implement this method
        pass
```

---

### Task 3 — HealthChecker Class

Create `health.py` with an async `HealthChecker` class:

```python
# health.py
import asyncio
import logging
import time
import httpx
from models import Server

logger = logging.getLogger(__name__)


class HealthChecker:
    """Checks the health of servers over HTTP."""

    def __init__(self, timeout: float = 5.0, degraded_threshold_ms: float = 500.0):
        self.timeout = timeout
        self.degraded_threshold_ms = degraded_threshold_ms

    async def check(self, server: Server) -> Server:
        """
        Check a single server's health endpoint.
        Updates server.status in-place and returns the server.

        Status rules:
          UP       — HTTP 200 and response_time ≤ threshold
          DEGRADED — HTTP 200 but slow, OR non-200 response
          DOWN     — connection error or timeout
        """
        url = f"{server.base_url()}/health"
        # TODO: implement using httpx.AsyncClient
        pass

    async def check_all(self, servers: list[Server]) -> list[Server]:
        """Check all servers concurrently."""
        # TODO: use asyncio.gather() to run check() for all servers in parallel
        pass
```

---

### Task 4 — FastAPI CRUD API

Create `main.py` with a FastAPI app that manages servers in memory:

#### Required Endpoints

| Method | Path | Description | Auth |
|---|---|---|---|
| `GET` | `/health` | API health check | None |
| `POST` | `/servers` | Register a server | None (add in stretch) |
| `GET` | `/servers` | List all servers | None |
| `GET` | `/servers/{server_id}` | Get one server | None |
| `DELETE` | `/servers/{server_id}` | Remove a server | None |
| `POST` | `/servers/{server_id}/check` | Trigger a health check | None |

```python
# main.py
from fastapi import FastAPI, HTTPException
from models import Server, ServerIn, ServerOut
from health import HealthChecker

app = FastAPI(title="DevOps Monitoring API", version="1.0")

_store: dict[int, Server] = {}
_counter = 0
checker = HealthChecker()


@app.get("/health")
async def health_check():
    return {"status": "ok", "servers_monitored": len(_store)}


@app.post("/servers", response_model=ServerOut, status_code=201)
async def register_server(server: ServerIn):
    # TODO: implement
    pass


@app.get("/servers", response_model=list[ServerOut])
async def list_servers(status: str | None = None):
    # TODO: implement — support optional ?status=UP filter
    pass


@app.get("/servers/{server_id}", response_model=ServerOut)
async def get_server(server_id: int):
    # TODO: implement — raise 404 if not found
    pass


@app.delete("/servers/{server_id}", status_code=204)
async def delete_server(server_id: int):
    # TODO: implement
    pass


@app.post("/servers/{server_id}/check", response_model=ServerOut)
async def trigger_health_check(server_id: int):
    # TODO: use checker.check() to update and return the server
    pass
```

---

### Task 5 — Verify in Swagger UI

Run the API:

```bash
uvicorn main:app --reload --port 8000
```

Open `http://localhost:8000/docs` and test:

1. `POST /servers` — register at least 3 servers:
   ```json
   {"name": "api-prod-1", "host": "httpbin.org", "port": 443}
   ```

2. `GET /servers` — verify all 3 appear with `status: "unknown"`

3. `POST /servers/1/check` — trigger a health check on server 1

4. `GET /servers?status=UP` — filter by status

5. `DELETE /servers/2` — remove server 2, then `GET /servers` to confirm

---

### Complete Solution

<details>
<summary>models.py</summary>

```python
from dataclasses import dataclass, field
from pydantic import BaseModel, Field


@dataclass
class Server:
    id: int
    name: str
    host: str
    port: int
    status: str = "unknown"
    tags: list[str] = field(default_factory=list)

    def base_url(self) -> str:
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
```

</details>

<details>
<summary>config.py</summary>

```python
import json
import logging
import pathlib
from models import Server

logger = logging.getLogger(__name__)


class ConfigError(ValueError):
    pass


class ConfigLoader:
    def __init__(self, path: str):
        self.path = pathlib.Path(path)

    def load(self) -> list[Server]:
        logger.info("Loading config from %s", self.path)
        try:
            raw = json.loads(self.path.read_text())
        except FileNotFoundError:
            logger.error("Config file not found: %s", self.path)
            raise ConfigError(f"File not found: {self.path}")
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON: %s", e)
            raise ConfigError(f"Invalid JSON: {e}") from e

        servers = []
        for i, entry in enumerate(raw, start=1):
            servers.append(Server(
                id=i,
                name=entry["name"],
                host=entry["host"],
                port=entry["port"],
            ))
        logger.info("Loaded %d servers", len(servers))
        return servers
```

</details>

<details>
<summary>health.py</summary>

```python
import asyncio
import logging
import time
import httpx
from models import Server

logger = logging.getLogger(__name__)


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
            logger.info("%-20s %s  (%.0f ms)", server.name, server.status, elapsed_ms)
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            server.status = "DOWN"
            logger.warning("%-20s DOWN — %s", server.name, e)
        return server

    async def check_all(self, servers: list[Server]) -> list[Server]:
        return await asyncio.gather(*[self.check(s) for s in servers])
```

</details>

<details>
<summary>main.py</summary>

```python
import logging
from fastapi import FastAPI, HTTPException
from models import Server, ServerIn, ServerOut
from health import HealthChecker

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s — %(message)s")

app = FastAPI(title="DevOps Monitoring API", version="1.0")

_store: dict[int, Server] = {}
_counter = 0
checker = HealthChecker()


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "servers_monitored": len(_store)}


@app.post("/servers", response_model=ServerOut, status_code=201, tags=["Servers"])
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


@app.get("/servers", response_model=list[ServerOut], tags=["Servers"])
async def list_servers(status: str | None = None):
    servers = list(_store.values())
    if status:
        servers = [s for s in servers if s.status == status]
    return servers


@app.get("/servers/{server_id}", response_model=ServerOut, tags=["Servers"])
async def get_server(server_id: int):
    if server_id not in _store:
        raise HTTPException(status_code=404, detail="Server not found")
    return _store[server_id]


@app.delete("/servers/{server_id}", status_code=204, tags=["Servers"])
async def delete_server(server_id: int):
    if server_id not in _store:
        raise HTTPException(status_code=404, detail="Server not found")
    del _store[server_id]


@app.post("/servers/{server_id}/check", response_model=ServerOut, tags=["Servers"])
async def trigger_health_check(server_id: int):
    if server_id not in _store:
        raise HTTPException(status_code=404, detail="Server not found")
    server = await checker.check(_store[server_id])
    return server
```

</details>

---

**Stretch Goal — API Key Auth**

Protect `POST /servers` and `DELETE /servers/{id}` with an API key header:

```python
from fastapi import Header

def require_api_key(x_api_key: str = Header(...)):
    if x_api_key != "ops-secret":
        raise HTTPException(403, "Invalid API key")
```
