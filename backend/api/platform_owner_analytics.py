"""
Platform Owner Analytics API
Аналітика для власника платформи CODEX

Цей файл містить всі ендпоінти для відстеження:
- Відвідувачів сайту
- Реєстрацій користувачів
- Підписок та тарифів
- Виторгу
- Джерел трафіку
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from datetime import datetime, timedelta
from typing import Optional, List
import csv
import io
from fastapi.responses import StreamingResponse

# Імпорти будуть оновлені після додавання моделей в main.py
from main import (
    SessionLocal, User, Subscription, Payment, 
    get_current_user
)

router = APIRouter(prefix="/api/owner/analytics", tags=["Owner Analytics"])


def get_db():
    """Dependency для отримання сесії БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_owner_access(current_user: User):
    """Перевіряє чи користувач є власником платформи (admin)"""
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=403,
            detail="Access denied. Only platform owners can access analytics."
        )


@router.get("/dashboard")
async def get_analytics_dashboard(
    days: int = Query(30, description="Кількість днів для аналізу"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    📊 ГОЛОВНИЙ ДАШБОРД АНАЛІТИКИ
    
    Повертає всі ключові метрики платформи:
    - Загальна статистика
    - Відвідувачі
    - Реєстрації
    - Підписки
    - Виторг
    """
    verify_owner_access(current_user)
    
    from services.analytics_service import AnalyticsService
    
    # Визначаємо період
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Збираємо всі дані
    dashboard_data = {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days
        },
        "summary": {
            "unique_visitors": AnalyticsService.get_unique_visitors_count(db, start_date, end_date),
            "total_page_views": AnalyticsService.get_total_page_views(db, start_date, end_date),
            "registrations": AnalyticsService.get_registrations_count(db, start_date, end_date),
            "active_subscriptions": db.query(func.count(Subscription.id)).filter(
                Subscription.status == 'active'
            ).scalar() or 0,
            "total_revenue": AnalyticsService.get_revenue_statistics(db, start_date, end_date)['total_revenue']
        },
        "traffic_sources": AnalyticsService.get_traffic_sources(db, start_date, end_date),
        "device_statistics": AnalyticsService.get_device_statistics(db, start_date, end_date),
        "subscription_statistics": AnalyticsService.get_subscription_statistics(db, start_date, end_date),
        "revenue_statistics": AnalyticsService.get_revenue_statistics(db, start_date, end_date),
        "conversion_funnel": AnalyticsService.get_conversion_funnel(db, start_date, end_date)
    }
    
    return dashboard_data


@router.get("/visitors")
async def get_visitor_analytics(
    days: int = Query(30, description="Кількість днів для аналізу"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    👥 АНАЛІТИКА ВІДВІДУВАЧІВ
    
    Детальна інформація про відвідувачів сайту
    """
    verify_owner_access(current_user)
    
    from services.analytics_service import AnalyticsService
    from main import VisitorTracking
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Графік відвідувачів по днях
    visitors_chart = AnalyticsService.get_time_series_data(db, 'visitors', days)
    
    # Топ джерела трафіку
    traffic_sources = AnalyticsService.get_traffic_sources(db, start_date, end_date)
    
    # Статистика по пристроях
    device_stats = AnalyticsService.get_device_statistics(db, start_date, end_date)
    
    # Останні відвідувачі
    recent_visitors = db.query(VisitorTracking).filter(
        VisitorTracking.first_visit >= start_date
    ).order_by(desc(VisitorTracking.first_visit)).limit(50).all()
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days
        },
        "total_unique_visitors": AnalyticsService.get_unique_visitors_count(db, start_date, end_date),
        "total_page_views": AnalyticsService.get_total_page_views(db, start_date, end_date),
        "visitors_chart": visitors_chart,
        "traffic_sources": traffic_sources,
        "device_statistics": device_stats,
        "recent_visitors": [
            {
                "id": v.id,
                "first_visit": v.first_visit.isoformat(),
                "last_visit": v.last_visit.isoformat(),
                "visit_count": v.visit_count,
                "traffic_source": v.traffic_source,
                "device_type": v.device_type,
                "browser": v.browser,
                "os": v.os,
                "is_registered": v.user_id is not None
            }
            for v in recent_visitors
        ]
    }


