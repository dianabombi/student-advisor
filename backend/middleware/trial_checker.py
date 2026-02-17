"""
Trial Period Checker Middleware

This middleware checks if a user's trial period is still active
and blocks access if the trial has expired and no active paid subscription exists.
"""

from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

async def check_trial_status(user, db: Session) -> bool:
    """
    Check if user has access to the platform
    
    Returns:
        True if access is allowed (active trial or paid subscription)
        False if access should be blocked (expired trial, no subscription)
    """
    from main import Subscription
    
    # Check for active paid subscription (not trial)
    active_subscription = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.status == 'active',
        Subscription.is_trial == False,
        Subscription.end_date > datetime.utcnow()
    ).first()
    
    if active_subscription:
        # User has active paid subscription - allow access
        if user.subscription_status != 'active':
            user.subscription_status = 'active'
            db.commit()
        return True
    
    # Check if trial period is still active
    if user.trial_end_date and user.trial_end_date > datetime.utcnow():
        # Trial is still active - allow access
        if user.subscription_status != 'trial':
            user.subscription_status = 'trial'
            db.commit()
        return True
    
    # Trial has expired and no active paid subscription
    if user.trial_end_date and user.trial_end_date <= datetime.utcnow():
        # Update user status to expired
        if user.subscription_status != 'expired':
            user.subscription_status = 'expired'
            
            # Expire the trial subscription
            trial_subscription = db.query(Subscription).filter(
                Subscription.user_id == user.id,
                Subscription.is_trial == True,
                Subscription.status == 'active'
            ).first()
            
            if trial_subscription:
                trial_subscription.status = 'expired'
            
            db.commit()
        
        return False
    
    # No trial period set - block access
    return False


def get_trial_info(user) -> dict:
    """
    Get trial period information for a user
    
    Returns:
        Dictionary with trial status information
    """
    if not user.trial_end_date:
        return {
            "has_trial": False,
            "days_remaining": 0,
            "is_active": False
        }
    
    now = datetime.utcnow()
    days_remaining = (user.trial_end_date - now).days
    
    return {
        "has_trial": True,
        "trial_start_date": user.trial_start_date.isoformat() if user.trial_start_date else None,
        "trial_end_date": user.trial_end_date.isoformat(),
        "days_remaining": max(0, days_remaining),
        "is_active": user.trial_end_date > now,
        "subscription_status": user.subscription_status
    }
