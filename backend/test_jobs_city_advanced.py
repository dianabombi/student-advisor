#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Розширений тест визначення міста з різними варіантами написання та помилками
"""

import sys
sys.path.append('/app')

from services.jobs_chat_service import JobsChatService

def test_advanced_city_detection():
    """Тестування визначення міста з різними варіантами та помилками"""
    service = JobsChatService()
    
    test_cases = [
        # Košice - різні варіанти
        ("Шукаю підробіток в Кошіце", "Košice"),  # Українська з 'е'
        ("Шукаю підробіток в Кошіц", "Košice"),   # Українська без 'е'
        ("Шукаю підробіток в Кошице", "Košice"),  # Українська без діакритики
        ("Looking for job in Kosice", "Košice"),  # Англійська
        ("Hľadám prácu v Košiciach", "Košice"),   # Словацька
        ("Praca w Koszycach", "Košice"),          # Польська
        
        # Bratislava - різні варіанти
        ("Робота в Братиславі", "Bratislava"),    # Українська
        ("Робота в Братиславе", "Bratislava"),    # Російська
        ("Job in Bratislava", "Bratislava"),      # Англійська
        ("Práca v Bratislave", "Bratislava"),     # Словацька
        
        # Nitra - різні варіанти
        ("Шукаю роботу в Нітрі", "Nitra"),        # Українська
        ("Шукаю роботу в Нітре", "Nitra"),        # Українська альтернатива
        ("Работа в Нитре", "Nitra"),              # Російська
        ("Brigáda v Nitre", "Nitra"),             # Словацька
        
        # Banská Bystrica
        ("Робота в Банській Бистриці", "Banská Bystrica"),  # Українська
        ("Práca v Banskej Bystrici", "Banská Bystrica"),    # Словацька
        
        # Тести з контекстом
        ("Привіт! Я студент і шукаю підробіток в Кошіце. Допоможіть!", "Košice"),
        ("Де можна знайти роботу в Братиславі для студентів?", "Bratislava"),
        ("Потрібна brigáda в Nitre на літо", "Nitra"),
    ]
    
    print("=" * 80)
    print("РОЗШИРЕНИЙ ТЕСТ ВИЗНАЧЕННЯ МІСТА")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for message, expected_city in test_cases:
        detected_city = service._extract_city_from_message(message, 'SK')
        
        if detected_city == expected_city:
            print(f"✅ '{message}' → {detected_city}")
            passed += 1
        else:
            print(f"❌ '{message}' → Очікувалось: {expected_city}, Отримано: {detected_city}")
            failed += 1
    
    print("=" * 80)
    print(f"РЕЗУЛЬТАТ: {passed} пройдено, {failed} провалено")
    print(f"Успішність: {passed/(passed+failed)*100:.1f}%")
    print("=" * 80)

if __name__ == "__main__":
    test_advanced_city_detection()
