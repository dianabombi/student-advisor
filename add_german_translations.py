"""
Додавання перекладів для німецької юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Німеччини
GERMANY_TRANSLATIONS = {
    'sk': {
        'universities': 'Nemecké Univerzity',
        'languageSchools': 'Nemecké Jazykové Školy',
        'vocationalSchools': 'Nemecké Stredné Odborné Školy',
        'conservatories': 'Nemecké Konzervatóriá',
        'foundationPrograms': 'Nemecké Prípravné Programy'
    },
    'cs': {
        'universities': 'Německé Univerzity',
        'languageSchools': 'Německé Jazykové Školy',
        'vocationalSchools': 'Německé Střední Odborné Školy',
        'conservatories': 'Německá Konzervatoře',
        'foundationPrograms': 'Německé Přípravné Programy'
    },
    'pl': {
        'universities': 'Niemieckie Uniwersytety',
        'languageSchools': 'Niemieckie Szkoły Językowe',
        'vocationalSchools': 'Niemieckie Szkoły Zawodowe',
        'conservatories': 'Niemieckie Konserwatoria',
        'foundationPrograms': 'Niemieckie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'German Universities',
        'languageSchools': 'German Language Schools',
        'vocationalSchools': 'German Vocational Schools',
        'conservatories': 'German Conservatories',
        'foundationPrograms': 'German Foundation Programs'
    },
    'de': {
        'universities': 'Deutsche Universitäten',
        'languageSchools': 'Deutsche Sprachschulen',
        'vocationalSchools': 'Deutsche Berufsschulen',
        'conservatories': 'Deutsche Konservatorien',
        'foundationPrograms': 'Deutsche Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Німецькі Університети',
        'languageSchools': 'Німецькі Мовні Школи',
        'vocationalSchools': 'Німецькі Професійні Школи',
        'conservatories': 'Німецькі Консерваторії',
        'foundationPrograms': 'Німецькі Підготовчі Програми'
    },
    'ru': {
        'universities': 'Немецкие Университеты',
        'languageSchools': 'Немецкие Языковые Школы',
        'vocationalSchools': 'Немецкие Профессиональные Школы',
        'conservatories': 'Немецкие Консерватории',
        'foundationPrograms': 'Немецкие Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Tedesche',
        'languageSchools': 'Scuole di Lingua Tedesche',
        'vocationalSchools': 'Scuole Professionali Tedesche',
        'conservatories': 'Conservatori Tedeschi',
        'foundationPrograms': 'Programmi Preparatori Tedeschi'
    },
    'fr': {
        'universities': 'Universités Allemandes',
        'languageSchools': 'Écoles de Langue Allemandes',
        'vocationalSchools': 'Écoles Professionnelles Allemandes',
        'conservatories': 'Conservatoires Allemands',
        'foundationPrograms': 'Programmes Préparatoires Allemands'
    },
    'es': {
        'universities': 'Universidades Alemanas',
        'languageSchools': 'Escuelas de Idiomas Alemanas',
        'vocationalSchools': 'Escuelas Profesionales Alemanas',
        'conservatories': 'Conservatorios Alemanes',
        'foundationPrograms': 'Programas Preparatorios Alemanes'
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
        
        # Додати німецькі переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['DE'] = GERMANY_TRANSLATIONS.get(lang_code, GERMANY_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding German jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll German translations added!")

if __name__ == "__main__":
    main()
