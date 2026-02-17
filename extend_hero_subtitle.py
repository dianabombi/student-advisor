#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extend hero subtitle with admission help message
Adds "and we will help you with admission to your chosen institution"
"""

import json
import os

# Extended hero subtitles for all languages
extended_subtitles = {
    'sk': "Objavte univerzity, získajte poradenstvo a naplánujte svoju akademickú budúcnosť, a my vám pomôžeme so vstupom do vybranej vzdelávacej inštitúcie",
    'en': "Discover universities, get guidance, and plan your academic future, and we will help you with admission to your chosen educational institution",
    'cs': "Objevte univerzity, získejte poradenství a naplánujte svou akademickou budoucnost, a my vám pomůžeme se vstupem do vybrané vzdělávací instituce",
    'pl': "Odkryj uniwersytety, uzyskaj poradę i zaplanuj swoją akademicką przyszłość, a my pomożemy ci w przyjęciu do wybranej instytucji edukacyjnej",
    'de': "Entdecken Sie Universitäten, erhalten Sie Beratung und planen Sie Ihre akademische Zukunft, und wir helfen Ihnen bei der Aufnahme an Ihrer gewählten Bildungseinrichtung",
    'fr': "Découvrez les universités, obtenez des conseils et planifiez votre avenir académique, et nous vous aiderons avec l'admission à l'établissement d'enseignement de votre choix",
    'es': "Descubre universidades, obtén orientación y planifica tu futuro académico, y te ayudaremos con la admisión a la institución educativa que elijas",
    'it': "Scopri le università, ottieni consulenza e pianifica il tuo futuro accademico, e ti aiuteremo con l'ammissione all'istituto educativo che hai scelto",
    'uk': "Відкрийте університети, отримайте консультацію та сплануйте своє академічне майбутнє, а ми допоможемо вам зі вступом до обраного навчального закладу",
    'ru': "Откройте университеты, получите консультацию и спланируйте свое академическое будущее, и мы поможем вам с поступлением в выбранное учебное заведение"
}

def update_hero_subtitle(lang_code, new_subtitle):
    """Update hero subtitle in translation file"""
    file_path = f'C:/Users/info/OneDrive/Dokumenty/Student/frontend/locales/{lang_code}/common.json'
    
    try:
        # Read existing file
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        
        # Update student.hero.subtitle
        if 'student' in data and 'hero' in data['student']:
            data['student']['hero']['subtitle'] = new_subtitle
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f'[OK] Updated {lang_code}/common.json with extended subtitle')
        return True
        
    except Exception as e:
        print(f'[ERROR] Error updating {lang_code}/common.json: {e}')
        return False

def main():
    """Update all translation files"""
    print('Extending hero subtitles with admission help message...\n')
    
    success_count = 0
    for lang_code, new_subtitle in extended_subtitles.items():
        if update_hero_subtitle(lang_code, new_subtitle):
            success_count += 1
    
    print(f'\n[OK] Successfully updated {success_count}/{len(extended_subtitles)} language files')
    print('Added: "and we will help you with admission" in all languages')

if __name__ == '__main__':
    main()
