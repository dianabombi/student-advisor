"""
MARKETPLACE PAYMENT SERVICE
Business logic for marketplace payment transactions
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
import uuid

async def create_transaction(
    db: Session,
    order_id: int,
    transaction_type: str,
    amount: float,
    payment_method: str = "stripe",
    payment_id: Optional[str] = None,
    status: str = "pending"
):
    """Create a new transaction record"""
    from main import Transaction
    
    transaction_number = f"TXN-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"
    
    transaction = Transaction(
        transaction_number=transaction_number,
        order_id=order_id,
        type=transaction_type,
        amount=amount,
        currency="EUR",
        status=status,
        payment_method=payment_method,
        payment_id=payment_id
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return transaction


async def update_transaction_status(db: Session, payment_id: str, status: str):
    """Update transaction status by payment ID"""
    from main import Transaction
    
    transaction = db.query(Transaction).filter(Transaction.payment_id == payment_id).first()
    if transaction:
        transaction.status = status
        if status == "completed":
            transaction.completed_at = datetime.now()
        db.commit()


async def get_user_transactions(
    db: Session,
    user_id: int,
    limit: int = 20,
    offset: int = 0
) -> List:
    """Get user's transaction history"""
    from main import Transaction, Order
    
    # Get transactions for user's orders
    transactions = db.query(Transaction).join(Order).filter(
        Order.client_id == user_id
    ).order_by(desc(Transaction.created_at)).limit(limit).offset(offset).all()
    
    return transactions


async def get_lawyer_wallet(db: Session, lawyer_id: int):
    """Get lawyer's wallet/balance"""
    from main import LawyerWallet
    
    wallet = db.query(LawyerWallet).filter(LawyerWallet.lawyer_id == lawyer_id).first()
    
    if not wallet:
        # Create wallet if doesn't exist
        wallet = LawyerWallet(
            lawyer_id=lawyer_id,
            total_earnings=0,
            available_balance=0,
            pending_balance=0,
            total_withdrawn=0
        )
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    
    return {
        "lawyer_id": wallet.lawyer_id,
        "total_earnings": float(wallet.total_earnings),
        "available_balance": float(wallet.available_balance),
        "pending_balance": float(wallet.pending_balance),
        "total_withdrawn": float(wallet.total_withdrawn),
        "currency": wallet.currency
    }


async def create_withdrawal_request(
    db: Session,
    lawyer_id: int,
    amount: float,
    bank_account: str,
    note: Optional[str] = None
):
    """Create withdrawal request"""
    from main import Withdrawal, LawyerWallet
    
    withdrawal_number = f"WD-{datetime.now().year}-{str(uuid.uuid4())[:8].upper()}"
    
    withdrawal = Withdrawal(
        withdrawal_number=withdrawal_number,
        lawyer_id=lawyer_id,
        amount=amount,
        bank_account=bank_account,
        status='pending',
        note=note
    )
    
    db.add(withdrawal)
    
    # Deduct from available balance
    wallet = db.query(LawyerWallet).filter(LawyerWallet.lawyer_id == lawyer_id).first()
    if wallet:
        wallet.available_balance -= amount
    
    db.commit()
    db.refresh(withdrawal)
    
    return withdrawal


async def get_withdrawal_history(
    db: Session,
    lawyer_id: int,
    limit: int = 20,
    offset: int = 0
):
    """Get withdrawal history"""
    from main import Withdrawal
    
    withdrawals = db.query(Withdrawal).filter(
        Withdrawal.lawyer_id == lawyer_id
    ).order_by(desc(Withdrawal.requested_at)).limit(limit).offset(offset).all()
    
    return withdrawals


async def approve_withdrawal(db: Session, withdrawal_id: int, admin_id: int):
    """Approve withdrawal (admin)"""
    from main import Withdrawal, LawyerWallet
    
    withdrawal = db.query(Withdrawal).filter(Withdrawal.id == withdrawal_id).first()
    if not withdrawal:
        raise ValueError("Withdrawal not found")
    
    withdrawal.status = 'approved'
    withdrawal.approved_by = admin_id
    withdrawal.approved_at = datetime.now()
    
    # Update wallet
    wallet = db.query(LawyerWallet).filter(LawyerWallet.lawyer_id == withdrawal.lawyer_id).first()
    if wallet:
        wallet.total_withdrawn += withdrawal.amount
    
    db.commit()
    
    # TODO: Process actual payout via Stripe
    
    return withdrawal


async def create_dispute(
    db: Session,
    order_id: int,
    raised_by: str,
    client_id: int,
    lawyer_id: int,
    reason: str,
    description: str,
    requested_refund_amount: Optional[float] = None
):
    """Create a dispute"""
    from main import Dispute
    
    dispute = Dispute(
        order_id=order_id,
        raised_by=raised_by,
        client_id=client_id,
        lawyer_id=lawyer_id,
        reason=reason,
        description=description,
        requested_refund_amount=requested_refund_amount,
        status='open'
    )
    
    db.add(dispute)
    db.commit()
    db.refresh(dispute)
    
    return dispute


async def get_user_disputes(db: Session, user_id: int):
    """Get user's disputes"""
    from main import Dispute
    
    disputes = db.query(Dispute).filter(
        (Dispute.client_id == user_id) | (Dispute.lawyer_id == user_id)
    ).order_by(desc(Dispute.created_at)).all()
    
    return disputes


async def get_dispute(db: Session, dispute_id: int):
    """Get dispute by ID"""
    from main import Dispute
    
    dispute = db.query(Dispute).filter(Dispute.id == dispute_id).first()
    if not dispute:
        raise ValueError("Dispute not found")
    
    return dispute


async def resolve_dispute(
    db: Session,
    dispute_id: int,
    resolution: str,
    refund_amount: float,
    admin_id: int
):
    """Resolve dispute (admin)"""
    from main import Dispute
    
    dispute = db.query(Dispute).filter(Dispute.id == dispute_id).first()
    if not dispute:
        raise ValueError("Dispute not found")
    
    dispute.status = 'resolved'
    dispute.resolution = resolution
    dispute.refund_amount = refund_amount
    dispute.resolved_by = admin_id
    dispute.resolved_at = datetime.now()
    
    db.commit()
    
    return dispute


async def get_order(db: Session, order_id: int):
    """Get order details"""
    from main import Order
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise ValueError("Order not found")
    
    return order


async def update_order_status(db: Session, order_id: int, status: str):
    """Update order status"""
    from main import Order
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = status
        db.commit()


async def process_paid_order(db: Session, order_id: int):
    """Process order after payment confirmed"""
    # Update order status to payment_confirmed
    await update_order_status(db, order_id, "payment_confirmed")
    
    # TODO: Assign to lawyer or put in marketplace
    # TODO: Send notification to lawyer
