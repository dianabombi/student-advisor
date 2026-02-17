#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

# Common UI translations for all languages
common_ui_translations = {
    'en': {
        "common": {
            "students": "students",
            "programs": "programs"
        }
    },
    'sk': {
        "common": {
            "students": "študentov",
            "programs": "programov"
        }
    },
    'cs': {
        "common": {
            "students": "studentů",
            "programs": "programů"
        }
    },
    'pl': {
        "common": {
            "students": "studentów",
            "programs": "programów"
        }
    },
    'de': {
        "common": {
            "students": "Studenten",
            "programs": "Programme"
        }
    },
    'fr': {
        "common": {
            "students": "étudiants",
            "programs": "programmes"
        }
    },
    'es': {
        "common": {
            "students": "estudiantes",
            "programs": "programas"
        }
    },
    'it': {
        "common": {
            "students": "studenti",
            "programs": "programmi"
        }
    },
    'uk': {
        "common": {
            "students": "студентів",
            "programs": "програм"
        }
    },
    'ru': {
        "common": {
            "students": "студентов",
            "programs": "программ"
        }
    }
}

# Process each language
base_path = r"C:\Users\info\OneDrive\Dokumenty\Student\frontend\locales"
for lang, translations in common_ui_translations.items():
    file_path = os.path.join(base_path, lang, "common.json")
    
    # Read existing file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add common section
    if 'common' not in data:
        data['common'] = {}
    data['common']['students'] = translations['common']['students']
    data['common']['programs'] = translations['common']['programs']
    
    # Write back with UTF-8
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Updated {lang}/common.json with common UI translations")

print("\nSUCCESS: All translation files updated with students/programs translations!")
