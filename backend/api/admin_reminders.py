"""
Reminder Check API Endpoint

Provides endpoint to manually trigger reminder checks.
In production, this would be called by a cron job.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from main import get_db
from auth.rbac import require_admin
from services.reminder_service import check_and_send_reminders

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.post("/check-reminders")
async def trigger_reminder_check(
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Manually trigger deadline reminder check.
    
    Admin only. In production, this runs via cron job.
    """
    sent_count = check_and_send_reminders(db)
    
    return {
        'success': True,
        'message': f'Checked deadlines and sent {sent_count} reminders',
        'reminders_sent': sent_count
    }
