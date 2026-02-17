#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Student Jobs API Router
Provides endpoints for finding student part-time jobs
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

# Import database dependency from main
try:
    from main import get_db
except ImportError:
    # Fallback if main not available
    def get_db():
        raise NotImplementedError("get_db dependency not configured")

def get_current_user():
    raise NotImplementedError("get_current_user dependency not configured")


class JobSearchRequest(BaseModel):
    """Request model for job search"""
    university_id: int
    language: Optional[str] = 'sk'


class JobAgencyResponse(BaseModel):
    """Response model for job agency"""
    name: str
    website: str
    description: str
    phone: Optional[str]
    email: Optional[str]
    specialization: Optional[str]


class JobChatRequest(BaseModel):
    """Request model for jobs chat"""
    message: str
    conversation_history: list = []
    jurisdiction: Optional[str] = 'SK'
    language: Optional[str] = 'sk'
    context: Optional[dict] = None


@router.get("/agencies/{city}")
async def get_job_agencies(
    city: str,
    country: str = 'SK',
    db: Session = Depends(get_db)
) -> List[JobAgencyResponse]:
    """
    Get job agencies for a specific city
    
    Args:
        city: City name
        country: Country code (default: SK)
        db: Database session
    
    Returns:
        List of job agencies
    """
    from main import JobAgency
    
    agencies = db.query(JobAgency).filter(
        JobAgency.city == city,
        JobAgency.country_code == country,
        JobAgency.is_active == True
    ).all()
    
    return [
        JobAgencyResponse(
            name=agency.name,
            website=agency.website_url,
            description=agency.description or "",
            phone=agency.phone,
            email=agency.email,
            specialization=agency.specialization
        )
        for agency in agencies
    ]


@router.get("/agencies/university/{university_id}")
async def get_job_agencies_for_university(
    university_id: int,
    db: Session = Depends(get_db)
) -> List[JobAgencyResponse]:
    """
    Get job agencies for university's city
    
    Args:
        university_id: University ID
        db: Database session
    
    Returns:
        List of job agencies in university's city
    """
    from main import University, JobAgency
    
    # Get university
    university = db.query(University).filter_by(id=university_id).first()
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    
    # Get agencies for this city
    agencies = db.query(JobAgency).filter(
        JobAgency.city == university.city,
        JobAgency.country_code == university.country,
        JobAgency.is_active == True
    ).all()
    
    return [
        JobAgencyResponse(
            name=agency.name,
            website=agency.website_url,
            description=agency.description or "",
            phone=agency.phone,
            email=agency.email,
            specialization=agency.specialization
        )
        for agency in agencies
    ]


@router.post("/chat")
async def jobs_chat(
    request: JobChatRequest,
    db: Session = Depends(get_db)
):
    """
    Chat with jobs consultant with RAG
    
    Args:
        request: Chat request with message and history
        db: Database session
    
    Returns:
        AI response with verified agencies data
    """
    try:
        from services.jobs_chat_service import JobsChatService
        
        user_name = "Student"
        
        # Extract city from context if provided
        city = None
        if hasattr(request, 'context') and request.context and isinstance(request.context, dict):
            city = request.context.get('city')
        
        print(f"🏛️ City from frontend context: {repr(city)}")
        
        chat_service = JobsChatService()
        
        response = await chat_service.chat(
            message=request.message,
            conversation_history=request.conversation_history,
            user_name=user_name,
            language=request.language,
            jurisdiction=request.jurisdiction,
            db=db,
            city=city
        )
        
        return {"response": response}
        
    except Exception as e:
        print(f"❌ Error in jobs chat: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
