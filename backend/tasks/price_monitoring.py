"""
AI Price Alert System - Proactive Monitoring
Monitors key metrics and alerts when pricing review is needed
"""

from celery import shared_task
from datetime import datetime, timedelta
from sqlalchemy import func
import json
import os
from openai import OpenAI

# OpenAI client (optional - won't crash if no API key)
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception:
    client = None  # Will be checked before use

# Thresholds for alerts
THRESHOLDS = {
    'high_usage_percent': 15,  # % of users hitting 500 request limit
    'min_margin_percent': 50,  # Minimum acceptable margin
    'openai_cost_increase': 30,  # % increase in OpenAI costs
}

@shared_task
def daily_price_monitoring():
    """
    Daily task to monitor pricing metrics and send alerts
    """
    from main import SessionLocal, User, logger
    from services.email_service import send_admin_alert
    
    db = SessionLocal()
    alerts = []
    
    try:
        # 1. Check high usage users (>15% hitting limit)
        total_users = db.query(User).filter(User.is_active == True).count()
        high_usage_users = db.query(User).filter(
            User.requests_used_this_month >= User.monthly_request_limit
        ).count()
        
        high_usage_percent = (high_usage_users / total_users * 100) if total_users > 0 else 0
        
        if high_usage_percent > THRESHOLDS['high_usage_percent']:
            alerts.append({
                'type': 'HIGH_USAGE',
                'severity': 'WARNING',
                'metric': f'{high_usage_percent:.1f}%',
                'threshold': f'{THRESHOLDS["high_usage_percent"]}%',
                'message': f'{high_usage_percent:.1f}% користувачів досягають ліміту 500 запитів (поріг: {THRESHOLDS["high_usage_percent"]}%)',
                'recommendation': 'Розгляньте підвищення цін або зменшення лімітів на базовому плані'
            })
        
        # 2. Check profit margin from logs
        margin_data = analyze_margin_from_logs()
        if margin_data['margin_percent'] < THRESHOLDS['min_margin_percent']:
            alerts.append({
                'type': 'LOW_MARGIN',
                'severity': 'CRITICAL',
                'metric': f'{margin_data["margin_percent"]:.1f}%',
                'threshold': f'{THRESHOLDS["min_margin_percent"]}%',
                'message': f'Маржа {margin_data["margin_percent"]:.1f}% нижче порогу {THRESHOLDS["min_margin_percent"]}%',
                'recommendation': 'ТЕРМІНОВО: Підвищіть ціни або оптимізуйте витрати на OpenAI',
                'details': margin_data
            })
        
        # 3. Check OpenAI cost trends
        cost_trend = analyze_openai_cost_trend()
        if cost_trend['increase_percent'] > THRESHOLDS['openai_cost_increase']:
            alerts.append({
                'type': 'OPENAI_COST_SPIKE',
                'severity': 'WARNING',
                'metric': f'+{cost_trend["increase_percent"]:.1f}%',
                'threshold': f'{THRESHOLDS["openai_cost_increase"]}%',
                'message': f'Витрати на OpenAI зросли на {cost_trend["increase_percent"]:.1f}% за тиждень',
                'recommendation': 'Перевірте чи не змінились ціни OpenAI. Можливо потрібно підняти ціни на {cost_trend["increase_percent"] * 0.7:.0f}%',
                'details': cost_trend
            })
        
        # 4. Log monitoring results
        logger.info("price_monitoring_completed",
                   total_users=total_users,
                   high_usage_percent=high_usage_percent,
                   margin_percent=margin_data['margin_percent'],
                   alerts_count=len(alerts))
        
        # 5. Send alerts if any
        if alerts:
            send_price_alerts(alerts)
            
        return {
            'status': 'completed',
            'alerts_count': len(alerts),
            'alerts': alerts
        }
        
    finally:
        db.close()


