#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add translations for 4 new educational categories to all 10 languages
"""

import json
import os

# Base directory for locales
LOCALES_DIR = "frontend/locales"

# Translations for category titles
CATEGORY_TRANSLATIONS = {
    'sk': {
        "languageSchools": {"title": "Jazykové školy"},
        "vocationalSchools": {"title": "Stredné odborné školy"},
        "conservatories": {"title": "Konzervatóriá"},
        "foundationPrograms": {"title": "Prípravné programy"}
    },
    'en': {
        "languageSchools": {"title": "Language Schools"},
        "vocationalSchools": {"title": "Vocational Schools"},
        "conservatories": {"title": "Conservatories"},
        "foundationPrograms": {"title": "Foundation Programs"}
    },
    'uk': {
        "languageSchools": {"title": "Мовні школи"},
        "vocationalSchools": {"title": "Професійні школи"},
        "conservatories": {"title": "Консерваторії"},
        "foundationPrograms": {"title": "Підготовчі програми"}
    },
    'cs': {
        "languageSchools": {"title": "Jazykové školy"},
        "vocationalSchools": {"title": "Střední odborné školy"},
        "conservatories": {"title": "Konzervatoře"},
        "foundationPrograms": {"title": "Přípravné programy"}
    },
    'pl': {
        "languageSchools": {"title": "Szkoły językowe"},
        "vocationalSchools": {"title": "Szkoły zawodowe"},
        "conservatories": {"title": "Konserwatoria"},
        "foundationPrograms": {"title": "Programy przygotowawcze"}
    },
    'de': {
        "languageSchools": {"title": "Sprachschulen"},
        "vocationalSchools": {"title": "Berufsschulen"},
        "conservatories": {"title": "Konservatorien"},
        "foundationPrograms": {"title": "Vorbereitungsprogramme"}
    },
    'fr': {
        "languageSchools": {"title": "Écoles de langues"},
        "vocationalSchools": {"title": "Écoles professionnelles"},
        "conservatories": {"title": "Conservatoires"},
        "foundationPrograms": {"title": "Programmes préparatoires"}
    },
    'es': {
        "languageSchools": {"title": "Escuelas de idiomas"},
        "vocationalSchools": {"title": "Escuelas profesionales"},
        "conservatories": {"title": "Conservatorios"},
        "foundationPrograms": {"title": "Programas preparatorios"}
    },
    'it': {
        "languageSchools": {"title": "Scuole di lingue"},
        "vocationalSchools": {"title": "Scuole professionali"},
        "conservatories": {"title": "Conservatori"},
        "foundationPrograms": {"title": "Programmi preparatori"}
    },
    'ru': {
        "languageSchools": {"title": "Языковые школы"},
        "vocationalSchools": {"title": "Профессиональные школы"},
        "conservatories": {"title": "Консерватории"},
        "foundationPrograms": {"title": "Подготовительные программы"}
    }
}

def add_category_translations():
    """Add category translations to all language files"""
    
    for lang_code, translations in CATEGORY_TRANSLATIONS.items():
        file_path = os.path.join(LOCALES_DIR, lang_code, "common.json")
        
        try:
            # Read existing translations
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Add new category translations under 'student' key
            if 'student' not in data:
                data['student'] = {}
            
            # Add each category
            for category_key, category_data in translations.items():
                data['student'][category_key] = category_data
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"[OK] Added category translations for {lang_code}")
            
        except Exception as e:
            print(f"[ERROR] Error processing {lang_code}: {e}")

if __name__ == '__main__':
    add_category_translations()
    print("\n[SUCCESS] Category translations added successfully!")
