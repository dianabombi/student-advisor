from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from pydantic import BaseModel

# Import from main.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter(prefix="/api/payments", tags=["payments"])

# These will be imported from main.py when the router is included
# For now, we'll define the dependencies here
def get_db():
    """Database dependency - will be overridden by main.py"""
    pass

def get_current_user():
    """Auth dependency - will be overridden by main.py"""
    pass

# Pydantic models (duplicated from main.py for clarity)
class PaymentCreate(BaseModel):
    plan_type: str  # '1month', '6months', '1year'
    amount: int

class PaymentResponse(BaseModel):
    id: int
    amount: int
    currency: str
    status: str
    payment_method: Optional[str]
    transaction_id: Optional[str]
    created_at: datetime

class SubscriptionResponse(BaseModel):
    id: int
    plan_type: str
    amount: int
    status: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime


@router.post("/create", response_model=PaymentResponse)
async def create_payment(
    payment_data: PaymentCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new payment (stub implementation)
    
    TODO: Integrate with payment gateway (Stripe, PayPal, or local Slovak gateway)
    - Initialize payment session with gateway
    - Get payment URL or token
    - Return payment URL to frontend
    - Handle webhook callbacks for payment confirmation
    """
    from main import Payment, Subscription
    
    # Calculate subscription duration based on plan type
    duration_map = {
        '1month': 30,
        '6months': 180,
        '1year': 365
    }
    
    # Create subscription first
    subscription = Subscription(
        user_id=current_user.id,
        plan_type=payment_data.plan_type,
        amount=payment_data.amount,
        status='pending'
    )
    db.add(subscription)
    db.flush()  # Get subscription ID without committing
    
    # Create payment record
    new_payment = Payment(
        user_id=current_user.id,
        subscription_id=subscription.id,
        amount=payment_data.amount,
        currency='EUR',
        status='pending',  # TODO: Change to 'completed' after real payment gateway integration
        payment_method=None,  # TODO: Set based on payment gateway response
        transaction_id=f"STUB_{subscription.id}_{datetime.utcnow().timestamp()}",  # TODO: Use real transaction ID from gateway
        payment_metadata={
            'plan_type': payment_data.plan_type,
            'note': 'STUB PAYMENT - No real payment gateway integrated yet'
        }
    )
    db.add(new_payment)
    
    # TODO: Remove this auto-activation after payment gateway integration
    # For now, automatically activate subscription for testing
    new_payment.status = 'completed'
    subscription.status = 'active'
    subscription.start_date = datetime.utcnow()
    subscription.end_date = datetime.utcnow() + timedelta(days=duration_map.get(payment_data.plan_type, 30))
    
    # Update user subscription status to active (restore access if trial expired)
    from main import User
    user = db.query(User).filter(User.id == current_user.id).first()
    if user:
        user.subscription_status = 'active'
    
    db.commit()
    db.refresh(new_payment)
    
    return PaymentResponse(
        id=new_payment.id,
        amount=new_payment.amount,
        currency=new_payment.currency,
        status=new_payment.status,
        payment_method=new_payment.payment_method,
        transaction_id=new_payment.transaction_id,
        created_at=new_payment.created_at
    )


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get payment details by ID"""
    from main import Payment
    
    payment = db.query(Payment).filter(
        Payment.id == payment_id,
        Payment.user_id == current_user.id
    ).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    return PaymentResponse(
        id=payment.id,
        amount=payment.amount,
        currency=payment.currency,
        status=payment.status,
        payment_method=payment.payment_method,
        transaction_id=payment.transaction_id,
        created_at=payment.created_at
    )


@router.get("/user/history", response_model=List[PaymentResponse])
async def get_user_payments(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all payments for the current user"""
    from main import Payment
    
    payments = db.query(Payment).filter(
        Payment.user_id == current_user.id
    ).order_by(Payment.created_at.desc()).all()
    
    return [
        PaymentResponse(
            id=p.id,
            amount=p.amount,
            currency=p.currency,
            status=p.status,
            payment_method=p.payment_method,
            transaction_id=p.transaction_id,
            created_at=p.created_at
        )
        for p in payments
    ]


@router.get("/subscriptions/current", response_model=Optional[SubscriptionResponse])
async def get_current_subscription(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's current active subscription"""
    from main import Subscription
    
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == 'active'
    ).order_by(Subscription.created_at.desc()).first()
    
    if not subscription:
        return None
    
    return SubscriptionResponse(
        id=subscription.id,
        plan_type=subscription.plan_type,
        amount=subscription.amount,
        status=subscription.status,
        start_date=subscription.start_date,
        end_date=subscription.end_date,
        created_at=subscription.created_at
    )


@router.get("/subscriptions/all", response_model=List[SubscriptionResponse])
async def get_all_subscriptions(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all subscriptions for the current user"""
    from main import Subscription
    
    subscriptions = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).order_by(Subscription.created_at.desc()).all()
    
    return [
        SubscriptionResponse(
            id=s.id,
            plan_type=s.plan_type,
            amount=s.amount,
            status=s.status,
            start_date=s.start_date,
            end_date=s.end_date,
            created_at=s.created_at
        )
        for s in subscriptions
    ]
