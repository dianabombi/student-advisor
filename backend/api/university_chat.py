#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
University Chat API Router
Isolated endpoints for university AI chat functionality
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import os

# Import dependencies
from main import get_db, University, UniversityChatSession
from services.university_chat_service import UniversityChatService


# Create router
router = APIRouter(
    prefix="/api/universities",
    tags=["university-chat"]
)


# Pydantic models for request/response
from pydantic import BaseModel

class UniversityChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    conversation_history: list = []  # Add conversation history from frontend
    language: Optional[str] = None  # User's platform language


class UniversityChatResponse(BaseModel):
    response: str
    session_id: str


# Dependency injection for chat service
def get_chat_service() -> UniversityChatService:
    """
    Dependency to get UniversityChatService instance
    Makes it easy to mock in tests
    """
    return UniversityChatService()


@router.post("/{university_id}/chat", response_model=UniversityChatResponse)
async def chat_with_university(
    university_id: int,
    chat_request: UniversityChatRequest,
    db: Session = Depends(get_db),
    chat_service: UniversityChatService = Depends(get_chat_service)
):
    """
    Chat with AI about a specific university using RAG
    
    Args:
        university_id: ID of the university
        chat_request: Chat request with message and optional session_id
        db: Database session (injected)
        chat_service: University chat service (injected)
    
    Returns:
        UniversityChatResponse with AI response and session_id
    
    Raises:
        HTTPException: 404 if university not found
    """
    
    # Verify university exists
    university = db.query(University).filter_by(id=university_id, is_active=True).first()
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    
    # Generate session ID if not provided
    session_id = chat_request.session_id
    if not session_id:
        session_id = f"univ_{university_id}_{datetime.utcnow().timestamp()}_{os.urandom(4).hex()}"
    
    # Use conversation history from request (frontend manages it)
    conversation_history = chat_request.conversation_history
    
    try:
        # Get AI response with RAG (using platform language if provided)
        ai_response_text = await chat_service.chat(
            db=db,
            message=chat_request.message,
            university_id=university_id,
            university_name=university.name,
            university_website=university.website_url or "https://university-website.com",
            university_description=university.description or "A prestigious university",
            conversation_history=conversation_history,
            language=chat_request.language  # Pass platform language
        )
    except Exception as e:
        # Log error and return user-friendly message
        print(f"Error in university chat: {e}")
        
        # Detect language for error message
        from langdetect import detect
        try:
            lang = detect(chat_request.message)
        except:
            lang = 'en'
        
        # Get error message in user's language
        error_messages = {
            'uk': 'Вибачте, сталася помилка. Спробуйте ще раз пізніше.',
            'sk': 'Prepáčte, nastala chyba. Skúste to prosím neskôr.',
            'cs': 'Promiňte, nastala chyba. Zkuste to prosím později.',
            'en': 'Sorry, an error occurred. Please try again later.',
            'pl': 'Przepraszamy, wystąpił błąd. Spróbuj ponownie później.',
            'ru': 'Извините, произошла ошибка. Попробуйте позже.',
            'de': 'Entschuldigung, ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.',
            'fr': 'Désolé, une erreur s\'est produite. Veuillez réessayer plus tard.',
            'es': 'Lo siento, ocurrió un error. Por favor, inténtalo más tarde.',
            'it': 'Spiacente, si è verificato un errore. Riprova più tardi.'
        }
        ai_response_text = error_messages.get(lang, error_messages['en'])
    
    # Return response (frontend manages conversation history)
    return UniversityChatResponse(
        response=ai_response_text,
        session_id=session_id
    )


@router.get("/{university_id}/chat/history")
def get_chat_history(
    university_id: int,
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get chat history for a specific session
    
    Args:
        university_id: ID of the university
        session_id: Session ID
        db: Database session (injected)
    
    Returns:
        Dict with messages array
    """
    chat_session = db.query(UniversityChatSession).filter_by(
        university_id=university_id,
        is_active=True
    ).first()
    
    if not chat_session:
        return {"messages": []}
    
    return {"messages": chat_session.messages or []}