@router.get("/users")
async def get_user_analytics(
    days: int = Query(30, description="Кількість днів для аналізу"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    👤 АНАЛІТИКА КОРИСТУВАЧІВ
    
    Інформація про реєстрації та користувачів
    """
    verify_owner_access(current_user)
    
    from services.analytics_service import AnalyticsService
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Графік реєстрацій по днях
    registrations_chart = AnalyticsService.get_time_series_data(db, 'registrations', days)
    
    # Останні реєстрації з детальною інформацією
    recent_users = db.query(User).filter(
        User.created_at >= start_date
    ).order_by(desc(User.created_at)).limit(100).all()
    
    # Статистика по ролях
    role_stats = db.query(
        User.role,
        func.count(User.id).label('count')
    ).filter(
        User.created_at >= start_date
    ).group_by(User.role).all()
    
    # Статистика по статусах підписок
    subscription_status_stats = db.query(
        User.subscription_status,
        func.count(User.id).label('count')
    ).filter(
        User.created_at >= start_date
    ).group_by(User.subscription_status).all()
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days
        },
        "total_registrations": AnalyticsService.get_registrations_count(db, start_date, end_date),
        "registrations_chart": registrations_chart,
        "role_statistics": [
            {"role": role or 'unknown', "count": count}
            for role, count in role_stats
        ],
        "subscription_status_statistics": [
            {"status": status or 'unknown', "count": count}
            for status, count in subscription_status_stats
        ],
        "recent_registrations": [
            {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "role": u.role,
                "created_at": u.created_at.isoformat(),
                "subscription_status": u.subscription_status,
                "trial_end_date": u.trial_end_date.isoformat() if u.trial_end_date else None,
                "consent_ip_address": u.consent_ip_address,
                "consent_user_agent": u.consent_user_agent,
                "traffic_source": None  # Можна додати зв'язок з VisitorTracking
            }
            for u in recent_users
        ]
    }


@router.get("/subscriptions")
async def get_subscription_analytics(
    days: int = Query(30, description="Кількість днів для аналізу"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    💳 АНАЛІТИКА ПІДПИСОК
    
    Статистика по тарифах та підписках
    """
    verify_owner_access(current_user)
    
    from services.analytics_service import AnalyticsService
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Графік підписок по днях
    subscriptions_chart = AnalyticsService.get_time_series_data(db, 'subscriptions', days)
    
    # Статистика по підписках
    subscription_stats = AnalyticsService.get_subscription_statistics(db, start_date, end_date)
    
    # Останні підписки
    recent_subscriptions = db.query(Subscription).filter(
        Subscription.created_at >= start_date
    ).order_by(desc(Subscription.created_at)).limit(100).all()
    
    # Статистика по статусах
    status_stats = db.query(
        Subscription.status,
        func.count(Subscription.id).label('count')
    ).filter(
        Subscription.created_at >= start_date
    ).group_by(Subscription.status).all()
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days
        },
        "subscriptions_chart": subscriptions_chart,
        "subscription_statistics": subscription_stats,
        "status_statistics": [
            {"status": status or 'unknown', "count": count}
            for status, count in status_stats
        ],
        "recent_subscriptions": [
            {
                "id": s.id,
                "user_id": s.user_id,
                "plan_type": s.plan_type,
                "amount": s.amount,
                "status": s.status,
                "is_trial": s.is_trial,
                "start_date": s.start_date.isoformat() if s.start_date else None,
                "end_date": s.end_date.isoformat() if s.end_date else None,
                "created_at": s.created_at.isoformat()
            }
            for s in recent_subscriptions
        ]
    }


