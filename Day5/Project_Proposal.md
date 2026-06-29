# Projet Final — DevOps Monitoring Dashboard
### Python from Beginner to Practitioner for DevOps — SupdeVinci

## Titre du projet

**DevOps Monitoring Dashboard** — un système de monitoring temps réel, construit entièrement en Python, containerisé avec Docker, et déployé sur Azure via un pipeline CI/CD GitHub Actions.

---



## Architecture cible

```
GitHub Repository
       │
       ▼  push to main
GitHub Actions CI/CD
  ├── lint (flake8)
  ├── test (pytest --cov ≥ 75 %)
  ├── build & push → Azure Container Registry (ACR)
  └── deploy → Azure Container Apps
       │
       ▼
Azure Container Apps Environment
  ├── devops-monitor-api  (FastAPI — port 8000)
  │   ├── GET  /health                  ← liveness probe
  │   ├── GET  /metrics                 ← CPU, mémoire, disque (psutil)
  │   ├── WS   /ws/metrics              ← stream JSON toutes les secondes
  │   ├── POST /servers                 ← enregistrer un serveur (API key)
  │   ├── GET  /servers                 ← lister les serveurs + statut
  │   ├── DELETE /servers/{id}          ← supprimer un serveur (API key)
  │   └── POST /servers/{id}/check      ← déclencher un health check manuel
  │
  └── devops-monitor-dashboard  (Streamlit — port 8501)
      ├── Onglet Métriques : KPIs + graphique live (fenêtre 60 s)
      └── Onglet Serveurs : tableau coloré + formulaire d'enregistrement
```

---

## Stack technique

| Couche | Technologie |
|--------|-------------|
| Langage | Python 3.11 |
| Framework API | FastAPI + Uvicorn (ASGI) |
| Frontend | Streamlit |
| Client HTTP async | httpx |
| Métriques système | psutil |
| Authentification | API Key (`X-API-Key` header) |
| Containerisation | Docker, Docker Compose |
| Tests | pytest, FastAPI TestClient |
| Versioning | Git, GitHub |
| CI/CD | GitHub Actions |
| Registry | Azure Container Registry |
| Hosting | Azure Container Apps |

---

## Structure complète du dépôt

Un dépôt propre et reproductible est une exigence du projet au même titre que le code. Voici la structure attendue à la soumission finale :

```
devops-monitor/
│
├── api/                          # Backend FastAPI
│   ├── __init__.py
│   ├── main.py                   # App, lifespan, routes, WebSocket
│   ├── models.py                 # Dataclass Server + schémas Pydantic
│   ├── auth.py                   # Dépendance API key
│   ├── metrics.py                # get_system_metrics() via psutil
│   ├── poller.py                 # Boucle async de polling
│   └── Dockerfile                # Build multi-stage
│
├── dashboard/                    # Frontend Streamlit
│   ├── app.py
│   └── Dockerfile
│
├── tests/
│   ├── test_metrics.py
│   └── test_routes.py
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml             # lint → test → build → deploy
│
├── docker-compose.yml            # Stack locale complète avec healthcheck
├── .dockerignore                 # Exclure .venv, __pycache__, .env, .git
├── .env.example                  # Template des variables d'environnement
├── Makefile                      # Commandes standardisées du projet
├── requirements.txt              # Dépendances Python (api + dashboard)
├── README.md                     # Documentation principale
└── CONTRIBUTING.md               # Conventions de contribution (optionnel)
```

> `.env` ne doit **jamais** être commité. Seul `.env.example` (sans valeurs sensibles) est versionné.

---

## Fichiers obligatoires — détail

### `README.md`

Le README est la carte d'identité du projet. Un relecteur doit pouvoir cloner le repo et lancer la stack en moins de 5 minutes en le suivant. Il doit contenir :

- Description du projet en 2–3 lignes
- Architecture (schéma ou liste des services)
- Prérequis (Python 3.11, Docker, Make)
- Instructions de lancement local :
  ```bash
  cp .env.example .env   # remplir les valeurs
  make up                # démarre la stack
  make test              # lance les tests
  ```
- URLs live (API et Dashboard) une fois déployé sur Azure
- Variables d'environnement expliquées

### `requirements.txt`

Liste toutes les dépendances Python avec des versions épinglées :

```
fastapi==0.111.0
uvicorn[standard]==0.29.0
pydantic==2.7.0
psutil==5.9.8
httpx==0.27.0
python-jose[cryptography]==3.3.0
streamlit==1.35.0
pandas==2.2.2
pytest==8.2.0
pytest-cov==5.0.0
```

Des versions non épinglées (`fastapi>=0.100`) rendent le projet non reproductible dans 6 mois.

### `Makefile`

Interface unifiée pour toutes les commandes du projet. Tout le monde — et la CI — utilise les mêmes commandes :

