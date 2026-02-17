"""
Case Deadlines API

Endpoints for managing deadlines and reminders.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from auth.rbac import get_current_user
from main import get_db

router = APIRouter(prefix="/api/cases", tags=["Case Deadlines"])


# Pydantic models
class DeadlineCreate(BaseModel):
    """Create deadline request."""
    title: str
    description: Optional[str] = None
    deadline: datetime


class DeadlineUpdate(BaseModel):
    """Update deadline request."""
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    completed: Optional[bool] = None


class DeadlineResponse(BaseModel):
    """Deadline response."""
    id: int
    case_id: int
    title: str
    description: Optional[str]
    deadline: datetime
    completed: bool
    completed_at: Optional[datetime]
    reminder_24h_sent: bool
    reminder_1h_sent: bool
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.post(
    "/{case_id}/deadlines",
    response_model=DeadlineResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Deadline"
)
async def create_deadline(
    case_id: int,
    deadline_data: DeadlineCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a deadline for a case."""
    from main import Case
    from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, Boolean
    from main import Base
    
    class CaseDeadline(Base):
        __tablename__ = "case_deadlines"
        id = Column(Integer, primary_key=True)
        case_id = Column(Integer, ForeignKey("cases.id"))
        title = Column(String)
        description = Column(Text)
        deadline = Column(DateTime)
        reminder_24h_sent = Column(Boolean, default=False)
        reminder_1h_sent = Column(Boolean, default=False)
        completed = Column(Boolean, default=False)
        completed_at = Column(DateTime)
        created_by = Column(Integer, ForeignKey("users.id"))
        created_at = Column(DateTime, default=datetime.utcnow)
    
    # Get case
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Check permissions
    if case.user_id != current_user.id and current_user.role not in ['admin', 'partner_lawyer']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Create deadline
    new_deadline = CaseDeadline(
        case_id=case_id,
        title=deadline_data.title,
        description=deadline_data.description,
        deadline=deadline_data.deadline,
        created_by=current_user.id
    )
    
    db.add(new_deadline)
    db.commit()
    db.refresh(new_deadline)
    
    return new_deadline


@router.get(
    "/{case_id}/deadlines",
    response_model=List[DeadlineResponse],
    summary="List Case Deadlines"
)
async def list_deadlines(
    case_id: int,
    include_completed: bool = True,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all deadlines for a case."""
    from main import Case
    from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, Boolean
    from main import Base
    
    class CaseDeadline(Base):
        __tablename__ = "case_deadlines"
        id = Column(Integer, primary_key=True)
        case_id = Column(Integer, ForeignKey("cases.id"))
        title = Column(String)
        description = Column(Text)
        deadline = Column(DateTime)
        reminder_24h_sent = Column(Boolean)
        reminder_1h_sent = Column(Boolean)
        completed = Column(Boolean)
        completed_at = Column(DateTime)
        created_by = Column(Integer)
        created_at = Column(DateTime)
    
    # Get case
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Check permissions
    if case.user_id != current_user.id and current_user.role not in ['admin', 'partner_lawyer']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Build query
    query = db.query(CaseDeadline).filter(CaseDeadline.case_id == case_id)
    
    if not include_completed:
        query = query.filter(CaseDeadline.completed == False)
    
    deadlines = query.order_by(CaseDeadline.deadline.asc()).all()
    
    return deadlines


@router.patch(
    "/{case_id}/deadlines/{deadline_id}",
    response_model=DeadlineResponse,
    summary="Update Deadline"
)
async def update_deadline(
    case_id: int,
    deadline_id: int,
    deadline_data: DeadlineUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a deadline."""
    from main import Case
    from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, Boolean
    from main import Base
    
    class CaseDeadline(Base):
        __tablename__ = "case_deadlines"
        id = Column(Integer, primary_key=True)
        case_id = Column(Integer, ForeignKey("cases.id"))
        title = Column(String)
        description = Column(Text)
        deadline = Column(DateTime)
        completed = Column(Boolean)
        completed_at = Column(DateTime)
        reminder_24h_sent = Column(Boolean)
        reminder_1h_sent = Column(Boolean)
        created_by = Column(Integer)
        created_at = Column(DateTime)
    
    # Get deadline
    deadline = db.query(CaseDeadline).filter(
        CaseDeadline.id == deadline_id,
        CaseDeadline.case_id == case_id
    ).first()
    
    if not deadline:
        raise HTTPException(status_code=404, detail="Deadline not found")
    
    # Get case for permission check
    case = db.query(Case).filter(Case.id == case_id).first()
    
    # Check permissions
    if case.user_id != current_user.id and current_user.role not in ['admin', 'partner_lawyer']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update fields
    update_data = deadline_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == 'completed' and value == True:
            deadline.completed_at = datetime.utcnow()
        setattr(deadline, field, value)
    
    db.commit()
    db.refresh(deadline)
    
    return deadline


@router.delete(
    "/{case_id}/deadlines/{deadline_id}",
    summary="Delete Deadline"
)
async def delete_deadline(
    case_id: int,
    deadline_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a deadline."""
    from main import Case
    from sqlalchemy import Column, Integer, ForeignKey
    from main import Base
    
    class CaseDeadline(Base):
        __tablename__ = "case_deadlines"
        id = Column(Integer, primary_key=True)
        case_id = Column(Integer, ForeignKey("cases.id"))
    
    # Get deadline
    deadline = db.query(CaseDeadline).filter(
        CaseDeadline.id == deadline_id,
        CaseDeadline.case_id == case_id
    ).first()
    
    if not deadline:
        raise HTTPException(status_code=404, detail="Deadline not found")
    
    # Get case for permission check
    case = db.query(Case).filter(Case.id == case_id).first()
    
    # Check permissions
    if case.user_id != current_user.id and current_user.role not in ['admin', 'partner_lawyer']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(deadline)
    db.commit()
    
    return {"success": True, "message": "Deadline deleted"}


@router.get(
    "/deadlines/upcoming",
    response_model=List[DeadlineResponse],
    summary="Get Upcoming Deadlines",
    description="Get all upcoming deadlines for current user's cases"
)
async def get_upcoming_deadlines(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all upcoming deadlines for user's cases."""
    from main import Case
    from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, Boolean
    from main import Base
    
    class CaseDeadline(Base):
        __tablename__ = "case_deadlines"
        id = Column(Integer, primary_key=True)
        case_id = Column(Integer, ForeignKey("cases.id"))
        title = Column(String)
        description = Column(Text)
        deadline = Column(DateTime)
        reminder_24h_sent = Column(Boolean)
        reminder_1h_sent = Column(Boolean)
        completed = Column(Boolean)
        completed_at = Column(DateTime)
        created_by = Column(Integer)
        created_at = Column(DateTime)
    
    # Get user's cases
    cases = db.query(Case).filter(Case.user_id == current_user.id).all()
    case_ids = [case.id for case in cases]
    
    # Get upcoming deadlines
    deadlines = db.query(CaseDeadline).filter(
        CaseDeadline.case_id.in_(case_ids),
        CaseDeadline.completed == False,
        CaseDeadline.deadline >= datetime.utcnow()
    ).order_by(CaseDeadline.deadline.asc()).limit(10).all()
    
    return deadlines
