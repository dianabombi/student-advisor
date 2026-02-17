"""
Cases Management API

Endpoints for managing user legal cases and drafts.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from auth.rbac import get_current_user, require_admin
from main import get_db

router = APIRouter(prefix="/api/cases", tags=["cases"])


# Pydantic models
class CaseCreate(BaseModel):
    """Case creation request."""
    title: str
    description: Optional[str] = None
    case_type: Optional[str] = None
    draft_data: Optional[dict] = None


class CaseUpdate(BaseModel):
    """Case update request."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    case_type: Optional[str] = None
    draft_data: Optional[dict] = None
    reference_number: Optional[str] = None
    court: Optional[str] = None
    case_date: Optional[datetime] = None


class CaseResponse(BaseModel):
    """Case response model."""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    status: str
    case_type: Optional[str]
    draft_data: Optional[dict]
    reference_number: Optional[str]
    court: Optional[str]
    case_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[CaseResponse])
async def get_cases(
    user_id: Optional[int] = None,
    status: Optional[str] = None,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get cases for current user or by user_id (admin only).
    
    - **user_id**: Filter by user ID (admin only)
    - **status**: Filter by status (draft, active, closed, archived)
    """
    from main import Case
    
    # Build query
    query = db.query(Case)
    
    # If user_id specified, check if admin
    if user_id is not None:
        if current_user.role != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can view other users' cases"
            )
        query = query.filter(Case.user_id == user_id)
    else:
        # Regular users see only their own cases
        query = query.filter(Case.user_id == current_user.id)
    
    # Filter by status if provided
    if status:
        query = query.filter(Case.status == status)
    
    # Order by created_at descending
    cases = query.order_by(Case.created_at.desc()).all()
    
    return cases


@router.get("/{case_id}", response_model=CaseResponse)
async def get_case(
    case_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific case by ID.
    
    Users can only access their own cases unless they are admin.
    """
    from main import Case
    
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Check ownership
    if case.user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this case"
        )
    
    return case


@router.post("/", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(
    case_data: CaseCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new case.
    
    - **title**: Case title (required)
    - **description**: Case description
    - **case_type**: Type of case (civil, criminal, administrative, etc.)
    - **draft_data**: JSON data for work-in-progress
    """
    from main import Case
    
    new_case = Case(
        user_id=current_user.id,
        title=case_data.title,
        description=case_data.description,
        case_type=case_data.case_type,
        draft_data=case_data.draft_data,
        status='draft'  # New cases start as draft
    )
    
    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    
    return new_case


@router.patch("/{case_id}", response_model=CaseResponse)
async def update_case(
    case_id: int,
    case_data: CaseUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a case (including draft data).
    
    Users can only update their own cases unless they are admin.
    """
    from main import Case
    
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Check ownership
    if case.user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this case"
        )
    
    # Update fields
    update_data = case_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(case, field, value)
    
    # If status is being changed to closed, set closed_at
    if case_data.status == 'closed' and case.status != 'closed':
        case.closed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(case)
    
    return case


@router.delete("/{case_id}")
async def delete_case(
    case_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a case.
    
    Users can only delete their own cases unless they are admin.
    """
    from main import Case
    
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found"
        )
    
    # Check ownership
    if case.user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this case"
        )
    
    db.delete(case)
    db.commit()
    
    return {"success": True, "message": "Case deleted successfully"}


@router.get("/stats/summary")
async def get_case_stats(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get case statistics for current user.
    """
    from main import Case
    from sqlalchemy import func
    
    # Get counts by status
    stats = db.query(
        Case.status,
        func.count(Case.id).label('count')
    ).filter(
        Case.user_id == current_user.id
    ).group_by(Case.status).all()
    
    # Format response
    result = {
        'total': 0,
        'draft': 0,
        'active': 0,
        'closed': 0,
        'archived': 0
    }
    
    for stat in stats:
        result[stat.status] = stat.count
        result['total'] += stat.count
    
    return result