| Cible | Commande réelle |
|-------|-----------------|
| `make up` | `docker compose up --build -d` |
| `make down` | `docker compose down -v` |
| `make logs` | `docker compose logs -f` |
| `make test` | `pytest tests/ -v --cov=api --cov-fail-under=75` |
| `make lint` | `flake8 api/ dashboard/ tests/` |
| `make dev` | Lance l'API et le dashboard sans Docker (dev local) |

### `docker-compose.yml`

Orchestre les deux services localement. Points obligatoires :

- Le service `dashboard` se connecte à l'API via `http://api:8000` (nom de service Docker), **jamais** `localhost`
- Healthcheck sur le service `api` (`GET /health`)
- `depends_on: condition: service_healthy` sur le `dashboard`
- Variables d'environnement chargées depuis `.env` via `env_file: .env`

### `.env.example`

Template versionné des variables d'environnement, sans aucune valeur sensible :

```bash
# Copier ce fichier en .env et remplir les valeurs
API_KEY=                        # clé d'accès à l'API (choisir une valeur)
API_BASE_URL=http://api:8000    # URL de l'API vue par le dashboard (Docker)
```

### `.dockerignore`

Empêche de copier des fichiers inutiles dans le contexte de build (ralentit le build et gonfle les images) :

```
.venv/
__pycache__/
*.pyc
*.pyo
.env
.git/
.github/
tests/
*.md
```

### `api/Dockerfile` — build multi-stage

Deux stages : `builder` installe les dépendances dans un répertoire isolé, `runtime` copie uniquement ce répertoire et le code source. L'image finale ne contient pas pip, les headers de compilation, ni les dépendances de dev.

### `dashboard/Dockerfile`

Build single-stage. Installe uniquement les dépendances runtime (streamlit, httpx, pandas).

### `.github/workflows/ci-cd.yml`

Pipeline en 3 jobs chaînés :

```
test  ──►  build  ──►  deploy
           (main only)  (main only)
```

- `test` : s'exécute sur chaque push et PR — lint flake8 + pytest avec coverage
- `build` : construit les deux images Docker et les pousse vers ACR
- `deploy` : met à jour les deux Azure Container Apps via `az containerapp update`
- Les credentials Azure (`AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`, `ACR_NAME`) sont dans les **GitHub Secrets** — jamais dans le YAML

---

## Partie 1

### Ce que vous devez construire

**`api/metrics.py`** — une fonction `get_system_metrics() -> dict` qui retourne un snapshot CPU/mémoire/disque via `psutil`. Utiliser `interval=None` (non-bloquant).

**`api/auth.py`** — une dépendance FastAPI `verify_api_key` basée sur `APIKeyHeader`. La clé est chargée depuis la variable d'environnement `API_KEY`. Retourne 403 si absente ou invalide.

**`api/models.py`** — un `@dataclass Server` avec `id`, `name`, `host`, `port`, `status` et une méthode `base_url()`. Des modèles Pydantic `ServerIn` / `ServerOut` pour les routes (valider que `port` est entre 1 et 65535).

**`api/poller.py`** — `poll_server()` qui teste `GET /health` d'un serveur et met à jour son statut (`UP` / `DEGRADED` / `DOWN`), et `run_poll_loop()` qui tourne en boucle toutes les 10 secondes via `asyncio.gather`.

**`api/main.py`** — l'app FastAPI complète avec lifespan (démarre `run_poll_loop` au startup), toutes les routes listées dans l'architecture, et l'endpoint WebSocket qui streame les métriques toutes les secondes en gérant `WebSocketDisconnect`.

