"""
Admin Panel API Router
Provides statistics and management endpoints for admin users
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import List, Dict, Any
from pydantic import BaseModel

from main import get_db, get_current_user, User, University, Document, PlatformSettings

router = APIRouter()


# Admin authentication dependency
async def get_admin_user(current_user: User = Depends(get_current_user)):
    """Verify that current user has admin role"""
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


# Response Models
class StatsOverview(BaseModel):
    total_users: int
    total_universities: int
    total_consultations: int
    total_documents: int


class UserGrowthPoint(BaseModel):
    date: str
    count: int


class RecentActivity(BaseModel):
    id: int
    type: str  # 'registration', 'document_upload', 'consultation'
    user_email: str
    timestamp: str
    details: str


class UniversityListItem(BaseModel):
    id: int
    name: str
    country: str
    city: str
    type: str
    website: str
    created_at: str


class UniversityListResponse(BaseModel):
    universities: List[UniversityListItem]
    total: int
    page: int
    limit: int


class UniversityStats(BaseModel):
    total: int
    by_country: Dict[str, int]
    by_type: Dict[str, int]


# Endpoints
@router.get("/stats/overview", response_model=StatsOverview)
async def get_stats_overview(
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get overview statistics for admin dashboard"""
    
    total_users = db.query(func.count(User.id)).scalar()
    total_universities = db.query(func.count(University.id)).scalar()
    total_consultations = 0  # TODO: Add consultation tracking
    total_documents = db.query(func.count(Document.id)).scalar()
    
    return StatsOverview(
        total_users=total_users or 0,
        total_universities=total_universities or 0,
        total_consultations=total_consultations or 0,
        total_documents=total_documents or 0
    )


