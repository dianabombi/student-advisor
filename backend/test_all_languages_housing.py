#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test all 11 languages in Housing AI
"""

import sys
import asyncio
sys.path.append('/app')

from services.housing_chat_service import HousingChatService
from main import SessionLocal

async def test_all_languages():
    db = SessionLocal()
    service = HousingChatService()
    
    print("=" * 70)
    print("TESTING ALL 11 LANGUAGES IN HOUSING AI")
    print("=" * 70)
    
    tests = [
        {'lang': 'sk', 'msg': 'Hľadám byt v Bratislave', 'city': 'Bratislava'},
        {'lang': 'cs', 'msg': 'Hledám byt v Praze', 'city': 'Praha'},
        {'lang': 'pl', 'msg': 'Szukam mieszkania w Warszawie', 'city': 'Warszawa'},
        {'lang': 'en', 'msg': 'Looking for apartment in Prague', 'city': 'Praha'},
        {'lang': 'de', 'msg': 'Suche Wohnung in Prag', 'city': 'Praha'},
        {'lang': 'fr', 'msg': 'Cherche logement à Prague', 'city': 'Praha'},
        {'lang': 'es', 'msg': 'Busco vivienda en Praga', 'city': 'Praha'},
        {'lang': 'uk', 'msg': 'Шукаю квартиру в Празі', 'city': 'Praha'},
        {'lang': 'it', 'msg': 'Cerco alloggio a Praga', 'city': 'Praha'},
        {'lang': 'ru', 'msg': 'Ищу квартиру в Праге', 'city': 'Praha'},
        {'lang': 'pt', 'msg': 'Procuro moradia em Praga', 'city': 'Praha'},
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
                jurisdiction='CZ',
                db=db
            )
            
            # Check if response is in correct language (basic check)
            has_portals = 'Sreality.cz' in response or 'sreality' in response.lower()
            response_len = len(response)
            
            # Language-specific checks
            lang_checks = {
                'sk': 'môžete' in response.lower() or 'hľadať' in response.lower(),
                'cs': 'můžete' in response.lower() or 'hledat' in response.lower(),
                'pl': 'możesz' in response.lower() or 'szukać' in response.lower(),
                'en': 'you can' in response.lower() or 'search' in response.lower(),
                'de': 'können sie' in response.lower() or 'suchen' in response.lower(),
                'fr': 'vous pouvez' in response.lower() or 'chercher' in response.lower(),
                'es': 'puede' in response.lower() or 'buscar' in response.lower(),
                'uk': 'можете' in response.lower() or 'шукати' in response.lower(),
                'it': 'puoi' in response.lower() or 'cercare' in response.lower(),
                'ru': 'можете' in response.lower() or 'искать' in response.lower(),
                'pt': 'pode' in response.lower() or 'procurar' in response.lower(),
            }
            
            correct_lang = lang_checks.get(test['lang'], False)
            
            status = '✅' if (has_portals and correct_lang) else '⚠️'
            results.append({
                'lang': test['lang'],
                'status': status,
                'has_portals': has_portals,
                'correct_lang': correct_lang,
                'length': response_len
            })
            
            print(f"  {status} Portals: {has_portals}, Correct language: {correct_lang}, Length: {response_len}")
            
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
            print(f"Portals: {r['has_portals']}, Language: {r['correct_lang']}")
    
    success_count = sum(1 for r in results if r['status'] == '✅')
    print(f"\n✅ {success_count}/11 languages working correctly")
    
    db.close()

if __name__ == "__main__":
    asyncio.run(test_all_languages())
