#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix feature3 translations - Global Coverage/Reach
"""

import json
import os

# All supported languages with correct translations
languages = ['sk', 'en', 'uk', 'cs', 'pl', 'de', 'fr', 'es', 'it', 'ru']

# Correct translations for feature3
updates = {
    'sk': {
        'title': 'Globálny Dosah',
        'description': 'Prístup k informáciám o univerzitách po celom svete'
    },
    'en': {
        'title': 'Global Reach',
        'description': 'Access information about universities worldwide'
    },
    'uk': {
        'title': 'Глобальне Охоплення',
        'description': 'Доступ до інформації про університети по всьому світу'
    },
    'cs': {
        'title': 'Globální Dosah',
        'description': 'Přístup k informacím o univerzitách po celém světě'
    },
    'pl': {
        'title': 'Globalny Zasięg',
        'description': 'Dostęp do informacji o uniwersytetach na całym świecie'
    },
    'de': {
        'title': 'Globale Reichweite',
        'description': 'Zugang zu Informationen über Universitäten weltweit'
    },
    'fr': {
        'title': 'Portée Mondiale',
        'description': 'Accès aux informations sur les universités du monde entier'
    },
    'es': {
        'title': 'Alcance Global',
        'description': 'Acceso a información sobre universidades de todo el mundo'
    },
    'it': {
        'title': 'Copertura Globale',
        'description': 'Accesso alle informazioni sulle università di tutto il mondo'
    },
    'ru': {
        'title': 'Глобальный Охват',
        'description': 'Доступ к информации об университетах по всему миру'
    }
}

base_path = 'C:/Users/info/OneDrive/Dokumenty/Student/frontend/locales'

for lang in languages:
    file_path = f'{base_path}/{lang}/common.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Update feature3 title and description
        if 'student' in data and 'features' in data['student']:
            if 'feature3' in data['student']['features']:
                data['student']['features']['feature3']['title'] = updates[lang]['title']
                data['student']['features']['feature3']['description'] = updates[lang]['description']
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f'[OK] Updated {lang}/common.json - {updates[lang]["title"]}')
        
    except Exception as e:
        print(f'[ERROR] {lang}: {e}')

print('\n[SUCCESS] All feature3 translations corrected!')
