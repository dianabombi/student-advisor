"""
Price monitoring API endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

# These will be injected by main.py
get_db = None
get_current_user = None

@router.get("/api/admin/price-monitoring/status")
async def get_price_monitoring_status(
    current_user=Depends(lambda: get_current_user),
    db: Session = Depends(lambda: get_db)
):
    """
    Get current pricing metrics and alert status
    """
    from tasks.price_monitoring import analyze_margin_from_logs, analyze_openai_cost_trend, THRESHOLDS
    from main import User
    
    # Calculate metrics
    total_users = db.query(User).filter(User.is_active == True).count()
    high_usage_users = db.query(User).filter(
        User.requests_used_this_month >= User.monthly_request_limit
    ).count()
    
    high_usage_percent = (high_usage_users / total_users * 100) if total_users > 0 else 0
    margin_data = analyze_margin_from_logs()
    cost_trend = analyze_openai_cost_trend()
    
    # Determine alert status
    alerts = []
    if high_usage_percent > THRESHOLDS['high_usage_percent']:
        alerts.append('HIGH_USAGE')
    if margin_data['margin_percent'] < THRESHOLDS['min_margin_percent']:
        alerts.append('LOW_MARGIN')
    if cost_trend['increase_percent'] > THRESHOLDS['openai_cost_increase']:
        alerts.append('OPENAI_COST_SPIKE')
    
    return {
        'status': 'critical' if len(alerts) > 0 else 'healthy',
        'metrics': {
            'high_usage_percent': round(high_usage_percent, 1),
            'margin_percent': round(margin_data['margin_percent'], 1),
            'openai_cost_trend': round(cost_trend['increase_percent'], 1),
        },
        'thresholds': THRESHOLDS,
        'alerts': alerts,
        'details': {
            'total_users': total_users,
            'high_usage_users': high_usage_users,
            'margin_data': margin_data,
            'cost_trend': cost_trend,
        }
    }


@router.post("/api/admin/price-monitoring/trigger")
async def trigger_price_monitoring(
    current_user=Depends(lambda: get_current_user)
):
    """
    Manually trigger price monitoring (for testing)
    """
    from tasks.price_monitoring import daily_price_monitoring
    
    task = daily_price_monitoring.delay()
    
    return {
        'status': 'triggered',
        'task_id': task.id,
        'message': 'Price monitoring task started'
    }
