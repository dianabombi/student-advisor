#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Комплексний тест Jobs AI для Чехії на всіх 11 мовах
"""

import sys
import asyncio
sys.path.append('/app')

from services.jobs_chat_service import JobsChatService
from main import SessionLocal

async def test_all_11_languages_czech():
    """Тестування всіх 11 мов для чеських міст"""
    service = JobsChatService()
    db = SessionLocal()
    
    # Тести для всіх 11 мов: sk, cs, pl, en, de, fr, es, uk, it, ru, pt
    tests = [
        # Словацька
        ("Hľadám brigádu v Prahe", "sk", "Praha"),
        ("Hľadám brigádu v Brne", "sk", "Brno"),
        
        # Чеська
        ("Hledám brigádu v Praze", "cs", "Praha"),
        ("Hledám brigádu v Brně", "cs", "Brno"),
        ("Hledám brigádu v Olomouci", "cs", "Olomouc"),
        
        # Польська
        ("Szukam pracy w Pradze", "pl", "Praha"),
        ("Szukam pracy w Brnie", "pl", "Brno"),
        
        # Англійська
        ("Looking for job in Prague", "en", "Praha"),
        ("Looking for job in Brno", "en", "Brno"),
        
        # Німецька
        ("Ich suche einen Job in Prag", "de", "Praha"),
        ("Ich suche einen Job in Brünn", "de", "Brno"),
        
        # Французька
        ("Je cherche un travail à Prague", "fr", "Praha"),
        ("Je cherche un travail à Brno", "fr", "Brno"),
        
        # Іспанська
        ("Busco trabajo en Praga", "es", "Praha"),
        ("Busco trabajo en Brno", "es", "Brno"),
        
        # Українська
        ("Шукаю роботу в Празі", "uk", "Praha"),
        ("Шукаю роботу в Брно", "uk", "Brno"),
        ("Шукаю роботу в Оломоуці", "uk", "Olomouc"),
        
        # Італійська
        ("Cerco lavoro a Praga", "it", "Praha"),
        ("Cerco lavoro a Brno", "it", "Brno"),
        
        # Російська
        ("Ищу работу в Праге", "ru", "Praha"),
        ("Ищу работу в Брно", "ru", "Brno"),
        
        # Португальська
        ("Procuro trabalho em Praga", "pt", "Praha"),
        ("Procuro trabalho em Brno", "pt", "Brno"),
    ]
    
    results = {
        'passed': 0,
        'failed': 0,
        'details': []
    }
    
    try:
        for message, lang, expected_city in tests:
            print(f"\n{'='*80}")
            print(f"Тест: {message} ({lang}) → очікується: {expected_city}")
            print('='*80)
            
            response = await service.chat(
                message=message,
                conversation_history=[],
                user_name="Test User",
                language=lang,
                jurisdiction='CZ',
                db=db,
                city=None
            )
            
            # Перевірки
            city_found = expected_city.lower() in response.lower()
            has_portals = any(portal in response.lower() for portal in ['jobs.cz', 'prace.cz', 'fajn-brigad', 'jenprace'])
            has_urls = 'https://' in response
            
            if city_found and has_portals and has_urls:
                print(f"✅ PASSED")
                results['passed'] += 1
                results['details'].append({
                    'test': f"{message} ({lang})",
                    'status': 'PASSED',
                    'city': expected_city
                })
            else:
                print(f"❌ FAILED")
                print(f"   City found: {city_found}")
                print(f"   Portals found: {has_portals}")
                print(f"   URLs found: {has_urls}")
                results['failed'] += 1
                results['details'].append({
                    'test': f"{message} ({lang})",
                    'status': 'FAILED',
                    'city': expected_city,
                    'city_found': city_found,
                    'portals_found': has_portals,
                    'urls_found': has_urls
                })
            
            # Показати частину відповіді
            print(f"\nВідповідь (перші 200 символів):")
            print(response[:200] + "...")
        
        # Підсумок
        print("\n" + "="*80)
        print("ПІДСУМОК ТЕСТУВАННЯ")
        print("="*80)
        print(f"Всього тестів: {len(tests)}")
        print(f"✅ Пройдено: {results['passed']}")
        print(f"❌ Провалено: {results['failed']}")
        print(f"Успішність: {results['passed']/len(tests)*100:.1f}%")
        
        # Статистика по мовах
        print("\nСтатистика по мовах:")
        langs = {}
        for detail in results['details']:
            lang = detail['test'].split('(')[1].split(')')[0]
            if lang not in langs:
                langs[lang] = {'passed': 0, 'total': 0}
            langs[lang]['total'] += 1
            if detail['status'] == 'PASSED':
                langs[lang]['passed'] += 1
        
        for lang, stats in sorted(langs.items()):
            success_rate = stats['passed']/stats['total']*100
            print(f"  {lang}: {stats['passed']}/{stats['total']} ({success_rate:.0f}%)")
        
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_all_11_languages_czech())
