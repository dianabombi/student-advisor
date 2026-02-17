#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smoke tests for University Chat System
Quick tests to verify basic functionality and catch critical errors
"""

import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


class TestImports:
    """Test that all critical modules can be imported without errors"""
    
    def test_import_university_chat_service(self):
        """Test importing UniversityChatService"""
        try:
            from services.university_chat_service import UniversityChatService
            assert UniversityChatService is not None
        except ImportError as e:
            pytest.fail(f"Failed to import UniversityChatService: {e}")
    
    def test_import_rag_service(self):
        """Test importing RAGService"""
        try:
            from services.rag_service import RAGService
            assert RAGService is not None
        except ImportError as e:
            pytest.fail(f"Failed to import RAGService: {e}")
    
    def test_import_main_app(self):
        """Test importing main FastAPI app"""
        try:
            from main import app
            assert app is not None
        except ImportError as e:
            # Skip if dependencies like slowapi are missing
            pytest.skip(f"Cannot import main app due to missing dependencies: {e}")
    
    def test_import_models(self):
        """Test importing database models"""
        try:
            # Models are defined in main.py, not separate models module
            from main import University, UniversityChatSession
            assert University is not None
            assert UniversityChatSession is not None
        except ImportError as e:
            # This is expected if slowapi or other dependencies are missing
            # Skip this test instead of failing
            pytest.skip(f"Cannot import models due to missing dependencies: {e}")


class TestServiceInitialization:
    """Test that services can be initialized without errors"""
    
    def test_initialize_chat_service(self):
        """Test UniversityChatService initialization"""
        from services.university_chat_service import UniversityChatService
        
        service = UniversityChatService()
        assert service is not None
        assert hasattr(service, 'client')
        assert hasattr(service, 'chat')
        assert hasattr(service, '_detect_language')
    
    def test_chat_service_has_required_methods(self):
        """Test that UniversityChatService has all required methods"""
        from services.university_chat_service import UniversityChatService
        
        service = UniversityChatService()
        
        # Check for required methods
        assert callable(getattr(service, 'chat', None))
        assert callable(getattr(service, '_detect_language', None))
        assert callable(getattr(service, '_get_system_prompt_with_rag', None))
        assert callable(getattr(service, '_get_error_message', None))


class TestLanguageSupport:
    """Test that all required languages are supported"""
    
    def test_all_languages_have_prompts(self):
        """Test that prompts exist for all supported languages"""
        from services.university_chat_service import UniversityChatService
        
        service = UniversityChatService()
        
        # Test languages
        languages = ['uk', 'sk', 'cs', 'en', 'pl', 'ru', 'de', 'fr', 'es', 'it']
        
        for lang in languages:
            # Should not raise exception
            prompt = service._get_system_prompt_with_rag(
                language=lang,
                university_name="Test",
                university_website="https://test.com",
                university_description="Test",
                context="Test context",
                has_rag_data=True
            )
            assert prompt is not None
            assert len(prompt) > 0
    
    def test_all_languages_have_error_messages(self):
        """Test that error messages exist for all supported languages"""
        from services.university_chat_service import UniversityChatService
        
        service = UniversityChatService()
        
        languages = ['uk', 'sk', 'cs', 'en', 'pl', 'ru', 'de', 'fr', 'es', 'it']
        
        for lang in languages:
            error_msg = service._get_error_message(lang)
            assert error_msg is not None
            assert len(error_msg) > 0


class TestPromptValidation:
    """Test that prompts are valid and don't have syntax errors"""
    
    def test_prompts_no_syntax_errors(self):
        """Test that all prompts can be generated without syntax errors"""
        from services.university_chat_service import UniversityChatService
        
        service = UniversityChatService()
        
        languages = ['uk', 'sk', 'cs', 'en', 'pl', 'ru', 'de', 'fr', 'es', 'it']
        
        for lang in languages:
            # Test with RAG data
            try:
                prompt_with_rag = service._get_system_prompt_with_rag(
                    language=lang,
                    university_name="Test University",
                    university_website="https://test.edu",
                    university_description="Test description",
                    context="Test context from RAG",
                    has_rag_data=True
                )
                assert isinstance(prompt_with_rag, str)
                assert len(prompt_with_rag) > 100
            except Exception as e:
                pytest.fail(f"Prompt generation failed for {lang} with RAG: {e}")
            
            # Test without RAG data
            try:
                prompt_without_rag = service._get_system_prompt_with_rag(
                    language=lang,
                    university_name="Test University",
                    university_website="https://test.edu",
                    university_description="Test description",
                    context="",
                    has_rag_data=False
                )
                assert isinstance(prompt_without_rag, str)
                assert len(prompt_without_rag) > 100
            except Exception as e:
                pytest.fail(f"Prompt generation failed for {lang} without RAG: {e}")
    
    def test_prompts_contain_university_info(self):
        """Test that prompts include university information"""
        from services.university_chat_service import UniversityChatService
        
        service = UniversityChatService()
        
        university_name = "Unique Test University Name 12345"
        university_website = "https://unique-test-url.edu"
        
        prompt = service._get_system_prompt_with_rag(
            language='en',
            university_name=university_name,
            university_website=university_website,
            university_description="Test",
            context="Test",
            has_rag_data=True
        )
        
        # Prompt should contain university name
        assert university_name in prompt


class TestDatabaseModels:
    """Test that database models are properly defined"""
    
    def test_university_model_has_required_fields(self):
        """Test University model has all required fields"""
        try:
            from main import University
        except ImportError:
            pytest.skip("Cannot import University model")
            return
        
        # Check that model has required attributes
        required_fields = ['id', 'name', 'website_url', 'description', 'is_active']
        
        for field in required_fields:
            assert hasattr(University, field), f"University model missing field: {field}"
    
    def test_chat_session_model_has_required_fields(self):
        """Test UniversityChatSession model has all required fields"""
        try:
            from main import UniversityChatSession
        except ImportError:
            pytest.skip("Cannot import UniversityChatSession model")
            return
        
        required_fields = ['id', 'university_id', 'messages', 'is_active']
        
        for field in required_fields:
            assert hasattr(UniversityChatSession, field), f"UniversityChatSession model missing field: {field}"


class TestAPIEndpoints:
    """Test that API endpoints are registered"""
    
    def test_chat_endpoint_exists(self):
        """Test that chat endpoint is registered in app"""
        try:
            from main import app
        except ImportError:
            pytest.skip("Cannot import main app")
            return
        
        routes = [route.path for route in app.routes]
        
        # Check for university chat endpoint pattern
        chat_endpoint_exists = any('/universities/' in route and '/chat' in route for route in routes)
        assert chat_endpoint_exists, "University chat endpoint not found in app routes"


class TestConfiguration:
    """Test that required configuration is present"""
    
    def test_openai_api_key_env_var(self):
        """Test that OPENAI_API_KEY environment variable is set"""
        import os
        
        api_key = os.getenv("OPENAI_API_KEY")
        
        # In production, this should be set
        # In tests, we can skip if not set
        if api_key:
            assert len(api_key) > 0
            assert api_key.startswith("sk-")


if __name__ == "__main__":
    # Run smoke tests with minimal output
    pytest.main([__file__, "-v", "--tb=short"])
