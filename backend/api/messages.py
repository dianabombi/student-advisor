"""
MESSAGES ROUTES
API endpoints for messaging and notifications

Base path: /api/messages
"""

from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from models.message import (
    SendMessageRequest,
    MarkAsReadRequest,
    MessageResponse,
    ConversationResponse,
    NotificationResponse
)
from main import get_current_user, get_db, logger
from services import message_service, notification_service
from websocket_manager import ws_manager

router = APIRouter(prefix="/api/messages", tags=["Messages"])

# ============================================
# MESSAGING ENDPOINTS
# ============================================

@router.post("/send", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    message_data: SendMessageRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message in order conversation
    
    **Odoslať správu v konverzácii objednávky**
    """
    try:
        from main import Order
        
        # Verify user has access to this order
        order = db.query(Order).filter(Order.id == message_data.order_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Objednávka nenájdená / Order not found"
            )
        
        # Determine receiver (simplified - would check client_id and lawyer_id)
        # For now, just use a placeholder
        receiver_id = 1  # TODO: Implement proper receiver logic
        
        # Create message
        message = await message_service.create_message(
            db=db,
            order_id=message_data.order_id,
            sender_id=current_user['id'],
            recipient_id=receiver_id,
            message=message_data.message,
            subject=message_data.subject
        )
        
        # Send real-time notification via WebSocket
        await ws_manager.send_personal_message(
            {
                "type": "new_message",
                "data": message
            },
            receiver_id
        )
        
        # Create notification
        await notification_service.create_notification(
            db=db,
            user_id=receiver_id,
            notification_type="new_message",
            title="Nová správa / New message",
            message=f"Máte novú správu v objednávke {order.order_number}",
            related_order_id=message_data.order_id,
            action_url=f"/orders/{message_data.order_id}"
        )
        
        logger.info("message_sent", order_id=message_data.order_id, sender_id=current_user['id'])
        return message
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("message_send_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba pri odosielaní správy / Error sending message: {str(e)}"
        )


@router.get("/conversation/{order_id}", response_model=ConversationResponse)
async def get_conversation(
    order_id: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get conversation for an order
    
    **Získať konverzáciu pre objednávku**
    """
    try:
        # Get messages
        conversation = await message_service.get_conversation(
            db=db,
            order_id=order_id,
            user_id=current_user['id'],
            limit=limit,
            offset=offset
        )
        
        return conversation
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.post("/mark-as-read")
async def mark_messages_as_read(
    request: MarkAsReadRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark messages as read
    
    **Označiť správy ako prečítané**
    """
    try:
        await message_service.mark_as_read(
            db=db,
            message_ids=request.message_ids,
            user_id=current_user['id']
        )
        
        return {
            "success": True,
            "message": "Správy označené ako prečítané / Messages marked as read"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.get("/unread-count")
async def get_unread_count(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get count of unread messages
    
    **Získať počet neprečítaných správ**
    """
    try:
        count = await message_service.get_unread_count(
            db=db,
            user_id=current_user['id']
        )
        
        return {
            "success": True,
            "data": {"unread_count": count}
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


# ============================================
# NOTIFICATIONS ENDPOINTS
# ============================================

@router.get("/notifications", response_model=List[NotificationResponse])
async def get_notifications(
    unread_only: bool = Query(False),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's notifications
    
    **Získať notifikácie používateľa**
    """
    try:
        notifications = await notification_service.get_notifications(
            db=db,
            user_id=current_user['id'],
            unread_only=unread_only,
            limit=limit,
            offset=offset
        )
        
        return notifications
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.post("/notifications/{notification_id}/mark-read")
async def mark_notification_as_read(
    notification_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark notification as read
    
    **Označiť notifikáciu ako prečítanú**
    """
    try:
        await notification_service.mark_as_read(
            db=db,
            notification_id=notification_id,
            user_id=current_user['id']
        )
        
        return {
            "success": True,
            "message": "Notifikácia označená / Notification marked as read"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.post("/notifications/mark-all-read")
async def mark_all_notifications_as_read(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Mark all notifications as read
    
    **Označiť všetky notifikácie ako prečítané**
    """
    try:
        await notification_service.mark_all_as_read(
            db=db,
            user_id=current_user['id']
        )
        
        return {
            "success": True,
            "message": "Všetky notifikácie označené / All notifications marked as read"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


@router.get("/notifications/unread-count")
async def get_unread_notifications_count(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get count of unread notifications
    
    **Získať počet neprečítaných notifikácií**
    """
    try:
        count = await notification_service.get_unread_count(
            db=db,
            user_id=current_user['id']
        )
        
        return {
            "success": True,
            "data": {"unread_count": count}
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba / Error: {str(e)}"
        )


# ============================================
# WEBSOCKET ENDPOINT
# ============================================

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int
):
    """
    WebSocket endpoint for real-time updates
    
    **WebSocket endpoint pre real-time aktualizácie**
    
    Client connects and receives real-time notifications about:
    - New messages
    - Order status changes
    - New orders (for lawyers)
    """
    await ws_manager.connect(websocket, user_id)
    
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            
            # Handle ping/pong for connection health
            if data == "ping":
                await websocket.send_text("pong")
            
    except WebSocketDisconnect:
        ws_manager.disconnect(user_id)
    except Exception as e:
        logger.error("websocket_error", error=str(e))
        ws_manager.disconnect(user_id)
