#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Czech Housing AI
"""

import sys
import asyncio
sys.path.append('/app')

from services.housing_chat_service import HousingChatService
from main import SessionLocal

async def test_czech_housing():
    db = SessionLocal()
    service = HousingChatService()
    
    print("=" * 60)
    print("TESTING CZECH HOUSING AI")
    print("=" * 60)
    
    tests = [
        {
            'message': 'Hledám byt v Praze',
            'language': 'cs',
            'jurisdiction': 'CZ',
            'description': 'Czech language - Praha'
        },
        {
            'message': 'Looking for apartment in Brno',
            'language': 'en',
            'jurisdiction': 'CZ',
            'description': 'English - Brno'
        },
        {
            'message': 'Шукаю квартиру в Остраві',
            'language': 'uk',
            'jurisdiction': 'CZ',
            'description': 'Ukrainian - Ostrava'
        },
        {
            'message': 'Hledám studentský byt v Olomouci',
            'language': 'cs',
            'jurisdiction': 'CZ',
            'description': 'Czech - Olomouc (student housing)'
        }
    ]
    
    for i, test in enumerate(tests, 1):
        print(f"\n📝 Test {i}: {test['description']}")
        print(f"Query: {test['message']}")
        
        response = await service.chat(
            message=test['message'],
            conversation_history=[],
            user_name='Test User',
            language=test['language'],
            jurisdiction=test['jurisdiction'],
            db=db
        )
        
        print(f"Response length: {len(response)} chars")
        print(f"Response preview:\n{response[:500]}...")
        
        # Check if response contains expected portals
        expected = ['Sreality.cz', 'Bezrealitky.cz', 'Reality.iDNES.cz', 'UlovDomov.cz']
        found = [portal for portal in expected if portal in response]
        print(f"✅ Found portals: {', '.join(found)}")
    
    db.close()
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(test_czech_housing())
