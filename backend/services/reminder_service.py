"""
Deadline Reminder Service

Checks for upcoming deadlines and sends reminders.
For MVP: logs to console. Can be extended with SendGrid/Twilio.
"""

from datetime import datetime, timedelta
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class ReminderService:
    """Service for managing deadline reminders."""
    
    def __init__(self):
        self.reminder_intervals = [
            7,   # 7 days before
            3,   # 3 days before
            1,   # 1 day before
            0    # On the day
        ]
    
    def check_upcoming_deadlines(self, db) -> List[Dict]:
        """
        Check for cases with upcoming deadlines that need reminders.
        
        Returns list of cases that need reminders sent.
        """
        from api.cases_v2 import Case
        
        now = datetime.utcnow()
        reminders_to_send = []
        
        # Check each reminder interval
        for days in self.reminder_intervals:
            target_date = now + timedelta(days=days)
            
            # Find cases with deadlines around this date
            cases = db.query(Case).filter(
                Case.deadline.isnot(None),
                Case.status.notin_(['resolved', 'cancelled'])
            ).all()
            
            for case in cases:
                if case.deadline:
                    days_until = (case.deadline - now).days
                    
                    # Check if reminder should be sent
                    if days_until == days:
                        reminders_to_send.append({
                            'case_id': case.id,
                            'case_title': case.title,
                            'deadline': case.deadline,
                            'days_until': days_until,
                            'user_id': case.user_id,
                            'assigned_to': case.assigned_to
                        })
        
        return reminders_to_send
    
    def send_reminder(self, reminder: Dict) -> bool:
        """
        Send reminder notification.
        
        For MVP: logs to console.
        For production: integrate SendGrid/Twilio.
        """
        try:
            # MVP: Console logging
            logger.info(f"""
            ========================================
            DEADLINE REMINDER
            ========================================
            Case ID: {reminder['case_id']}
            Title: {reminder['case_title']}
            Deadline: {reminder['deadline']}
            Days Until: {reminder['days_until']}
            User ID: {reminder['user_id']}
            Assigned To: {reminder.get('assigned_to', 'Unassigned')}
            ========================================
            """)
            
            # TODO: Production implementation
            # self._send_email(reminder)
            # self._send_sms(reminder)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send reminder: {e}")
            return False
    
    def _send_email(self, reminder: Dict):
        """
        Send email reminder using SendGrid.
        
        TODO: Implement when ready for production.
        """
        # Example SendGrid integration:
        # from sendgrid import SendGridAPIClient
        # from sendgrid.helpers.mail import Mail
        # 
        # message = Mail(
        #     from_email='noreply@codex.com',
        #     to_emails=user_email,
        #     subject=f'Deadline Reminder: {reminder["case_title"]}',
        #     html_content=f'Your case deadline is in {reminder["days_until"]} days.'
        # )
        # sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        # response = sg.send(message)
        pass
    
    def _send_sms(self, reminder: Dict):
        """
        Send SMS reminder using Twilio.
        
        TODO: Implement when ready for production.
        """
        # Example Twilio integration:
        # from twilio.rest import Client
        # 
        # client = Client(account_sid, auth_token)
        # message = client.messages.create(
        #     body=f'Reminder: {reminder["case_title"]} deadline in {reminder["days_until"]} days',
        #     from_='+1234567890',
        #     to=user_phone
        # )
        pass
    
    def create_reminder_log(self, db, case_id: str, user_id: int, days_before: int):
        """
        Create log entry for scheduled reminder.
        """
        from api.cases_v2 import CaseLog
        
        log_entry = CaseLog(
            case_id=case_id,
            event_type='reminder_scheduled',
            new_value=f'{days_before} days before deadline',
            created_by=user_id,
            comment=f'Reminder scheduled for {days_before} days before deadline'
        )
        db.add(log_entry)
        db.commit()
        
        return log_entry


# Singleton instance
reminder_service = ReminderService()


def schedule_deadline_reminders(db, case_id: str, deadline: datetime, user_id: int):
    """
    Schedule reminders for a case deadline.
    
    Called when case is created/updated with a deadline.
    """
    if not deadline:
        return
    
    # Log that reminders are scheduled
    reminder_service.create_reminder_log(db, case_id, user_id, 7)
    reminder_service.create_reminder_log(db, case_id, user_id, 3)
    reminder_service.create_reminder_log(db, case_id, user_id, 1)
    
    logger.info(f"Scheduled reminders for case {case_id} with deadline {deadline}")


def check_and_send_reminders(db):
    """
    Check for upcoming deadlines and send reminders.
    
    This should be called by a cron job or scheduled task.
    For development: can be called manually or via API endpoint.
    """
    reminders = reminder_service.check_upcoming_deadlines(db)
    
    sent_count = 0
    for reminder in reminders:
        if reminder_service.send_reminder(reminder):
            sent_count += 1
    
    logger.info(f"Sent {sent_count} deadline reminders")
    return sent_count