@router.get("/stats/users-growth", response_model=List[UserGrowthPoint])
async def get_users_growth(
    days: int = 30,
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get user registration growth over time"""
    
    # Calculate date range
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    
    # Query users grouped by date
    results = db.query(
        func.date(User.created_at).label('date'),
        func.count(User.id).label('count')
    ).filter(
        User.created_at >= start_date
    ).group_by(
        func.date(User.created_at)
    ).all()
    
    # Create dict for quick lookup
    data_dict = {str(r.date): r.count for r in results}
    
    # Fill in missing dates with 0
    growth_data = []
    current_date = start_date
    while current_date <= end_date:
        date_str = str(current_date)
        growth_data.append(UserGrowthPoint(
            date=date_str,
            count=data_dict.get(date_str, 0)
        ))
        current_date += timedelta(days=1)
    
    return growth_data


@router.get("/stats/recent-activity", response_model=List[RecentActivity])
async def get_recent_activity(
    limit: int = 10,
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get recent user activities"""
    
    activities = []
    
    # Get recent user registrations
    recent_users = db.query(User).order_by(User.created_at.desc()).limit(limit).all()
    for user in recent_users:
        activities.append({
            'id': user.id,
            'type': 'registration',
            'user_email': user.email,
            'timestamp': user.created_at.isoformat() if user.created_at else '',
            'details': f'New user registered: {user.name}'
        })
    
    # Get recent document uploads
    recent_docs = db.query(Document).order_by(Document.uploaded_at.desc()).limit(limit).all()
    for doc in recent_docs:
        user = db.query(User).filter(User.id == doc.user_id).first()
        if user:
            activities.append({
                'id': doc.id,
                'type': 'document_upload',
                'user_email': user.email,
                'timestamp': doc.uploaded_at.isoformat() if doc.uploaded_at else '',
                'details': f'Document uploaded: {doc.filename}'
            })
    
    # Sort all activities by timestamp
    activities.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Return top N activities
    return [RecentActivity(**activity) for activity in activities[:limit]]


# User Management Models
class UserListItem(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: str
    subscription_status: str


class UserListResponse(BaseModel):
    users: List[UserListItem]
    total: int
    page: int
    limit: int


class UserDetail(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: str
    trial_start_date: str | None
    trial_end_date: str | None
    subscription_status: str
    monthly_request_limit: int
    requests_used_this_month: int


class UpdateUserStatusRequest(BaseModel):
    is_active: bool


# User Management Endpoints
@router.get("/users", response_model=UserListResponse)
async def get_users(
    page: int = 1,
    limit: int = 50,
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get paginated list of users"""
    
    # Calculate offset
    offset = (page - 1) * limit
    
    # Get total count
    total = db.query(func.count(User.id)).scalar()
    
    # Get users with pagination
    users = db.query(User).order_by(User.created_at.desc()).offset(offset).limit(limit).all()
    
    # Format response
    user_list = [
        UserListItem(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at.isoformat() if user.created_at else '',
            subscription_status=user.subscription_status or 'none'
        )
        for user in users
    ]
    
    return UserListResponse(
        users=user_list,
        total=total or 0,
        page=page,
        limit=limit
    )


@router.get("/users/{user_id}", response_model=UserDetail)
async def get_user_detail(
    user_id: int,
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific user"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    return UserDetail(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at.isoformat() if user.created_at else '',
        trial_start_date=user.trial_start_date.isoformat() if user.trial_start_date else None,
        trial_end_date=user.trial_end_date.isoformat() if user.trial_end_date else None,
        subscription_status=user.subscription_status or 'none',
        monthly_request_limit=user.monthly_request_limit or 0,
        requests_used_this_month=user.requests_used_this_month or 0
    )


@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: int,
    request: UpdateUserStatusRequest,
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update user active status (block/unblock user)"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Update status
    user.is_active = request.is_active
    db.commit()
    db.refresh(user)
    
    return {
        "success": True,
        "message": f"User {user.email} {'activated' if request.is_active else 'deactivated'}",
        "user": {
            "id": user.id,
            "email": user.email,
            "is_active": user.is_active
        }
    }


# Universities Management Endpoints
@router.get("/universities", response_model=UniversityListResponse)
async def get_universities(
    page: int = 1,
    limit: int = 50,
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get paginated list of universities"""
    
    # Calculate offset
    offset = (page - 1) * limit
    
    # Get total count
    total = db.query(func.count(University.id)).scalar()
    
    # Get universities with pagination
    universities = db.query(University).order_by(University.name).offset(offset).limit(limit).all()
    
    # Format response
    university_list = [
        UniversityListItem(
            id=uni.id,
            name=uni.name,
            country=uni.country,
            city=uni.city,
            type=uni.type,
            website=uni.website_url or '',
            created_at=uni.created_at.isoformat() if uni.created_at else ''
        )
        for uni in universities
    ]
    
    return UniversityListResponse(
        universities=university_list,
        total=total or 0,
        page=page,
        limit=limit
    )


@router.get("/universities/stats", response_model=UniversityStats)
async def get_universities_stats(
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get statistics about universities"""
    
    # Total count
    total = db.query(func.count(University.id)).scalar()
    
    # Count by country
    by_country_results = db.query(
        University.country,
        func.count(University.id).label('count')
    ).group_by(University.country).all()
    
    by_country = {result.country: result.count for result in by_country_results}
    
    # Count by type
    by_type_results = db.query(
        University.type,
        func.count(University.id).label('count')
    ).group_by(University.type).all()
    
    by_type = {result.type: result.count for result in by_type_results}
    
    return UniversityStats(
        total=total or 0,
        by_country=by_country,
        by_type=by_type
    )


# ============ Settings Management ============

class SettingsResponse(BaseModel):
    platform_name: str
    support_email: str
    maintenance_mode: bool
    openai_api_key: str

class SettingsUpdate(BaseModel):
    platform_name: str
    support_email: str
    maintenance_mode: bool
    openai_api_key: str


@router.get("/settings", response_model=SettingsResponse)
async def get_settings(
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get platform settings"""
    settings = db.query(PlatformSettings).first()
    
    # Create default settings if none exist
    if not settings:
        settings = PlatformSettings(
            platform_name="Student Platform",
            support_email="support@example.com",
            maintenance_mode=False,
            openai_api_key=""
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    return SettingsResponse(
        platform_name=settings.platform_name or "Student Platform",
        support_email=settings.support_email or "support@example.com",
        maintenance_mode=settings.maintenance_mode or False,
        openai_api_key=settings.openai_api_key or ""
    )


@router.put("/settings")
async def update_settings(
    settings_update: SettingsUpdate,
    current_admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update platform settings"""
    settings = db.query(PlatformSettings).first()
    
    if not settings:
        settings = PlatformSettings()
        db.add(settings)
    
    # Update fields
    settings.platform_name = settings_update.platform_name
    settings.support_email = settings_update.support_email
    settings.maintenance_mode = settings_update.maintenance_mode
    settings.openai_api_key = settings_update.openai_api_key
    settings.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(settings)
    
    return {
        "success": True,
        "message": "Settings updated successfully",
        "settings": {
            "platform_name": settings.platform_name,
            "support_email": settings.support_email,
            "maintenance_mode": settings.maintenance_mode
        }
    }
