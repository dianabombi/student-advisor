#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Ostrava city detection fix
"""

import sys
import asyncio
sys.path.append('/app')

from services.housing_chat_service import HousingChatService
from main import SessionLocal

async def test_ostrava():
    db = SessionLocal()
    service = HousingChatService()
    
    print("=" * 60)
    print("TESTING OSTRAVA CITY DETECTION FIX")
    print("=" * 60)
    
    # Test Ukrainian query for Ostrava
    print("\n📝 Test: Ukrainian - Ostrava")
    print("Query: Шукаю квартиру в Остраві")
    
    response = await service.chat(
        message='Шукаю квартиру в Остраві',
        conversation_history=[],
        user_name='Test User',
        language='uk',
        jurisdiction='CZ',
        db=db
    )
    
    print(f"\nResponse length: {len(response)} chars")
    print(f"Response:\n{response}\n")
    
    # Check if response contains expected portals
    expected = ['Sreality.cz', 'Bezrealitky.cz', 'Reality.iDNES.cz', 'UlovDomov.cz']
    found = [portal for portal in expected if portal in response]
    
    if len(found) >= 3:
        print(f"✅ SUCCESS! Found portals: {', '.join(found)}")
    else:
        print(f"❌ FAILED! Only found: {', '.join(found) if found else 'none'}")
    
    db.close()

if __name__ == "__main__":
    asyncio.run(test_ostrava())
