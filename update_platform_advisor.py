#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update Platform to Advisor and remove AI prefix in all languages
"""

import json
import os

# All supported languages
languages = ['sk', 'en', 'uk', 'cs', 'pl', 'de', 'fr', 'es', 'it', 'ru']

# Translations for "Why Choose Student Advisor?" and "Consultations"
updates = {
    'sk': {
        'features_title': 'Prečo si vybrať Student Advisor?',
        'feature2_title': 'Konzultácie'
    },
    'en': {
        'features_title': 'Why Choose Student Advisor?',
        'feature2_title': 'Consultations'
    },
    'uk': {
        'features_title': 'Чому Обрати Student Advisor?',
        'feature2_title': 'Консультації'
    },
    'cs': {
        'features_title': 'Proč si vybrat Student Advisor?',
        'feature2_title': 'Konzultace'
    },
    'pl': {
        'features_title': 'Dlaczego wybrać Student Advisor?',
        'feature2_title': 'Konsultacje'
    },
    'de': {
        'features_title': 'Warum Student Advisor wählen?',
        'feature2_title': 'Beratungen'
    },
    'fr': {
        'features_title': 'Pourquoi choisir Student Advisor?',
        'feature2_title': 'Consultations'
    },
    'es': {
        'features_title': '¿Por qué elegir Student Advisor?',
        'feature2_title': 'Consultas'
    },
    'it': {
        'features_title': 'Perché scegliere Student Advisor?',
        'feature2_title': 'Consulenze'
    },
    'ru': {
        'features_title': 'Почему выбрать Student Advisor?',
        'feature2_title': 'Консультации'
    }
}

base_path = 'C:/Users/info/OneDrive/Dokumenty/Student/frontend/locales'

for lang in languages:
    file_path = f'{base_path}/{lang}/common.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Update features title
        if 'student' in data and 'features' in data['student']:
            data['student']['features']['title'] = updates[lang]['features_title']
            
            # Update feature2 title (AI Consultations -> Consultations)
            if 'feature2' in data['student']['features']:
                data['student']['features']['feature2']['title'] = updates[lang]['feature2_title']
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f'[OK] Updated {lang}/common.json')
        
    except Exception as e:
        print(f'[ERROR] {lang}: {e}')

print('\n[SUCCESS] All translations updated!')
