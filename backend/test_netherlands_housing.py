#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Netherlands housing - all 11 languages
"""

import sys
import asyncio
sys.path.append('/app')

from services.housing_chat_service import HousingChatService
from main import SessionLocal

async def test_netherlands_all_languages():
    db = SessionLocal()
    service = HousingChatService()
    
    print("=" * 70)
    print("TESTING NETHERLANDS - ALL 11 LANGUAGES")
    print("=" * 70)
    
    tests = [
        {'lang': 'nl', 'msg': 'Zoek appartement in Amsterdam', 'city': 'Amsterdam'},
        {'lang': 'en', 'msg': 'Looking for apartment in Amsterdam', 'city': 'Amsterdam'},
        {'lang': 'de', 'msg': 'Suche Wohnung in Amsterdam', 'city': 'Amsterdam'},
        {'lang': 'fr', 'msg': 'Cherche logement à Amsterdam', 'city': 'Amsterdam'},
        {'lang': 'es', 'msg': 'Busco vivienda en Ámsterdam', 'city': 'Amsterdam'},
        {'lang': 'uk', 'msg': 'Шукаю квартиру в Амстердамі', 'city': 'Amsterdam'},
        {'lang': 'it', 'msg': 'Cerco alloggio ad Amsterdam', 'city': 'Amsterdam'},
        {'lang': 'ru', 'msg': 'Ищу квартиру в Амстердаме', 'city': 'Amsterdam'},
        {'lang': 'pt', 'msg': 'Procuro moradia em Amsterdã', 'city': 'Amsterdam'},
        {'lang': 'sk', 'msg': 'Hľadám byt v Amsterdame', 'city': 'Amsterdam'},
        {'lang': 'cs', 'msg': 'Hledám byt v Amsterdamu', 'city': 'Amsterdam'},
        {'lang': 'pl', 'msg': 'Szukam mieszkania w Amsterdamie', 'city': 'Amsterdam'},
    ]
    
    results = []
    
    for test in tests:
        print(f"\n🌍 Testing {test['lang'].upper()}: {test['msg']}")
        
        try:
            response = await service.chat(
                message=test['msg'],
                conversation_history=[],
                user_name='Test User',
                language=test['lang'],
                jurisdiction='NL',
                db=db
            )
            
            has_funda = 'funda' in response.lower()
            has_kamernet = 'kamernet' in response.lower()
            response_len = len(response)
            
            status = '✅' if (has_funda or has_kamernet) else '⚠️'
            results.append({
                'lang': test['lang'],
                'status': status,
                'has_portals': has_funda or has_kamernet,
                'length': response_len
            })
            
            print(f"  {status} Portals: {has_funda or has_kamernet}, Length: {response_len}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append({'lang': test['lang'], 'status': '❌', 'error': str(e)})
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for r in results:
        print(f"{r['status']} {r['lang'].upper()}: ", end='')
        if 'error' in r:
            print(f"Error - {r['error']}")
        else:
            print(f"Portals: {r['has_portals']}")
    
    success_count = sum(1 for r in results if r['status'] == '✅')
    print(f"\n✅ {success_count}/12 languages working correctly")
    
    db.close()

if __name__ == "__main__":
    asyncio.run(test_netherlands_all_languages())
