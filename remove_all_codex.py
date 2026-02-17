#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove all CODEX references from translation files
"""

import json
import os
import re

# All supported languages
languages = ['sk', 'en', 'uk', 'cs', 'pl', 'de', 'fr', 'es', 'it', 'ru']

base_path = 'C:/Users/info/OneDrive/Dokumenty/Student/frontend/locales'

def remove_codex_from_value(value):
    """Recursively remove CODEX from string values"""
    if isinstance(value, str):
        # Replace CODEX with Student Advisor
        value = value.replace('CODEX', 'Student Advisor')
        value = value.replace('Codex', 'Student Advisor')
        return value
    elif isinstance(value, dict):
        return {k: remove_codex_from_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [remove_codex_from_value(item) for item in value]
    else:
        return value

for lang in languages:
    file_path = f'{base_path}/{lang}/common.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Remove CODEX from all values
        data = remove_codex_from_value(data)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f'[OK] Updated {lang}/common.json')
        
    except Exception as e:
        print(f'[ERROR] {lang}: {e}')

print('\n[SUCCESS] All CODEX references removed from translation files!')
