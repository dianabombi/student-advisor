"""
Analytics Service для обробки та агрегації аналітичних даних
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, extract
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json


class AnalyticsService:
    """Сервіс для обробки аналітичних даних"""
    
    @staticmethod
    def get_unique_visitors_count(db: Session, start_date: Optional[datetime] = None, 
                                  end_date: Optional[datetime] = None) -> int:
        """
        Підраховує кількість унікальних відвідувачів за період
        """
        from main import VisitorTracking
        
        query = db.query(func.count(func.distinct(VisitorTracking.visitor_fingerprint)))
        
        if start_date:
            query = query.filter(VisitorTracking.first_visit >= start_date)
        if end_date:
            query = query.filter(VisitorTracking.first_visit <= end_date)
        
        return query.scalar() or 0
    
    @staticmethod
    def get_total_page_views(db: Session, start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None) -> int:
        """
        Підраховує загальну кількість переглядів сторінок
        """
        from main import PageView
        
        query = db.query(func.count(PageView.id))
        
        if start_date:
            query = query.filter(PageView.created_at >= start_date)
        if end_date:
            query = query.filter(PageView.created_at <= end_date)
        
        return query.scalar() or 0
    
    @staticmethod
    def get_registrations_count(db: Session, start_date: Optional[datetime] = None,
                                end_date: Optional[datetime] = None) -> int:
        """
        Підраховує кількість реєстрацій за період
        """
        from main import User
        
        query = db.query(func.count(User.id))
        
        if start_date:
            query = query.filter(User.created_at >= start_date)
        if end_date:
            query = query.filter(User.created_at <= end_date)
        
        return query.scalar() or 0
    
    @staticmethod
    def get_traffic_sources(db: Session, start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None) -> List[Dict]:
        """
        Отримує статистику по джерелах трафіку
        """
        from main import VisitorTracking
        
        query = db.query(
            VisitorTracking.traffic_source,
            func.count(VisitorTracking.id).label('count')
        ).group_by(VisitorTracking.traffic_source)
        
        if start_date:
            query = query.filter(VisitorTracking.first_visit >= start_date)
        if end_date:
            query = query.filter(VisitorTracking.first_visit <= end_date)
        
        results = query.all()
        
        return [
            {
                'source': source or 'unknown',
                'count': count
            }
            for source, count in results
        ]
    
    @staticmethod
    def get_device_statistics(db: Session, start_date: Optional[datetime] = None,
                             end_date: Optional[datetime] = None) -> Dict:
        """
        Отримує статистику по пристроях
        """
        from main import VisitorTracking
        
        # Статистика по типах пристроїв
        device_query = db.query(
            VisitorTracking.device_type,
            func.count(VisitorTracking.id).label('count')
        ).group_by(VisitorTracking.device_type)
        
        if start_date:
            device_query = device_query.filter(VisitorTracking.first_visit >= start_date)
        if end_date:
            device_query = device_query.filter(VisitorTracking.first_visit <= end_date)
        
        devices = device_query.all()
        
        # Статистика по браузерах
        browser_query = db.query(
            VisitorTracking.browser,
            func.count(VisitorTracking.id).label('count')
        ).group_by(VisitorTracking.browser)
        
        if start_date:
            browser_query = browser_query.filter(VisitorTracking.first_visit >= start_date)
        if end_date:
            browser_query = browser_query.filter(VisitorTracking.first_visit <= end_date)
        
        browsers = browser_query.all()
        
        # Статистика по ОС
        os_query = db.query(
            VisitorTracking.os,
            func.count(VisitorTracking.id).label('count')
        ).group_by(VisitorTracking.os)
        
        if start_date:
            os_query = os_query.filter(VisitorTracking.first_visit >= start_date)
        if end_date:
            os_query = os_query.filter(VisitorTracking.first_visit <= end_date)
        
        operating_systems = os_query.all()
        
        return {
            'devices': [{'type': d or 'unknown', 'count': c} for d, c in devices],
            'browsers': [{'name': b or 'unknown', 'count': c} for b, c in browsers],
            'operating_systems': [{'name': o or 'unknown', 'count': c} for o, c in operating_systems]
        }
    
    @staticmethod
    def get_subscription_statistics(db: Session, start_date: Optional[datetime] = None,
                                   end_date: Optional[datetime] = None) -> Dict:
        """
        Отримує статистику по підписках
        """
        from main import Subscription
        
        # Статистика по тарифах
        plan_query = db.query(
            Subscription.plan_type,
            func.count(Subscription.id).label('count'),
            func.sum(Subscription.amount).label('total_amount')
        ).group_by(Subscription.plan_type)
        
        if start_date:
            plan_query = plan_query.filter(Subscription.created_at >= start_date)
        if end_date:
            plan_query = plan_query.filter(Subscription.created_at <= end_date)
        
        plans = plan_query.all()
        
        # Конверсія з trial в платну підписку
        trial_count = db.query(func.count(Subscription.id)).filter(
            Subscription.is_trial == True
        )
        if start_date:
            trial_count = trial_count.filter(Subscription.created_at >= start_date)
        if end_date:
            trial_count = trial_count.filter(Subscription.created_at <= end_date)
        trial_count = trial_count.scalar() or 0
        
        paid_count = db.query(func.count(Subscription.id)).filter(
            Subscription.is_trial == False,
            Subscription.status == 'active'
        )
        if start_date:
            paid_count = paid_count.filter(Subscription.created_at >= start_date)
        if end_date:
            paid_count = paid_count.filter(Subscription.created_at <= end_date)
        paid_count = paid_count.scalar() or 0
        
        conversion_rate = (paid_count / trial_count * 100) if trial_count > 0 else 0
        
        return {
            'plans': [
                {
                    'plan_type': plan or 'unknown',
                    'count': count,
                    'total_revenue': total or 0
                }
                for plan, count, total in plans
            ],
            'trial_count': trial_count,
            'paid_count': paid_count,
            'conversion_rate': round(conversion_rate, 2)
        }
    
    @staticmethod
    def get_revenue_statistics(db: Session, start_date: Optional[datetime] = None,
                              end_date: Optional[datetime] = None) -> Dict:
        """
        Отримує статистику по виторгу
        """
        from main import Payment, Subscription
        
        # Загальний виторг з платежів
        payment_query = db.query(
            func.sum(Payment.amount).label('total')
        ).filter(Payment.status == 'completed')
        
        if start_date:
            payment_query = payment_query.filter(Payment.created_at >= start_date)
        if end_date:
            payment_query = payment_query.filter(Payment.created_at <= end_date)
        
        total_revenue = payment_query.scalar() or 0
        
        # Виторг по тарифах
        revenue_by_plan = db.query(
            Subscription.plan_type,
            func.sum(Subscription.amount).label('revenue')
        ).filter(
            Subscription.status == 'active',
            Subscription.is_trial == False
        ).group_by(Subscription.plan_type)
        
        if start_date:
            revenue_by_plan = revenue_by_plan.filter(Subscription.created_at >= start_date)
        if end_date:
            revenue_by_plan = revenue_by_plan.filter(Subscription.created_at <= end_date)
        
        revenue_by_plan = revenue_by_plan.all()
        
        # Кількість платежів
        payment_count = db.query(func.count(Payment.id)).filter(
            Payment.status == 'completed'
        )
        if start_date:
            payment_count = payment_count.filter(Payment.created_at >= start_date)
        if end_date:
            payment_count = payment_count.filter(Payment.created_at <= end_date)
        payment_count = payment_count.scalar() or 0
        
        # Середній чек
        average_payment = (total_revenue / payment_count) if payment_count > 0 else 0
        
        return {
            'total_revenue': total_revenue,
            'payment_count': payment_count,
            'average_payment': round(average_payment, 2),
            'revenue_by_plan': [
                {
                    'plan_type': plan or 'unknown',
                    'revenue': revenue or 0
                }
                for plan, revenue in revenue_by_plan
            ]
        }
    
    @staticmethod
    def get_time_series_data(db: Session, metric: str, days: int = 30) -> List[Dict]:
        """
        Отримує дані для графіків по днях
        metric: 'visitors', 'registrations', 'subscriptions', 'revenue'
        """
        from main import VisitorTracking, User, Subscription, Payment
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        result = []
        
        for i in range(days):
            day_start = start_date + timedelta(days=i)
            day_end = day_start + timedelta(days=1)
            
            if metric == 'visitors':
                count = db.query(func.count(func.distinct(VisitorTracking.visitor_fingerprint))).filter(
                    and_(
                        VisitorTracking.first_visit >= day_start,
                        VisitorTracking.first_visit < day_end
                    )
                ).scalar() or 0
            elif metric == 'registrations':
                count = db.query(func.count(User.id)).filter(
                    and_(
                        User.created_at >= day_start,
                        User.created_at < day_end
                    )
                ).scalar() or 0
            elif metric == 'subscriptions':
                count = db.query(func.count(Subscription.id)).filter(
                    and_(
                        Subscription.created_at >= day_start,
                        Subscription.created_at < day_end,
                        Subscription.is_trial == False
                    )
                ).scalar() or 0
            elif metric == 'revenue':
                count = db.query(func.sum(Payment.amount)).filter(
                    and_(
                        Payment.created_at >= day_start,
                        Payment.created_at < day_end,
                        Payment.status == 'completed'
                    )
                ).scalar() or 0
            else:
                count = 0
            
            result.append({
                'date': day_start.strftime('%Y-%m-%d'),
                'value': count
            })
        
        return result
    
    @staticmethod
    def get_conversion_funnel(db: Session, start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None) -> Dict:
        """
        Отримує дані воронки конверсії
        """
        from main import VisitorTracking, User, Subscription
        
        # Крок 1: Відвідувачі
        visitors_query = db.query(func.count(func.distinct(VisitorTracking.visitor_fingerprint)))
        if start_date:
            visitors_query = visitors_query.filter(VisitorTracking.first_visit >= start_date)
        if end_date:
            visitors_query = visitors_query.filter(VisitorTracking.first_visit <= end_date)
        visitors = visitors_query.scalar() or 0
        
        # Крок 2: Реєстрації
        registrations_query = db.query(func.count(User.id))
        if start_date:
            registrations_query = registrations_query.filter(User.created_at >= start_date)
        if end_date:
            registrations_query = registrations_query.filter(User.created_at <= end_date)
        registrations = registrations_query.scalar() or 0
        
        # Крок 3: Trial активації
        trials_query = db.query(func.count(Subscription.id)).filter(Subscription.is_trial == True)
        if start_date:
            trials_query = trials_query.filter(Subscription.created_at >= start_date)
        if end_date:
            trials_query = trials_query.filter(Subscription.created_at <= end_date)
        trials = trials_query.scalar() or 0
        
        # Крок 4: Платні підписки
        paid_query = db.query(func.count(Subscription.id)).filter(
            Subscription.is_trial == False,
            Subscription.status == 'active'
        )
        if start_date:
            paid_query = paid_query.filter(Subscription.created_at >= start_date)
        if end_date:
            paid_query = paid_query.filter(Subscription.created_at <= end_date)
        paid = paid_query.scalar() or 0
        
        # Розрахунок конверсій
        visitor_to_registration = (registrations / visitors * 100) if visitors > 0 else 0
        registration_to_trial = (trials / registrations * 100) if registrations > 0 else 0
        trial_to_paid = (paid / trials * 100) if trials > 0 else 0
        overall_conversion = (paid / visitors * 100) if visitors > 0 else 0
        
        return {
            'funnel': [
                {'step': 'Відвідувачі', 'count': visitors, 'conversion': 100},
                {'step': 'Реєстрації', 'count': registrations, 'conversion': round(visitor_to_registration, 2)},
                {'step': 'Trial', 'count': trials, 'conversion': round(registration_to_trial, 2)},
                {'step': 'Платні підписки', 'count': paid, 'conversion': round(trial_to_paid, 2)}
            ],
            'overall_conversion': round(overall_conversion, 2)
        }
    
    # ==================== MARKETING ANALYTICS ====================
    
    @staticmethod
    def get_marketing_roi_by_channel(db: Session, start_date: Optional[datetime] = None,
                                     end_date: Optional[datetime] = None) -> List[Dict]:
        """
        Розраховує ROI (Return on Investment) по каналах
        ROI = (Revenue - Cost) / Cost * 100%
        """
        from main import MarketingCampaign, VisitorTracking, User, Payment
        
        # Отримуємо всі кампанії
        campaigns_query = db.query(MarketingCampaign).filter(MarketingCampaign.cost > 0)
        
        if start_date:
            campaigns_query = campaigns_query.filter(
                or_(
                    MarketingCampaign.start_date >= start_date,
                    MarketingCampaign.start_date == None
                )
            )
        if end_date:
            campaigns_query = campaigns_query.filter(
                or_(
                    MarketingCampaign.end_date <= end_date,
                    MarketingCampaign.end_date == None
                )
            )
        
        campaigns = campaigns_query.all()
        
        roi_by_channel = {}
        
        for campaign in campaigns:
            channel = campaign.channel or 'unknown'
            
            # Знаходимо відвідувачів з цієї кампанії
            visitors_query = db.query(VisitorTracking).filter(
                or_(
                    VisitorTracking.utm_campaign == campaign.utm_campaign,
                    and_(
                        VisitorTracking.utm_source == campaign.utm_source,
                        VisitorTracking.utm_medium == campaign.utm_medium
                    )
                )
            )
            
            if start_date:
                visitors_query = visitors_query.filter(VisitorTracking.first_visit >= start_date)
            if end_date:
                visitors_query = visitors_query.filter(VisitorTracking.first_visit <= end_date)
            
            visitors = visitors_query.all()
            visitor_ids = [v.user_id for v in visitors if v.user_id]
            
            # Рахуємо виторг від цих користувачів
            if visitor_ids:
                revenue = db.query(func.sum(Payment.amount)).filter(
                    Payment.user_id.in_(visitor_ids),
                    Payment.status == 'completed'
                ).scalar() or 0
            else:
                revenue = 0
            
            # Агрегуємо по каналах
            if channel not in roi_by_channel:
                roi_by_channel[channel] = {
                    'channel': channel,
                    'cost': 0,
                    'revenue': 0,
                    'conversions': 0,
                    'visitors': 0
                }
            
            roi_by_channel[channel]['cost'] += campaign.cost
            roi_by_channel[channel]['revenue'] += revenue
            roi_by_channel[channel]['conversions'] += len(visitor_ids)
            roi_by_channel[channel]['visitors'] += len(visitors)
        
        # Розраховуємо ROI для кожного каналу
        result = []
        for channel_data in roi_by_channel.values():
            cost = channel_data['cost']
            revenue = channel_data['revenue']
            
            if cost > 0:
                roi = ((revenue - cost) / cost) * 100
                roas = (revenue / cost) if cost > 0 else 0  # Return on Ad Spend
            else:
                roi = 0
                roas = 0
            
            result.append({
                'channel': channel_data['channel'],
                'cost': cost,
                'revenue': revenue,
                'profit': revenue - cost,
                'roi': round(roi, 2),
                'roas': round(roas, 2),
                'conversions': channel_data['conversions'],
                'visitors': channel_data['visitors'],
                'conversion_rate': round((channel_data['conversions'] / channel_data['visitors'] * 100), 2) if channel_data['visitors'] > 0 else 0
            })
        
        # Сортуємо по ROI (найкращі спочатку)
        result.sort(key=lambda x: x['roi'], reverse=True)
        
        return result
    
    @staticmethod
    def calculate_cac(db: Session, start_date: Optional[datetime] = None,
                     end_date: Optional[datetime] = None) -> Dict:
        """
        Розраховує CAC (Customer Acquisition Cost) - вартість залучення клієнта
        CAC = Total Marketing Cost / Number of New Customers
        """
        from main import MarketingCampaign, User, Subscription
        
        # Загальні витрати на маркетинг
        campaigns_query = db.query(func.sum(MarketingCampaign.cost))
        
        if start_date:
            campaigns_query = campaigns_query.filter(
                or_(
                    MarketingCampaign.start_date >= start_date,
                    MarketingCampaign.start_date == None
                )
            )
        if end_date:
            campaigns_query = campaigns_query.filter(
                or_(
                    MarketingCampaign.end_date <= end_date,
                    MarketingCampaign.end_date == None
                )
            )
        
        total_marketing_cost = campaigns_query.scalar() or 0
        
        # Кількість нових платних клієнтів
        paid_customers_query = db.query(func.count(func.distinct(Subscription.user_id))).filter(
            Subscription.is_trial == False,
            Subscription.status == 'active'
        )
        
        if start_date:
            paid_customers_query = paid_customers_query.filter(Subscription.created_at >= start_date)
        if end_date:
            paid_customers_query = paid_customers_query.filter(Subscription.created_at <= end_date)
        
        paid_customers = paid_customers_query.scalar() or 0
        
        # Кількість всіх реєстрацій (включаючи trial)
        registrations_query = db.query(func.count(User.id))
        
        if start_date:
            registrations_query = registrations_query.filter(User.created_at >= start_date)
        if end_date:
            registrations_query = registrations_query.filter(User.created_at <= end_date)
        
        total_registrations = registrations_query.scalar() or 0
        
        # CAC для платних клієнтів
        cac_paid = (total_marketing_cost / paid_customers) if paid_customers > 0 else 0
        
        # CAC для всіх реєстрацій
        cac_all = (total_marketing_cost / total_registrations) if total_registrations > 0 else 0
        
        # Середній LTV (Lifetime Value) - середній виторг на клієнта
        avg_revenue_query = db.query(func.avg(Subscription.amount)).filter(
            Subscription.is_trial == False,
            Subscription.status == 'active'
        )
        
        if start_date:
            avg_revenue_query = avg_revenue_query.filter(Subscription.created_at >= start_date)
        if end_date:
            avg_revenue_query = avg_revenue_query.filter(Subscription.created_at <= end_date)
        
        avg_ltv = avg_revenue_query.scalar() or 0
        
        # LTV:CAC Ratio (має бути > 3 для здорового бізнесу)
        ltv_cac_ratio = (avg_ltv / cac_paid) if cac_paid > 0 else 0
        
        return {
            'total_marketing_cost': total_marketing_cost,
            'paid_customers': paid_customers,
            'total_registrations': total_registrations,
            'cac_paid_customers': round(cac_paid, 2),
            'cac_all_users': round(cac_all, 2),
            'average_ltv': round(avg_ltv, 2),
            'ltv_cac_ratio': round(ltv_cac_ratio, 2),
            'is_healthy': ltv_cac_ratio > 3  # Здоровий бізнес якщо LTV > 3x CAC
        }
    
    @staticmethod
    def get_campaign_effectiveness(db: Session, start_date: Optional[datetime] = None,
                                   end_date: Optional[datetime] = None) -> List[Dict]:
        """
        Аналіз ефективності кожної рекламної кампанії
        """
        from main import MarketingCampaign, VisitorTracking, User, Payment, Subscription
        
        campaigns_query = db.query(MarketingCampaign)
        
        if start_date:
            campaigns_query = campaigns_query.filter(
                or_(
                    MarketingCampaign.start_date >= start_date,
                    MarketingCampaign.start_date == None
                )
            )
        if end_date:
            campaigns_query = campaigns_query.filter(
                or_(
                    MarketingCampaign.end_date <= end_date,
                    MarketingCampaign.end_date == None
                )
            )
        
        campaigns = campaigns_query.all()
        
        results = []
        
        for campaign in campaigns:
            # Знаходимо відвідувачів з цієї кампанії
            visitors_query = db.query(VisitorTracking).filter(
                or_(
                    VisitorTracking.utm_campaign == campaign.utm_campaign,
                    and_(
                        VisitorTracking.utm_source == campaign.utm_source,
                        VisitorTracking.utm_medium == campaign.utm_medium
                    )
                )
            )
            
            if start_date:
                visitors_query = visitors_query.filter(VisitorTracking.first_visit >= start_date)
            if end_date:
                visitors_query = visitors_query.filter(VisitorTracking.first_visit <= end_date)
            
            visitors = visitors_query.all()
            total_visitors = len(visitors)
            
            # Користувачі що зареєструвалися
            registered_user_ids = [v.user_id for v in visitors if v.user_id]
            registrations = len(registered_user_ids)
            
            # Платні підписки
            if registered_user_ids:
                paid_subscriptions = db.query(func.count(Subscription.id)).filter(
                    Subscription.user_id.in_(registered_user_ids),
                    Subscription.is_trial == False,
                    Subscription.status == 'active'
                ).scalar() or 0
                
                # Виторг
                revenue = db.query(func.sum(Payment.amount)).filter(
                    Payment.user_id.in_(registered_user_ids),
                    Payment.status == 'completed'
                ).scalar() or 0
            else:
                paid_subscriptions = 0
                revenue = 0
            
            # Розрахунки
            cost = campaign.cost
            profit = revenue - cost
            roi = ((revenue - cost) / cost * 100) if cost > 0 else 0
            cpa = (cost / paid_subscriptions) if paid_subscriptions > 0 else 0  # Cost Per Acquisition
            cpc = (cost / total_visitors) if total_visitors > 0 else 0  # Cost Per Click/Visit
            conversion_rate = (paid_subscriptions / total_visitors * 100) if total_visitors > 0 else 0
            
            results.append({
                'campaign_id': campaign.id,
                'campaign_name': campaign.campaign_name,
                'channel': campaign.channel or 'unknown',
                'utm_campaign': campaign.utm_campaign,
                'utm_source': campaign.utm_source,
                'cost': cost,
                'visitors': total_visitors,
                'registrations': registrations,
                'paid_subscriptions': paid_subscriptions,
                'revenue': revenue,
                'profit': profit,
                'roi': round(roi, 2),
                'cpa': round(cpa, 2),  # Cost Per Acquisition
                'cpc': round(cpc, 2),  # Cost Per Click
                'conversion_rate': round(conversion_rate, 2),
                'is_active': campaign.is_active,
                'start_date': campaign.start_date.isoformat() if campaign.start_date else None,
                'end_date': campaign.end_date.isoformat() if campaign.end_date else None
            })
        
        # Сортуємо по ROI
        results.sort(key=lambda x: x['roi'], reverse=True)
        
        return results
    
    @staticmethod
    def get_channel_comparison(db: Session, start_date: Optional[datetime] = None,
                               end_date: Optional[datetime] = None) -> Dict:
        """
        Порівняння ефективності різних маркетингових каналів
        """
        roi_data = AnalyticsService.get_marketing_roi_by_channel(db, start_date, end_date)
        
        if not roi_data:
            return {
                'best_channel': None,
                'worst_channel': None,
                'channels': []
            }
        
        # Знаходимо найкращий та найгірший канали
        best_channel = max(roi_data, key=lambda x: x['roi'])
        worst_channel = min(roi_data, key=lambda x: x['roi'])
        
        return {
            'best_channel': {
                'name': best_channel['channel'],
                'roi': best_channel['roi'],
                'revenue': best_channel['revenue'],
                'cost': best_channel['cost']
            },
            'worst_channel': {
                'name': worst_channel['channel'],
                'roi': worst_channel['roi'],
                'revenue': worst_channel['revenue'],
                'cost': worst_channel['cost']
            },
            'channels': roi_data,
            'total_channels': len(roi_data)
        }
