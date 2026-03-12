# AI Research Agent - Setup Guide

A complete setup guide for running the AI Research Agent with cloud services (Neon PostgreSQL, Redis Cloud).

## Prerequisites

- Python 3.13+
- Neon account (https://neon.tech)
- Redis Cloud account (https://redis.io)
- Pinecone account (https://pinecone.io)
- OpenRouter account (https://openrouter.ai)

## Tech Stack

| Service | Purpose | Free Tier |
|---------|---------|------------|
| Neon | PostgreSQL Database | 0.5GB storage |
| Redis Cloud | Cache & Message Broker | 30MB |
| Pinecone | Vector Store | 1 index |
| OpenRouter | LLM API | Free credits |

---

## Step 1: Create Neon Database

1. Go to https://neon.tech and sign up
2. Create a new project:
   - Name: `ai-research-agent`
   - Region: Select closest to you
3. Once created, click **Connect** → **Node.js**
4. Copy the connection string. It looks like:
   ```
   postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
   ```
5. **Important:** Replace `/neondb` with your database name or keep as is for default

---

## Step 2: Create Redis Cloud

1. Go to https://redis.io and sign up for Redis Cloud
2. Create a free subscription:
   - Fixed: Free (30MB) - select this
3. Create a database:
   - Name: `ai-research-agent`
4. Copy the **Public Endpoint** URL, e.g.:
   ```
   redis://default:password@redis-cloud-host.redis.cloud:port
   ```

---

## Step 3: Get API Keys

### OpenRouter
1. Go to https://openrouter.ai
2. Sign up and go to Settings → API Keys
3. Create a new key

### Pinecone
1. Go to https://pinecone.io
2. Create a free account
3. Create an index named `research-agent`
4. Get your API Key from Keys section

---

## Step 4: Environment Setup

Navigate to the server directory:
```bash
cd server
```

Create the `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# ========================
# API Keys
# ========================
OPENROUTER_API_KEY=your_openrouter_key_here
HUGGINGFACE_API_KEY=your_huggingface_key_here
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_ENVIRONMENT=us-east-1

# ========================
# Database (Neon)
# ========================
# Replace with your Neon connection string (add ?sslmode=require at the end)
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require

# ========================
# Redis (Redis Cloud)
# ========================
REDIS_URL=redis://default:password@redis-host.redis.cloud:port

# ========================
# Celery
# ========================
CELERY_BROKER_URL=redis://default:password@redis-host.redis.cloud:port
CELERY_RESULT_BACKEND=redis://default:password@redis-host.redis.cloud:port

# ========================
# App Settings
# ========================
APP_ENV=development
DEBUG=True
API_PREFIX=/api/v1
PROJECT_NAME=AI Research Agent
VERSION=1.0.0

FRONTEND_URL=http://localhost:3000
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## Step 5: Install Dependencies

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

---

## Step 6: Run Database Migrations

```bash
alembic upgrade head
```

---

## Step 7: Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Health**: http://localhost:8000/health

---

## Step 8: Test the API

### Using curl:
```bash
curl -X POST "http://localhost:8000/api/v1/research/run?query=What%20is%20AI?&user_id=test-user"
```

### Using Swagger UI:
1. Open http://localhost:8000/docs
2. Click on `/api/v1/research/run`
3. Click **Try it out**
4. Fill in query and user_id
5. Click **Execute**

---

## Environment Variables Summary

| Variable | Description | Where to Get |
|----------|-------------|--------------|
| `OPENROUTER_API_KEY` | LLM API key | openrouter.ai |
| `PINECONE_API_KEY` | Vector store key | pinecone.io |
| `PINECONE_ENVIRONMENT` | Pinecone region | pinecone.io |
| `HUGGINGFACE_API_KEY` | HuggingFace (optional) | huggingface.co |
| `DATABASE_URL` | Neon PostgreSQL | neon.tech |
| `REDIS_URL` | Redis Cloud | redis.cloud |
| `CELERY_BROKER_URL` | Redis Cloud | redis.cloud |
| `CELERY_RESULT_BACKEND` | Redis Cloud | redis.cloud |

---

## Troubleshooting

### Connection Errors
- **PostgreSQL**: Ensure `?sslmode=require` is at the end of DATABASE_URL
- **Redis**: Check that your Redis Cloud allows external connections
- **Pinecone**: Make sure index exists and region matches

### Common Issues
- `asyncpg` requires `sslmode=require` for Neon
- Use pooled connections in Neon for better performance (`?sslmode=prefer&connection_limit=1`)

---

## Project Structure

```
server/
├── app/
│   ├── agents/          # Research agent (LangGraph)
│   ├── api/routes/      # FastAPI endpoints
│   ├── core/            # Config, exceptions
│   ├── crud/            # Database operations
│   ├── db/              # SQLAlchemy setup
│   ├── models/          # DB models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Web search, vector store
│   └── main.py          # FastAPI app
├── alembic/             # DB migrations
├── requirements.txt     # Python deps
└── .env                 # Your config
```

---

## License

MIT
