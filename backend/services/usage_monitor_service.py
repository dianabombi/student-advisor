#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Usage Monitor Service - Захист від збитків
Моніторинг використання AI запитів та попередження користувачів
"""

import os
from datetime import datetime, timedelta
from typing import Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)


class UsageMonitorService:
    """Сервіс моніторингу використання AI для захисту від збитків"""
    
    # Тарифні плани з лімітами
    PLANS = {
        'free': {
            'price_eur': 0,
            'daily_limit': 0,  # Тільки перегляд закладів
            'monthly_limit': 0,
            'cost_threshold_eur': 0,  # Поріг витрат
        },
        'basic': {
            'price_eur': 10,
            'daily_limit': 25,
            'monthly_limit': 750,
            'cost_threshold_eur': 5,  # 50% від ціни плану
            'warning_threshold': 0.7,  # Попередження при 70% використання
        },
        'standard': {
            'price_eur': 20,
            'daily_limit': 50,
            'monthly_limit': 1500,
            'cost_threshold_eur': 10,  # 50% від ціни плану
            'warning_threshold': 0.7,
        },
        'premium': {
            'price_eur': 30,
            'daily_limit': 100,
            'monthly_limit': 3000,
            'cost_threshold_eur': 15,  # 50% від ціни плану
            'warning_threshold': 0.7,
        }
    }
    
    # Вартість запитів (середня)
    COST_PER_REQUEST = {
        'simple': 0.02,   # Короткий запит
        'detailed': 0.10,  # Детальний запит
        'average': 0.05,   # Середній запит
    }
    
    def __init__(self):
        self.metrics = {
            'total_checks': 0,
            'warnings_sent': 0,
            'blocks_applied': 0,
        }
    
    def check_usage_limits(
        self,
        db: Session,
        user_id: int,
        user_plan: str,
        request_type: str = 'average'
    ) -> Dict:
        """
        Перевірка лімітів використання перед виконанням запиту
        
        Args:
            db: Database session
            user_id: ID користувача
            user_plan: План підписки ('free', 'basic', 'standard', 'premium')
            request_type: Тип запиту ('simple', 'detailed', 'average')
            
        Returns:
            Dict з результатами перевірки:
            {
                'allowed': bool,  # Чи дозволено запит
                'warning': str,   # Попередження (якщо є)
                'usage': dict,    # Статистика використання
                'action': str     # Рекомендована дія
            }
        """
        self.metrics['total_checks'] += 1
        
        # Отримати план користувача
        plan_config = self.PLANS.get(user_plan.lower(), self.PLANS['free'])
        
        # Якщо FREE план - заборонити AI запити
        if user_plan.lower() == 'free':
            return {
                'allowed': False,
                'warning': 'AI консультант доступний тільки на платних планах',
                'usage': {'daily': 0, 'monthly': 0, 'cost': 0},
                'action': 'upgrade',
                'upgrade_url': '/pricing'
            }
        
        # Отримати використання за сьогодні
        today_usage = self._get_daily_usage(db, user_id)
        
        # Отримати використання за місяць
        monthly_usage = self._get_monthly_usage(db, user_id)
        
        # Розрахувати витрати
        estimated_cost = self._calculate_cost(monthly_usage, request_type)
        
        # Перевірка денного ліміту
        if today_usage['count'] >= plan_config['daily_limit']:
            self.metrics['blocks_applied'] += 1
            return {
                'allowed': False,
                'warning': f"Ви досягли денного ліміту ({plan_config['daily_limit']} запитів). Спробуйте завтра або оновіть план.",
                'usage': {
                    'daily': today_usage['count'],
                    'daily_limit': plan_config['daily_limit'],
                    'monthly': monthly_usage['count'],
                    'monthly_limit': plan_config['monthly_limit'],
                    'cost_eur': estimated_cost,
                },
                'action': 'wait_or_upgrade',
                'reset_time': self._get_next_reset_time('daily')
            }
        
        # Перевірка місячного ліміту
        if monthly_usage['count'] >= plan_config['monthly_limit']:
            self.metrics['blocks_applied'] += 1
            return {
                'allowed': False,
                'warning': f"Ви досягли місячного ліміту ({plan_config['monthly_limit']} запитів). Оновіть план для продовження.",
                'usage': {
                    'daily': today_usage['count'],
                    'monthly': monthly_usage['count'],
                    'monthly_limit': plan_config['monthly_limit'],
                    'cost_eur': estimated_cost,
                },
                'action': 'upgrade',
                'upgrade_url': '/pricing'
            }
        
        # Перевірка порогу витрат (захист від збитків!)
        if estimated_cost >= plan_config['cost_threshold_eur']:
            self.metrics['blocks_applied'] += 1
            logger.warning(
                f"Cost threshold exceeded for user {user_id}: "
                f"€{estimated_cost:.2f} >= €{plan_config['cost_threshold_eur']}"
            )
            return {
                'allowed': False,
                'warning': f"Ви досягли ліміту використання для вашого плану. Наші витрати на AI: €{estimated_cost:.2f}. Оновіть план для продовження.",
                'usage': {
                    'daily': today_usage['count'],
                    'monthly': monthly_usage['count'],
                    'cost_eur': estimated_cost,
                    'cost_threshold': plan_config['cost_threshold_eur'],
                },
                'action': 'upgrade',
                'upgrade_url': '/pricing',
                'reason': 'cost_protection'  # Важливо для логування
            }
        
        # Попередження при 70% використання
        warning_threshold = plan_config.get('warning_threshold', 0.7)
        daily_usage_percent = today_usage['count'] / plan_config['daily_limit']
        monthly_usage_percent = monthly_usage['count'] / plan_config['monthly_limit']
        cost_usage_percent = estimated_cost / plan_config['cost_threshold_eur']
        
        warning_message = None
        
        if daily_usage_percent >= warning_threshold:
            remaining = plan_config['daily_limit'] - today_usage['count']
            warning_message = f"⚠️ Ви використали {int(daily_usage_percent * 100)}% денного ліміту. Залишилось {remaining} запитів на сьогодні."
            self.metrics['warnings_sent'] += 1
        
        elif monthly_usage_percent >= warning_threshold:
            remaining = plan_config['monthly_limit'] - monthly_usage['count']
            warning_message = f"⚠️ Ви використали {int(monthly_usage_percent * 100)}% місячного ліміту. Залишилось {remaining} запитів."
            self.metrics['warnings_sent'] += 1
        
        elif cost_usage_percent >= warning_threshold:
            remaining_cost = plan_config['cost_threshold_eur'] - estimated_cost
            warning_message = f"⚠️ Витрати на AI досягли €{estimated_cost:.2f} з €{plan_config['cost_threshold_eur']}. Залишилось ~€{remaining_cost:.2f}."
            self.metrics['warnings_sent'] += 1
        
        # Дозволити запит
        return {
            'allowed': True,
            'warning': warning_message,
            'usage': {
                'daily': today_usage['count'],
                'daily_limit': plan_config['daily_limit'],
                'daily_percent': int(daily_usage_percent * 100),
                'monthly': monthly_usage['count'],
                'monthly_limit': plan_config['monthly_limit'],
                'monthly_percent': int(monthly_usage_percent * 100),
                'cost_eur': estimated_cost,
                'cost_threshold': plan_config['cost_threshold_eur'],
                'cost_percent': int(cost_usage_percent * 100),
            },
            'action': 'continue'
        }
    
    def _get_daily_usage(self, db: Session, user_id: int) -> Dict:
        """Отримати використання за сьогодні"""
        from models import ChatMessage  # Import here to avoid circular dependency
        
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        count = db.query(func.count(ChatMessage.id)).filter(
            ChatMessage.user_id == user_id,
            ChatMessage.role == 'user',
            ChatMessage.created_at >= today_start
        ).scalar() or 0
        
        return {
            'count': count,
            'date': today_start.date()
        }
    
    def _get_monthly_usage(self, db: Session, user_id: int) -> Dict:
        """Отримати використання за місяць"""
        from models import ChatMessage
        
        month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        count = db.query(func.count(ChatMessage.id)).filter(
            ChatMessage.user_id == user_id,
            ChatMessage.role == 'user',
            ChatMessage.created_at >= month_start
        ).scalar() or 0
        
        return {
            'count': count,
            'month': month_start.date()
        }
    
    def _calculate_cost(self, monthly_usage: Dict, request_type: str = 'average') -> float:
        """
        Розрахувати орієнтовну вартість використання
        
        Args:
            monthly_usage: Статистика за місяць
            request_type: Тип запиту
            
        Returns:
            Вартість в євро
        """
        count = monthly_usage['count']
        cost_per_request = self.COST_PER_REQUEST.get(request_type, self.COST_PER_REQUEST['average'])
        
        # Додати вартість поточного запиту
        total_cost_usd = (count + 1) * cost_per_request
        
        # Конвертувати в євро (приблизно 1 USD = 0.92 EUR)
        total_cost_eur = total_cost_usd * 0.92
        
        return round(total_cost_eur, 2)
    
    def _get_next_reset_time(self, period: str) -> str:
        """Отримати час наступного скидання ліміту"""
        now = datetime.now()
        
        if period == 'daily':
            next_reset = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        else:  # monthly
            if now.month == 12:
                next_reset = now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            else:
                next_reset = now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
        
        return next_reset.isoformat()
    
    def log_usage(
        self,
        db: Session,
        user_id: int,
        request_type: str,
        tokens_used: int,
        cost_usd: float
    ):
        """
        Логування використання для аналітики
        
        Args:
            db: Database session
            user_id: ID користувача
            request_type: Тип запиту
            tokens_used: Кількість токенів
            cost_usd: Вартість в доларах
        """
        from models import UsageLog
        
        try:
            usage_log = UsageLog(
                user_id=user_id,
                request_type=request_type,
                tokens_used=tokens_used,
                cost_usd=cost_usd,
                cost_eur=cost_usd * 0.92,
                created_at=datetime.now()
            )
            db.add(usage_log)
            db.commit()
            
            logger.info(
                f"Usage logged: user={user_id}, type={request_type}, "
                f"tokens={tokens_used}, cost=${cost_usd:.4f}"
            )
        except Exception as e:
            logger.error(f"Failed to log usage: {e}")
            db.rollback()
    
    def get_user_statistics(self, db: Session, user_id: int) -> Dict:
        """
        Отримати детальну статистику користувача
        
        Returns:
            Статистика використання
        """
        from models import ChatMessage, UsageLog
        
        # Використання за сьогодні
        daily_usage = self._get_daily_usage(db, user_id)
        
        # Використання за місяць
        monthly_usage = self._get_monthly_usage(db, user_id)
        
        # Загальні витрати за місяць
        month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        total_cost = db.query(func.sum(UsageLog.cost_eur)).filter(
            UsageLog.user_id == user_id,
            UsageLog.created_at >= month_start
        ).scalar() or 0.0
        
        return {
            'daily_requests': daily_usage['count'],
            'monthly_requests': monthly_usage['count'],
            'monthly_cost_eur': round(total_cost, 2),
            'last_updated': datetime.now().isoformat()
        }
    
    def get_metrics(self) -> Dict:
        """Отримати метрики сервісу"""
        return self.metrics


# Глобальний інстанс
usage_monitor = UsageMonitorService()
