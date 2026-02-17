"""
Case Assignments API

Endpoints for managing lawyer assignments to cases.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from auth.rbac import get_current_user, require_admin
from main import get_db

router = APIRouter(prefix="/api/cases", tags=["Case Assignments"])


# Pydantic models
class AssignmentCreate(BaseModel):
    """Create assignment request."""
    lawyer_id: int
    role: str = "assistant"  # primary or assistant
    notes: Optional[str] = None


class AssignmentResponse(BaseModel):
    """Assignment response."""
    id: int
    case_id: int
    lawyer_id: int
    lawyer_name: str
    lawyer_email: str
    assigned_at: datetime
    assigned_by: Optional[int]
    role: str
    notes: Optional[str]
    
    class Config:
        from_attributes = True


@router.post(
    "/{case_id}/assignments",
    response_model=AssignmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Assign Lawyer to Case",
    description="""
    Assign a lawyer to a case with specified role (primary or assistant).
    
    **Permissions:**
    - Case owner can assign
    - Admins can assign to any case
    - Lawyers cannot self-assign
    
    **Roles:**
    - primary: Main responsible lawyer
    - assistant: Supporting lawyer
    """
)
async def assign_lawyer(
    case_id: int,
    assignment: AssignmentCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Assign a lawyer to a case."""
    from main import Case, User
    
    # Import CaseAssignment model
    from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
    from sqlalchemy.orm import relationship
    from main import Base
    
    class CaseAssignment(Base):
        __tablename__ = "case_assignments"
        id = Column(Integer, primary_key=True)
        case_id = Column(Integer, ForeignKey("cases.id"))
        lawyer_id = Column(Integer, ForeignKey("users.id"))
        assigned_at = Column(DateTime, default=datetime.utcnow)
        assigned_by = Column(Integer, ForeignKey("users.id"))
        role = Column(String)
        notes = Column(Text)
    
    # Get case
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Check permissions
    if case.user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Verify lawyer exists and has lawyer role
    lawyer = db.query(User).filter(User.id == assignment.lawyer_id).first()
    if not lawyer:
        raise HTTPException(status_code=404, detail="Lawyer not found")
    
    if lawyer.role not in ['partner_lawyer', 'admin']:
        raise HTTPException(status_code=400, detail="User is not a lawyer")
    
    # Check if already assigned
    existing = db.query(CaseAssignment).filter(
        CaseAssignment.case_id == case_id,
        CaseAssignment.lawyer_id == assignment.lawyer_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Lawyer already assigned to this case")
    
    # Create assignment
    new_assignment = CaseAssignment(
        case_id=case_id,
        lawyer_id=assignment.lawyer_id,
        assigned_by=current_user.id,
        role=assignment.role,
        notes=assignment.notes
    )
    
    db.add(new_assignment)
    
    # Update case assigned_lawyer_id if primary
    if assignment.role == 'primary':
        case.assigned_lawyer_id = assignment.lawyer_id
    
    db.commit()
    db.refresh(new_assignment)
    
    # Build response
    return AssignmentResponse(
        id=new_assignment.id,
        case_id=new_assignment.case_id,
        lawyer_id=new_assignment.lawyer_id,
        lawyer_name=lawyer.name,
        lawyer_email=lawyer.email,
        assigned_at=new_assignment.assigned_at,
        assigned_by=new_assignment.assigned_by,
        role=new_assignment.role,
        notes=new_assignment.notes
    )


@router.get(
    "/{case_id}/assignments",
    response_model=List[AssignmentResponse],
    summary="List Case Assignments"
)
async def list_assignments(
    case_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all lawyer assignments for a case."""
    from main import Case, User
    from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
    from main import Base
    
    class CaseAssignment(Base):
        __tablename__ = "case_assignments"
        id = Column(Integer, primary_key=True)
        case_id = Column(Integer, ForeignKey("cases.id"))
        lawyer_id = Column(Integer, ForeignKey("users.id"))
        assigned_at = Column(DateTime)
        assigned_by = Column(Integer)
        role = Column(String)
        notes = Column(Text)
    
    # Get case
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Check permissions
    if case.user_id != current_user.id and current_user.role != 'admin':
        # Check if current user is assigned lawyer
        is_assigned = db.query(CaseAssignment).filter(
            CaseAssignment.case_id == case_id,
            CaseAssignment.lawyer_id == current_user.id
        ).first()
        
        if not is_assigned:
            raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get assignments
    assignments = db.query(CaseAssignment).filter(
        CaseAssignment.case_id == case_id
    ).all()
    
    # Build response
    result = []
    for assignment in assignments:
        lawyer = db.query(User).filter(User.id == assignment.lawyer_id).first()
        result.append(AssignmentResponse(
            id=assignment.id,
            case_id=assignment.case_id,
            lawyer_id=assignment.lawyer_id,
            lawyer_name=lawyer.name if lawyer else "Unknown",
            lawyer_email=lawyer.email if lawyer else "",
            assigned_at=assignment.assigned_at,
            assigned_by=assignment.assigned_by,
            role=assignment.role,
            notes=assignment.notes
        ))
    
    return result


@router.delete(
    "/{case_id}/assignments/{assignment_id}",
    summary="Remove Assignment"
)
async def remove_assignment(
    case_id: int,
    assignment_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a lawyer assignment from a case."""
    from main import Case
    from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Text
    from main import Base
    
    class CaseAssignment(Base):
        __tablename__ = "case_assignments"
        id = Column(Integer, primary_key=True)
        case_id = Column(Integer, ForeignKey("cases.id"))
        lawyer_id = Column(Integer, ForeignKey("users.id"))
        role = Column(String)
    
    # Get case
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Check permissions
    if case.user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get assignment
    assignment = db.query(CaseAssignment).filter(
        CaseAssignment.id == assignment_id,
        CaseAssignment.case_id == case_id
    ).first()
    
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    # If removing primary, clear case.assigned_lawyer_id
    if assignment.role == 'primary':
        case.assigned_lawyer_id = None
    
    db.delete(assignment)
    db.commit()
    
    return {"success": True, "message": "Assignment removed"}
