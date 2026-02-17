#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update hero subtitle to remove "AI" reference
Changes "AI poradenstvo/guidance/conseil" to just "poradenstvo/guidance/conseil"
"""

import json
import os

# Hero subtitle updates - removing "AI" from all languages
hero_updates = {
    'sk': "Objavte univerzity, získajte poradenstvo a naplánujte svoju akademickú budúcnosť",
    'en': "Discover universities, get guidance, and plan your academic future",
    'cs': "Objevte univerzity, získejte poradenství a naplánujte svou akademickou budoucnost",
    'pl': "Odkryj uniwersytety, uzyskaj poradę i zaplanuj swoją akademicką przyszłość",
    'de': "Entdecken Sie Universitäten, erhalten Sie Beratung und planen Sie Ihre akademische Zukunft",
    'fr': "Découvrez les universités, obtenez des conseils et planifiez votre avenir académique",
    'es': "Descubre universidades, obtén orientación y planifica tu futuro académico",
    'it': "Scopri le università, ottieni consulenza e pianifica il tuo futuro accademico",
    'uk': "Відкрийте університети, отримайте консультацію та сплануйте своє академічне майбутнє",
    'ru': "Откройте университеты, получите консультацию и спланируйте свое академическое будущее"
}

def update_hero_subtitle(lang_code, new_subtitle):
    """Update hero subtitle in translation file"""
    file_path = f'C:/Users/info/OneDrive/Dokumenty/Student/frontend/locales/{lang_code}/common.json'
    
    try:
        # Read existing file
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        
        # Update hero subtitle
        if 'home' in data and 'hero' in data['home']:
            data['home']['hero']['subtitle'] = new_subtitle
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f'[OK] Updated {lang_code}/common.json hero subtitle')
        return True
        
    except Exception as e:
        print(f'[ERROR] Error updating {lang_code}/common.json: {e}')
        return False

def main():
    """Update all translation files"""
    print('Updating hero subtitles to remove "AI" reference...\n')
    
    success_count = 0
    for lang_code, new_subtitle in hero_updates.items():
        if update_hero_subtitle(lang_code, new_subtitle):
            success_count += 1
    
    print(f'\n[OK] Successfully updated {success_count}/{len(hero_updates)} language files')
    print('Changes: "AI poradenstvo/guidance" -> "poradenstvo/guidance" in hero section')

if __name__ == '__main__':
    main()
