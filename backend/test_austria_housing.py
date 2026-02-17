#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Austria housing - all 11 languages
"""

import sys
import asyncio
sys.path.append('/app')

from services.housing_chat_service import HousingChatService
from main import SessionLocal

async def test_austria_all_languages():
    db = SessionLocal()
    service = HousingChatService()
    
    print("=" * 70)
    print("TESTING AUSTRIA - ALL 11 LANGUAGES")
    print("=" * 70)
    
    tests = [
        {'lang': 'de', 'msg': 'Suche Wohnung in Wien', 'city': 'Wien'},
        {'lang': 'en', 'msg': 'Looking for apartment in Vienna', 'city': 'Wien'},
        {'lang': 'fr', 'msg': 'Cherche logement à Vienne', 'city': 'Wien'},
        {'lang': 'es', 'msg': 'Busco vivienda en Viena', 'city': 'Wien'},
        {'lang': 'uk', 'msg': 'Шукаю квартиру у Відні', 'city': 'Wien'},
        {'lang': 'it', 'msg': 'Cerco alloggio a Vienna', 'city': 'Wien'},
        {'lang': 'ru', 'msg': 'Ищу квартиру в Вене', 'city': 'Wien'},
        {'lang': 'pt', 'msg': 'Procuro moradia em Viena', 'city': 'Wien'},
        {'lang': 'sk', 'msg': 'Hľadám byt vo Viedni', 'city': 'Wien'},
        {'lang': 'cs', 'msg': 'Hledám byt ve Vídni', 'city': 'Wien'},
        {'lang': 'pl', 'msg': 'Szukam mieszkania w Wiedniu', 'city': 'Wien'},
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
                jurisdiction='AT',
                db=db
            )
            
            has_willhaben = 'willhaben' in response.lower()
            has_immoscout = 'immobilien' in response.lower() or 'scout' in response.lower()
            response_len = len(response)
            
            status = '✅' if (has_willhaben or has_immoscout) else '⚠️'
            results.append({
                'lang': test['lang'],
                'status': status,
                'has_portals': has_willhaben or has_immoscout,
                'length': response_len
            })
            
            print(f"  {status} Portals: {has_willhaben or has_immoscout}, Length: {response_len}")
            
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
    asyncio.run(test_austria_all_languages())
