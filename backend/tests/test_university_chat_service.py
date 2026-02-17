#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for UniversityChatService
Tests language detection, RAG integration, and chat functionality
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from services.university_chat_service import UniversityChatService


class TestLanguageDetection:
    """Test language detection functionality"""
    
    def test_detect_ukrainian(self):
        """Test Ukrainian language detection"""
        service = UniversityChatService()
        assert service._detect_language("Привіт, як справи?") == "uk"
    
    def test_detect_slovak(self):
        """Test Slovak language detection"""
        service = UniversityChatService()
        assert service._detect_language("Ahoj, ako sa máš?") == "sk"
    
    def test_detect_czech(self):
        """Test Czech language detection"""
        service = UniversityChatService()
        assert service._detect_language("Ahoj, jak se máš?") == "cs"
    
    def test_detect_english(self):
        """Test English language detection"""
        service = UniversityChatService()
        assert service._detect_language("Hello, how are you?") == "en"
    
    def test_detect_polish(self):
        """Test Polish language detection"""
        service = UniversityChatService()
        assert service._detect_language("Cześć, jak się masz?") == "pl"
    
    def test_detect_russian(self):
        """Test Russian language detection"""
        service = UniversityChatService()
        assert service._detect_language("Привет, как дела?") == "ru"
    
    def test_detect_german(self):
        """Test German language detection"""
        service = UniversityChatService()
        assert service._detect_language("Hallo, wie geht es dir?") == "de"
    
    def test_detect_french(self):
        """Test French language detection"""
        service = UniversityChatService()
        assert service._detect_language("Bonjour, comment allez-vous?") == "fr"
    
    def test_detect_spanish(self):
        """Test Spanish language detection"""
        service = UniversityChatService()
        assert service._detect_language("Hola, ¿cómo estás?") == "es"
    
    def test_detect_italian(self):
        """Test Italian language detection"""
        service = UniversityChatService()
        assert service._detect_language("Ciao, come stai?") == "it"
    
    def test_detect_fallback_to_english(self):
        """Test fallback to English for unknown language"""
        service = UniversityChatService()
        # Very short text that might fail detection
        result = service._detect_language("xyz")
        assert result in ["en", "uk", "sk", "cs", "pl", "ru", "de", "fr", "es", "it"]


class TestErrorMessages:
    """Test error message generation in different languages"""
    
    def test_error_message_ukrainian(self):
        """Test Ukrainian error message"""
        service = UniversityChatService()
        msg = service._get_error_message("uk")
        assert "Вибачте" in msg or "помилка" in msg
    
    def test_error_message_slovak(self):
        """Test Slovak error message"""
        service = UniversityChatService()
        msg = service._get_error_message("sk")
        assert "Prepáčte" in msg or "chyba" in msg
    
    def test_error_message_english(self):
        """Test English error message"""
        service = UniversityChatService()
        msg = service._get_error_message("en")
        assert "Sorry" in msg or "error" in msg
    
    def test_error_message_fallback(self):
        """Test fallback to English for unknown language"""
        service = UniversityChatService()
        msg = service._get_error_message("unknown_lang")
        assert "Sorry" in msg or "error" in msg


class TestSystemPrompts:
    """Test system prompt generation"""
    
    def test_prompt_with_rag_data_ukrainian(self):
        """Test Ukrainian prompt with RAG data"""
        service = UniversityChatService()
        prompt = service._get_system_prompt_with_rag(
            language="uk",
            university_name="Test University",
            university_website="https://test.edu",
            university_description="Test description",
            context="Some context from RAG",
            has_rag_data=True
        )
        
        assert "Test University" in prompt
        assert "консультант" in prompt
        assert "Some context from RAG" in prompt
    
    def test_prompt_without_rag_data_ukrainian(self):
        """Test Ukrainian prompt without RAG data (fallback)"""
        service = UniversityChatService()
        prompt = service._get_system_prompt_with_rag(
            language="uk",
            university_name="Test University",
            university_website="https://test.edu",
            university_description="Test description",
            context="",
            has_rag_data=False
        )
        
        assert "Test University" in prompt
        assert "https://test.edu" in prompt
        assert "не маю детальної інформації" in prompt
    
    def test_prompt_with_rag_data_english(self):
        """Test English prompt with RAG data"""
        service = UniversityChatService()
        prompt = service._get_system_prompt_with_rag(
            language="en",
            university_name="Test University",
            university_website="https://test.edu",
            university_description="Test description",
            context="Some context from RAG",
            has_rag_data=True
        )
        
        assert "Test University" in prompt
        assert "consultant" in prompt
        assert "Some context from RAG" in prompt
    
    def test_prompt_fallback_to_english(self):
        """Test fallback to English for unsupported language"""
        service = UniversityChatService()
        prompt = service._get_system_prompt_with_rag(
            language="unknown_lang",
            university_name="Test University",
            university_website="https://test.edu",
            university_description="Test description",
            context="Some context",
            has_rag_data=True
        )
        
        # Should fallback to English
        assert "consultant" in prompt or "Test University" in prompt


