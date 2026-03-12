# Research Agent

AI-powered research agent built with FastAPI and LangGraph.

## Project Structure

```
reseach_agent/
└── server/                 # Backend API
    ├── app/                 # Application code
    │   ├── agents/          # Research agent (LangGraph)
    │   ├── api/routes/      # REST endpoints
    │   ├── core/            # Config & exceptions
    │   ├── services/       # Web search, vector store
    │   └── ...
    ├── docker-compose.yml  # Docker services
    ├── requirements.txt     # Python dependencies
    └── README.md            # Detailed server documentation
```

## Quick Start

### Prerequisites

- Python 3.13+
- PostgreSQL
- Redis
- Pinecone account

### Setup

1. **Navigate to server**
   ```bash
   cd server
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Add your API keys
   ```

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

Or with Docker:
```bash
cd server && docker-compose up --build
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| API | 8000 | FastAPI application |
| PostgreSQL | 5432 | Database |
| Redis | 6379 | Cache & message broker |
| Flower | 5555 | Celery monitoring |

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Architecture

The research agent uses a LangGraph workflow:

```
initialize → generate_queries → web_search → extract_content → synthesize_report
```

- **LLM**: OpenRouter (nvidia/nemotron-nano-12b-v2-vl:free)
- **Vector Store**: Pinecone
- **Task Queue**: Celery with Redis

## License

MIT
