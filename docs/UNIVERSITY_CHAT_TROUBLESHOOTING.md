# University Chat System - Troubleshooting Guide

## Common Issues and Solutions

---

## 1. Chat Not Responding

### Symptoms
- User sends message but gets no response
- Loading indicator stuck
- Error message displayed

### Possible Causes & Solutions

#### A. OpenAI API Key Missing
**Error:** `The api_key client option must be set`

**Solution:**
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Set API key in .env file
OPENAI_API_KEY=sk-your-key-here

# Restart backend
docker-compose restart backend
```

#### B. Database Connection Failed
**Error:** `could not connect to server`

**Solution:**
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart database
docker-compose restart postgres

# Check logs
docker-compose logs postgres
```

#### C. RAG Service Error
**Error:** `No module named 'services.rag_service'`

**Solution:**
```bash
# Verify file exists
ls backend/services/rag_service.py

# Check Python path
cd backend
python -c "from services.rag_service import RAGService"
```

---

## 2. Wrong Language Response

### Symptoms
- User asks in Ukrainian, gets English response
- Language detection fails

### Possible Causes & Solutions

#### A. langdetect Not Installed
**Solution:**
```bash
pip install langdetect
```

#### B. Message Too Short
**Issue:** Very short messages (1-2 words) may be misdetected

**Solution:** This is expected behavior. The system defaults to English for ambiguous cases.

#### C. Mixed Languages
**Issue:** Message contains multiple languages

**Solution:** System detects primary language. This is working as intended.

---

## 3. No RAG Data / Generic Responses

### Symptoms
- AI says "I don't have detailed information"
- Responses are too generic
- No university-specific details

### Possible Causes & Solutions

#### A. University Not Scraped
**Check:**
```bash
# Check RAG status
curl http://localhost:8002/api/admin/rag-status/1
```

**Solution:**
```bash
# Trigger scraping
curl -X POST http://localhost:8002/api/admin/scrape-university/1
```

#### B. Embeddings Not Generated
**Check database:**
```sql
SELECT COUNT(*) FROM university_rag_content WHERE university_id = 1;
```

**Solution:** Re-run scraping task or manually add content.

#### C. Web Search Fallback Failing
**Check logs:**
```bash
docker-compose logs backend | grep "web search"
```

**Solution:** This is a fallback mechanism. Check internet connectivity.

---

## 4. Session Not Persisting

### Symptoms
- Conversation history lost
- Each message treated as new conversation

### Possible Causes & Solutions

#### A. Session ID Not Sent
**Check frontend:**
```javascript
// Ensure session_id is included in request
{
  "message": "...",
  "session_id": "univ_1_..."  // ← Must be present
}
```

#### B. Database Session Expired
**Check:**
```sql
SELECT * FROM university_chat_sessions WHERE is_active = true;
```

**Solution:** Sessions are created per university. This is expected behavior.

---

## 5. Slow Response Times

### Symptoms
- Chat takes 10+ seconds to respond
- Timeout errors

### Possible Causes & Solutions

#### A. OpenAI API Slow
**Check:**
```bash
# Monitor response time
docker-compose logs backend | grep "duration_ms"
```

**Solution:**
- Use GPT-3.5-turbo instead of GPT-4 (faster, cheaper)
- Reduce max_tokens in service

#### B. RAG Search Slow
**Check:**
```bash
# Check database query time
docker-compose logs postgres
```

**Solution:**
- Add indexes to `university_rag_content` table
- Reduce `top_k` parameter (currently 5)

#### C. Too Much Context
**Check:**
```python
print(f"Context length: {len(context)} chars")
```

**Solution:**
- Limit context to 2000 characters
- Implement better chunking

---

## 6. Tests Failing

### Symptoms
- `pytest` returns errors
- Import errors
- Mock failures

### Possible Causes & Solutions

#### A. Missing Dependencies
**Error:** `ModuleNotFoundError: No module named 'pytest'`

**Solution:**
```bash
pip install -r backend/requirements-test.txt
```

#### B. OPENAI_API_KEY Required
**Error:** `The api_key client option must be set`

**Solution:** Tests should use mocks from `conftest.py`. If error persists:
```bash
# Set fake key for tests
export OPENAI_API_KEY=sk-test-fake-key
```