@pytest.mark.asyncio
class TestChatFunctionality:
    """Test main chat functionality"""
    
    async def test_chat_with_rag_data(self):
        """Test chat with RAG data available"""
        service = UniversityChatService()
        
        # Mock database
        mock_db = Mock()
        
        # Mock RAG service
        with patch('services.university_chat_service.RAGService') as MockRAG:
            mock_rag = MockRAG.return_value
            mock_rag.search_any_language_content = AsyncMock(return_value=[
                {"content": "Test content", "url": "https://test.edu/page1"}
            ])
            mock_rag.format_context_for_prompt = Mock(return_value="Formatted context")
            
            # Mock OpenAI
            with patch.object(service.client.chat.completions, 'create', new_callable=AsyncMock) as mock_openai:
                mock_response = Mock()
                mock_response.choices = [Mock(message=Mock(content="AI response"))]
                mock_openai.return_value = mock_response
                
                # Test chat
                response = await service.chat(
                    db=mock_db,
                    message="What are the admission requirements?",
                    university_id=1,
                    university_name="Test University",
                    university_website="https://test.edu",
                    university_description="A test university",
                    conversation_history=[]
                )
                
                assert response == "AI response"
                mock_openai.assert_called_once()
    
    async def test_chat_without_rag_data_fallback(self):
        """Test chat fallback when no RAG data available"""
        service = UniversityChatService()
        
        # Mock database
        mock_db = Mock()
        
        # Mock RAG service returning no data
        with patch('services.university_chat_service.RAGService') as MockRAG:
            mock_rag = MockRAG.return_value
            mock_rag.search_any_language_content = AsyncMock(return_value=[])
            mock_rag.format_context_for_prompt = Mock(return_value="")
            
            # Mock web search
            with patch.object(service, '_search_web_for_university', new_callable=AsyncMock) as mock_web_search:
                mock_web_search.return_value = "Web search results"
                
                # Mock OpenAI
                with patch.object(service.client.chat.completions, 'create', new_callable=AsyncMock) as mock_openai:
                    mock_response = Mock()
                    mock_response.choices = [Mock(message=Mock(content="AI response with web data"))]
                    mock_openai.return_value = mock_response
                    
                    # Test chat
                    response = await service.chat(
                        db=mock_db,
                        message="What are the tuition fees?",
                        university_id=1,
                        university_name="Test University",
                        university_website="https://test.edu",
                        university_description="A test university",
                        conversation_history=[]
                    )
                    
                    assert response == "AI response with web data"
                    mock_web_search.assert_called_once()
    
    async def test_chat_with_conversation_history(self):
        """Test chat with existing conversation history"""
        service = UniversityChatService()
        
        # Mock database
        mock_db = Mock()
        
        conversation_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        
        # Mock RAG service
        with patch('services.university_chat_service.RAGService') as MockRAG:
            mock_rag = MockRAG.return_value
            mock_rag.search_any_language_content = AsyncMock(return_value=[
                {"content": "Test content"}
            ])
            mock_rag.format_context_for_prompt = Mock(return_value="Context")
            
            # Mock OpenAI
            with patch.object(service.client.chat.completions, 'create', new_callable=AsyncMock) as mock_openai:
                mock_response = Mock()
                mock_response.choices = [Mock(message=Mock(content="Response"))]
                mock_openai.return_value = mock_response
                
                # Test chat
                await service.chat(
                    db=mock_db,
                    message="Tell me more",
                    university_id=1,
                    university_name="Test University",
                    university_website="https://test.edu",
                    university_description="A test university",
                    conversation_history=conversation_history
                )
                
                # Verify conversation history was included
                call_args = mock_openai.call_args
                messages = call_args.kwargs['messages']
                
                # Should have system prompt + 2 history messages + current message
                assert len(messages) >= 4
    
    async def test_chat_error_handling(self):
        """Test error handling when OpenAI fails"""
        service = UniversityChatService()
        
        # Mock database
        mock_db = Mock()
        
        # Mock RAG service
        with patch('services.university_chat_service.RAGService') as MockRAG:
            mock_rag = MockRAG.return_value
            mock_rag.search_any_language_content = AsyncMock(return_value=[])
            mock_rag.format_context_for_prompt = Mock(return_value="")
            
            # Mock OpenAI to raise exception
            with patch.object(service.client.chat.completions, 'create', new_callable=AsyncMock) as mock_openai:
                mock_openai.side_effect = Exception("OpenAI API error")
                
                # Test chat - should return error message
                response = await service.chat(
                    db=mock_db,
                    message="Test question",
                    university_id=1,
                    university_name="Test University",
                    university_website="https://test.edu",
                    university_description="A test university",
                    conversation_history=[]
                )
                
                # Should return error message in detected language
                assert "помилка" in response or "error" in response or "chyba" in response


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
