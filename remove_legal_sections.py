#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove legal sections that don't fit educational platform
"""

import json
import os

languages = ['sk', 'en', 'uk', 'cs', 'pl', 'de', 'fr', 'es', 'it', 'ru']
base_path = 'C:/Users/info/OneDrive/Dokumenty/Student/frontend/locales'

# Sections to remove (legal-only content)
sections_to_remove = [
    'howItWorks',  # Legal platform guide
    'marketplace',  # Lawyer marketplace
    'payment',  # Payment for legal services
    'aiSupport'  # Technical support (can be added later if needed)
]

for lang in languages:
    file_path = f'{base_path}/{lang}/common.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        removed = []
        for section in sections_to_remove:
            if section in data:
                del data[section]
                removed.append(section)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        if removed:
            print(f'[OK] {lang}/common.json - Removed: {", ".join(removed)}')
        else:
            print(f'[SKIP] {lang}/common.json - No sections to remove')
        
    except Exception as e:
        print(f'[ERROR] {lang}: {e}')

print('\n[SUCCESS] All legal-only sections removed!')
