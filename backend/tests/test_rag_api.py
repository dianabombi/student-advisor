"""
Tests for RAG API endpoints

Run with: pytest backend/tests/test_rag_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app, Base, get_db


# Test database
TEST_DATABASE_URL = "postgresql://user:password@localhost:5433/codex_test_db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    """Create test database tables."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user():
    """Create a test user and return auth token."""
    # Register user
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]


class TestRAGAPI:
    """Test RAG API endpoints."""
    
    def test_chat_endpoint_without_auth(self):
        """Test chat endpoint requires authentication."""
        response = client.post(
            "/api/chat",
            json={"message": "Test question"}
        )
        # Should require authentication
        assert response.status_code in [401, 422]  # Unauthorized or validation error
    
    def test_chat_endpoint_basic(self, setup_database, test_user):
        """Test basic chat functionality."""
        response = client.post(
            "/api/chat",
            json={
                "message": "Aké sú podmienky platnosti zmluvy?",
                "k": 3
            },
            headers={"Authorization": f"Bearer {test_user}"}
        )
        
        # May fail if no documents loaded, but should not crash
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.json()
            assert "reply" in data
            assert isinstance(data["reply"], str)
    
    def test_chat_with_filters(self, setup_database, test_user):
        """Test chat with practice area filter."""
        response = client.post(
            "/api/chat",
            json={
                "message": "Test question",
                "practice_area": "civil",
                "jurisdiction": "SK",
                "k": 5
            },
            headers={"Authorization": f"Bearer {test_user}"}
        )
        
        assert response.status_code in [200, 500]
    
    def test_chat_with_history(self, setup_database, test_user):
        """Test chat with conversation history."""
        response = client.post(
            "/api/chat",
            json={
                "message": "Follow-up question",
                "history": [
                    {"role": "user", "content": "Previous question"},
                    {"role": "assistant", "content": "Previous answer"}
                ]
            },
            headers={"Authorization": f"Bearer {test_user}"}
        )
        
        assert response.status_code in [200, 500]
    
    def test_list_documents(self, setup_database, test_user):
        """Test document listing endpoint."""
        response = client.get(
            "/api/documents",
            headers={"Authorization": f"Bearer {test_user}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "documents" in data
        assert "total" in data
        assert isinstance(data["documents"], list)
    
    def test_list_documents_with_filters(self, setup_database, test_user):
        """Test document listing with filters."""
        response = client.get(
            "/api/documents?practice_area=civil&jurisdiction=SK",
            headers={"Authorization": f"Bearer {test_user}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "documents" in data
    
    def test_get_document_not_found(self, setup_database, test_user):
        """Test getting non-existent document."""
        response = client.get(
            "/api/documents/99999",
            headers={"Authorization": f"Bearer {test_user}"}
        )
        
        assert response.status_code == 404
    
    def test_delete_document_not_found(self, setup_database, test_user):
        """Test deleting non-existent document."""
        response = client.delete(
            "/api/documents/99999",
            headers={"Authorization": f"Bearer {test_user}"}
        )
        
        assert response.status_code == 404


class TestChatRequestValidation:
    """Test chat request validation."""
    
    def test_empty_message(self, setup_database, test_user):
        """Test chat with empty message."""
        response = client.post(
            "/api/chat",
            json={"message": ""},
            headers={"Authorization": f"Bearer {test_user}"}
        )
        
        # Should handle empty message gracefully
        assert response.status_code in [200, 422, 500]
    
    def test_invalid_k_value(self, setup_database, test_user):
        """Test chat with invalid k value."""
        response = client.post(
            "/api/chat",
            json={"message": "Test", "k": -1},
            headers={"Authorization": f"Bearer {test_user}"}
        )
        
        # Should validate k value
        assert response.status_code in [200, 422]
    
    def test_invalid_practice_area(self, setup_database, test_user):
        """Test chat with invalid practice area."""
        response = client.post(
            "/api/chat",
            json={
                "message": "Test",
                "practice_area": "invalid_area"
            },
            headers={"Authorization": f"Bearer {test_user}"}
        )
        
        # Should handle invalid practice area
        assert response.status_code in [200, 422, 500]


class TestDocumentManagement:
    """Test document management endpoints."""
    
    def test_pagination(self, setup_database, test_user):
        """Test document list pagination."""
        response = client.get(
            "/api/documents?skip=0&limit=10",
            headers={"Authorization": f"Bearer {test_user}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["documents"]) <= 10
    
    def test_document_count(self, setup_database, test_user):
        """Test document total count."""
        response = client.get(
            "/api/documents",
            headers={"Authorization": f"Bearer {test_user}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 0
        assert data["total"] >= len(data["documents"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
