# Testing Guide for CODEX Backend

## Setup

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Test Database

```bash
# Create test database
docker exec -it codex-db-1 psql -U user -c "CREATE DATABASE codex_test_db;"

# Enable pgvector extension
docker exec -it codex-db-1 psql -U user -d codex_test_db -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

## Running Tests

### Run All Tests

```bash
# From backend directory
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_rag_api.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_rag_api.py::TestRAGAPI -v
```

### Run Specific Test

```bash
pytest tests/test_rag_api.py::TestRAGAPI::test_chat_endpoint_basic -v
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py           # Shared fixtures
└── test_rag_api.py       # RAG API endpoint tests
```

## Test Coverage

### RAG API Tests (`test_rag_api.py`)

**TestRAGAPI**:
- ✅ `test_chat_endpoint_without_auth` - Authentication required
- ✅ `test_chat_endpoint_basic` - Basic chat functionality
- ✅ `test_chat_with_filters` - Practice area/jurisdiction filtering
- ✅ `test_chat_with_history` - Conversation history
- ✅ `test_list_documents` - Document listing
- ✅ `test_list_documents_with_filters` - Filtered document listing
- ✅ `test_get_document_not_found` - 404 handling
- ✅ `test_delete_document_not_found` - 404 handling

**TestChatRequestValidation**:
- ✅ `test_empty_message` - Empty message handling
- ✅ `test_invalid_k_value` - K value validation
- ✅ `test_invalid_practice_area` - Practice area validation

**TestDocumentManagement**:
- ✅ `test_pagination` - Pagination functionality
- ✅ `test_document_count` - Total count accuracy

## Writing New Tests

### Example Test

```python
def test_new_feature(setup_database, test_user):
    """Test description."""
    response = client.post(
        "/api/endpoint",
        json={"data": "value"},
        headers={"Authorization": f"Bearer {test_user}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "expected_field" in data
```

### Using Fixtures

```python
@pytest.fixture
def sample_document():
    """Create a sample document for testing."""
    return {
        "filename": "test.pdf",
        "content": "Test content"
    }

def test_with_fixture(sample_document):
    assert sample_document["filename"] == "test.pdf"
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: ankane/pgvector:latest
        env:
          POSTGRES_PASSWORD: password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
```

## Troubleshooting

### Database Connection Error
```bash
# Ensure test database exists
docker exec -it codex-db-1 psql -U user -l
```

### Import Errors
```bash
# Run from backend directory
cd backend
pytest tests/ -v
```

### OpenAI API Errors
Tests should handle missing API key gracefully. Set `OPENAI_API_KEY=test_key` for testing.

## Best Practices

1. **Isolation**: Each test should be independent
2. **Cleanup**: Use fixtures to clean up test data
3. **Assertions**: Use specific assertions, not just `assert True`
4. **Documentation**: Add docstrings to all tests
5. **Coverage**: Aim for >80% code coverage
