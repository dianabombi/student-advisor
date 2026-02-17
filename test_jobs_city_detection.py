#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест визначення міста для AI-консультанта підробітків
"""

import sys
sys.path.append('/app')

from services.jobs_chat_service import JobsChatService

def test_city_detection():
    """Тестування визначення міста на різних мовах"""
    service = JobsChatService()
    
    test_cases = [
        # Словацька
        ("Hľadám brigádu v Košiciach", "sk", "Košice"),
        ("Hľadám brigádu v Nitre", "sk", "Nitra"),
        ("Potrebujem prácu v Bratislave", "sk", "Bratislava"),
        
        # Українська
        ("Шукаю підробіток в Кошіце", "uk", "Košice"),
        ("Шукаю роботу в Нітрі", "uk", "Nitra"),
        ("Де знайти роботу в Братиславі?", "uk", "Bratislava"),
        
        # Чеська
        ("Hledám brigádu v Košicích", "cs", "Košice"),
        ("Hledám práci v Nitře", "cs", "Nitra"),
        
        # Англійська
        ("Looking for a job in Kosice", "en", "Košice"),
        ("I need work in Nitra", "en", "Nitra"),
        ("Where to find a job in Bratislava?", "en", "Bratislava"),
        
        # Польська
        ("Szukam pracy w Koszycach", "pl", "Košice"),
        ("Potrzebuję pracy w Nitrze", "pl", "Nitra"),
        
        # Російська
        ("Ищу работу в Кошице", "ru", "Košice"),
        ("Нужна работа в Нитре", "ru", "Nitra"),
    ]
    
    print("=" * 80)
    print("ТЕСТ ВИЗНАЧЕННЯ МІСТА")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for message, lang, expected_city in test_cases:
        detected_city = service._extract_city_from_message(message, 'SK')
        
        if detected_city == expected_city:
            print(f"✅ [{lang}] '{message}' → {detected_city}")
            passed += 1
        else:
            print(f"❌ [{lang}] '{message}' → Очікувалось: {expected_city}, Отримано: {detected_city}")
            failed += 1
    
    print("=" * 80)
    print(f"РЕЗУЛЬТАТ: {passed} пройдено, {failed} провалено")
    print("=" * 80)

if __name__ == "__main__":
    test_city_detection()
