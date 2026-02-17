#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Housing Search API Router
Provides endpoints for searching student accommodation
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.housing_search_service import HousingSearchAgent

router = APIRouter(prefix="/api/housing", tags=["housing"])

# Import database dependency from main
try:
    from main import get_db
except ImportError:
    # Fallback if main not available
    def get_db():
        raise NotImplementedError("get_db dependency not configured")

def get_current_user():
    raise NotImplementedError("get_current_user dependency not configured")


class HousingSearchRequest(BaseModel):
    """Request model for housing search"""
    university_id: int
    language: Optional[str] = 'sk'


class HousingSearchResponse(BaseModel):
    """Response model for housing search"""
    title: str
    university_housing: dict
    real_estate_agencies: list
    agencies_label: str
    visit_label: str
    recommendation: str


@router.post("/search", response_model=HousingSearchResponse)
async def search_housing(
    request: HousingSearchRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Search for student housing options
    
    This endpoint:
    1. Checks if the university provides student accommodation
    2. Finds real estate agencies in the city
    3. Returns direct links for the student
    """
    
    # Import University model
    from main import University
    
    # Get university data
    university = db.query(University).filter(University.id == request.university_id).first()
    
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    
    # Initialize housing search agent
    agent = HousingSearchAgent()
    
    # Perform housing search
    result = await agent.search_housing(
        university_name=university.name,
        university_website=university.website_url or "",
        city=university.city or "",
        country=university.country or "SK",
        language=request.language
    )
    
    return result


@router.get("/quick-search/{university_id}")
async def quick_housing_search(
    university_id: int,
    language: str = 'sk',
    db: Session = Depends(get_db)
):
    """
    Quick housing search without authentication (for landing page)
    """
    
    # Import University model
    from main import University
    
    # Get university data
    university = db.query(University).filter(University.id == university_id).first()
    
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    
    # Initialize housing search agent
    agent = HousingSearchAgent()
    
    # Perform housing search
    result = await agent.search_housing(
        university_name=university.name,
        university_website=university.website_url or "",
        city=university.city or "",
        country=university.country or "SK",
        language=language
    )
    
    return result


class HousingChatRequest(BaseModel):
    """Request model for housing chat"""
    message: str
    conversation_history: list = []
    jurisdiction: Optional[str] = 'SK'  # Country code (SK, CZ, PL, etc.)
    language: Optional[str] = 'sk'  # User's language
    context: Optional[dict] = None  # Optional context (city, university)


@router.post("/chat")
async def housing_chat(
    request: HousingChatRequest,
    db: Session = Depends(get_db)
):
    """
    Chat with housing consultant with RAG
    
    Args:
        request: Chat request with message and history
        db: Database session
    
    Returns:
        AI response with verified housing agencies data
    """
    
    try:
        # Use default user name for testing
        user_name = "Student"
        
        print(f"🏠 Housing chat request received")
        print(f"🏠 Jurisdiction: {request.jurisdiction}")
        print(f"🏠 Language: {request.language}")
        print(f"🏠 Message: {request.message}")
        
        # Extract city from context if provided
        city = None
        if hasattr(request, 'context') and request.context and isinstance(request.context, dict):
            city = request.context.get('city')
        
        # Import chat service
        from services.housing_chat_service import HousingChatService
        
        # Initialize chat service
        chat_service = HousingChatService()
        
        # Get AI response with RAG
        response = await chat_service.chat(
            message=request.message,
            conversation_history=request.conversation_history,
            user_name=user_name,
            language=request.language,
            jurisdiction=request.jurisdiction,
            db=db,
            city=city
        )
        
        print(f"✅ Housing chat response generated successfully")
        return {"response": response}
        
    except Exception as e:
        print(f"❌ Error in housing chat: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
