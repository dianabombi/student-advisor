#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Germany housing - all 11 languages
"""

import sys
import asyncio
sys.path.append('/app')

from services.housing_chat_service import HousingChatService
from main import SessionLocal

async def test_germany_all_languages():
    db = SessionLocal()
    service = HousingChatService()
    
    print("=" * 70)
    print("TESTING GERMANY - ALL 11 LANGUAGES")
    print("=" * 70)
    
    tests = [
        {'lang': 'de', 'msg': 'Suche Wohnung in Berlin', 'city': 'Berlin'},
        {'lang': 'en', 'msg': 'Looking for apartment in Berlin', 'city': 'Berlin'},
        {'lang': 'fr', 'msg': 'Cherche logement à Berlin', 'city': 'Berlin'},
        {'lang': 'es', 'msg': 'Busco vivienda en Berlín', 'city': 'Berlin'},
        {'lang': 'uk', 'msg': 'Шукаю квартиру в Берліні', 'city': 'Berlin'},
        {'lang': 'it', 'msg': 'Cerco alloggio a Berlino', 'city': 'Berlin'},
        {'lang': 'ru', 'msg': 'Ищу квартиру в Берлине', 'city': 'Berlin'},
        {'lang': 'pt', 'msg': 'Procuro moradia em Berlim', 'city': 'Berlin'},
        {'lang': 'sk', 'msg': 'Hľadám byt v Berlíne', 'city': 'Berlin'},
        {'lang': 'cs', 'msg': 'Hledám byt v Berlíně', 'city': 'Berlin'},
        {'lang': 'pl', 'msg': 'Szukam mieszkania w Berlinie', 'city': 'Berlin'},
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
                jurisdiction='DE',
                db=db
            )
            
            has_immoscout = 'immobilien' in response.lower() or 'scout' in response.lower()
            has_wg = 'wg-gesucht' in response.lower() or 'wg gesucht' in response.lower()
            response_len = len(response)
            
            status = '✅' if (has_immoscout or has_wg) else '⚠️'
            results.append({
                'lang': test['lang'],
                'status': status,
                'has_portals': has_immoscout or has_wg,
                'length': response_len
            })
            
            print(f"  {status} Portals: {has_immoscout or has_wg}, Length: {response_len}")
            
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
    asyncio.run(test_germany_all_languages())
