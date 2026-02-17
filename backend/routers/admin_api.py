"""
Admin API endpoints for dashboard statistics and management
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Form, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, text as sql_text
from typing import Optional, List
from datetime import datetime, timedelta
import logging
from pathlib import Path
import tempfile
import os

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin", tags=["Admin"])

# These will be injected from main.py
get_db = None
get_current_user = None

# Models will be imported at runtime to avoid circular imports
User = None
University = None
Document = None
UniversityChatSession = None
JobAgency = None
RealEstateAgency = None


def _init_models():
    """Lazy import models to avoid circular imports"""
    global User, University, Document, UniversityChatSession, JobAgency, RealEstateAgency
    if User is None:
        from main import User as _User, University as _University, Document as _Document
        from main import UniversityChatSession as _UniversityChatSession
        from main import JobAgency as _JobAgency, RealEstateAgency as _RealEstateAgency
        User = _User
        University = _University
        Document = _Document
        UniversityChatSession = _UniversityChatSession
        JobAgency = _JobAgency
        RealEstateAgency = _RealEstateAgency


async def get_admin_user(current_user = None):
    """Dependency to check if current user is admin"""
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


# =======================
# STATISTICS ENDPOINTS
# =======================

@router.get("/stats/overview")
async def get_stats_overview(db: Session = Depends(lambda: next(get_db()))):
    """
    Get overview statistics for admin dashboard.
    Returns counts of users, universities, consultations, documents.
    """
    _init_models()
    
    try:
        # Count total users
        total_users = db.query(func.count(User.id)).scalar() or 0
        
        # Count active users (logged in last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        active_users = db.query(func.count(User.id)).filter(
            User.created_at >= thirty_days_ago
        ).scalar() or 0
        
        # Count universities
        total_universities = db.query(func.count(University.id)).scalar() or 0
        
        # Count chat sessions (consultations)
        total_consultations = db.query(func.count(UniversityChatSession.id)).scalar() or 0
        
        # Count documents
        total_documents = db.query(func.count(Document.id)).scalar() or 0
        
        # Count job agencies
        total_job_agencies = db.query(func.count(JobAgency.id)).filter(
            JobAgency.is_active == True
        ).scalar() or 0
        
        # Count real estate agencies
        total_housing_agencies = db.query(func.count(RealEstateAgency.id)).filter(
            RealEstateAgency.is_active == True
        ).scalar() or 0
        
        # Users registered today
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        users_today = db.query(func.count(User.id)).filter(
            User.created_at >= today_start
        ).scalar() or 0
        
        # Consultations today
        consultations_today = db.query(func.count(UniversityChatSession.id)).filter(
            UniversityChatSession.created_at >= today_start
        ).scalar() or 0
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "users_today": users_today,
            "total_universities": total_universities,
            "total_consultations": total_consultations,
            "consultations_today": consultations_today,
            "total_documents": total_documents,
            "total_job_agencies": total_job_agencies,
            "total_housing_agencies": total_housing_agencies,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting stats overview: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching statistics: {str(e)}"
        )


@router.get("/stats/users-growth")
async def get_users_growth(
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(lambda: next(get_db()))
):
    """
    Get user registration growth data for chart.
    Returns daily counts for the specified number of days.
    """
    _init_models()
    
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Query users grouped by date
        result = db.query(
            func.date(User.created_at).label('date'),
            func.count(User.id).label('count')
        ).filter(
            User.created_at >= start_date
        ).group_by(
            func.date(User.created_at)
        ).order_by(
            func.date(User.created_at)
        ).all()
        
        # Convert to dict for easy lookup
        data_dict = {str(row.date): row.count for row in result}
        
        # Fill in missing dates with 0
        growth_data = []
        current_date = start_date.date()
        end_date = datetime.utcnow().date()
        
        while current_date <= end_date:
            date_str = str(current_date)
            growth_data.append({
                "date": date_str,
                "count": data_dict.get(date_str, 0)
            })
            current_date += timedelta(days=1)
        
        # Calculate totals
        total_new_users = sum(item['count'] for item in growth_data)
        
        return {
            "period_days": days,
            "total_new_users": total_new_users,
            "data": growth_data
        }
    except Exception as e:
        logger.error(f"Error getting users growth: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching growth data: {str(e)}"
        )


@router.get("/stats/recent-activity")
async def get_recent_activity(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(lambda: next(get_db()))
):
    """
    Get recent platform activity.
    Returns recent users, chat sessions, and documents.
    """
    _init_models()
    
    try:
        activities = []
        
        # Recent user registrations
        recent_users = db.query(User).order_by(
            User.created_at.desc()
        ).limit(limit).all()
        
        for user in recent_users:
            activities.append({
                "type": "user_registered",
                "icon": "🟢",
                "message": f"User {user.name} registered",
                "email": user.email,
                "timestamp": user.created_at.isoformat() if user.created_at else None
            })
        
        # Recent chat sessions
        recent_chats = db.query(UniversityChatSession).order_by(
            UniversityChatSession.created_at.desc()
        ).limit(limit).all()
        
        for chat in recent_chats:
            activities.append({
                "type": "ai_consultation",
                "icon": "🔵",
                "message": f"AI Consultation session #{chat.id}",
                "university_id": chat.university_id,
                "timestamp": chat.created_at.isoformat() if chat.created_at else None
            })
        
        # Recent documents
        recent_docs = db.query(Document).order_by(
            Document.uploaded_at.desc()
        ).limit(limit).all()
        
        for doc in recent_docs:
            activities.append({
                "type": "document_uploaded",
                "icon": "🟠",
                "message": f"Document uploaded: {doc.filename}",
                "document_type": doc.document_type,
                "timestamp": doc.uploaded_at.isoformat() if doc.uploaded_at else None
            })
        
        # Sort all activities by timestamp
        activities.sort(
            key=lambda x: x.get('timestamp') or '1970-01-01',
            reverse=True
        )
        
        # Return only the requested limit
        return {
            "activities": activities[:limit]
        }
    except Exception as e:
        logger.error(f"Error getting recent activity: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching activity: {str(e)}"
        )


# =======================
# USERS MANAGEMENT
# =======================

@router.get("/users")
async def get_users_list(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=100),
    search: Optional[str] = None,
    role: Optional[str] = None,
    db: Session = Depends(lambda: next(get_db()))
):
    """
    Get paginated list of users for admin management.
    """
    _init_models()
    
    try:
        query = db.query(User)
        
        # Apply filters
        if search:
            query = query.filter(
                (User.name.ilike(f"%{search}%")) |
                (User.email.ilike(f"%{search}%"))
            )
        
        if role:
            query = query.filter(User.role == role)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        users = query.order_by(User.created_at.desc()).offset(offset).limit(limit).all()
        
        users_data = []
        for user in users:
            users_data.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "subscription_status": user.subscription_status,
                "created_at": user.created_at.isoformat() if user.created_at else None
            })
        
        return {
            "users": users_data,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
    except Exception as e:
        logger.error(f"Error getting users list: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching users: {str(e)}"
        )


@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    is_active: bool,
    db: Session = Depends(lambda: next(get_db()))
):
    """
    Block or unblock a user.
    """
    _init_models()
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.is_active = is_active
        db.commit()
        
        action = "activated" if is_active else "deactivated"
        logger.info(f"User {user_id} ({user.email}) {action} by admin")
        
        return {
            "success": True,
            "message": f"User {action} successfully",
            "user_id": user_id,
            "is_active": is_active
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )


# =======================
# UNIVERSITIES STATS
# =======================

@router.get("/universities/stats")
async def get_universities_stats(db: Session = Depends(lambda: next(get_db()))):
    """
    Get statistics about universities.
    """
    _init_models()
    
    try:
        total = db.query(func.count(University.id)).scalar() or 0
        
        # By country
        by_country = db.query(
            University.country,
            func.count(University.id).label('count')
        ).group_by(University.country).all()
        
        # By type
        by_type = db.query(
            University.type,
            func.count(University.id).label('count')
        ).group_by(University.type).all()
        
        return {
            "total": total,
            "by_country": {row.country: row.count for row in by_country},
            "by_type": {row.type or "unknown": row.count for row in by_type}
        }
    except Exception as e:
        logger.error(f"Error getting universities stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching stats: {str(e)}"
        )
