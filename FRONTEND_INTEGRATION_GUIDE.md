# Frontend Integration Guide - AI Research Agent

## Project Overview

Build a **Next.js + TypeScript + Tailwind** frontend for an AI Research Agent API. The app allows users to research topics by submitting queries, and the backend autonomously generates search queries, fetches web content, and synthesizes comprehensive reports.

---

## Backend Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Agent**: LangGraph (research workflow)
- **LLM**: OpenRouter (nvidia/nemotron-nano-12b-v2-vl:free)
- **Vector Store**: Pinecone

---

## API Base URL

```
Development: http://localhost:8000/api/v1
Production:  https://your-api-domain.com/api/v1
```

---

## API Endpoints

### 1. Health Check

**GET** `/health`

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

### 2. Run Research

**POST** `/research/run`

Query Parameters:
- `query` (string, required) - The research question/topic
- `user_id` (string, required) - User identifier

Request Example:
```
POST /api/v1/research/run?query=What is machine learning?&user_id=user123
```

Response:
```json
{
  "status": "success",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "report": "Machine learning is a subset of artificial intelligence...",
  "search_results": 15
}
```

### 3. Create Conversation

**POST** `/research/conversations` or `/conversations`

Request Body:
```json
{
  "user_id": "user123",
  "session_id": "optional-session-id",
  "messages": [
    { "role": "user", "content": "Hello" }
  ],
  "conversation_metadata": {
    "source": "web"
  }
}
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user123",
  "session_id": "optional-session-id",
  "messages": [
    { "role": "user", "content": "Hello" }
  ],
  "conversation_metadata": { "source": "web" },
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### 4. Get Conversation by ID

**GET** `/research/conversations/{id}` or `/conversations/{id}`

Response: Same as Create Conversation response

### 5. Get User Conversations

**GET** `/research/conversations/user/{user_id}` or `/conversations/user/{user_id}`

Query Parameters:
- `skip` (int, default=0) - Pagination offset
- `limit` (int, default=10) - Pagination limit

Response:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user123",
    "session_id": "session-1",
    "messages": [...],
    "conversation_metadata": {},
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

### 6. Add Message to Conversation

**POST** `/research/conversations/{id}/messages` or `/conversations/{id}/messages`

Request Body:
```json
{
  "role": "user",
  "content": "What is deep learning?",
  "metadata": {}
}
```

Response: Updated conversation object

### 7. Delete Conversation

**DELETE** `/research/conversations/{id}` or `/conversations/{id}`

Response:
```json
{
  "status": "deleted",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 8. Get Agent Logs

**GET** `/research/logs/{conversation_id}` or `/conversations/{conversation_id}/logs`

Query Parameters:
- `skip` (int, default=0)
- `limit` (int, default=100)

Response:
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
    "agent_type": "research",
    "action": "generate_queries",
    "input_data": { "query": "What is machine learning?" },
    "output_data": { "queries": ["query1", "query2"] },
    "execution_time": 1500,
    "status": "success",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

## Data Models

### Conversation
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| user_id | string | User identifier |
| session_id | string | Session identifier |
| messages | JSON Array | `[{role: "user"|"assistant", content: "..."}]` |
| conversation_metadata | JSON | Custom metadata |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update |

### AgentLog
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| conversation_id | UUID | Foreign key |
| agent_type | string | "research" |
| action | string | "initialize", "generate_queries", "web_search", "extract_content", "synthesize_report" |
| input_data | JSON | Input for the action |
| output_data | JSON | Output from the action |
| execution_time | int | Milliseconds |
| status | string | "success", "error" |
| created_at | datetime | Timestamp |

---

## Research Flow (User Perspective)

1. User enters a research query (e.g., "What is quantum computing?")
2. Frontend calls `POST /research/run?query=...&user_id=...`
3. Backend:
   - Creates a conversation
   - Generates 3-5 search queries via LLM
   - Searches DuckDuckGo for each query
   - Stores results in Pinecone vector DB
   - Retrieves relevant content
   - Synthesizes a comprehensive report
4. Frontend receives: conversation_id, final_report, search_results count
5. User can view their conversation history via `/conversations/user/{user_id}`

---

## Frontend Recommended Features

### Pages
1. **Home** - Search input to submit research queries
2. **Research Result** - Display the generated report
3. **History** - List of user's past conversations
4. **Conversation Detail** - View a specific conversation with messages and logs

### Components
- SearchBar - Input for research queries
- ResearchCard - Display research result summary
- ConversationList - List of user's conversations
- MessageBubble - Display messages (user/assistant)
- LoadingSpinner - Show during research processing
- AgentLogViewer - Show agent execution steps

### State Management
- Use React Query or SWR for API calls
- Store user_id in localStorage or context

---

## Environment Variables (Frontend)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## API Documentation

Interactive docs available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Quick Start - Next.js Setup

```bash
npx create-next-app@latest frontend --typescript --tailwind --eslint
cd frontend

# Add API client utilities
# Create pages and components as described above
```

---

## Example API Client (TypeScript)

```typescript
// lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

interface ResearchResponse {
  status: string;
  conversation_id: string;
  report: string;
  search_results: number;
}

interface Conversation {
  id: string;
  user_id: string;
  session_id: string;
  messages: { role: string; content: string }[];
  conversation_metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export async function runResearch(query: string, userId: string): Promise<ResearchResponse> {
  const res = await fetch(`${API_URL}/research/run?query=${encodeURIComponent(query)}&user_id=${userId}`, {
    method: 'POST',
  });
  return res.json();
}

export async function getUserConversations(userId: string): Promise<Conversation[]> {
  const res = await fetch(`${API_URL}/conversations/user/${userId}`);
  return res.json();
}

export async function getConversation(id: string): Promise<Conversation> {
  const res = await fetch(`${API_URL}/conversations/${id}`);
  return res.json();
}
```

---

## Notes

- No authentication required for this version (user_id is passed directly)
- The `/conversations` and `/research/conversations` endpoints are identical - use either
- Research requests may take 10-30 seconds due to web searches and LLM processing
- Consider showing loading states during research execution
