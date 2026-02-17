#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест відповіді AI для Jobs консультанта
"""

import sys
import asyncio
sys.path.append('/app')

from services.jobs_chat_service import JobsChatService
from main import SessionLocal

async def test_jobs_response():
    """Тестування відповіді AI з посиланнями"""
    service = JobsChatService()
    db = SessionLocal()
    
    try:
        # Тестовий запит
        message = "Шукаю підробіток в Кошіце"
        
        print("=" * 80)
        print("ТЕСТ ВІДПОВІДІ AI З ПОСИЛАННЯМИ")
        print("=" * 80)
        print(f"\nЗапит користувача: {message}\n")
        
        # Отримуємо відповідь
        response = await service.chat(
            message=message,
            conversation_history=[],
            user_name="Test User",
            language='uk',
            jurisdiction='SK',
            db=db,
            city=None
        )
        
        print("Відповідь AI:")
        print("-" * 80)
        print(response)
        print("-" * 80)
        
        # Перевіряємо, чи є посилання
        if 'https://' in response:
            print("\n✅ Відповідь містить посилання!")
            
            # Витягуємо всі посилання
            import re
            urls = re.findall(r'https?://[^\s]+', response)
            print(f"\nЗнайдено {len(urls)} посилань:")
            for i, url in enumerate(urls, 1):
                print(f"  {i}. {url}")
        else:
            print("\n❌ Відповідь НЕ містить посилань!")
        
        # Перевіряємо, чи є інструкції
        if 'Instructions:' in response or 'Як hľadať:' in response or 'Інструкції:' in response:
            print("\n✅ Відповідь містить інструкції!")
        else:
            print("\n⚠️ Відповідь НЕ містить інструкцій")
        
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_jobs_response())
