#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update "Track Applications" to "My Universities" in all languages
"""

import json
import os

languages = ['sk', 'en', 'uk', 'cs', 'pl', 'de', 'fr', 'es', 'it', 'ru']

# Translations for "My Universities"
my_universities = {
    'sk': {
        'title': 'Moje Univerzity',
        'description': 'Uložte si vybrané univerzity a programy'
    },
    'en': {
        'title': 'My Universities',
        'description': 'Save your selected universities and programs'
    },
    'uk': {
        'title': 'Мої Університети',
        'description': 'Зберігайте обрані університети та програми'
    },
    'cs': {
        'title': 'Moje Univerzity',
        'description': 'Uložte si vybrané univerzity a programy'
    },
    'pl': {
        'title': 'Moje Uniwersytety',
        'description': 'Zapisz wybrane uniwersytety i programy'
    },
    'de': {
        'title': 'Meine Universitäten',
        'description': 'Speichern Sie Ihre ausgewählten Universitäten und Programme'
    },
    'fr': {
        'title': 'Mes Universités',
        'description': 'Enregistrez vos universités et programmes sélectionnés'
    },
    'es': {
        'title': 'Mis Universidades',
        'description': 'Guarda tus universidades y programas seleccionados'
    },
    'it': {
        'title': 'Le Mie Università',
        'description': 'Salva le tue università e programmi selezionati'
    },
    'ru': {
        'title': 'Мои Университеты',
        'description': 'Сохраняйте выбранные университеты и программы'
    }
}

base_path = 'C:/Users/info/OneDrive/Dokumenty/Student/frontend/locales'

for lang in languages:
    file_path = f'{base_path}/{lang}/common.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Update dashboard declaration_card
        if 'dashboard' in data and 'declaration_card' in data['dashboard']:
            data['dashboard']['declaration_card']['title'] = my_universities[lang]['title']
            data['dashboard']['declaration_card']['description'] = my_universities[lang]['description']
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f'[OK] {lang}/common.json - {my_universities[lang]["title"]}')
        
    except Exception as e:
        print(f'[ERROR] {lang}: {e}')

print('\n[SUCCESS] Updated to "My Universities" in all languages!')
