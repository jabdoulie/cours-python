# Docker for DevOps

### 1. Docker for Multi-Service Applications

#### Why Docker?

Without Docker, deploying your app means:
- Installing the right Python version on the target machine
- Installing all dependencies — hoping versions match
- Configuring environment variables manually
- Dealing with "works on my machine" bugs

Docker packages your application and **all its dependencies** into a portable image. Run it on any machine with Docker installed and it behaves identically.

**Core concepts:**

| Concept | Definition |
|---|---|
| **Image** | A read-only snapshot of your app + dependencies + OS layer |
| **Container** | A running instance of an image |
| **Dockerfile** | Instructions for building an image |
| **Registry** | A storage service for images (Docker Hub, Azure Container Registry) |
| **Layer** | Each `RUN`, `COPY`, `ADD` instruction adds a cached layer to the image |

---

#### The Dockerfile

A `Dockerfile` is a text file with instructions Docker executes top-to-bottom to build an image.

```
FROM python:3.11-slim        ← base image
WORKDIR /app                 ← set working directory inside the container
COPY requirements.txt .      ← copy one file
RUN pip install ...          ← execute a shell command
COPY . .                     ← copy the rest of the source
EXPOSE 8000                  ← document which port the app uses
CMD [...]                    ← default command when container starts
```

---

#### Multi-Stage Build for FastAPI

Multi-stage builds separate the dependency installation (heavy, slow) from the final runtime image (lean, fast):

```dockerfile
# ── Stage 1: install dependencies ─────────────────────────────────────────
FROM python:3.11-slim AS builder
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: runtime image ─────────────────────────────────────────────────
FROM python:3.11-slim
WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /install /usr/local

# Copy application source
COPY api/ ./api/

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

> The final image contains **no pip, no build tools, no cache** — only the runtime. This reduces attack surface and image size.

---

#### Dockerfile for Streamlit

```dockerfile
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dashboard/ ./dashboard/

EXPOSE 8501

# --server.address=0.0.0.0 is required so Streamlit binds to all interfaces
CMD ["streamlit", "run", "dashboard/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0"]
```

---

#### .dockerignore

Like `.gitignore` — tells Docker what to exclude from the build context. Always include this:

```
.venv/
__pycache__/
*.pyc
*.pyo
.git/
.env
.pytest_cache/
*.egg-info/
dist/
build/
```

Without `.dockerignore`, Docker copies `.venv/` (hundreds of MB) into the build context on every build.

---

#### Building and Running Images Manually

```bash
# Build the API image (run from project root)
docker build -t devops-monitor-api:latest -f api/Dockerfile .

# Build the dashboard image
docker build -t devops-monitor-dashboard:latest -f dashboard/Dockerfile .

# Run the API container
docker run -d \
  --name api \
  -p 8000:8000 \
  -e API_KEY=my-secret \
  devops-monitor-api:latest

# Run the dashboard container
docker run -d \
  --name dashboard \
  -p 8501:8501 \
  -e API_BASE=http://host.docker.internal:8000 \
  devops-monitor-dashboard:latest

# Inspect logs
docker logs -f api

# Open a shell inside a running container
docker exec -it api /bin/sh

# Stop and remove
docker stop api && docker rm api
```

> `host.docker.internal` resolves to the host machine's IP from inside a container — useful during local development before switching to Compose networking.

---

### 2. Docker Compose

Running multiple containers individually is tedious. Docker Compose defines your entire stack in a single `docker-compose.yml` file and manages them together.

#### docker-compose.yml

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
      - API_BASE=http://api:8000      # ← service name, not localhost
      - API_KEY=${API_KEY}
    depends_on:
      api:
        condition: service_healthy    # wait until API passes health check
    restart: unless-stopped
```

> Inside Docker Compose, services find each other by **service name** (`http://api:8000`), not `localhost`. Each service gets its own hostname on the shared Docker network.

#### .env file

```bash
# .env  — never commit this file
API_KEY=super-secret-ops-key
```

Compose automatically loads `.env` — reference variables with `${VAR_NAME}` in the YAML.

#### Common Compose Commands

```bash
# Build images and start all services in the background
docker compose up --build -d

# View logs for all services (follow mode)
docker compose logs -f

# View logs for one service
docker compose logs -f api

# Check container status
docker compose ps

# Stop all services (containers remain)
docker compose stop

# Stop and remove containers + networks
docker compose down

# Stop, remove containers, AND delete images
docker compose down --rmi all

# Rebuild a single service without restarting others
docker compose build api
docker compose up -d --no-deps api

# Run a one-off command in a service container
docker compose run --rm api pytest tests/
```

---

#### How Container Networking Works

```
┌─────────────────────────────────────────────────────┐
│  Docker Compose Network: devops-monitor_default      │
│                                                      │
│  ┌──────────────────┐     ┌──────────────────────┐  │
│  │  api             │     │  dashboard            │  │
│  │  hostname: api   │◀────│  API_BASE=            │  │
│  │  port: 8000      │     │  http://api:8000      │  │
│  └──────────────────┘     └──────────────────────┘  │
│          │                          │                │
└──────────┼──────────────────────────┼────────────────┘
           │ port 8000                │ port 8501
    ┌──────┴──────────────────────────┴──────┐
    │              Host machine              │
    └────────────────────────────────────────┘
```

---

#### Health Checks

A health check lets Docker know when a container is **truly ready** to accept traffic, not just started:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 10s      # how often to run the check
  timeout: 5s        # how long to wait for a response
  retries: 3         # how many failures before marking unhealthy
  start_period: 5s   # grace period after container starts
```

`depends_on` with `condition: service_healthy` ensures the dashboard only starts once the API is healthy — preventing startup race conditions.

---
