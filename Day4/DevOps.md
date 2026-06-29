# Git, Github, and Gihub Actions


### 1. Git & GitHub Flow

#### Why Version Control Matters in DevOps

- Every change is recorded — you can always roll back
- Multiple people can work in parallel without overwriting each other
- CI/CD pipelines trigger on Git events (push, PR)
- Tags map code versions to deployments

#### GitHub Flow

A simple, deployment-friendly branching strategy:

```
main  ──────────────────────────────────────────────▶  always deployable
         │                              │
         └── feat/websocket-stream ─────┘  PR → review → squash merge
         └── fix/auth-header-bug ────────┘  PR → review → squash merge
```

1. `main` is **always in a deployable state**
2. Create a branch for every piece of work: `feat/`, `fix/`, `ci/`, `docs/`
3. Push the branch and open a Pull Request
4. CI runs automatically on the PR
5. After code review, squash-merge into `main`
6. Deployment triggers automatically

#### Essential Git Commands

```bash
# Start a new feature
git checkout -b feat/streamlit-dashboard

# Stage and commit
git add api/main.py tests/test_routes.py
git commit -m "feat: add WebSocket metrics endpoint"

# Push the branch
git push origin feat/streamlit-dashboard

# Keep your branch up to date with main
git fetch origin
git rebase origin/main

# After the PR is merged — clean up locally
git checkout main
git pull origin main
git branch -d feat/streamlit-dashboard

# Tag a release
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

#### Conventional Commits

A standard format that makes commit history readable and enables automated changelogs:

| Prefix | When to use |
|---|---|
| `feat:` | A new feature |
| `fix:` | A bug fix |
| `test:` | Adding or updating tests |
| `ci:` | CI/CD pipeline changes |
| `docs:` | Documentation only |
| `refactor:` | Code change that's not a fix or feature |
| `chore:` | Dependency updates, tooling |

Examples:
```
feat: add WebSocket metrics streaming endpoint
fix: handle WebSocketDisconnect without logging traceback
test: add test for POST /servers with missing API key
ci: add coverage threshold check to GitHub Actions
docs: add local setup instructions to README
```

---

### 2. GitHub Actions — CI/CD Pipeline

GitHub Actions is a workflow automation platform built into GitHub. Every push, PR, or tag can trigger a workflow.

#### Core Concepts

| Concept | Definition |
|---|---|
| **Workflow** | A YAML file in `.github/workflows/` — triggered by events |
| **Event** | What triggers the workflow (`push`, `pull_request`, `schedule`) |
| **Job** | A group of steps that run on the same runner |
| **Step** | A single command or action |
| **Action** | A reusable step from the GitHub Marketplace (`actions/checkout@v4`) |
| **Runner** | The VM that executes the job (`ubuntu-latest`) |
| **Secret** | An encrypted variable stored in GitHub repo settings |

#### CI Workflow — Lint + Test

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Lint & Test
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Check formatting (Black)
        run: black --check api/ dashboard/ tests/

      - name: Lint (Flake8)
        run: flake8 api/ dashboard/ tests/ --max-line-length=88

      - name: Run tests with coverage
        run: pytest tests/ -v --cov=api --cov-fail-under=75
```

#### Full CI/CD Workflow — Build, Push, Deploy

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD — DevOps Monitor

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:

  # ── Job 1: Lint + Test ────────────────────────────────────────────────────
  test:
    name: Lint & Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - run: pip install -r requirements.txt

      - name: Lint
        run: |
          black --check api/ dashboard/ tests/
          flake8 api/ dashboard/ tests/ --max-line-length=88

      - name: Test
        run: pytest tests/ -v --cov=api --cov-fail-under=75

  # ── Job 2: Build & Push images (main branch only) ─────────────────────────
  build-and-push:
    name: Build & Push to ACR
    needs: test                          # only runs if test job passes
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'  # skip on PRs

    steps:
      - uses: actions/checkout@v4

      - name: Log in to Azure Container Registry
        uses: azure/docker-login@v1
        with:
          login-server: ${{ secrets.ACR_LOGIN_SERVER }}
          username: ${{ secrets.ACR_USERNAME }}
          password: ${{ secrets.ACR_PASSWORD }}

      - name: Build and push API image
        run: |
          docker build \
            -t ${{ secrets.ACR_LOGIN_SERVER }}/devops-monitor-api:${{ github.sha }} \
            -f api/Dockerfile .
          docker push ${{ secrets.ACR_LOGIN_SERVER }}/devops-monitor-api:${{ github.sha }}

      - name: Build and push Dashboard image
        run: |
          docker build \
            -t ${{ secrets.ACR_LOGIN_SERVER }}/devops-monitor-dashboard:${{ github.sha }} \
            -f dashboard/Dockerfile .
          docker push ${{ secrets.ACR_LOGIN_SERVER }}/devops-monitor-dashboard:${{ github.sha }}

  # ── Job 3: Deploy to Azure Container Apps ─────────────────────────────────
  deploy:
    name: Deploy to Azure
    needs: build-and-push
    runs-on: ubuntu-latest

    steps:
      - name: Log in to Azure
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Deploy API
        run: |
          az containerapp update \
            --name devops-monitor-api \
            --resource-group ${{ secrets.RG_NAME }} \
            --image ${{ secrets.ACR_LOGIN_SERVER }}/devops-monitor-api:${{ github.sha }}

      - name: Deploy Dashboard
        run: |
          az containerapp update \
            --name devops-monitor-dashboard \
            --resource-group ${{ secrets.RG_NAME }} \
            --image ${{ secrets.ACR_LOGIN_SERVER }}/devops-monitor-dashboard:${{ github.sha }}
```

#### Understanding the Job Chain

```
Push to main
    │
    ▼
┌─────────┐      passes      ┌──────────────────┐      passes      ┌────────┐
│  test   │ ───────────────▶ │ build-and-push   │ ───────────────▶ │ deploy │
│ lint    │                  │ docker build api │                  │ az     │
│ pytest  │                  │ docker build dash│                  │ update │
└─────────┘                  │ docker push both │                  └────────┘
     │                       └──────────────────┘
     │ fails
     ▼
  ✗ Pipeline stops — nothing is deployed
```

**`needs: test`** creates a dependency — `build-and-push` only runs if `test` passes. This prevents broken code from ever reaching production.

#### Setting Up GitHub Secrets

In your repo: **Settings → Secrets and variables → Actions → New repository secret**

| Secret | Value |
|---|---|
| `ACR_LOGIN_SERVER` | `devopsmonitoracr.azurecr.io` |
| `ACR_USERNAME` | From `az acr credential show` |
| `ACR_PASSWORD` | From `az acr credential show` |
| `AZURE_CREDENTIALS` | JSON output of `az ad sp create-for-rbac` |
| `RG_NAME` | `devops-monitor-rg` |
| `API_KEY` | Your chosen API key |

Generate Azure credentials:
```bash
az ad sp create-for-rbac \
  --name devops-monitor-sp \
  --role contributor \
  --scopes /subscriptions/<subscription-id>/resourceGroups/devops-monitor-rg \
  --sdk-auth
```
Copy the entire JSON output as the `AZURE_CREDENTIALS` secret.

