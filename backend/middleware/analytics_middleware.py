"""
Analytics Middleware для автоматичного збору даних про відвідувачів
"""
from fastapi import Request
from sqlalchemy.orm import Session
from datetime import datetime
import hashlib
from typing import Optional
import re


class AnalyticsMiddleware:
    """Middleware для відстеження відвідувачів та збору аналітичних даних"""
    
    @staticmethod
    def get_visitor_fingerprint(request: Request) -> str:
        """
        Створює унікальний fingerprint відвідувача на основі IP + User Agent
        """
        ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        fingerprint_string = f"{ip}:{user_agent}"
        return hashlib.md5(fingerprint_string.encode()).hexdigest()
    
    @staticmethod
    def extract_utm_params(request: Request) -> dict:
        """
        Витягує UTM параметри з URL
        """
        query_params = dict(request.query_params)
        utm_params = {}
        
        utm_keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']
        for key in utm_keys:
            if key in query_params:
                utm_params[key] = query_params[key]
        
        return utm_params if utm_params else None
    
    @staticmethod
    def get_referrer(request: Request) -> Optional[str]:
        """
        Отримує referrer URL
        """
        return request.headers.get("referer") or request.headers.get("referrer")
    
    @staticmethod
    def extract_device_info(user_agent: str) -> dict:
        """
        Витягує інформацію про пристрій з User Agent
        """
        user_agent_lower = user_agent.lower()
        
        # Визначення типу пристрою
        if 'mobile' in user_agent_lower or 'android' in user_agent_lower or 'iphone' in user_agent_lower:
            device_type = 'mobile'
        elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
            device_type = 'tablet'
        else:
            device_type = 'desktop'
        
        # Визначення браузера
        if 'chrome' in user_agent_lower and 'edg' not in user_agent_lower:
            browser = 'Chrome'
        elif 'firefox' in user_agent_lower:
            browser = 'Firefox'
        elif 'safari' in user_agent_lower and 'chrome' not in user_agent_lower:
            browser = 'Safari'
        elif 'edg' in user_agent_lower:
            browser = 'Edge'
        elif 'opera' in user_agent_lower or 'opr' in user_agent_lower:
            browser = 'Opera'
        else:
            browser = 'Other'
        
        # Визначення ОС
        if 'windows' in user_agent_lower:
            os = 'Windows'
        elif 'mac' in user_agent_lower:
            os = 'macOS'
        elif 'linux' in user_agent_lower:
            os = 'Linux'
        elif 'android' in user_agent_lower:
            os = 'Android'
        elif 'ios' in user_agent_lower or 'iphone' in user_agent_lower or 'ipad' in user_agent_lower:
            os = 'iOS'
        else:
            os = 'Other'
        
        return {
            'device_type': device_type,
            'browser': browser,
            'os': os
        }
    
    @staticmethod
    def determine_traffic_source(utm_params: Optional[dict], referrer: Optional[str]) -> str:
        """
        Визначає джерело трафіку
        """
        # Якщо є UTM параметри, використовуємо їх
        if utm_params and 'utm_source' in utm_params:
            return utm_params['utm_source']
        
        # Якщо є referrer, аналізуємо його
        if referrer:
            referrer_lower = referrer.lower()
            if 'google' in referrer_lower:
                return 'google'
            elif 'facebook' in referrer_lower or 'fb.com' in referrer_lower:
                return 'facebook'
            elif 'instagram' in referrer_lower:
                return 'instagram'
            elif 'linkedin' in referrer_lower:
                return 'linkedin'
            elif 'twitter' in referrer_lower or 't.co' in referrer_lower:
                return 'twitter'
            elif 'youtube' in referrer_lower:
                return 'youtube'
            else:
                return 'referral'
        
        # Якщо немає ні UTM, ні referrer - це прямий трафік
        return 'direct'
    
    @staticmethod
    async def track_page_view(request: Request, db: Session, user_id: Optional[int] = None):
        """
        Відстежує перегляд сторінки
        """
        from main import PageView, VisitorTracking
        
        # Отримуємо дані про відвідувача
        fingerprint = AnalyticsMiddleware.get_visitor_fingerprint(request)
        ip_address = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        utm_params = AnalyticsMiddleware.extract_utm_params(request)
        referrer = AnalyticsMiddleware.get_referrer(request)
        device_info = AnalyticsMiddleware.extract_device_info(user_agent)
        traffic_source = AnalyticsMiddleware.determine_traffic_source(utm_params, referrer)
        
        # Перевіряємо чи це новий відвідувач
        visitor = db.query(VisitorTracking).filter(
            VisitorTracking.visitor_fingerprint == fingerprint
        ).first()
        
        if not visitor:
            # Новий відвідувач
            visitor = VisitorTracking(
                visitor_fingerprint=fingerprint,
                ip_address=ip_address,
                user_agent=user_agent,
                first_visit=datetime.utcnow(),
                last_visit=datetime.utcnow(),
                visit_count=1,
                traffic_source=traffic_source,
                utm_source=utm_params.get('utm_source') if utm_params else None,
                utm_medium=utm_params.get('utm_medium') if utm_params else None,
                utm_campaign=utm_params.get('utm_campaign') if utm_params else None,
                referrer=referrer,
                device_type=device_info['device_type'],
                browser=device_info['browser'],
                os=device_info['os'],
                user_id=user_id
            )
            db.add(visitor)
        else:
            # Оновлюємо існуючого відвідувача
            visitor.last_visit = datetime.utcnow()
            visitor.visit_count += 1
            if user_id and not visitor.user_id:
                visitor.user_id = user_id
        
        # Записуємо перегляд сторінки
        page_view = PageView(
            visitor_fingerprint=fingerprint,
            user_id=user_id,
            page_url=str(request.url.path),
            page_title=None,  # Можна додати з frontend
            referrer=referrer,
            utm_params=utm_params,
            device_type=device_info['device_type'],
            browser=device_info['browser'],
            os=device_info['os'],
            created_at=datetime.utcnow()
        )
        db.add(page_view)
        
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error tracking page view: {e}")
