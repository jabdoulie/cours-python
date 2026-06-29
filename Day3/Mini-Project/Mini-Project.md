
## Project Part 1 — DevOps Monitoring Dashboard MVP (4 h)

### Goal

Build a working DevOps Monitoring Dashboard from scratch. It consists of two services: a **FastAPI backend** that exposes live system metrics and manages a list of monitored servers, and a **Streamlit frontend** that displays those metrics in real time and lets users register/remove servers.

This is not a tutorial — you write the code. The sections below describe *what* each component must do and what the expected behaviour is. Use everything you've learned in Days 1–3.

This project is the foundation for Day 5's full Azure deployment, so structure it cleanly: separate files per concern, type hints everywhere, no business logic inside route handlers.

---

### Repository Structure

Organise your project like this:

```
devops-monitor/
├── api/
│   ├── __init__.py
│   ├── main.py          # FastAPI app entry point (lifespan, route registration)
│   ├── models.py        # Pydantic schemas + Server dataclass
│   ├── auth.py          # API key dependency
│   ├── metrics.py       # psutil helper — returns a dict of system stats
│   └── poller.py        # Background health-check logic
├── dashboard/
│   └── app.py           # Streamlit frontend
├── tests/
│   ├── test_metrics.py
│   └── test_routes.py
├── requirements.txt
└── README.md
```

---

### Step 1 — FastAPI Backend (1.5 h)

#### api/metrics.py — System metrics helper

Write a single function `get_system_metrics() -> dict` that uses `psutil` to return a snapshot of the current machine's CPU percentage, memory percentage and usage in GB, and disk usage percentage.

**Key constraint:** use `psutil.cpu_percent(interval=None)` — the non-blocking form. Using `interval=1` blocks the event loop for a full second on every call.

---

#### api/auth.py — API key dependency

Write a FastAPI dependency `verify_api_key` using `APIKeyHeader` that reads the key from the `X-API-Key` header. Load the expected key from an environment variable (`API_KEY`) with a fallback default for local dev. Raise `HTTP 403` for any missing or invalid key.

Protected endpoints (writes): `POST /servers`, `DELETE /servers/{id}`.  
Public endpoints (reads): `GET /health`, `GET /metrics`, `GET /servers`, WebSocket.

---

#### api/models.py — Data models

You need two things:

1. A **`Server` dataclass** with fields `id`, `name`, `host`, `port`, and `status` (default `"unknown"`). Add a `base_url()` method that returns `http://{host}:{port}`.

2. **Pydantic models** for the API: `ServerIn` for incoming requests (validate that `port` is between 1 and 65535), and `ServerOut` for responses (includes `id` and `status`).

---

#### api/poller.py — Background health checking

Write two async functions:

- `poll_server(server_id, url, store)` — makes a GET request to `{url}/health` using `httpx.AsyncClient`. Sets the server's status to `"UP"`, `"DEGRADED"` (non-200), or `"DOWN"` (connection error). Updates the server object in `store` in place.

- `run_poll_loop(store, interval=10)` — an infinite async loop that calls `poll_server` for every server in `store` concurrently (use `asyncio.gather`), then sleeps for `interval` seconds. This is designed to run as a background task started at app startup.

---

#### api/main.py — App entry point

Wire everything together. Your app must expose the following endpoints:

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/health` | public | Returns `{"status": "ok"}` |
| `GET` | `/metrics` | public | Returns the current system metrics snapshot |
| `WebSocket` | `/ws/metrics` | public | Streams a metrics JSON frame every second, forever |
| `POST` | `/servers` | API key | Registers a new server, returns it with `status="unknown"` |
| `GET` | `/servers` | public | Lists all servers; accepts optional `?status=UP` filter |
| `GET` | `/servers/{id}` | public | Returns one server or 404 |
| `DELETE` | `/servers/{id}` | API key | Removes a server or 404 |
| `POST` | `/servers/{id}/check` | public | Triggers an immediate background health check for one server |

**Lifespan:** on startup, launch `run_poll_loop` as a background `asyncio.Task`. On shutdown, cancel the task cleanly.

**WebSocket:** accept the connection, then loop: send the metrics JSON, sleep 1 second, repeat. Handle `WebSocketDisconnect` so a client closing the tab doesn't crash the server.

Start with:
```bash
uvicorn api.main:app --reload --port 8000
```

---

### Step 2 — Streamlit Dashboard (1.5 h)

#### dashboard/app.py

The dashboard connects to the FastAPI backend at `http://localhost:8000` and must have two tabs.

**Tab 1 — Metrics**

- Fetch `/metrics` every 2 seconds using `@st.cache_data(ttl=2)`.
- Display CPU %, Memory %, and Disk % as `st.metric` tiles.
- Accumulate the last 60 data points in `st.session_state` and render a live `st.line_chart` of CPU and memory over time.
- Use `st.empty()` + `st.rerun()` for the live-refresh loop.

**Tab 2 — Servers**

- Fetch `/servers` using `@st.cache_data(ttl=5)` and display the list in `st.dataframe` with colour-coding by status (green for UP, amber for DEGRADED, red for DOWN).
- A form (use `st.form` to prevent reruns on every keystroke) lets users enter a name, host, and port to `POST /servers`. The API key must be sent in the `X-API-Key` header.
- A selectbox + button lets users trigger an immediate health check (`POST /servers/{id}/check`) and see the result after a rerun.

Start with:
```bash
streamlit run dashboard/app.py
```

---

### Step 3 — Tests (1 h)

Write pytest tests in the `tests/` folder. You do not need 100% coverage — focus on the critical paths.

**tests/test_metrics.py** — unit tests for `get_system_metrics()`:
- Verify the returned dict contains `cpu_percent`, `memory_percent`, `disk_percent`.
- Verify each value is between 0 and 100.

**tests/test_routes.py** — route tests using FastAPI's `TestClient`:
- `GET /health` returns 200 with `{"status": "ok"}`.
- `GET /metrics` returns 200 and includes `cpu_percent`.
- `POST /servers` without a key returns 403.
- `POST /servers` with a valid key returns 201; the server appears in `GET /servers`.
- `GET /servers/{nonexistent_id}` returns 404.

Run with:
```bash
pip install pytest
pytest tests/ -v
```

---

### Grading — Project Part 1 (30 %)

| Criterion | Points |
|---|---|
| All API endpoints functional (`/health`, `/metrics`, `/servers` CRUD) | 35 |
| WebSocket `/ws/metrics` delivering live JSON frames | 20 |
| Streamlit dashboard connected to the API | 20 |
| Test coverage ≥ 75 % (`pytest --cov=api`) | 15 |
| Code quality: type hints, docstrings, clean module structure | 10 |

**Submission:** Push to a GitHub repository and share the URL. Include a `README.md` with local setup instructions.

---

### Stretch Goals

**Stretch 1 — Disk partitions breakdown**

Add `GET /metrics/disk` that returns per-partition usage using `psutil.disk_partitions()`.

**Stretch 2 — Network stats**

Add network I/O counters (`psutil.net_io_counters()`) to `/metrics` and display bytes sent/received in the dashboard.

**Stretch 3 — Alert thresholds**

Add a `POST /alerts/config` endpoint that accepts `{ "cpu_threshold": 85, "memory_threshold": 90 }`. The WebSocket payload should include an `"alert"` field when any threshold is exceeded.

**Stretch 4 — WebSocket in Streamlit**

Replace the polling `st.rerun()` loop in the Metrics tab with a direct WebSocket connection to `/ws/metrics` using the `websockets` library.