@router.get("/revenue")
async def get_revenue_analytics(
    days: int = Query(30, description="Кількість днів для аналізу"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    💰 АНАЛІТИКА ВИТОРГУ
    
    Детальна інформація про доходи платформи
    """
    verify_owner_access(current_user)
    
    from services.analytics_service import AnalyticsService
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Графік виторгу по днях
    revenue_chart = AnalyticsService.get_time_series_data(db, 'revenue', days)
    
    # Статистика виторгу
    revenue_stats = AnalyticsService.get_revenue_statistics(db, start_date, end_date)
    
    # Останні платежі
    recent_payments = db.query(Payment).filter(
        Payment.created_at >= start_date,
        Payment.status == 'completed'
    ).order_by(desc(Payment.created_at)).limit(100).all()
    
    # Виторг по місяцях (останні 12 місяців)
    monthly_revenue = []
    for i in range(12):
        month_start = datetime.utcnow().replace(day=1) - timedelta(days=30*i)
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1)
        
        revenue = db.query(func.sum(Payment.amount)).filter(
            and_(
                Payment.created_at >= month_start,
                Payment.created_at < month_end,
                Payment.status == 'completed'
            )
        ).scalar() or 0
        
        monthly_revenue.append({
            "month": month_start.strftime('%Y-%m'),
            "revenue": revenue
        })
    
    monthly_revenue.reverse()
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days
        },
        "revenue_chart": revenue_chart,
        "revenue_statistics": revenue_stats,
        "monthly_revenue": monthly_revenue,
        "recent_payments": [
            {
                "id": p.id,
                "user_id": p.user_id,
                "amount": p.amount,
                "currency": p.currency,
                "status": p.status,
                "payment_method": p.payment_method,
                "transaction_id": p.transaction_id,
                "created_at": p.created_at.isoformat()
            }
            for p in recent_payments
        ]
    }


@router.get("/charts/visitors")
async def get_visitors_chart(
    days: int = Query(30, description="Кількість днів"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """📈 Графік відвідувачів по днях"""
    verify_owner_access(current_user)
    
    from services.analytics_service import AnalyticsService
    
    return {
        "chart_data": AnalyticsService.get_time_series_data(db, 'visitors', days)
    }


@router.get("/charts/registrations")
async def get_registrations_chart(
    days: int = Query(30, description="Кількість днів"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """📈 Графік реєстрацій по днях"""
    verify_owner_access(current_user)
    
    from services.analytics_service import AnalyticsService
    
    return {
        "chart_data": AnalyticsService.get_time_series_data(db, 'registrations', days)
    }


@router.get("/charts/revenue")
async def get_revenue_chart(
    days: int = Query(30, description="Кількість днів"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """📈 Графік виторгу по днях"""
    verify_owner_access(current_user)
    
    from services.analytics_service import AnalyticsService
    
    return {
        "chart_data": AnalyticsService.get_time_series_data(db, 'revenue', days)
    }


@router.get("/export/csv")
async def export_analytics_csv(
    report_type: str = Query(..., description="Тип звіту: users, subscriptions, payments, visitors"),
    days: int = Query(30, description="Кількість днів"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    📥 ЕКСПОРТ ДАНИХ В CSV
    
    Експортує аналітичні дані в CSV файл
    """
    verify_owner_access(current_user)
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Створюємо CSV в пам'яті
    output = io.StringIO()
    writer = csv.writer(output)
    
    if report_type == 'users':
        # Експорт користувачів
        writer.writerow(['ID', 'Name', 'Email', 'Role', 'Created At', 'Subscription Status', 'Trial End', 'IP Address', 'User Agent'])
        users = db.query(User).filter(User.created_at >= start_date).order_by(desc(User.created_at)).all()
        for u in users:
            writer.writerow([
                u.id, u.name, u.email, u.role, u.created_at.isoformat(),
                u.subscription_status, u.trial_end_date.isoformat() if u.trial_end_date else '',
                u.consent_ip_address or '', u.consent_user_agent or ''
            ])
    
    elif report_type == 'subscriptions':
        # Експорт підписок
        writer.writerow(['ID', 'User ID', 'Plan Type', 'Amount', 'Status', 'Is Trial', 'Start Date', 'End Date', 'Created At'])
        subscriptions = db.query(Subscription).filter(Subscription.created_at >= start_date).order_by(desc(Subscription.created_at)).all()
        for s in subscriptions:
            writer.writerow([
                s.id, s.user_id, s.plan_type, s.amount, s.status, s.is_trial,
                s.start_date.isoformat() if s.start_date else '',
                s.end_date.isoformat() if s.end_date else '',
                s.created_at.isoformat()
            ])
    
    elif report_type == 'payments':
        # Експорт платежів
        writer.writerow(['ID', 'User ID', 'Amount', 'Currency', 'Status', 'Payment Method', 'Transaction ID', 'Created At'])
        payments = db.query(Payment).filter(Payment.created_at >= start_date).order_by(desc(Payment.created_at)).all()
        for p in payments:
            writer.writerow([
                p.id, p.user_id, p.amount, p.currency, p.status,
                p.payment_method or '', p.transaction_id or '',
                p.created_at.isoformat()
            ])
    
    elif report_type == 'visitors':
        # Експорт відвідувачів
        from main import VisitorTracking
        writer.writerow(['ID', 'First Visit', 'Last Visit', 'Visit Count', 'Traffic Source', 'UTM Source', 'Device Type', 'Browser', 'OS', 'Registered'])
        visitors = db.query(VisitorTracking).filter(VisitorTracking.first_visit >= start_date).order_by(desc(VisitorTracking.first_visit)).all()
        for v in visitors:
            writer.writerow([
                v.id, v.first_visit.isoformat(), v.last_visit.isoformat(),
                v.visit_count, v.traffic_source or '', v.utm_source or '',
                v.device_type or '', v.browser or '', v.os or '',
                'Yes' if v.user_id else 'No'
            ])
    
    else:
        raise HTTPException(status_code=400, detail="Invalid report type")
    
    # Повертаємо CSV файл
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=codex_analytics_{report_type}_{datetime.utcnow().strftime('%Y%m%d')}.csv"
        }
    )