**`dashboard/app.py`** — deux onglets : Métriques (`st.cache_data`, `st.metric`, `st.line_chart`, `st.session_state`, `st.rerun`) et Serveurs (`st.dataframe` coloré, `st.form` d'enregistrement).

**`tests/`** — `test_metrics.py` (champs présents, valeurs 0–100) et `test_routes.py` (health, métriques, auth 403, création 201, 404).

### Critères d'acceptation

- [ ] `GET /health` retourne `{"status": "ok"}`
- [ ] `GET /metrics` contient `cpu_percent`, `memory_percent`, `disk_percent`
- [ ] `POST /servers` sans `X-API-Key` retourne 403
- [ ] `GET /servers` liste les serveurs avec leur statut
- [ ] `WS /ws/metrics` envoie un frame JSON toutes les secondes
- [ ] Le dashboard Streamlit affiche les KPIs et le graphique live
- [ ] Le tableau des serveurs est coloré par statut
- [ ] `make test` passe avec coverage ≥ 75 %

---

## Partie 2 — Déploiement Azure 

### Ce que vous devez construire

**Dockerfiles** — multi-stage pour l'API (image légère sans outils de build), single-stage pour le dashboard.

**`docker-compose.yml`** — stack locale complète avec healthcheck, `depends_on`, et communication inter-services par nom de service.

**`ci-cd.yml`** — pipeline 3 jobs : test → build → deploy, avec conditions sur `main` et credentials dans les Secrets.

**Infra Azure** — à provisionner en Jour 5 AM :
```bash
# Groupe de ressources
az group create --name devops-monitor-rg --location westeurope

# Azure Container Registry
az acr create --name <votre-acr> --resource-group devops-monitor-rg --sku Basic

# Container Apps Environment
az containerapp env create \
  --name devops-monitor-env \
  --resource-group devops-monitor-rg \
  --location westeurope

# Déploiement initial des deux apps
az containerapp create --name devops-monitor-api ...
az containerapp create --name devops-monitor-dashboard ...
```

**GitHub Secrets à configurer :**

| Secret | Contenu |
|--------|---------|
| `AZURE_CLIENT_ID` | App registration client ID |
| `AZURE_CLIENT_SECRET` | App registration secret |
| `AZURE_TENANT_ID` | Azure tenant ID |
| `AZURE_SUBSCRIPTION_ID` | Subscription ID |
| `ACR_NAME` | Nom du registry (sans `.azurecr.io`) |
| `API_KEY` | Clé d'API injectée dans les Container Apps |

### Critères d'acceptation

- [ ] `make up` démarre la stack sans erreur
- [ ] Le dashboard dans Docker se connecte à l'API via `http://api:8000`
- [ ] Le pipeline CI passe sur chaque push et PR
- [ ] Les images sont poussées vers ACR après merge sur `main`
- [ ] Les deux Container Apps se mettent à jour automatiquement après un push
- [ ] `GET https://<api-url>/health` retourne `{"status": "ok"}` depuis internet
- [ ] Le dashboard Streamlit live affiche des métriques réelles
- [ ] Le WebSocket fonctionne depuis l'URL Azure
- [ ] Le `README.md` contient les URLs live et les instructions de setup (clone → run en < 5 min)
- [ ] Le dépôt est tagué `v1.0.0`

---


## Barème détaillé

### Partie 1 — MVP local 

| Critère | Points |
|---------|--------|
| Tous les endpoints API fonctionnels (`/health`, `/metrics`, `/servers` CRUD) | 30 |
| WebSocket `/ws/metrics` qui envoie des frames JSON | 20 |
| Dashboard Streamlit connecté et fonctionnel | 20 |
| Couverture de tests ≥ 75 % | 15 |
| Qualité du code (type hints, docstrings, structure modulaire) | 15 |
| **Total** | **100** |

### Partie 2 — Déploiement Azure 

| Critère | Points |
|---------|--------|
| Stack Docker Compose fonctionnelle (`make up`) | 10 |
| Pipeline CI : lint + test passent sur chaque push | 15 |
| Pipeline CD : déploiement automatique sur push `main` | 20 |
| API et Dashboard live et accessibles sur Azure | 20 |
| WebSocket fonctionnel depuis l'URL Azure | 10 |
| Repo propre : README complet, `.env.example`, Makefile, structure lisible | 25 |
| **Total** | **100** |

---

## Soumission

À remettre avant la fin du Jour 5 :

1. **URL du dépôt GitHub** (public ou partagé avec l'instructeur)
2. **URL de l'API live** — `https://<api>.<env>.azurecontainerapps.io/docs`
3. **URL du Dashboard live** — `https://<dashboard>.<env>.azurecontainerapps.io`
4. **Screenshot** du dashboard Streamlit live avec des métriques réelles

Le dépôt Github doit contenir tout le code source, les Dockerfiles, le workflow CI/CD, le Makefile et la documentation. Ne jamais commiter `.env`, des secrets ou des credentials.

---

## Critères qualitatifs

Au-delà du barème, l'instructeur évaluera :

- **Reproductibilité** — `git clone` + `cp .env.example .env` + `make up` suffit à lancer la stack. Si ce n'est pas le cas, des points sont retirés.
- **Propreté du repo** — pas de fichiers inutiles, pas de code commenté oublié, `.gitignore` correct, commits en Conventional Commits
- **Sécurité** — aucun secret dans le code ou dans Git, API key dans les variables d'environnement
- **Fiabilité** — le déploiement Azure reste opérationnel et répond aux requêtes au moment de l'évaluation

---

## Conseils

- Committer régulièrement en Conventional Commits (`feat:`, `fix:`, `test:`, `ci:`, `docs:`).
- Écrire le `README.md` au fur et à mesure, pas à la dernière minute.
- Faire passer les tests dès le Jour 3 — ne pas attendre le Jour 5.
- Ne jamais utiliser `localhost` dans `docker-compose.yml` — les services se parlent par nom de service.
- Utiliser `make logs` pour déboguer les erreurs de démarrage des conteneurs.
- Tester `docker compose up` localement avant de configurer Azure.

