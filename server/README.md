# AI Research Agent

An AI-powered research agent built with FastAPI, LangGraph, and modern ML tools. It autonomously researches topics by generating search queries, fetching web content, and synthesizing comprehensive reports.

## Features

- **LangGraph Workflow**: Multi-stage research pipeline (query generation → web search → content extraction → report synthesis)
- **Vector Storage**: Pinecone-powered semantic search
- **Async Processing**: Celery workers for background task execution
- **REST API**: FastAPI-based endpoints with automatic OpenAPI docs
- **PostgreSQL**: Persistent storage for conversations and agent logs
- **Redis**: Caching and message broker for Celery

## Tech Stack

- **Backend**: FastAPI
- **Agent Framework**: LangGraph
- **LLM**: OpenRouter (nvidia/nemotron-nano-12b-v2-vl:free)
- **Database**: PostgreSQL with SQLAlchemy async
- **Task Queue**: Celery with Redis
- **Vector Store**: Pinecone
- **Migration**: Alembic

## Project Structure

```
server/
├── app/
│   ├── agents/          # Research agent implementation
│   ├── api/routes/      # API endpoints
│   ├── core/            # Config, exceptions, error handlers
│   ├── crud/            # Database operations
│   ├── db/              # Database session & base
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Web search, vector store, cache
│   ├── tasks/           # Celery tasks
│   └── main.py          # FastAPI app entry point
├── alembic/             # Database migrations
├── docker-compose.yml   # Docker services
├── Dockerfile           # Container build
├── requirements.txt     # Python dependencies
└── .env.example         # Environment template
```

## Setup

### Prerequisites

- Python 3.13+
- PostgreSQL
- Redis
- Pinecone account

### Installation

1. **Clone and navigate to server directory**
   ```bash
   cd server
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENROUTER_API_KEY` | API key for LLM (openrouter.ai) |
| `PINECONE_API_KEY` | Pinecone vector database key |
| `PINECONE_ENVIRONMENT` | Pinecone environment |
| `HUGGINGFACE_API_KEY` | HuggingFace API key |
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection URL |
| `CELERY_BROKER_URL` | Celery broker (Redis) |
| `CELERY_RESULT_BACKEND` | Celery results backend |

## Running the Application

### Local Development

**Using FastAPI (recommended)**
```bash
uvicorn app.main:app --reload
```

**Using Docker Compose**
```bash
docker-compose up --build
```

### Docker Services

| Service | Port | Description |
|---------|------|-------------|
| API | 8000 | FastAPI application |
| PostgreSQL | 5432 | Database |
| Redis | 6379 | Cache/Broker |
| Flower | 5555 | Celery monitoring |

## API Endpoints

### Research

- `POST /api/v1/research` - Start a research task
- `GET /api/v1/research/{task_id}` - Get research status

### Conversations

- `POST /api/v1/conversations` - Create conversation
- `GET /api/v1/conversations` - List conversations
- `GET /api/v1/conversations/{id}` - Get conversation

### Health

- `GET /health` - Health check
- `GET /` - Root endpoint

## Agent Workflow

```
initialize → generate_queries → web_search → extract_content → synthesize_report
```

1. **Initialize**: Create conversation record
2. **Generate Queries**: LLM creates 3-5 search queries
3. **Web Search**: Fetch results from web
4. **Extract Content**: Store in Pinecone, retrieve relevant docs
5. **Synthesize Report**: Generate final research report

## License

MIT
