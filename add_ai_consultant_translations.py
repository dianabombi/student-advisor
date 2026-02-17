#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

# AI Consultant button translations
ai_consultant_translations = {
    'en': 'AI Consultant',
    'sk': 'AI Konzultant',
    'cs': 'AI Konzultant',
    'pl': 'Konsultant AI',
    'de': 'KI-Berater',
    'fr': 'Consultant IA',
    'es': 'Consultor IA',
    'it': 'Consulente IA',
    'uk': 'AI Консультант',
    'ru': 'AI Консультант'
}

# Process each language
base_path = r"C:\Users\info\OneDrive\Dokumenty\Student\frontend\locales"
for lang, translation in ai_consultant_translations.items():
    file_path = os.path.join(base_path, lang, "common.json")
    
    # Read existing file
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    # Add university.aiConsultant
    if 'university' not in data:
        data['university'] = {}
    data['university']['aiConsultant'] = translation
    
    # Write back with UTF-8
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Updated {lang}/common.json: {translation}")

print("\nSUCCESS: All translation files updated with AI Consultant button!")
