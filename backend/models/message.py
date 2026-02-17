"""
MESSAGE PYDANTIC MODELS
Data validation schemas for messaging system
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ============================================
# ENUMS
# ============================================

class MessageType(str, Enum):
    TEXT = "text"
    FILE = "file"
    SYSTEM = "system"

class NotificationType(str, Enum):
    NEW_ORDER = "new_order"
    ORDER_ACCEPTED = "order_accepted"
    ORDER_DELIVERED = "order_delivered"
    ORDER_COMPLETED = "order_completed"
    NEW_MESSAGE = "new_message"
    PAYMENT_RECEIVED = "payment_received"
    REVIEW_RECEIVED = "review_received"
    DEADLINE_REMINDER = "deadline_reminder"
    VERIFICATION_APPROVED = "verification_approved"
    SYSTEM = "system"

# ============================================
# REQUEST MODELS
# ============================================

class SendMessageRequest(BaseModel):
    """Schema for sending a message"""
    order_id: int = Field(..., description="ID objednávky")
    message: str = Field(..., min_length=1, max_length=5000, description="Text správy")
    subject: Optional[str] = Field(None, max_length=500, description="Predmet správy")
    
    class Config:
        json_schema_extra = {
            "example": {
                "order_id": 123,
                "message": "Dobrý deň, mám otázku ohľadom dokumentu...",
                "subject": "Otázka k dokumentu"
            }
        }

class MarkAsReadRequest(BaseModel):
    """Schema for marking messages as read"""
    message_ids: List[int] = Field(..., description="Zoznam ID správ")

# ============================================
# RESPONSE MODELS
# ============================================

class MessageResponse(BaseModel):
    """Message details"""
    id: int
    order_id: Optional[int] = None
    sender_id: int
    recipient_id: int  # Using existing field name
    sender_name: str
    sender_role: str
    subject: Optional[str] = None
    body: str  # Using existing field name
    attachments: Optional[List[dict]] = None
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    """Conversation with pagination"""
    order_id: int
    order_number: str
    messages: List[MessageResponse]
    unread_count: int
    total_messages: int
    has_more: bool
    other_party: dict

class NotificationResponse(BaseModel):
    """Notification details"""
    id: int
    type: str
    title: str
    message: str
    action_url: Optional[str] = None
    action_label: Optional[str] = None
    is_read: bool
    read_at: Optional[datetime] = None
    created_at: datetime
    related_order_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class ApiResponse(BaseModel):
    """Generic API response"""
    success: bool
    message: str
    data: Optional[dict] = None
