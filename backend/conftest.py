#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pytest configuration and fixtures for university chat tests
Provides mocks and setup for all tests
"""

import pytest
import os
import sys
from unittest.mock import Mock, AsyncMock, patch, MagicMock

# Add backend to Python path
backend_path = os.path.dirname(os.path.abspath(__file__))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)


# ============================================================================
# Environment Setup
# ============================================================================

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment variables"""
    # Set fake OpenAI API key for tests
    os.environ["OPENAI_API_KEY"] = "sk-test-fake-key-for-testing-only"
    
    # Set other required environment variables
    os.environ["DATABASE_URL"] = "sqlite:///./test.db"
    os.environ["SECRET_KEY"] = "test-secret-key-for-testing"
    
    yield
    
    # Cleanup after all tests
    if "OPENAI_API_KEY" in os.environ:
        del os.environ["OPENAI_API_KEY"]


# ============================================================================
# Mock OpenAI Client
# ============================================================================

@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing"""
    mock_client = Mock()
    
    # Mock chat completions
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="Test AI response"))]
    mock_response.usage = Mock(
        prompt_tokens=10,
        completion_tokens=20,
        total_tokens=30
    )
    
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
    
    return mock_client


@pytest.fixture(autouse=True)
def mock_openai_for_all_tests(monkeypatch):
    """Automatically mock OpenAI for all tests"""
    
    # Create a mock AsyncOpenAI class
    class MockAsyncOpenAI:
        def __init__(self, api_key=None):
            self.api_key = api_key
            self.chat = Mock()
            self.chat.completions = Mock()
            
            # Mock response
            mock_response = Mock()
            mock_response.choices = [Mock(message=Mock(content="Test AI response"))]
            mock_response.usage = Mock(
                prompt_tokens=10,
                completion_tokens=20,
                total_tokens=30
            )
            
            self.chat.completions.create = AsyncMock(return_value=mock_response)
    
    # Patch the AsyncOpenAI import
    monkeypatch.setattr("openai.AsyncOpenAI", MockAsyncOpenAI)


# ============================================================================
# Mock Database Models
# ============================================================================

@pytest.fixture
def mock_university():
    """Mock University model"""
    university = Mock()
    university.id = 1
    university.name = "Test University"
    university.name_local = "Testovacia Univerzita"
    university.type = "university"
    university.city = "Bratislava"
    university.country = "Slovakia"
    university.description = "A test university"
    university.website_url = "https://test-university.sk"
    university.is_active = True
    university.programs = []
    
    return university


@pytest.fixture
def mock_chat_session():
    """Mock UniversityChatSession"""
    session = Mock()
    session.id = 1
    session.university_id = 1
    session.user_id = None
    session.messages = []
    session.context = {"university_name": "Test University"}
    session.is_active = True
    
    return session


@pytest.fixture
def mock_db():
    """Mock database session"""
    db = Mock()
    db.query = Mock(return_value=Mock())
    db.add = Mock()
    db.commit = Mock()
    db.refresh = Mock()
    db.close = Mock()
    
    return db


# ============================================================================
# Mock RAG Service
# ============================================================================

@pytest.fixture
def mock_rag_service():
    """Mock RAG service"""
    rag = Mock()
    rag.search_any_language_content = AsyncMock(return_value=[
        {
            "content": "Test content from university website",
            "url": "https://test-university.sk/admissions",
            "relevance_score": 0.95
        }
    ])
    rag.format_context_for_prompt = Mock(return_value="Formatted test context")
    
    return rag


@pytest.fixture(autouse=True)
def mock_rag_for_all_tests(monkeypatch):
    """Automatically mock RAG service for all tests"""
    
    class MockRAGService:
        async def search_any_language_content(self, db, university_id, query, top_k=5):
            return [
                {
                    "content": "Test content from university website",
                    "url": "https://test-university.sk/page",
                    "relevance_score": 0.9
                }
            ]
        
        def format_context_for_prompt(self, content):
            return "Formatted test context"
    
    # Only patch if RAGService is being imported
    try:
        monkeypatch.setattr("services.rag_service.RAGService", MockRAGService)
    except:
        pass  # RAGService not imported yet


# ============================================================================
# Mock External Dependencies
# ============================================================================

@pytest.fixture(autouse=True)
def mock_external_dependencies(monkeypatch):
    """Mock external dependencies that might not be installed"""
    
    # Mock pytesseract
    mock_pytesseract = Mock()
    mock_pytesseract.image_to_string = Mock(return_value="Test OCR text")
    monkeypatch.setitem(sys.modules, "pytesseract", mock_pytesseract)
    
    # Mock PIL
    mock_pil = Mock()
    monkeypatch.setitem(sys.modules, "PIL", mock_pil)
    monkeypatch.setitem(sys.modules, "PIL.Image", Mock())


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_messages():
    """Sample conversation messages"""
    return [
        {"role": "user", "content": "What are the admission requirements?"},
        {"role": "assistant", "content": "The admission requirements are..."}
    ]


@pytest.fixture
def sample_university_data():
    """Sample university data"""
    return {
        "id": 1,
        "name": "Test University",
        "website_url": "https://test-university.sk",
        "description": "A prestigious test university",
        "city": "Bratislava",
        "country": "Slovakia"
    }


# ============================================================================
# Async Test Support
# ============================================================================

@pytest.fixture
def event_loop():
    """Create event loop for async tests"""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# Test Markers
# ============================================================================

def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "smoke: Quick smoke tests"
    )
    config.addinivalue_line(
        "markers", "unit: Unit tests"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests"
    )
    config.addinivalue_line(
        "markers", "slow: Slow running tests"
    )


# ============================================================================
# Test Collection Hooks
# ============================================================================

def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    for item in items:
        # Add markers based on test file names
        if "smoke" in item.nodeid:
            item.add_marker(pytest.mark.smoke)
        elif "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "service" in item.nodeid:
            item.add_marker(pytest.mark.unit)
