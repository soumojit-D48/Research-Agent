# Git Push Guide - AI Research Agent (Updated)

Follow these steps sequentially to push your code to GitHub.

## Prerequisites
```bash
git init
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

---

## Step 1: Core Config & Base Files

```bash
git add server/.gitignore server/README.md server/SETUP.md server/API_TESTING.md
git commit -m "Add gitignore, README, setup guide, and API testing docs"
```

---

## Step 2: Environment & Docker

```bash
git add server/.env.example server/Dockerfile server/docker-compose.yml
git commit -m "Add env template and Docker configuration"
```

---

## Step 3: Requirements & Setup

```bash
git add server/requirements.txt server/setup.py
git commit -m "Add Python dependencies and setup"
```

---

## Step 4: Alembic Migrations

```bash
git add server/alembic.ini server/alembic/
git commit -m "Add Alembic configuration and migrations"
```

---

## Step 5: Core Application

```bash
git add server/app/main.py server/app/core/
git commit -m "Add FastAPI app with config, exceptions, error handlers"
```

---

## Step 6: Database Layer

```bash
git add server/app/db/
git commit -m "Add database session, models, and base"
```

---

## Step 7: Models & Schemas

```bash
git add server/app/models/ server/app/schemas/
git commit -m "Add SQLAlchemy models and Pydantic schemas"
```

---

## Step 8: CRUD Operations

```bash
git add server/app/crud/
git commit -m "Add database CRUD operations"
```

---

## Step 9: API Routes

```bash
git add server/app/api/
git commit -m "Add API routes: research and conversations endpoints"
```

---

## Step 10: Services

```bash
git add server/app/services/
git commit -m "Add services: web search, vector store, cache"
```

---

## Step 11: Research Agent

```bash
git add server/app/agents/
git commit -m "Add LangGraph research agent with 5-stage workflow"
```

---

## Step 12: Tasks & Utils

```bash
git add server/app/tasks/ server/app/utils/ server/app/tools/ server/app/tests/
git commit -m "Add Celery tasks, utilities, tools, and tests"
```

---

## Push to GitHub

```bash
git push -u origin main
```

---

## Files Summary

| Step | Files | Commit Message |
|------|-------|----------------|
| 1 | .gitignore, README.md, SETUP.md, API_TESTING.md | Add gitignore, README, setup guide, and API testing docs |
| 2 | .env.example, Dockerfile, docker-compose.yml | Add env template and Docker configuration |
| 3 | requirements.txt, setup.py | Add Python dependencies and setup |
| 4 | alembic.ini, alembic/ | Add Alembic configuration and migrations |
| 5 | main.py, core/ | Add FastAPI app with config, exceptions, error handlers |
| 6 | db/ | Add database session, models, and base |
| 7 | models/, schemas/ | Add SQLAlchemy models and Pydantic schemas |
| 8 | crud/ | Add database CRUD operations |
| 9 | api/ | Add API routes: research and conversations endpoints |
| 10 | services/ | Add services: web search, vector store, cache |
| 11 | agents/ | Add LangGraph research agent with 5-stage workflow |
| 12 | tasks/, utils/, tools/, tests/ | Add Celery tasks, utilities, tools, and tests |

---

## What Was Fixed/Updated

1. **Alembic config** - Added alembic.ini with proper settings
2. **Database** - Fixed asyncpg connection for Neon PostgreSQL
3. **Vector Store** - Fixed Pinecone integration with proper API key loading
4. **Web Search** - Fixed DuckDuckGo URL extraction
5. **Config** - Fixed .env path for production
6. **Research Agent** - Added fallback when Pinecone fails

---

## ⚠️ Important: Don't Push These

- `.env` - Contains your API keys
- `.venv/` - Virtual environment
- `__pycache__/` - Python cache
- `*.log` - Log files
- `log.txt` - Your log file
