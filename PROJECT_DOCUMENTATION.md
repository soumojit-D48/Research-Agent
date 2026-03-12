# AI Research Agent - Project Documentation

## Overview

This is an **AI Research Agent Backend API** built with FastAPI. It uses LangGraph for workflow orchestration to autonomously research topics by generating search queries, fetching web content, and synthesizing comprehensive reports.

## Project Structure

```
reseach_agent/
├── server/
│   ├── app/
│   │   ├── agents/          # LangGraph research agent
│   │   ├── api/routes/     # REST API endpoints
│   │   ├── core/           # Config, exceptions, error handlers   ├── crud/           # Database operations
│   │   ├── db/
│   │             # Database session & base
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Web search, vector store, cache
│   │   ├── tasks/          # Celery tasks
│   │   └── main.py         # FastAPI entry point
│   ├── alembic/            # Database migrations
│   ├── docker-compose.yml  # Docker services
│   ├── requirements.txt    # Dependencies
│   └── .env                # Environment variables
```

## Technology Stack

| Category | Technology |
|----------|------------|
| Framework | FastAPI 0.127.0 |
| Agent Framework | LangGraph 1.0.5 |
| LLM | OpenRouter (nvidia/nemotron-nano-12b-v2-vl:free) |
| Database | PostgreSQL (async via SQLAlchemy 2.0) |
| Task Queue | Celery 5.6.0 |
| Message Broker | Redis 7 |
| Vector Store | Pinecone |
| Embeddings | HuggingFace (sentence-transformers/all-MiniLM-L6-v2) |
| Web Scraping | BeautifulSoup, httpx |

## Architecture Flow

### Research Agent Workflow

The Research Agent uses a **LangGraph StateGraph** with the following pipeline:

```
User Query
    │
    ▼
┌─────────────────┐
│  initialize     │ ──► Create conversation in database
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  generate_queries   │ ──► LLM generates 3-5 search queries
└────────┬────────────┘
         │
         ▼
┌─────────────────┐
│  web_search     │ ──► DuckDuckGo search for each query
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  extract_content    │ ──► Store in Pinecone, retrieve relevant docs
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  synthesize_report   │ ──► Generate final research report
└─────────────────────┘
         │
         ▼
    Final Report
```

### Key Components

1. **ResearchAgentV3** (`app/agents/research_agent.py`): Main agent that orchestrates the research workflow using LangGraph
2. **WebSearchService** (`app/services/web_search.py`): Handles DuckDuckGo searches and content fetching
3. **VectorStoreService** (`app/services/vector_store.py`): Pinecone integration for semantic search
4. **ConversationCRUD**: Database operations for conversations
5. **AgentLogCRUD**: Logging agent execution steps

## API Endpoints

### Base URL
```
http://localhost:8000/api/v1
```

### Health & Root Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check - returns API status, version, environment |
| GET | `/` | Root endpoint - returns API name, version, docs link |

### Research Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/research/run` | Run research agent with a query |
| POST | `/research/conversations` | Create a new conversation |
| GET | `/research/conversations/{id}` | Get conversation by ID |
| GET | `/research/conversations/user/{user_id}` | Get all conversations for a user |
| POST | `/research/conversations/{id}/messages` | Add a message to conversation |
| DELETE | `/research/conversations/{id}` | Delete a conversation |
| GET | `/research/logs/{conversation_id}` | Get agent logs for a conversation |

### Conversations Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/conversations` | Create a new conversation |
| GET | `/conversations/{id}` | Get conversation by ID |
| GET | `/conversations/user/{user_id}` | Get all conversations for a user |
| POST | `/conversations/{id}/messages` | Add a message to conversation |
| DELETE | `/conversations/{id}` | Delete a conversation |
| GET | `/conversations/{id}/logs` | Get agent logs for a conversation |

---

## Endpoint Details

### 1. POST `/research/run`

Run the research agent to generate a comprehensive report.

**Query Parameters:**
- `query` (string, required): The research question/topic
- `user_id` (string, required): The user identifier

**Response:**
```json
{
  "status": "success",
  "conversation_id": "uuid",
  "report": "full report text...",
  "search_results": 15
}
```

**Flow:**
1. Validates query and user_id
2. Creates ResearchAgentV3 instance
3. Executes LangGraph workflow
4. Returns conversation_id, final report, and search count

---

