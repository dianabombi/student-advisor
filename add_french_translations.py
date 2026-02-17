"""
Додавання перекладів для французької юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Франції
FRANCE_TRANSLATIONS = {
    'sk': {
        'universities': 'Francúzske Univerzity',
        'languageSchools': 'Francúzske Jazykové Školy',
        'vocationalSchools': 'Francúzske Stredné Odborné Školy',
        'conservatories': 'Francúzske Konzervatóriá',
        'foundationPrograms': 'Francúzske Prípravné Programy'
    },
    'cs': {
        'universities': 'Francouzské Univerzity',
        'languageSchools': 'Francouzské Jazykové Školy',
        'vocationalSchools': 'Francouzské Střední Odborné Školy',
        'conservatories': 'Francouzská Konzervatoře',
        'foundationPrograms': 'Francouzské Přípravné Programy'
    },
    'pl': {
        'universities': 'Francuskie Uniwersytety',
        'languageSchools': 'Francuskie Szkoły Językowe',
        'vocationalSchools': 'Francuskie Szkoły Zawodowe',
        'conservatories': 'Francuskie Konserwatoria',
        'foundationPrograms': 'Francuskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'French Universities',
        'languageSchools': 'French Language Schools',
        'vocationalSchools': 'French Vocational Schools',
        'conservatories': 'French Conservatories',
        'foundationPrograms': 'French Foundation Programs'
    },
    'de': {
        'universities': 'Französische Universitäten',
        'languageSchools': 'Französische Sprachschulen',
        'vocationalSchools': 'Französische Berufsschulen',
        'conservatories': 'Französische Konservatorien',
        'foundationPrograms': 'Französische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Французькі Університети',
        'languageSchools': 'Французькі Мовні Школи',
        'vocationalSchools': 'Французькі Професійні Школи',
        'conservatories': 'Французькі Консерваторії',
        'foundationPrograms': 'Французькі Підготовчі Програми'
    },
    'ru': {
        'universities': 'Французские Университеты',
        'languageSchools': 'Французские Языковые Школы',
        'vocationalSchools': 'Французские Профессиональные Школы',
        'conservatories': 'Французские Консерватории',
        'foundationPrograms': 'Французские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Francesi',
        'languageSchools': 'Scuole di Lingua Francesi',
        'vocationalSchools': 'Scuole Professionali Francesi',
        'conservatories': 'Conservatori Francesi',
        'foundationPrograms': 'Programmi Preparatori Francesi'
    },
    'fr': {
        'universities': 'Universités Françaises',
        'languageSchools': 'Écoles de Langue Françaises',
        'vocationalSchools': 'Écoles Professionnelles Françaises',
        'conservatories': 'Conservatoires Français',
        'foundationPrograms': 'Programmes Préparatoires Français'
    },
    'es': {
        'universities': 'Universidades Francesas',
        'languageSchools': 'Escuelas de Idiomas Francesas',
        'vocationalSchools': 'Escuelas Profesionales Francesas',
        'conservatories': 'Conservatorios Franceses',
        'foundationPrograms': 'Programas Preparatorios Franceses'
    }
}

def update_locale_file(lang_code):
    """Оновити файл перекладів для мови"""
    file_path = os.path.join(LOCALES_DIR, lang_code, 'common.json')
    
    if not os.path.exists(file_path):
        print(f"Skipping {lang_code} - file not found")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Додати французькі переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['FR'] = FRANCE_TRANSLATIONS.get(lang_code, FRANCE_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding French jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll French translations added!")

if __name__ == "__main__":
    main()