def analyze_margin_from_logs():
    """
    Analyze profit margin from structured logs
    """
    try:
        # Read last 7 days of logs
        seven_days_ago = datetime.now() - timedelta(days=7)
        
        total_revenue = 0  # From subscriptions
        total_openai_cost = 0
        
        # Parse logs for OpenAI costs
        with open('/app/logs/codex.log', 'r') as f:
            for line in f:
                try:
                    log = json.loads(line)
                    if log.get('timestamp', '') > seven_days_ago.isoformat():
                        if log.get('event') == 'openai_api_call':
                            total_openai_cost += log.get('cost_usd', 0)
                except:
                    continue
        
        # Estimate revenue (assuming $30/month average, 7 days = ~$7 per user)
        from main import SessionLocal, User
        db = SessionLocal()
        active_users = db.query(User).filter(User.is_active == True).count()
        db.close()
        
        estimated_weekly_revenue = active_users * 7  # $7 per user per week
        
        margin = estimated_weekly_revenue - total_openai_cost
        margin_percent = (margin / estimated_weekly_revenue * 100) if estimated_weekly_revenue > 0 else 0
        
        return {
            'revenue': estimated_weekly_revenue,
            'openai_cost': total_openai_cost,
            'margin': margin,
            'margin_percent': margin_percent,
            'period': '7 days'
        }
    except Exception as e:
        return {
            'revenue': 0,
            'openai_cost': 0,
            'margin': 0,
            'margin_percent': 100,
            'error': str(e)
        }


def analyze_openai_cost_trend():
    """
    Compare OpenAI costs: this week vs last week
    """
    try:
        now = datetime.now()
        this_week_start = now - timedelta(days=7)
        last_week_start = now - timedelta(days=14)
        
        this_week_cost = 0
        last_week_cost = 0
        
        with open('/app/logs/codex.log', 'r') as f:
            for line in f:
                try:
                    log = json.loads(line)
                    timestamp = log.get('timestamp', '')
                    
                    if log.get('event') == 'openai_api_call':
                        cost = log.get('cost_usd', 0)
                        
                        if timestamp > this_week_start.isoformat():
                            this_week_cost += cost
                        elif timestamp > last_week_start.isoformat():
                            last_week_cost += cost
                except:
                    continue
        
        increase = this_week_cost - last_week_cost
        increase_percent = (increase / last_week_cost * 100) if last_week_cost > 0 else 0
        
        return {
            'this_week_cost': this_week_cost,
            'last_week_cost': last_week_cost,
            'increase': increase,
            'increase_percent': increase_percent
        }
    except Exception as e:
        return {
            'this_week_cost': 0,
            'last_week_cost': 0,
            'increase': 0,
            'increase_percent': 0,
            'error': str(e)
        }


def send_price_alerts(alerts):
    """
    Send email alerts to admin
    """
    from services.email_service import send_admin_alert
    from main import logger
    
    # Group by severity
    critical = [a for a in alerts if a['severity'] == 'CRITICAL']
    warnings = [a for a in alerts if a['severity'] == 'WARNING']
    
    # Create email content
    subject = f"🚨 CODEX Price Alert: {len(critical)} Critical, {len(warnings)} Warnings"
    
    message = f"""
<h2>🚨 CODEX Price Monitoring Alert</h2>

<p><strong>Дата:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

<h3>📊 Підсумок</h3>
<ul>
    <li>Критичні попередження: {len(critical)}</li>
    <li>Попередження: {len(warnings)}</li>
</ul>
"""
    
    if critical:
        message += "<h3>🔴 КРИТИЧНО - Потребує негайних дій</h3><ul>"
        for alert in critical:
            message += f"""
<li>
    <strong>{alert['type']}</strong>: {alert['message']}<br>
    Метрика: {alert['metric']} (поріг: {alert['threshold']})<br>
    <em>Рекомендація: {alert['recommendation']}</em>
</li>
"""
        message += "</ul>"
    
    if warnings:
        message += "<h3>⚠️ Попередження</h3><ul>"
        for alert in warnings:
            message += f"""
<li>
    <strong>{alert['type']}</strong>: {alert['message']}<br>
    Метрика: {alert['metric']} (поріг: {alert['threshold']})<br>
    <em>Рекомендація: {alert['recommendation']}</em>
</li>
"""
        message += "</ul>"
    
    message += """
<hr>
<p><small>Це автоматичне повідомлення від AI Price Alert System</small></p>
"""
    
    # Send email
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@codex.com')
    
    try:
        send_admin_alert(admin_email, subject, message)
        logger.info("price_alert_sent", 
                   alerts_count=len(alerts),
                   critical=len(critical),
                   warnings=len(warnings))
    except Exception as e:
        logger.error("price_alert_send_failed", error=str(e))


# Manual trigger endpoint (for testing)
def trigger_price_monitoring():
    """
    Manually trigger price monitoring (for testing)
    """
    return daily_price_monitoring.delay()
