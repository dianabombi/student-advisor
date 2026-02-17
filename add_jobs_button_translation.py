#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add student jobs button translation to all 10 languages
"""

import json
import os

# Define translations for all 10 languages
TRANSLATIONS = {
    'sk': 'Brigády pre študentov',
    'cs': 'Brigády pro studenty',
    'pl': 'Praca dla studentów',
    'en': 'Student Jobs',
    'de': 'Studentenjobs',
    'fr': 'Jobs étudiants',
    'es': 'Trabajos para estudiantes',
    'uk': 'Підробіток для студентів',
    'it': 'Lavori per studenti',
    'ru': 'Подработка для студентов'
}

def add_translation():
    """Add student jobs button translation to all language files"""
    
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    locales_dir = os.path.join(frontend_dir, 'locales')
    
    if not os.path.exists(locales_dir):
        print(f"[-] Locales directory not found: {locales_dir}")
        return
    
    success_count = 0
    error_count = 0
    
    for lang_code, translation_text in TRANSLATIONS.items():
        lang_file = os.path.join(locales_dir, lang_code, 'common.json')
        
        try:
            # Read existing translations (handle UTF-8 BOM)
            if os.path.exists(lang_file):
                with open(lang_file, 'r', encoding='utf-8-sig') as f:
                    data = json.load(f)
            else:
                print(f"[!] File not found: {lang_file}")
                continue
            
            # Add student jobs translation
            if 'student' not in data:
                data['student'] = {}
            if 'hero' not in data['student']:
                data['student']['hero'] = {}
            
            data['student']['hero']['studentJobs'] = translation_text
            
            # Write back to file
            with open(lang_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"[+] Updated {lang_code}/common.json: '{translation_text}'")
            success_count += 1
            
        except Exception as e:
            print(f"[-] Error updating {lang_code}: {e}")
            error_count += 1
    
    print(f"\n{'='*50}")
    print(f"[+] Successfully updated: {success_count} files")
    if error_count > 0:
        print(f"[-] Errors: {error_count} files")
    print(f"{'='*50}")


if __name__ == "__main__":
    print("Adding student jobs button translation to all 10 languages...\n")
    add_translation()
    print("\nDone! Translation added successfully.")
