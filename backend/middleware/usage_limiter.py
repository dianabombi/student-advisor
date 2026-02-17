"""
Usage Limiter Middleware

Handles monthly request limit checking and usage tracking.
Resets limits on 1st of each calendar month.
"""

from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.orm import Session


class UsageLimiter:
    """Middleware for tracking and limiting monthly API usage"""
    
    @staticmethod
    async def check_monthly_limit(user, db: Session):
        """
        Check if user has exceeded monthly limit.
        Auto-resets on 1st of each month.
        
        Args:
            user: User object from database
            db: Database session
            
        Returns:
            dict: Usage information (used, limit, remaining, warning)
            
        Raises:
            HTTPException: If monthly limit exceeded
        """
        # Auto-reset on 1st of month
        if datetime.now().day == 1 and user.requests_used_this_month > 0:
            user.requests_used_this_month = 0
            db.commit()
        
        # Check if limit exceeded
        if user.requests_used_this_month >= user.monthly_request_limit:
            # Calculate next reset date (1st of next month)
            now = datetime.now()
            if now.month == 12:
                next_month = 1
                next_year = now.year + 1
            else:
                next_month = now.month + 1
                next_year = now.year
            
            next_reset = datetime(next_year, next_month, 1)
            days_until_reset = (next_reset - now).days
            
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "monthly_limit_exceeded",
                    "message": f"Ви досягли місячного ліміту ({user.monthly_request_limit} запитів). Наступне оновлення: 1-го {next_reset.strftime('%B %Y')}",
                    "used": user.requests_used_this_month,
                    "limit": user.monthly_request_limit,
                    "reset_date": next_reset.isoformat(),
                    "days_until_reset": days_until_reset
                }
            )
        
        # Increment counter
        user.requests_used_this_month += 1
        db.commit()
        
        # Calculate usage percentage and warning
        remaining = user.monthly_request_limit - user.requests_used_this_month
        usage_percent = (user.requests_used_this_month / user.monthly_request_limit) * 100
        
        warning = None
        if usage_percent >= 80:
            warning = f"⚠️ Ви використали {user.requests_used_this_month}/{user.monthly_request_limit} запитів. Залишилось: {remaining}"
        
        return {
            "used": user.requests_used_this_month,
            "limit": user.monthly_request_limit,
            "remaining": remaining,
            "usage_percent": round(usage_percent, 1),
            "warning": warning
        }
    
    @staticmethod
    async def log_usage(user_id: int, request_type: str, tokens_used: int, db: Session):
        """
        Log usage to history table for analytics.
        
        Args:
            user_id: User ID
            request_type: Type of request ('chat', 'document_upload', etc.)
            tokens_used: Estimated tokens used
            db: Database session
        """
        from main import UsageHistory  # Import here to avoid circular dependency
        
        # Estimate cost (€0.037 per 1000 tokens for GPT-4)
        cost = tokens_used * 0.000037
        
        usage_log = UsageHistory(
            user_id=user_id,
            request_type=request_type,
            tokens_used=tokens_used,
            cost_estimate=cost
        )
        db.add(usage_log)
        db.commit()
