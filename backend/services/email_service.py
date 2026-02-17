"""
Email service for admin alerts
"""

import os
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

async def send_admin_alert(to_email: str, subject: str, html_content: str):
    """
    Send email alert to admin
    """
    # Email configuration
    smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER', '')
    smtp_password = os.getenv('SMTP_PASSWORD', '')
    from_email = os.getenv('FROM_EMAIL', smtp_user)
    
    # Create message
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email
    
    # Add HTML content
    html_part = MIMEText(html_content, 'html')
    message.attach(html_part)
    
    # Send email
    try:
        await aiosmtplib.send(
            message,
            hostname=smtp_host,
            port=smtp_port,
            username=smtp_user,
            password=smtp_password,
            start_tls=True
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        # Fallback: print to console
        print(f"\n{'='*80}")
        print(f"EMAIL ALERT: {subject}")
        print(f"To: {to_email}")
        print(f"{'='*80}")
        print(html_content)
        print(f"{'='*80}\n")
        return False


def send_admin_alert_sync(to_email: str, subject: str, html_content: str):
    """
    Synchronous wrapper for Celery tasks
    """
    import asyncio
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(send_admin_alert(to_email, subject, html_content))
