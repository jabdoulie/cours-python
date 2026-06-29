
## Lab 3 — Containerise the Stack (1.5 h)

### Goal

Take the Day 3 project and run the full FastAPI + Streamlit stack locally using Docker Compose.

### Learning Objectives

- Write multi-stage and single-stage Dockerfiles
- Configure Docker Compose with health checks and service dependencies
- Use a `.env` file for secret injection
- Verify inter-service networking inside Compose
- Use `docker compose logs` to debug container issues

---

### Task 1 — Dockerfile for the FastAPI API

Create `api/Dockerfile`:

```dockerfile
# Stage 1 — install dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2 — runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY api/ ./api/
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Verify it builds:**
```bash
docker build -t devops-monitor-api -f api/Dockerfile .
docker run --rm -p 8000:8000 devops-monitor-api
# → curl http://localhost:8000/health should return {"status":"ok"}
```

---

### Task 2 — Dockerfile for the Streamlit Dashboard

Create `dashboard/Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY dashboard/ ./dashboard/
EXPOSE 8501
CMD ["streamlit", "run", "dashboard/app.py", \
     "--server.port=8501", "--server.address=0.0.0.0"]
```

---

### Task 3 — .dockerignore

Create `.dockerignore` at the project root:

```
.venv/
__pycache__/
*.pyc
*.pyo
.git/
.env
.pytest_cache/
*.egg-info/
```

---

### Task 4 — docker-compose.yml

Create `docker-compose.yml` at the project root:

```yaml
version: "3.9"

services:
  api:
    build:
      context: .
      dockerfile: api/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - API_KEY=${API_KEY}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 5s
    restart: unless-stopped

  dashboard:
    build:
      context: .
      dockerfile: dashboard/Dockerfile
    ports:
      - "8501:8501"
    environment:
      - API_BASE=http://api:8000
      - API_KEY=${API_KEY}
    depends_on:
      api:
        condition: service_healthy
    restart: unless-stopped
```

---

### Task 5 — .env File

Create `.env` (add it to `.gitignore`!):

```bash
API_KEY=super-secret-ops-key
```

---

### Task 6 — Update dashboard/app.py for Environment Variables

The dashboard's `API_BASE` and `API_KEY` must come from environment variables when running in Docker:

```python
import os

API_BASE = os.getenv("API_BASE", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "dev-secret")
HEADERS = {"X-API-Key": API_KEY}
```

---

### Task 7 — Build and Run

```bash
docker compose up --build -d
```

**Verify:**
- `http://localhost:8000/docs` → Swagger UI loads ✓
- `http://localhost:8000/health` → `{"status": "ok"}` ✓
- `http://localhost:8501` → Streamlit dashboard loads and shows metrics ✓

```bash
# Check container status
docker compose ps

# Watch logs
docker compose logs -f

# Test the WebSocket from host
python -c "
import asyncio, websockets, json
async def t():
    async with websockets.connect('ws://localhost:8000/ws/metrics') as ws:
        print(json.loads(await ws.recv()))
asyncio.run(t())
"
```

---

### Stretch Goals

**Stretch 1 — Run tests inside Docker**

```bash
docker compose run --rm api pytest tests/ -v
```

**Stretch 2 — Non-root user**

Add a non-root user to your Dockerfiles for improved security:

```dockerfile
RUN adduser --disabled-password --gecos "" appuser
USER appuser
```

**Stretch 3 — Image size audit**

```bash
docker images | grep devops-monitor
docker history devops-monitor-api --human
```

Experiment with removing unnecessary packages or using `--no-install-recommends` to reduce image size.

