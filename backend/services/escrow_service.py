"""
ESCROW SERVICE
Business logic for escrow fund management
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

async def hold_funds(db: Session, order_id: int, amount: float):
    """
    Hold funds in escrow when payment is received
    
    Args:
        db: Database session
        order_id: Order ID
        amount: Total amount paid by client
    """
    from main import Escrow
    
    # Calculate platform fee (20%) and lawyer payout (80%)
    platform_fee = round(amount * 0.20, 2)
    lawyer_payout = round(amount * 0.80, 2)
    
    # Auto-release after 72 hours
    auto_release_at = datetime.now() + timedelta(hours=72)
    
    escrow = Escrow(
        order_id=order_id,
        total_amount=amount,
        platform_fee=platform_fee,
        lawyer_payout=lawyer_payout,
        status='held',
        auto_release_at=auto_release_at
    )
    
    db.add(escrow)
    db.commit()
    db.refresh(escrow)
    
    return escrow


async def freeze_funds(db: Session, order_id: int):
    """
    Freeze escrow funds during dispute
    """
    from main import Escrow
    
    escrow = db.query(Escrow).filter(Escrow.order_id == order_id).first()
    if escrow:
        escrow.status = 'frozen'
        db.commit()


async def release_to_lawyer(db: Session, order_id: int):
    """
    Release funds from escrow to lawyer
    
    This happens when:
    - Client confirms completion
    - Auto-release after 72 hours
    - Admin resolves dispute in lawyer's favor
    """
    from main import Escrow, LawyerWallet, Order
    
    escrow = db.query(Escrow).filter(Escrow.order_id == order_id).first()
    if not escrow or escrow.status == 'released':
        return
    
    # Get order to find lawyer
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order or not order.lawyer_id:
        return
    
    # Update or create lawyer wallet
    wallet = db.query(LawyerWallet).filter(LawyerWallet.lawyer_id == order.lawyer_id).first()
    if not wallet:
        wallet = LawyerWallet(
            lawyer_id=order.lawyer_id,
            total_earnings=0,
            available_balance=0,
            pending_balance=0,
            total_withdrawn=0
        )
        db.add(wallet)
    
    # Add to lawyer's available balance
    wallet.total_earnings += escrow.lawyer_payout
    wallet.available_balance += escrow.lawyer_payout
    
    # Update escrow status
    escrow.status = 'released'
    escrow.released_at = datetime.now()
    
    db.commit()
    
    return escrow


async def refund_to_client(db: Session, order_id: int, amount: Optional[float] = None):
    """
    Refund funds from escrow to client
    
    Args:
        db: Database session
        order_id: Order ID
        amount: Refund amount (None = full refund)
    """
    from main import Escrow
    
    escrow = db.query(Escrow).filter(Escrow.order_id == order_id).first()
    if not escrow:
        return
    
    refund_amount = amount if amount is not None else escrow.total_amount
    
    # Update escrow status
    escrow.status = 'refunded'
    escrow.released_at = datetime.now()
    escrow.notes = f"Refunded {refund_amount} EUR to client"
    
    db.commit()
    
    # TODO: Process actual refund via Stripe
    
    return escrow


async def check_auto_release():
    """
    Background task to auto-release funds after 72 hours
    
    This should be run periodically (e.g., every hour)
    """
    from main import Escrow, SessionLocal
    
    db = SessionLocal()
    try:
        # Find escrows ready for auto-release
        now = datetime.now()
        escrows = db.query(Escrow).filter(
            Escrow.status == 'held',
            Escrow.auto_release_at <= now
        ).all()
        
        for escrow in escrows:
            await release_to_lawyer(db, escrow.order_id)
            
    finally:
        db.close()