@router.get("/funnel")
async def get_conversion_funnel(
    days: int = Query(30, description="Кількість днів"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    🎯 ВОРОНКА КОНВЕРСІЇ
    
    Показує як відвідувачі конвертуються в платних користувачів
    """
    verify_owner_access(current_user)
    
    from services.analytics_service import AnalyticsService
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    funnel_data = AnalyticsService.get_conversion_funnel(db, start_date, end_date)
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days
        },
        **funnel_data
    }


# ==================== MARKETING ANALYTICS ENDPOINTS ====================

@router.get("/marketing/roi")
async def get_marketing_roi(
    days: int = Query(30, description="Кількість днів для аналізу"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    💰 ROI ПО КАНАЛАХ
    
    Розраховує ROI (Return on Investment) для кожного маркетингового каналу
    """
    verify_owner_access(current_user)
    
    from services.analytics_service import AnalyticsService
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    roi_data = AnalyticsService.get_marketing_roi_by_channel(db, start_date, end_date)
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days
        },
        "channels": roi_data
    }


@router.get("/marketing/cac")
async def get_customer_acquisition_cost(
    days: int = Query(30, description="Кількість днів для аналізу"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    💵 CAC (Customer Acquisition Cost)
    
    Розраховує вартість залучення клієнта
    """
    verify_owner_access(current_user)
    
    from services.analytics_service import AnalyticsService
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    cac_data = AnalyticsService.calculate_cac(db, start_date, end_date)
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days
        },
        **cac_data
    }


@router.get("/marketing/campaigns")
async def get_campaign_effectiveness(
    days: int = Query(30, description="Кількість днів для аналізу"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    📊 ЕФЕКТИВНІСТЬ РЕКЛАМНИХ КАМПАНІЙ
    
    Детальний аналіз кожної рекламної кампанії
    """
    verify_owner_access(current_user)
    
    from services.analytics_service import AnalyticsService
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    campaigns_data = AnalyticsService.get_campaign_effectiveness(db, start_date, end_date)
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days
        },
        "campaigns": campaigns_data,
        "total_campaigns": len(campaigns_data)
    }


@router.get("/marketing/channel-comparison")
async def get_channel_comparison(
    days: int = Query(30, description="Кількість днів для аналізу"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    🔍 ПОРІВНЯННЯ КАНАЛІВ
    
    Порівняння ефективності різних маркетингових каналів
    """
    verify_owner_access(current_user)
    
    from services.analytics_service import AnalyticsService
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    comparison_data = AnalyticsService.get_channel_comparison(db, start_date, end_date)
    
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days
        },
        **comparison_data
    }


# Campaign Management Endpoints (CRUD)

from pydantic import BaseModel

class CampaignCreate(BaseModel):
    campaign_name: str
    utm_campaign: Optional[str] = None
    utm_source: Optional[str] = None
    utm_medium: Optional[str] = None
    channel: Optional[str] = None
    cost: int  # in EUR cents
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    notes: Optional[str] = None


@router.post("/marketing/campaigns/create")
async def create_campaign(
    campaign: CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    ➕ СТВОРИТИ КАМПАНІЮ
    
    Додає нову маркетингову кампанію для відстеження
    """
    verify_owner_access(current_user)
    
    from main import MarketingCampaign
    
    new_campaign = MarketingCampaign(
        campaign_name=campaign.campaign_name,
        utm_campaign=campaign.utm_campaign,
        utm_source=campaign.utm_source,
        utm_medium=campaign.utm_medium,
        channel=campaign.channel,
        cost=campaign.cost,
        start_date=campaign.start_date,
        end_date=campaign.end_date,
        notes=campaign.notes,
        is_active=True
    )
    
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    
    return {
        "message": "Campaign created successfully",
        "campaign_id": new_campaign.id,
        "campaign_name": new_campaign.campaign_name
    }


@router.get("/marketing/campaigns/list")
async def list_campaigns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    📋 СПИСОК КАМПАНІЙ
    
    Отримує список всіх маркетингових кампаній
    """
    verify_owner_access(current_user)
    
    from main import MarketingCampaign
    
    campaigns = db.query(MarketingCampaign).order_by(desc(MarketingCampaign.created_at)).all()
    
    return {
        "campaigns": [
            {
                "id": c.id,
                "campaign_name": c.campaign_name,
                "utm_campaign": c.utm_campaign,
                "utm_source": c.utm_source,
                "utm_medium": c.utm_medium,
                "channel": c.channel,
                "cost": c.cost,
                "start_date": c.start_date.isoformat() if c.start_date else None,
                "end_date": c.end_date.isoformat() if c.end_date else None,
                "is_active": c.is_active,
                "created_at": c.created_at.isoformat()
            }
            for c in campaigns
        ],
        "total": len(campaigns)
    }
