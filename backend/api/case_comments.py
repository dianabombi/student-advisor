"""
Case Comments API

Endpoints for managing comments on cases.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from auth.rbac import get_current_user
from main import get_db

router = APIRouter(prefix="/api/cases", tags=["Case Comments"])


# Pydantic models
class CommentCreate(BaseModel):
    """Create comment request."""
    comment: str
    is_internal: bool = False


class CommentUpdate(BaseModel):
    """Update comment request."""
    comment: str


class CommentResponse(BaseModel):
    """Comment response."""
    id: int
    case_id: int
    user_id: int
    user_name: str
    comment: str
    is_internal: bool
    edited: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


@router.post(
    "/{case_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add Comment to Case"
)
async def add_comment(
    case_id: int,
    comment_data: CommentCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a comment to a case."""
    from main import Case, User
    from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean, DateTime
    from main import Base
    
    class CaseComment(Base):
        __tablename__ = "case_comments"
        id = Column(Integer, primary_key=True)
        case_id = Column(Integer, ForeignKey("cases.id"))
        user_id = Column(Integer, ForeignKey("users.id"))
        comment = Column(Text)
        is_internal = Column(Boolean, default=False)
        edited = Column(Boolean, default=False)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Get case
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Check permissions
    if case.user_id != current_user.id and current_user.role not in ['admin', 'partner_lawyer']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Create comment
    new_comment = CaseComment(
        case_id=case_id,
        user_id=current_user.id,
        comment=comment_data.comment,
        is_internal=comment_data.is_internal
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return CommentResponse(
        id=new_comment.id,
        case_id=new_comment.case_id,
        user_id=new_comment.user_id,
        user_name=current_user.name,
        comment=new_comment.comment,
        is_internal=new_comment.is_internal,
        edited=new_comment.edited,
        created_at=new_comment.created_at,
        updated_at=new_comment.updated_at
    )


@router.get(
    "/{case_id}/comments",
    response_model=List[CommentResponse],
    summary="List Case Comments"
)
async def list_comments(
    case_id: int,
    include_internal: bool = True,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all comments for a case."""
    from main import Case, User
    from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean, DateTime
    from main import Base
    
    class CaseComment(Base):
        __tablename__ = "case_comments"
        id = Column(Integer, primary_key=True)
        case_id = Column(Integer, ForeignKey("cases.id"))
        user_id = Column(Integer, ForeignKey("users.id"))
        comment = Column(Text)
        is_internal = Column(Boolean)
        edited = Column(Boolean)
        created_at = Column(DateTime)
        updated_at = Column(DateTime)
    
    # Get case
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Check permissions
    if case.user_id != current_user.id and current_user.role not in ['admin', 'partner_lawyer']:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Build query
    query = db.query(CaseComment).filter(CaseComment.case_id == case_id)
    
    # Filter internal comments for regular users
    if current_user.role == 'user' or not include_internal:
        query = query.filter(CaseComment.is_internal == False)
    
    comments = query.order_by(CaseComment.created_at.asc()).all()
    
    # Build response
    result = []
    for comment in comments:
        user = db.query(User).filter(User.id == comment.user_id).first()
        result.append(CommentResponse(
            id=comment.id,
            case_id=comment.case_id,
            user_id=comment.user_id,
            user_name=user.name if user else "Unknown",
            comment=comment.comment,
            is_internal=comment.is_internal,
            edited=comment.edited,
            created_at=comment.created_at,
            updated_at=comment.updated_at
        ))
    
    return result


@router.patch(
    "/{case_id}/comments/{comment_id}",
    response_model=CommentResponse,
    summary="Edit Comment"
)
async def edit_comment(
    case_id: int,
    comment_id: int,
    comment_data: CommentUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Edit a comment (only by author)."""
    from main import User
    from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean, DateTime
    from main import Base
    
    class CaseComment(Base):
        __tablename__ = "case_comments"
        id = Column(Integer, primary_key=True)
        case_id = Column(Integer, ForeignKey("cases.id"))
        user_id = Column(Integer, ForeignKey("users.id"))
        comment = Column(Text)
        is_internal = Column(Boolean)
        edited = Column(Boolean)
        created_at = Column(DateTime)
        updated_at = Column(DateTime)
    
    # Get comment
    comment = db.query(CaseComment).filter(
        CaseComment.id == comment_id,
        CaseComment.case_id == case_id
    ).first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Check if user is author or admin
    if comment.user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to edit this comment")
    
    # Update comment
    comment.comment = comment_data.comment
    comment.updated_at = datetime.utcnow()
    comment.edited = True
    
    db.commit()
    db.refresh(comment)
    
    user = db.query(User).filter(User.id == comment.user_id).first()
    
    return CommentResponse(
        id=comment.id,
        case_id=comment.case_id,
        user_id=comment.user_id,
        user_name=user.name if user else "Unknown",
        comment=comment.comment,
        is_internal=comment.is_internal,
        edited=comment.edited,
        created_at=comment.created_at,
        updated_at=comment.updated_at
    )


@router.delete(
    "/{case_id}/comments/{comment_id}",
    summary="Delete Comment"
)
async def delete_comment(
    case_id: int,
    comment_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a comment (only by author or admin)."""
    from sqlalchemy import Column, Integer, ForeignKey, Text, Boolean, DateTime
    from main import Base
    
    class CaseComment(Base):
        __tablename__ = "case_comments"
        id = Column(Integer, primary_key=True)
        case_id = Column(Integer, ForeignKey("cases.id"))
        user_id = Column(Integer, ForeignKey("users.id"))
        comment = Column(Text)
    
    # Get comment
    comment = db.query(CaseComment).filter(
        CaseComment.id == comment_id,
        CaseComment.case_id == case_id
    ).first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Check if user is author or admin
    if comment.user_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    db.delete(comment)
    db.commit()
    
    return {"success": True, "message": "Comment deleted"}
