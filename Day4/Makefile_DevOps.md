# Makefile for DevOps



A `Makefile` gives your project a standard command interface. Instead of remembering long docker/uvicorn/pytest commands, everyone (and CI) uses the same short commands.

```makefile
.PHONY: install test lint build up down clean deploy

# ── Local development ─────────────────────────────────────────────────────

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=api --cov-report=term-missing

lint:
	black --check api/ dashboard/ tests/
	flake8 api/ dashboard/ tests/

format:
	black api/ dashboard/ tests/

run-api:
	uvicorn api.main:app --reload --port 8000

run-dashboard:
	streamlit run dashboard/app.py

# ── Docker ────────────────────────────────────────────────────────────────

build:
	docker compose build

up: build
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

clean:
	docker compose down --rmi all --volumes

# ── Azure deployment ──────────────────────────────────────────────────────

deploy: build
	az acr login --name $(ACR_NAME)
	docker tag devops-monitor-api $(ACR_NAME).azurecr.io/devops-monitor-api:$(TAG)
	docker tag devops-monitor-dashboard $(ACR_NAME).azurecr.io/devops-monitor-dashboard:$(TAG)
	docker push $(ACR_NAME).azurecr.io/devops-monitor-api:$(TAG)
	docker push $(ACR_NAME).azurecr.io/devops-monitor-dashboard:$(TAG)
```

Usage:
```bash
make install     # set up dependencies
make lint        # check formatting and style
make test        # run the test suite
make up          # build and start the full stack
make down        # stop everything
make deploy TAG=v1.0.0 ACR_NAME=devopsmonitoracr
```
