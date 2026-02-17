#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove CODEX references from all translation files
"""

import json
import os

# All supported languages
languages = ['sk', 'en', 'uk', 'cs', 'pl', 'de', 'fr', 'es', 'it', 'ru']

# Translation updates
updates = {
    'sk': {
        'subtitle': 'Vytvorte si účet',
        'ai_tool': 'Rozumiem, že Student Advisor je AI nástroj, NIE právnik',
        'no_advice': 'Rozumiem, že Student Advisor NEPOSKYTUJE právne poradenstvo',
        'no_attorney': 'Rozumiem, že používanie Student Advisor NEVYTVÁRA vzťah klient-advokát'
    },
    'en': {
        'subtitle': 'Create your account',
        'ai_tool': 'I understand Student Advisor is an AI tool, NOT a lawyer',
        'no_advice': 'I understand Student Advisor does NOT provide legal advice',
        'no_attorney': 'I understand using Student Advisor does NOT create attorney-client relationship'
    },
    'uk': {
        'subtitle': 'Створіть свій обліковий запис',
        'ai_tool': 'Я розумію, що Student Advisor - це AI інструмент, а НЕ юрист',
        'no_advice': 'Я розумію, що Student Advisor НЕ надає юридичних порад',
        'no_attorney': 'Я розумію, що використання Student Advisor НЕ створює відносин клієнт-адвокат'
    },
    'cs': {
        'subtitle': 'Vytvořte si účet',
        'ai_tool': 'Rozumím, že Student Advisor je AI nástroj, NIKOLI právník',
        'no_advice': 'Rozumím, že Student Advisor NEPOSKYTUJE právní poradenství',
        'no_attorney': 'Rozumím, že používání Student Advisor NEVYTVÁŘÍ vztah klient-advokát'
    },
    'pl': {
        'subtitle': 'Utwórz konto',
        'ai_tool': 'Rozumiem, że Student Advisor to narzędzie AI, a NIE prawnik',
        'no_advice': 'Rozumiem, że Student Advisor NIE świadczy porad prawnych',
        'no_attorney': 'Rozumiem, że korzystanie z Student Advisor NIE tworzy relacji klient-adwokat'
    },
    'de': {
        'subtitle': 'Konto erstellen',
        'ai_tool': 'Ich verstehe, dass Student Advisor ein KI-Tool ist, KEIN Anwalt',
        'no_advice': 'Ich verstehe, dass Student Advisor KEINE Rechtsberatung bietet',
        'no_attorney': 'Ich verstehe, dass die Nutzung von Student Advisor KEINE Mandantenbeziehung schafft'
    },
    'fr': {
        'subtitle': 'Créer un compte',
        'ai_tool': "Je comprends que Student Advisor est un outil IA, PAS un avocat",
        'no_advice': "Je comprends que Student Advisor NE fournit PAS de conseils juridiques",
        'no_attorney': "Je comprends que l'utilisation de Student Advisor NE crée PAS de relation avocat-client"
    },
    'es': {
        'subtitle': 'Crear cuenta',
        'ai_tool': 'Entiendo que Student Advisor es una herramienta de IA, NO un abogado',
        'no_advice': 'Entiendo que Student Advisor NO proporciona asesoramiento legal',
        'no_attorney': 'Entiendo que usar Student Advisor NO crea una relación abogado-cliente'
    },
    'it': {
        'subtitle': 'Crea account',
        'ai_tool': 'Capisco che Student Advisor è uno strumento AI, NON un avvocato',
        'no_advice': 'Capisco che Student Advisor NON fornisce consulenza legale',
        'no_attorney': 'Capisco che usare Student Advisor NON crea un rapporto avvocato-cliente'
    },
    'ru': {
        'subtitle': 'Создать аккаунт',
        'ai_tool': 'Я понимаю, что Student Advisor - это AI инструмент, а НЕ юрист',
        'no_advice': 'Я понимаю, что Student Advisor НЕ предоставляет юридических консультаций',
        'no_attorney': 'Я понимаю, что использование Student Advisor НЕ создает отношений клиент-адвокат'
    }
}

base_path = 'C:/Users/info/OneDrive/Dokumenty/Student/frontend/locales'

for lang in languages:
    file_path = f'{base_path}/{lang}/common.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Update registration subtitle
        if 'auth' in data and 'register' in data['auth']:
            data['auth']['register']['subtitle'] = updates[lang]['subtitle']
            
            # Update consent messages
            if 'consent' in data['auth']['register']:
                data['auth']['register']['consent']['ai_tool'] = updates[lang]['ai_tool']
                data['auth']['register']['consent']['no_advice'] = updates[lang]['no_advice']
                data['auth']['register']['consent']['no_attorney'] = updates[lang]['no_attorney']
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f'[OK] Updated {lang}/common.json')
        
    except Exception as e:
        print(f'[ERROR] {lang}: {e}')

print('\n[SUCCESS] All translation files updated!')
