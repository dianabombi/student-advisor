"""
Notifications API

Endpoints for managing user notifications.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from auth.rbac import get_current_user
from main import get_db

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


# Pydantic models
class NotificationResponse(BaseModel):
    """Notification response."""
    id: int
    type: str
    title: str
    message: str
    link: Optional[str]
    read: bool
    read_at: Optional[datetime]
    created_at: datetime
    related_case_id: Optional[int]
    
    class Config:
        from_attributes = True


@router.get(
    "/",
    response_model=List[NotificationResponse],
    summary="Get User Notifications"
)
async def get_notifications(
    unread_only: bool = False,
    limit: int = 50,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notifications for current user."""
    from sqlalchemy import Column, Integer, ForeignKey, String, Text, Boolean, DateTime
    from main import Base
    
    class Notification(Base):
        __tablename__ = "notifications"
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"))
        type = Column(String)
        title = Column(String)
        message = Column(Text)
        link = Column(String)
        read = Column(Boolean)
        read_at = Column(DateTime)
        created_at = Column(DateTime)
        related_case_id = Column(Integer)
    
    # Build query
    query = db.query(Notification).filter(Notification.user_id == current_user.id)
    
    if unread_only:
        query = query.filter(Notification.read == False)
    
    notifications = query.order_by(
        Notification.created_at.desc()
    ).limit(limit).all()
    
    return notifications


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
    summary="Mark Notification as Read"
)
async def mark_as_read(
    notification_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a notification as read."""
    from sqlalchemy import Column, Integer, ForeignKey, String, Text, Boolean, DateTime
    from main import Base
    
    class Notification(Base):
        __tablename__ = "notifications"
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"))
        type = Column(String)
        title = Column(String)
        message = Column(Text)
        link = Column(String)
        read = Column(Boolean)
        read_at = Column(DateTime)
        created_at = Column(DateTime)
        related_case_id = Column(Integer)
    
    # Get notification
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    # Mark as read
    notification.read = True
    notification.read_at = datetime.utcnow()
    
    db.commit()
    db.refresh(notification)
    
    return notification


@router.post(
    "/mark-all-read",
    summary="Mark All Notifications as Read"
)
async def mark_all_as_read(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark all notifications as read for current user."""
    from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
    from main import Base
    
    class Notification(Base):
        __tablename__ = "notifications"
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"))
        read = Column(Boolean)
        read_at = Column(DateTime)
    
    # Update all unread notifications
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.read == False
    ).update({
        "read": True,
        "read_at": datetime.utcnow()
    })
    
    db.commit()
    
    return {"success": True, "message": "All notifications marked as read"}


@router.get(
    "/unread-count",
    summary="Get Unread Count"
)
async def get_unread_count(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get count of unread notifications."""
    from sqlalchemy import Column, Integer, ForeignKey, Boolean, func
    from main import Base
    
    class Notification(Base):
        __tablename__ = "notifications"
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"))
        read = Column(Boolean)
    
    count = db.query(func.count(Notification.id)).filter(
        Notification.user_id == current_user.id,
        Notification.read == False
    ).scalar()
    
    return {"unread_count": count}


@router.delete(
    "/{notification_id}",
    summary="Delete Notification"
)
async def delete_notification(
    notification_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a notification."""
    from sqlalchemy import Column, Integer, ForeignKey
    from main import Base
    
    class Notification(Base):
        __tablename__ = "notifications"
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"))
    
    # Get notification
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    db.delete(notification)
    db.commit()
    
    return {"success": True, "message": "Notification deleted"}


# Helper function to create notifications (used by other modules)
def create_notification(
    db: Session,
    user_id: int,
    notification_type: str,
    title: str,
    message: str,
    link: Optional[str] = None,
    related_case_id: Optional[int] = None
):
    """Create a notification for a user."""
    from sqlalchemy import Column, Integer, ForeignKey, String, Text, Boolean, DateTime
    from main import Base
    
    class Notification(Base):
        __tablename__ = "notifications"
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"))
        type = Column(String)
        title = Column(String)
        message = Column(Text)
        link = Column(String)
        read = Column(Boolean, default=False)
        read_at = Column(DateTime)
        created_at = Column(DateTime, default=datetime.utcnow)
        related_case_id = Column(Integer)
    
    notification = Notification(
        user_id=user_id,
        type=notification_type,
        title=title,
        message=message,
        link=link,
        related_case_id=related_case_id
    )
    
    db.add(notification)
    db.commit()
    
    return notification
