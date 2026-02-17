#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест відповіді AI для чеських міст
"""

import sys
import asyncio
sys.path.append('/app')

from services.jobs_chat_service import JobsChatService
from main import SessionLocal

async def test_czech_response():
    """Тестування відповіді AI для Чехії"""
    service = JobsChatService()
    db = SessionLocal()
    
    try:
        # Тестові запити
        tests = [
            ("Hledám brigádu v Praze", "cs", "CZ"),
            ("Шукаю підробіток в Празі", "uk", "CZ"),
            ("Looking for part-time job in Brno", "en", "CZ"),
        ]
        
        for message, lang, jurisdiction in tests:
            print("=" * 80)
            print(f"Тест: {message} ({lang})")
            print("=" * 80)
            
            response = await service.chat(
                message=message,
                conversation_history=[],
                user_name="Test User",
                language=lang,
                jurisdiction=jurisdiction,
                db=db,
                city=None
            )
            
            print(response)
            print("\n")
            
            # Перевірки
            if 'jobs.cz' in response.lower() or 'prace.cz' in response.lower():
                print("✅ Чеські портали знайдено!")
            else:
                print("❌ Чеські портали НЕ знайдено!")
            
            if 'google' in response.lower() or 'alternative' in response.lower():
                print("✅ Інструкції з Google є!")
            else:
                print("⚠️ Інструкцій з Google немає")
            
            print("\n")
        
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_czech_response())
