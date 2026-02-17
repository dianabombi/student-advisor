"""
NOTIFICATION SERVICE
Business logic for notifications
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from typing import List, Optional
from datetime import datetime

async def create_notification(
    db: Session,
    user_id: int,
    notification_type: str,
    title: str,
    message: str,
    related_order_id: Optional[int] = None,
    action_url: Optional[str] = None,
    action_label: Optional[str] = None
):
    """Create a new notification"""
    from main import Notification
    
    notification = Notification(
        user_id=user_id,
        type=notification_type,
        title=title,
        message=message,
        action_url=action_url,
        action_label=action_label,
        related_order_id=related_order_id,
        is_read=False
    )
    
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    return notification


async def get_notifications(
    db: Session,
    user_id: int,
    unread_only: bool = False,
    limit: int = 20,
    offset: int = 0
):
    """Get user's notifications"""
    from main import Notification
    
    query = db.query(Notification).filter(Notification.user_id == user_id)
    
    if unread_only:
        query = query.filter(Notification.is_read == False)
    
    notifications = query.order_by(desc(Notification.created_at)).limit(limit).offset(offset).all()
    
    return notifications


async def mark_as_read(db: Session, notification_id: int, user_id: int):
    """Mark notification as read"""
    from main import Notification
    
    notification = db.query(Notification).filter(
        and_(
            Notification.id == notification_id,
            Notification.user_id == user_id
        )
    ).first()
    
    if notification:
        notification.is_read = True
        notification.read_at = datetime.now()
        db.commit()


async def mark_all_as_read(db: Session, user_id: int):
    """Mark all notifications as read"""
    from main import Notification
    
    db.query(Notification).filter(
        Notification.user_id == user_id
    ).update({
        "is_read": True,
        "read_at": datetime.now()
    }, synchronize_session=False)
    
    db.commit()


async def get_unread_count(db: Session, user_id: int) -> int:
    """Get count of unread notifications"""
    from main import Notification
    
    return db.query(Notification).filter(
        and_(
            Notification.user_id == user_id,
            Notification.is_read == False
        )
    ).count()


async def send_email_notification(receiver_id: int, subject: str, template: str, data: dict):
    """Send email notification (stub for now)"""
    # TODO: Implement email sending via SMTP or SendGrid
    print(f"Email notification to user {receiver_id}: {subject}")
    pass
