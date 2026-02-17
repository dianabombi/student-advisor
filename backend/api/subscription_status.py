"""
Subscription Status API

Provides endpoints to check user subscription and trial status
"""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

router = APIRouter(prefix="/api/subscription", tags=["subscription"])

# These will be imported from main.py when the router is included
def get_db():
    """Database dependency - will be overridden by main.py"""
    pass

def get_current_user():
    """Auth dependency - will be overridden by main.py"""
    pass

# Response models
class SubscriptionStatusResponse(BaseModel):
    subscription_status: str  # trial, active, expired, none
    trial_start_date: Optional[str]
    trial_end_date: Optional[str]
    trial_used: bool
    days_remaining: int
    is_trial_active: bool
    active_subscription: Optional[dict]

class TrialInfoResponse(BaseModel):
    has_trial: bool
    trial_start_date: Optional[str]
    trial_end_date: Optional[str]
    days_remaining: int
    is_active: bool
    subscription_status: str


@router.get("/status", response_model=SubscriptionStatusResponse)
async def get_subscription_status(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed subscription status for the current user
    
    Returns trial period information and active subscription details
    """
    from main import Subscription
    from middleware.trial_checker import get_trial_info
    
    # Get active subscription (excluding trial)
    active_subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.status == 'active',
        Subscription.is_trial == False
    ).order_by(Subscription.end_date.desc()).first()
    
    # Get trial information
    trial_info = get_trial_info(current_user)
    
    # Format active subscription data
    subscription_data = None
    if active_subscription:
        subscription_data = {
            "id": active_subscription.id,
            "plan_type": active_subscription.plan_type,
            "amount": active_subscription.amount,
            "start_date": active_subscription.start_date.isoformat() if active_subscription.start_date else None,
            "end_date": active_subscription.end_date.isoformat() if active_subscription.end_date else None,
            "status": active_subscription.status
        }
    
    return SubscriptionStatusResponse(
        subscription_status=current_user.subscription_status,
        trial_start_date=trial_info.get("trial_start_date"),
        trial_end_date=trial_info.get("trial_end_date"),
        trial_used=current_user.trial_used,
        days_remaining=trial_info.get("days_remaining", 0),
        is_trial_active=trial_info.get("is_active", False),
        active_subscription=subscription_data
    )


@router.get("/trial", response_model=TrialInfoResponse)
async def get_trial_info_endpoint(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get trial period information for the current user
    """
    from middleware.trial_checker import get_trial_info
    
    trial_info = get_trial_info(current_user)
    
    return TrialInfoResponse(
        has_trial=trial_info.get("has_trial", False),
        trial_start_date=trial_info.get("trial_start_date"),
        trial_end_date=trial_info.get("trial_end_date"),
        days_remaining=trial_info.get("days_remaining", 0),
        is_active=trial_info.get("is_active", False),
        subscription_status=current_user.subscription_status
    )
