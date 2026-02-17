#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Повний тест визначення міста на ВСІХ 11 мовах платформи (включно з португальською)
"""

import sys
sys.path.append('/app')

from services.jobs_chat_service import JobsChatService

def test_all_11_languages():
    """Тестування визначення міста на всіх 11 мовах"""
    service = JobsChatService()
    
    # Тести для всіх 11 мов: sk, cs, pl, en, de, fr, es, uk, it, ru, pt
    test_cases = [
        # ========== KOŠICE ==========
        # Словацька (sk)
        ("Hľadám brigádu v Košiciach", "sk", "Košice"),
        ("Potrebujem prácu v Košiciach", "sk", "Košice"),
        
        # Чеська (cs)
        ("Hledám brigádu v Košicích", "cs", "Košice"),
        ("Potřebuji práci v Košicích", "cs", "Košice"),
        
        # Польська (pl)
        ("Szukam pracy w Koszycach", "pl", "Košice"),
        ("Potrzebuję pracy w Koszycach", "pl", "Košice"),
        
        # Англійська (en)
        ("Looking for a job in Kosice", "en", "Košice"),
        ("I need work in Kosice", "en", "Košice"),
        
        # Німецька (de)
        ("Ich suche Arbeit in Kaschau", "de", "Košice"),
        ("Job in Kosice gesucht", "de", "Košice"),
        
        # Французька (fr)
        ("Je cherche du travail à Košice", "fr", "Košice"),
        ("Travail à Kosice", "fr", "Košice"),
        
        # Іспанська (es)
        ("Busco trabajo en Košice", "es", "Košice"),
        ("Necesito trabajo en Kosice", "es", "Košice"),
        
        # Українська (uk)
        ("Шукаю підробіток в Кошіце", "uk", "Košice"),
        ("Шукаю роботу в Кошіц", "uk", "Košice"),
        ("Робота в Кошице", "uk", "Košice"),
        
        # Італійська (it)
        ("Cerco lavoro a Košice", "it", "Košice"),
        ("Lavoro a Kosice", "it", "Košice"),
        
        # Російська (ru)
        ("Ищу работу в Кошице", "ru", "Košice"),
        ("Нужна работа в Кошиц", "ru", "Košice"),
        
        # Португальська (pt)
        ("Procuro trabalho em Košice", "pt", "Košice"),
        ("Preciso de trabalho em Kosice", "pt", "Košice"),
        
        # ========== BRATISLAVA ==========
        # Словацька (sk)
        ("Brigáda v Bratislave", "sk", "Bratislava"),
        
        # Чеська (cs)
        ("Práce v Bratislavě", "cs", "Bratislava"),
        
        # Польська (pl)
        ("Praca w Bratysławie", "pl", "Bratislava"),
        
        # Англійська (en)
        ("Job in Bratislava", "en", "Bratislava"),
        
        # Німецька (de)
        ("Arbeit in Pressburg", "de", "Bratislava"),
        ("Job in Bratislava", "de", "Bratislava"),
        
        # Французька (fr)
        ("Travail à Bratislava", "fr", "Bratislava"),
        
        # Іспанська (es)
        ("Trabajo en Bratislava", "es", "Bratislava"),
        
        # Українська (uk)
        ("Робота в Братиславі", "uk", "Bratislava"),
        ("Підробіток в Братиславе", "uk", "Bratislava"),
        
        # Італійська (it)
        ("Lavoro a Bratislava", "it", "Bratislava"),
        
        # Російська (ru)
        ("Работа в Братиславе", "ru", "Bratislava"),
        
        # Португальська (pt)
        ("Trabalho em Bratislava", "pt", "Bratislava"),
        
        # ========== NITRA ==========
        # Словацька (sk)
        ("Brigáda v Nitre", "sk", "Nitra"),
        
        # Чеська (cs)
        ("Práce v Nitře", "cs", "Nitra"),
        
        # Польська (pl)
        ("Praca w Nitrze", "pl", "Nitra"),
        
        # Англійська (en)
        ("Job in Nitra", "en", "Nitra"),
        
        # Німецька (de)
        ("Arbeit in Neutra", "de", "Nitra"),
        ("Job in Nitra", "de", "Nitra"),
        
        # Французька (fr)
        ("Travail à Nitra", "fr", "Nitra"),
        
        # Іспанська (es)
        ("Trabajo en Nitra", "es", "Nitra"),
        
        # Українська (uk)
        ("Робота в Нітрі", "uk", "Nitra"),
        ("Підробіток в Нітре", "uk", "Nitra"),
        ("Шукаю роботу в Нітра", "uk", "Nitra"),
        
        # Італійська (it)
        ("Lavoro a Nitra", "it", "Nitra"),
        
        # Російська (ru)
        ("Работа в Нитре", "ru", "Nitra"),
        
        # Португальська (pt)
        ("Trabalho em Nitra", "pt", "Nitra"),
        
        # ========== BANSKÁ BYSTRICA ==========
        # Словацька (sk)
        ("Brigáda v Banskej Bystrici", "sk", "Banská Bystrica"),
        
        # Чеська (cs)
        ("Práce v Banské Bystrici", "cs", "Banská Bystrica"),
        
        # Польська (pl)
        ("Praca w Bańskiej Bystrzycy", "pl", "Banská Bystrica"),
        
        # Англійська (en)
        ("Job in Banska Bystrica", "en", "Banská Bystrica"),
        
        # Німецька (de)
        ("Arbeit in Neusohl", "de", "Banská Bystrica"),
        
        # Французька (fr)
        ("Travail à Banská Bystrica", "fr", "Banská Bystrica"),
        
        # Іспанська (es)
        ("Trabajo en Banska Bystrica", "es", "Banská Bystrica"),
        
        # Українська (uk)
        ("Робота в Банській Бистриці", "uk", "Banská Bystrica"),
        ("Підробіток в Банской Быстрице", "uk", "Banská Bystrica"),
        
        # Італійська (it)
        ("Lavoro a Banská Bystrica", "it", "Banská Bystrica"),
        
        # Російська (ru)
        ("Работа в Банской Быстрице", "ru", "Banská Bystrica"),
        
        # Португальська (pt)
        ("Trabalho em Banská Bystrica", "pt", "Banská Bystrica"),
    ]
    
    print("=" * 100)
    print("ПОВНИЙ ТЕСТ ВИЗНАЧЕННЯ МІСТА НА ВСІХ 11 МОВАХ ПЛАТФОРМИ")
    print("Мови: sk, cs, pl, en, de, fr, es, uk, it, ru, pt")
    print("=" * 100)
    
    passed = 0
    failed = 0
    results_by_language = {}
    
    for message, lang, expected_city in test_cases:
        detected_city = service._extract_city_from_message(message, 'SK')
        
        if lang not in results_by_language:
            results_by_language[lang] = {'passed': 0, 'failed': 0}
        
        if detected_city == expected_city:
            print(f"✅ [{lang:2}] '{message}' → {detected_city}")
            passed += 1
            results_by_language[lang]['passed'] += 1
        else:
            print(f"❌ [{lang:2}] '{message}' → Очікувалось: {expected_city}, Отримано: {detected_city}")
            failed += 1
            results_by_language[lang]['failed'] += 1
    
    print("=" * 100)
    print(f"ЗАГАЛЬНИЙ РЕЗУЛЬТАТ: {passed} пройдено, {failed} провалено")
    print(f"Успішність: {passed/(passed+failed)*100:.1f}%")
    print("=" * 100)
    
    print("\nРЕЗУЛЬТАТИ ПО МОВАХ:")
    print("-" * 100)
    language_names = {
        'sk': 'Словацька',
        'cs': 'Чеська',
        'pl': 'Польська',
        'en': 'Англійська',
        'de': 'Німецька',
        'fr': 'Французька',
        'es': 'Іспанська',
        'uk': 'Українська',
        'it': 'Італійська',
        'ru': 'Російська',
        'pt': 'Португальська'
    }
    
    for lang in ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru', 'pt']:
        if lang in results_by_language:
            stats = results_by_language[lang]
            total = stats['passed'] + stats['failed']
            success_rate = stats['passed'] / total * 100 if total > 0 else 0
            status = "✅" if stats['failed'] == 0 else "⚠️"
            print(f"{status} {language_names[lang]:14} ({lang}): {stats['passed']}/{total} ({success_rate:.0f}%)")
        else:
            print(f"⚪ {language_names[lang]:14} ({lang}): не тестувалась")
    
    print("=" * 100)

if __name__ == "__main__":
    test_all_11_languages()
