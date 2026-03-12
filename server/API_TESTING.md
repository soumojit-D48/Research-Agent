# API Testing Guide - AI Research Agent

## Running the Server

```bash
cd server
uvicorn app.main:app --reload
```

Server runs at: **http://127.0.0.1:8000**

---

## Swagger UI

Access the interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## API Endpoints

### 1. Health Check

**GET** `/health`

Check if the server is running.

```bash
curl http://127.0.0.1:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

---

### 2. Run Research Agent

**POST** `/api/v1/research/run`

Start a research task. This is the main endpoint.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | string | Yes | The research question |
| `user_id` | string | Yes | User identifier |

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/research/run?query=What%20is%20AI%20agents?&user_id=user123"
```

**Response:**
```json
{
  "status": "success",
  "conversation_id": "uuid-here",
  "report": "Your comprehensive research report...",
  "search_results": 15
}
```

**Using Swagger UI:**
1. Go to http://127.0.0.1:8000/docs
2. Click on `POST /api/v1/research/run`
3. Click **Try it out**
4. Enter parameters:
   - `query`: "What is artificial intelligence?"
   - `user_id`: "test-user-1"
5. Click **Execute**

---

### 3. Create Conversation

**POST** `/api/v1/research/conversations`

Create a new conversation.

**Request Body:**
```json
{
  "user_id": "user123",
  "session_id": "session-456",
  "messages": [
    {
      "role": "user",
      "content": "Hello"
    }
  ],
  "metadata": {}
}
```

---

### 4. Get Conversation

**GET** `/api/v1/research/conversations/{conversation_id}`

Get a conversation by ID.

**Example:**
```bash
curl http://127.0.0.1:8000/api/v1/research/conversations/{conversation_id}
```

---

### 5. Get User Conversations

**GET** `/api/v1/research/conversations/user/{user_id}`

Get all conversations for a user.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Max records to return (default: 10)

**Example:**
```bash
curl "http://127.0.0.1:8000/api/v1/research/conversations/user/user123?limit=5"
```

---

### 6. Add Message to Conversation

**POST** `/api/v1/research/conversations/{conversation_id}/messages`

Add a message to an existing conversation.

**Request Body:**
```json
{
  "role": "user",
  "content": "Tell me more about AI"
}
```

---

### 7. Delete Conversation

**DELETE** `/api/v1/research/conversations/{conversation_id}`

Delete a conversation.

---

### 8. Get Agent Logs

**GET** `/api/v1/research/logs/{conversation_id}`

Get agent execution logs for a conversation.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Max records to return (default: 100)

---

## Testing with Python

```python
import requests

# Run research
response = requests.post(
    "http://127.0.0.1:8000/api/v1/research/run",
    params={
        "query": "What is machine learning?",
        "user_id": "test-user"
    }
)
print(response.json())
```

---

## Testing with JavaScript/Fetch

```javascript
// Run research
fetch('http://127.0.0.1:8000/api/v1/research/run?query=What%20is%20AI%20agents?&user_id=user123', {
    method: 'POST'
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## Quick Test Commands

```bash
# Health check
curl http://127.0.0.1:8000/health

# Run research
curl -X POST "http://127.0.0.1:8000/api/v1/research/run?query=What%20is%20Python?&user_id=test"

# Get user conversations
curl "http://127.0.0.1:8000/api/v1/research/conversations/user/test"
```

---

## Notes

- The research endpoint may take 10-30 seconds to complete
- Responses include a `conversation_id` for tracking
- All endpoints require valid parameters
- Check `/docs` for full interactive documentation
