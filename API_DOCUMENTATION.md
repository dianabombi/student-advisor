# CODEX RAG API Documentation

## Overview

The CODEX platform provides a comprehensive RAG (Retrieval-Augmented Generation) API for legal document analysis and intelligent chat consultation. The API enables semantic search across legal documents and context-aware responses using OpenAI's GPT models.

## Base URL

```
http://localhost:8001/api
```

## Authentication

All endpoints require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

---

## RAG Chat Endpoints

### POST /api/chat

Intelligent chat with RAG-powered context retrieval.

**Request Body:**

```json
{
  "message": "Aké sú podmienky platnosti zmluvy?",
  "history": [
    {
      "role": "user",
      "content": "Previous question"
    },
    {
      "role": "assistant",
      "content": "Previous answer"
    }
  ],
  "practice_area": "civil",
  "jurisdiction": "SK",
  "k": 5,
  "include_context": false
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `message` | string | Yes | User's question or message |
| `history` | array | No | Conversation history for context |
| `practice_area` | string | No | Filter by practice area (civil, criminal, etc.) |
| `jurisdiction` | string | No | Filter by jurisdiction (SK, EU, etc.) |
| `k` | integer | No | Number of document chunks to retrieve (default: 3, max: 10) |
| `include_context` | boolean | No | Include raw context in response (default: false) |

**Response:**

```json
{
  "reply": "Zmluva je platná, ak spĺňa tieto podmienky...",
  "sources": [
    {
      "filename": "obciansky_zakonnik.txt",
      "chunk_index": 5,
      "distance": 0.234
    }
  ],
  "context": "Optional raw context if include_context=true"
}
```

**Status Codes:**

- `200 OK` - Successful response
- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Missing or invalid authentication
- `500 Internal Server Error` - Server error

**Example:**

```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Čo je to zmluva?",
    "k": 5
  }'
```

---

## Document Management Endpoints

### GET /api/documents

List all documents with optional filtering.

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `practice_area` | string | Filter by practice area |
| `jurisdiction` | string | Filter by jurisdiction |
| `document_type` | string | Filter by document type |
| `skip` | integer | Pagination offset (default: 0) |
| `limit` | integer | Results per page (default: 50, max: 100) |

**Response:**

```json
{
  "documents": [
    {
      "id": 1,
      "filename": "obciansky_zakonnik.txt",
      "document_type": "legislation",
      "practice_area": "civil",
      "jurisdiction": "SK",
      "uploaded_at": "2025-12-04T10:00:00Z",
      "chunk_count": 45
    }
  ],
  "total": 100,
  "skip": 0,
  "limit": 50
}
```

**Example:**

```bash
curl -X GET "http://localhost:8001/api/documents?practice_area=civil&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### GET /api/documents/{document_id}

Get detailed information about a specific document.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | integer | Document ID |

**Response:**

```json
{
  "id": 1,
  "filename": "obciansky_zakonnik.txt",
  "document_type": "legislation",
  "practice_area": "civil",
  "jurisdiction": "SK",
  "uploaded_at": "2025-12-04T10:00:00Z",
  "chunks": [
    {
      "chunk_index": 0,
      "content": "OBČIANSKY ZÁKONNÍK...",
      "created_at": "2025-12-04T10:00:00Z"
    }
  ]
}
```

**Status Codes:**

- `200 OK` - Document found
- `404 Not Found` - Document doesn't exist

---

### DELETE /api/documents/{document_id}

Delete a document and all its chunks.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `document_id` | integer | Document ID |

**Response:**

```json
{
  "message": "Document deleted successfully",
  "document_id": 1
}
```

**Status Codes:**

- `200 OK` - Document deleted
- `404 Not Found` - Document doesn't exist

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "detail": "Error message description"
}
```

**Common Error Codes:**

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Missing/invalid token |
| 404 | Not Found - Resource doesn't exist |
| 422 | Validation Error - Invalid request body |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently no rate limiting is implemented. This may change in production.

---

## Data Models

### ChatRequest

```typescript
interface ChatRequest {
  message: string;              // Required
  history?: Message[];          // Optional
  practice_area?: string;       // Optional
  jurisdiction?: string;        // Optional
  k?: number;                   // Optional, default: 3
  include_context?: boolean;    // Optional, default: false
}
```

### ChatResponse

```typescript
interface ChatResponse {
  reply: string;
  sources: Source[];
  context?: string;  // Only if include_context=true
}
```

### Source

```typescript
interface Source {
  filename: string;
  chunk_index: number;
  distance: number;  // Lower is more relevant
}
```

### Document

```typescript
interface Document {
  id: number;
  filename: string;
  document_type: string;
  practice_area: string | null;
  jurisdiction: string | null;
  uploaded_at: string;  // ISO 8601 datetime
  chunk_count?: number;
}
```

---

## Best Practices

### 1. Conversation History

For multi-turn conversations, include history:

```json
{
  "message": "A čo keď je zmluva ústna?",
  "history": [
    {
      "role": "user",
      "content": "Čo je to zmluva?"
    },
    {
      "role": "assistant",
      "content": "Zmluva je právny úkon..."
    }
  ]
}
```

### 2. Filtering

Use filters to improve relevance:

```json
{
  "message": "Aké sú podmienky platnosti zmluvy?",
  "practice_area": "civil",
  "jurisdiction": "SK",
  "k": 5
}
```

### 3. Source Attribution

Always display sources to users for transparency:

```javascript
response.sources.forEach(source => {
  console.log(`Source: ${source.filename}, chunk ${source.chunk_index}`);
});
```

### 4. Error Handling

Handle errors gracefully:

```javascript
try {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(request)
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
  
  const data = await response.json();
  return data;
} catch (error) {
  console.error('Chat error:', error);
  // Show user-friendly message
}
```

---

## Testing

### Health Check

```bash
curl http://localhost:8001/health
```

Expected response:
```json
{
  "status": "ok",
  "database": "connected",
  "ocr_provider": "mindee"
}
```

### Test Chat (requires authentication)

```bash
# Get token first
TOKEN=$(curl -X POST http://localhost:8001/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}' \
  | jq -r '.access_token')

# Test chat
curl -X POST http://localhost:8001/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Test query","k":3}'
```

---

## OpenAI Configuration

The RAG system requires an OpenAI API key. Configure in `.env`:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Models Used:**

- **Embeddings**: `text-embedding-3-small` (1536 dimensions)
- **Chat**: `gpt-4` (configurable)

**Cost Estimation:**

- Embeddings: ~$0.0001 per 1K tokens
- Chat: ~$0.03 per 1K tokens (GPT-4)

---

## Troubleshooting

### "OpenAI API key not configured"

Set `OPENAI_API_KEY` in `.env` and restart backend:

```bash
docker restart codex-backend-1
```

### "No relevant documents found"

- Ensure documents are imported with embeddings
- Check if filters are too restrictive
- Verify database has document_chunks

### Slow responses

- Reduce `k` parameter (fewer chunks)
- Use `gpt-3.5-turbo` instead of `gpt-4`
- Add database indexes (already created)

---

## Support

For issues or questions:
- Check logs: `docker logs codex-backend-1`
- Review database: Connect to PostgreSQL on port 5433
- Contact: [support email]

---

**Last Updated**: 2025-12-04
**API Version**: 1.0