### 2. POST `/research/conversations` / POST `/conversations`

Create a new conversation.

**Request Body:**
```json
{
  "user_id": "user123",
  "session_id": "optional-session-id",
  "messages": [{"role": "user", "content":  "conversation_metadata "Hello"}],
": {"source": "web"}
}
```

**Response:** Conversation object with ID, timestamps

---

### 3. GET `/research/conversations/{id}` / GET `/conversations/{id}`

Get a conversation by its UUID.

**Path Parameters:**
- `id` (UUID): Conversation ID

**Response:** Conversation object

---

### 4. GET `/research/conversations/user/{user_id}` / GET `/conversations/user/{user_id}`

Get all conversations for a specific user.

**Path Parameters:**
- `user_id` (string): User identifier

**Query Parameters:**
- `skip` (int, default=0): Pagination offset
- `limit` (int, default=10): Pagination limit

**Response:** List of conversation objects

---

### 5. POST `/research/conversations/{id}/messages` / POST `/conversations/{id}/messages`

Add a message to an existing conversation.

**Path Parameters:**
- `id` (UUID): Conversation ID

**Request Body:**
```json
{
  "role": "user",
  "content": "What is machine learning?",
  "metadata": {}
}
```

**Response:** Updated conversation object

---

### 6. DELETE `/research/conversations/{id}` / DELETE `/conversations/{id}`

Delete a conversation.

**Path Parameters:**
- `id` (UUID): Conversation ID

**Response:**
```json
{
  "status": "deleted",
  "conversation_id": "uuid"
}
```

---

### 7. GET `/research/logs/{conversation_id}` / GET `/conversations/{id}/logs`

Get agent execution logs for a conversation.

**Path Parameters:**
- `conversation_id` (UUID): Conversation ID

**Query Parameters:**
- `skip` (int, default=0): Pagination offset
- `limit` (int, default=100): Pagination limit

**Response:** List of agent log objects

---

### 8. GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

---

### 9. GET `/`

Root endpoint.

**Response:**
```json
{
  "message": "AI Research Agent API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

## Database Models

### Conversation Table

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | String | User identifier (indexed) |
| session_id | String | Session identifier (indexed) |
| messages | JSON | Array of message objects |
| metadata | JSON | Custom metadata |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### AgentLog Table

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| conversation_id | UUID | Foreign key to conversation |
| agent_type | String | Type of agent (e.g., "research") |
| action | String | Action name (e.g., "generate_queries") |
| input_data | JSON | Input data for the action |
| output_data | JSON | Output data from the action |
| execution_time | Integer | Execution time in milliseconds |
| status | String | Status (success, error, timeout) |
| created_at | DateTime | Creation timestamp |

---

## Pydantic Schemas

### ConversationCreate
```python
{
  "user_id": str,
  "session_id": Optional[str],
  "messages": Optional[List[Dict]],
  "conversation_metadata": Optional[Dict]
}
```

### ConversationResponse
```python
{
  "id": UUID,
  "user_id": str,
  "session_id": str,
  "messages": List[Dict],
  "conversation_metadata": Dict,
  "created_at": datetime,
  "updated_at": datetime
}
```

### MessageAdd
```python
{
  "role": str,          # user, assistant, system
  "content": str,
  "metadata": Optional[Dict]
}
```

### AgentLogResponse
```python
{
  "id": UUID,
  "conversation_id": UUID,
  "agent_type": str,
  "action": str,
  "input_data": Dict,
  "output_data": Dict,
  "execution_time": int,
  "status": str,
  "created_at": datetime
}
```

---

## Running the Application

### Development
```bash
cd server
uvicorn app.main:app --reload
```

### Docker
```bash
docker-compose up --build
```

This starts:
- API on port 8000
- PostgreSQL on port 5432
- Redis on port 6379
- Flower (Celery monitoring) on port 5555

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| OPENROUTER_API_KEY | LLM API key |
| HUGGINGFACE_API_KEY | HuggingFace API key |
| PINECONE_API_KEY | Pinecone vector DB key |
| PINECONE_ENVIRONMENT | Pinecone environment |
| DATABASE_URL | PostgreSQL connection string |
| REDIS_URL | Redis URL |
| CELERY_BROKER_URL | Celery broker (Redis) |
| APP_ENV | Environment (development/production) |
| DEBUG | Debug mode (True/False) |

---

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
