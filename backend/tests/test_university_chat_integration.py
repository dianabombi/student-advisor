#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration tests for University Chat API endpoint
Tests the full flow from HTTP request to response
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, AsyncMock, Mock

# Import main app
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app, get_db, Base
from models import University, UniversityChatSession, Jurisdiction


# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_university_chat.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def test_db():
    """Create test database and tables"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_jurisdiction(test_db):
    """Create test jurisdiction"""
    jurisdiction = Jurisdiction(
        code="SK",
        name="Slovakia",
        name_local="Slovensko",
        flag_emoji="🇸🇰"
    )
    test_db.add(jurisdiction)
    test_db.commit()
    test_db.refresh(jurisdiction)
    return jurisdiction


@pytest.fixture(scope="function")
def test_university(test_db, test_jurisdiction):
    """Create test university"""
    university = University(
        name="Test University",
        name_local="Testovacia Univerzita",
        type="university",
        city="Bratislava",
        country="Slovakia",
        description="A test university for integration testing",
        website_url="https://test-university.sk",
        jurisdiction_id=test_jurisdiction.id,
        is_active=True
    )
    test_db.add(university)
    test_db.commit()
    test_db.refresh(university)
    return university


@pytest.fixture(scope="function")
def client():
    """Create test client"""
    return TestClient(app)


class TestUniversityChatEndpoint:
    """Integration tests for /api/universities/{id}/chat endpoint"""
    
    def test_chat_endpoint_success(self, client, test_university):
        """Test successful chat request"""
        
        # Mock UniversityChatService
        with patch('main.UniversityChatService') as MockChatService:
            mock_service = MockChatService.return_value
            mock_service.chat = AsyncMock(return_value="This is a test response from AI")
            
            response = client.post(
                f"/api/universities/{test_university.id}/chat",
                json={
                    "message": "What are the admission requirements?",
                    "session_id": "test_session_123"
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert "session_id" in data
            assert data["response"] == "This is a test response from AI"
    
    def test_chat_endpoint_ukrainian_message(self, client, test_university):
        """Test chat with Ukrainian message"""
        
        with patch('main.UniversityChatService') as MockChatService:
            mock_service = MockChatService.return_value
            mock_service.chat = AsyncMock(return_value="Згідно з інформацією на сайті університету...")
            
            response = client.post(
                f"/api/universities/{test_university.id}/chat",
                json={
                    "message": "Які документи потрібні для вступу?",
                    "session_id": None
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "response" in data
            assert "Згідно" in data["response"] or "університету" in data["response"]
    
    def test_chat_endpoint_creates_session(self, client, test_university, test_db):
        """Test that chat endpoint creates session in database"""
        
        with patch('main.UniversityChatService') as MockChatService:
            mock_service = MockChatService.return_value
            mock_service.chat = AsyncMock(return_value="AI response")
            
            response = client.post(
                f"/api/universities/{test_university.id}/chat",
                json={
                    "message": "Test message",
                    "session_id": None
                }
            )
            
            assert response.status_code == 200
            
            # Check session was created
            session = test_db.query(UniversityChatSession).filter_by(
                university_id=test_university.id
            ).first()
            
            assert session is not None
            assert session.university_id == test_university.id
            assert session.is_active == True
            assert len(session.messages) >= 2  # User message + AI response
    
    def test_chat_endpoint_university_not_found(self, client):
        """Test chat with non-existent university"""
        
        response = client.post(
            "/api/universities/99999/chat",
            json={
                "message": "Test message",
                "session_id": None
            }
        )
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_chat_endpoint_invalid_request(self, client, test_university):
        """Test chat with invalid request body"""
        
        response = client.post(
            f"/api/universities/{test_university.id}/chat",
            json={
                # Missing required 'message' field
                "session_id": "test"
            }
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_chat_endpoint_preserves_history(self, client, test_university, test_db):
        """Test that conversation history is preserved"""
        
        with patch('main.UniversityChatService') as MockChatService:
            mock_service = MockChatService.return_value
            mock_service.chat = AsyncMock(return_value="Response")
            
            # First message
            response1 = client.post(
                f"/api/universities/{test_university.id}/chat",
                json={
                    "message": "First question",
                    "session_id": "test_session"
                }
            )
            assert response1.status_code == 200
            
            # Second message
            response2 = client.post(
                f"/api/universities/{test_university.id}/chat",
                json={
                    "message": "Second question",
                    "session_id": "test_session"
                }
            )
            assert response2.status_code == 200
            
            # Check history
            session = test_db.query(UniversityChatSession).filter_by(
                university_id=test_university.id
            ).first()
            
            # Should have 4 messages: 2 user + 2 assistant
            assert len(session.messages) >= 4


class TestChatHistoryEndpoint:
    """Integration tests for /api/universities/{id}/chat/history endpoint"""
    
    def test_get_chat_history_empty(self, client, test_university):
        """Test getting history when no chat exists"""
        
        response = client.get(
            f"/api/universities/{test_university.id}/chat/history",
            params={"session_id": "nonexistent"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "messages" in data
        assert data["messages"] == []
    
    def test_get_chat_history_with_messages(self, client, test_university, test_db):
        """Test getting history with existing messages"""
        
        # Create session with messages
        session = UniversityChatSession(
            university_id=test_university.id,
            user_id=None,
            messages=[
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"}
            ],
            context={"university_name": test_university.name},
            is_active=True
        )
        test_db.add(session)
        test_db.commit()
        
        response = client.get(
            f"/api/universities/{test_university.id}/chat/history",
            params={"session_id": "test"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["messages"]) == 2
        assert data["messages"][0]["role"] == "user"
        assert data["messages"][1]["role"] == "assistant"


class TestUniversityEndpoints:
    """Test related university endpoints"""
    
    def test_get_universities(self, client, test_university):
        """Test getting list of universities"""
        
        response = client.get("/api/universities")
        
        assert response.status_code == 200
        data = response.json()
        assert "universities" in data
        assert len(data["universities"]) >= 1
    
    def test_get_university_by_id(self, client, test_university):
        """Test getting specific university"""
        
        response = client.get(f"/api/universities/{test_university.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_university.id
        assert data["name"] == test_university.name
    
    def test_get_universities_by_jurisdiction(self, client, test_university):
        """Test filtering universities by jurisdiction"""
        
        response = client.get("/api/universities?jurisdiction_code=SK")
        
        assert response.status_code == 200
        data = response.json()
        assert "universities" in data
        assert len(data["universities"]) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
