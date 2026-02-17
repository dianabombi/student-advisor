#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Poland housing agencies - all 11 languages
"""

import sys
import asyncio
sys.path.append('/app')

from services.housing_chat_service import HousingChatService
from main import SessionLocal

async def test_poland_all_languages():
    db = SessionLocal()
    service = HousingChatService()
    
    print("=" * 70)
    print("TESTING POLAND - ALL 11 LANGUAGES")
    print("=" * 70)
    
    tests = [
        {'lang': 'pl', 'msg': 'Szukam mieszkania w Warszawie', 'city': 'Warszawa'},
        {'lang': 'en', 'msg': 'Looking for apartment in Warsaw', 'city': 'Warszawa'},
        {'lang': 'de', 'msg': 'Suche Wohnung in Warschau', 'city': 'Warszawa'},
        {'lang': 'fr', 'msg': 'Cherche logement à Varsovie', 'city': 'Warszawa'},
        {'lang': 'es', 'msg': 'Busco vivienda en Varsovia', 'city': 'Warszawa'},
        {'lang': 'uk', 'msg': 'Шукаю квартиру у Варшаві', 'city': 'Warszawa'},
        {'lang': 'it', 'msg': 'Cerco alloggio a Varsavia', 'city': 'Warszawa'},
        {'lang': 'ru', 'msg': 'Ищу квартиру в Варшаве', 'city': 'Warszawa'},
        {'lang': 'pt', 'msg': 'Procuro moradia em Varsóvia', 'city': 'Warszawa'},
        {'lang': 'sk', 'msg': 'Hľadám byt vo Varšave', 'city': 'Warszawa'},
        {'lang': 'cs', 'msg': 'Hledám byt ve Varšavě', 'city': 'Warszawa'},
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
                jurisdiction='PL',
                db=db
            )
            
            has_otodom = 'Otodom' in response or 'otodom' in response.lower()
            has_olx = 'OLX' in response or 'olx' in response.lower()
            response_len = len(response)
            
            status = '✅' if (has_otodom or has_olx) else '⚠️'
            results.append({
                'lang': test['lang'],
                'status': status,
                'has_portals': has_otodom or has_olx,
                'length': response_len
            })
            
            print(f"  {status} Portals: {has_otodom or has_olx}, Length: {response_len}")
            
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
    print(f"\n✅ {success_count}/11 languages working correctly")
    
    db.close()

if __name__ == "__main__":
    asyncio.run(test_poland_all_languages())
