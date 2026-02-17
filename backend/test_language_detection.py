#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test language auto-detection
"""

import sys
import asyncio
sys.path.append('/app')

from services.housing_chat_service import HousingChatService
from main import SessionLocal

async def test_language_switching():
    db = SessionLocal()
    service = HousingChatService()
    
    print("=" * 70)
    print("TESTING LANGUAGE AUTO-DETECTION")
    print("=" * 70)
    
    # Test: Frontend sends 'cs' but message is in Ukrainian
    print("\n📝 Test: Frontend language='cs', Message in Ukrainian")
    print("Message: Шукаю гуртожиток в Остраві. Пиши українською")
    
    response = await service.chat(
        message='Шукаю гуртожиток в Остраві. Пиши українською',
        conversation_history=[],
        user_name='Ivan Draga',
        language='cs',  # Frontend sends Czech
        jurisdiction='CZ',
        db=db
    )
    
    print(f"\nResponse length: {len(response)} chars")
    print(f"Response:\n{response}\n")
    
    # Check if response is in Ukrainian
    ukrainian_indicators = ['можете', 'шукати', 'веб-сайт', 'відкрийте']
    found_ukrainian = any(indicator in response.lower() for indicator in ukrainian_indicators)
    
    if found_ukrainian:
        print("✅ SUCCESS! Response is in Ukrainian")
    else:
        print("❌ FAILED! Response is NOT in Ukrainian")
        print(f"Checked for: {ukrainian_indicators}")
    
    db.close()

if __name__ == "__main__":
    asyncio.run(test_language_switching())