#### C. Import Errors
**Error:** `cannot import name 'University' from 'models'`

**Solution:**
```bash
# Models are in main.py, not separate module
# Update imports:
from main import University, UniversityChatSession
```

---

## 7. Router Not Loading

### Symptoms
- `❌ Warning: Could not import university_chat router`
- 404 errors on `/api/universities/{id}/chat`

### Possible Causes & Solutions

#### A. File Not Found
**Check:**
```bash
ls backend/api/university_chat.py
```

**Solution:** Ensure file exists and is in correct location.

#### B. Import Error
**Check logs:**
```bash
docker-compose logs backend | grep "university_chat"
```

**Solution:** Fix any import errors in `university_chat.py`

#### C. Router Not Registered
**Check `main.py`:**
```python
# Should have:
from api.university_chat import router as university_chat_router
app.include_router(university_chat_router)
```

---

## 8. Database Migration Issues

### Symptoms
- Table `university_chat_sessions` doesn't exist
- Column errors

### Solution
```bash
# Run migrations
cd backend
alembic upgrade head

# Or manually create table
docker-compose exec postgres psql -U user -d dbname -f migrations/001_add_educational_tables.sql
```

---

## 9. Frontend Not Connecting

### Symptoms
- CORS errors
- Network errors
- 404 on API calls

### Possible Causes & Solutions

#### A. Backend Not Running
**Check:**
```bash
curl http://localhost:8002/api/universities
```

**Solution:**
```bash
docker-compose up backend
```

#### B. Wrong API URL
**Check frontend `.env.local`:**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8002
```

#### C. CORS Not Configured
**Check `main.py`:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    ...
)
```

---

## 10. High OpenAI Costs

### Symptoms
- Unexpected API bills
- Too many tokens used

### Solutions

#### A. Monitor Usage
```bash
# Check logs for token usage
docker-compose logs backend | grep "total_tokens"
```

#### B. Reduce Token Limits
```python
# In university_chat_service.py
response = await self.client.chat.completions.create(
    model="gpt-4-turbo",
    max_tokens=500,  # ← Reduce from 1000
    ...
)
```

#### C. Use Cheaper Model
```python
model="gpt-3.5-turbo"  # Instead of gpt-4-turbo
```

#### D. Add Rate Limiting
```python
# In router
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@router.post("/{university_id}/chat")
@limiter.limit("10/minute")
async def chat_with_university(...):
```

---

## Debugging Tips

### Enable Debug Logging

```python
# In university_chat_service.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check All Logs

```bash
# Backend logs
docker-compose logs -f backend

# Database logs
docker-compose logs -f postgres

# All logs
docker-compose logs -f
```

### Test Manually

```bash
# Test chat endpoint
curl -X POST http://localhost:8002/api/universities/1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the admission requirements?", "session_id": null}'
```

### Verify Database

```bash
# Connect to database
docker-compose exec postgres psql -U user -d dbname

# Check universities
SELECT id, name FROM universities LIMIT 5;

# Check chat sessions
SELECT * FROM university_chat_sessions;

# Check RAG content
SELECT COUNT(*) FROM university_rag_content GROUP BY university_id;
```

---

## Getting Help

### Before Asking for Help

1. ✅ Check this troubleshooting guide
2. ✅ Review logs (`docker-compose logs`)
3. ✅ Run tests (`pytest backend/tests/test_university_chat*.py`)
4. ✅ Check architecture docs (`docs/UNIVERSITY_CHAT_ARCHITECTURE.md`)

### Where to Get Help

1. **Check Documentation:**
   - `docs/UNIVERSITY_CHAT_ARCHITECTURE.md`
   - `backend/api/university_chat.py` (docstrings)
   - `backend/services/university_chat_service.py` (docstrings)

2. **Review Tests:**
   - `backend/tests/test_university_chat_service.py` (examples)
   - `backend/tests/test_university_chat_integration.py` (API examples)

3. **Check Implementation Plan:**
   - `implementation_plan.md` (design decisions)

---

## Quick Reference

### Restart Everything
```bash
docker-compose down
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f backend
```

### Run Tests
```bash
python backend/run_university_chat_tests.py
```

### Check API Health
```bash
curl http://localhost:8002/api/universities
```

### Verify OpenAI Key
```bash
echo $OPENAI_API_KEY
```
