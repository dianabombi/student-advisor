"""
MESSAGE SERVICE
Business logic for messaging system
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from typing import List, Optional
from datetime import datetime
import json

async def create_message(
    db: Session,
    order_id: int,
    sender_id: int,
    recipient_id: int,
    message: str,
    subject: Optional[str] = None,
    attachments: Optional[List[dict]] = None
):
    """Create a new message"""
    from main import Message, User
    
    msg = Message(
        order_id=order_id,
        sender_id=sender_id,
        recipient_id=recipient_id,
        subject=subject or "",
        body=message,
        attachments=attachments or [],
        is_read=False
    )
    
    db.add(msg)
    db.commit()
    db.refresh(msg)
    
    # Get sender info
    sender = db.query(User).filter(User.id == sender_id).first()
    
    # Convert to dict with sender info
    result = {
        "id": msg.id,
        "order_id": msg.order_id,
        "sender_id": msg.sender_id,
        "recipient_id": msg.recipient_id,
        "sender_name": f"{sender.first_name} {sender.last_name}" if sender else "Unknown",
        "sender_role": "client",  # Would determine from user type
        "subject": msg.subject,
        "body": msg.body,
        "attachments": msg.attachments,
        "is_read": msg.is_read,
        "read_at": msg.read_at,
        "created_at": msg.created_at
    }
    
    return result


async def get_conversation(
    db: Session,
    order_id: int,
    user_id: int,
    limit: int = 50,
    offset: int = 0
):
    """Get conversation messages for an order"""
    from main import Message, Order, User
    
    # Get messages
    messages = db.query(Message).filter(
        Message.order_id == order_id
    ).order_by(desc(Message.created_at)).limit(limit).offset(offset).all()
    
    # Get order
    order = db.query(Order).filter(Order.id == order_id).first()
    
    # Get unread count
    unread_count = db.query(Message).filter(
        and_(
            Message.order_id == order_id,
            Message.recipient_id == user_id,
            Message.is_read == False
        )
    ).count()
    
    # Get total count
    total_messages = db.query(Message).filter(Message.order_id == order_id).count()
    
    # Format messages
    formatted_messages = []
    for msg in messages:
        sender = db.query(User).filter(User.id == msg.sender_id).first()
        formatted_messages.append({
            "id": msg.id,
            "order_id": msg.order_id,
            "sender_id": msg.sender_id,
            "recipient_id": msg.recipient_id,
            "sender_name": f"{sender.first_name} {sender.last_name}" if sender else "Unknown",
            "sender_role": "client",
            "subject": msg.subject,
            "body": msg.body,
            "attachments": msg.attachments,
            "is_read": msg.is_read,
            "read_at": msg.read_at,
            "created_at": msg.created_at
        })
    
    return {
        "order_id": order_id,
        "order_number": order.order_number if order else "",
        "messages": list(reversed(formatted_messages)),
        "unread_count": unread_count,
        "total_messages": total_messages,
        "has_more": (offset + limit) < total_messages,
        "other_party": {}
    }


async def mark_as_read(db: Session, message_ids: List[int], user_id: int):
    """Mark messages as read"""
    from main import Message
    
    db.query(Message).filter(
        and_(
            Message.id.in_(message_ids),
            Message.recipient_id == user_id
        )
    ).update({
        "is_read": True,
        "read_at": datetime.now()
    }, synchronize_session=False)
    
    db.commit()


async def get_unread_count(db: Session, user_id: int) -> int:
    """Get total unread messages count"""
    from main import Message
    
    return db.query(Message).filter(
        and_(
            Message.recipient_id == user_id,
            Message.is_read == False
        )
    ).count()
