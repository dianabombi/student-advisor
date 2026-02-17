"""
Додавання перекладів для грецької юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Греції
GREECE_TRANSLATIONS = {
    'sk': {
        'universities': 'Grécke Univerzity',
        'languageSchools': 'Grécke Jazykové Školy',
        'vocationalSchools': 'Grécke Stredné Odborné Školy',
        'conservatories': 'Grécke Konzervatóriá',
        'foundationPrograms': 'Grécke Prípravné Programy'
    },
    'cs': {
        'universities': 'Řecké Univerzity',
        'languageSchools': 'Řecké Jazykové Školy',
        'vocationalSchools': 'Řecké Střední Odborné Školy',
        'conservatories': 'Řecká Konzervatoře',
        'foundationPrograms': 'Řecké Přípravné Programy'
    },
    'pl': {
        'universities': 'Greckie Uniwersytety',
        'languageSchools': 'Greckie Szkoły Językowe',
        'vocationalSchools': 'Greckie Szkoły Zawodowe',
        'conservatories': 'Greckie Konserwatoria',
        'foundationPrograms': 'Greckie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Greek Universities',
        'languageSchools': 'Greek Language Schools',
        'vocationalSchools': 'Greek Vocational Schools',
        'conservatories': 'Greek Conservatories',
        'foundationPrograms': 'Greek Foundation Programs'
    },
    'de': {
        'universities': 'Griechische Universitäten',
        'languageSchools': 'Griechische Sprachschulen',
        'vocationalSchools': 'Griechische Berufsschulen',
        'conservatories': 'Griechische Konservatorien',
        'foundationPrograms': 'Griechische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Грецькі Університети',
        'languageSchools': 'Грецькі Мовні Школи',
        'vocationalSchools': 'Грецькі Професійні Школи',
        'conservatories': 'Грецькі Консерваторії',
        'foundationPrograms': 'Грецькі Підготовчі Програми'
    },
    'ru': {
        'universities': 'Греческие Университеты',
        'languageSchools': 'Греческие Языковые Школы',
        'vocationalSchools': 'Греческие Профессиональные Школы',
        'conservatories': 'Греческие Консерватории',
        'foundationPrograms': 'Греческие Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Greche',
        'languageSchools': 'Scuole di Lingua Greche',
        'vocationalSchools': 'Scuole Professionali Greche',
        'conservatories': 'Conservatori Greci',
        'foundationPrograms': 'Programmi Preparatori Greci'
    },
    'fr': {
        'universities': 'Universités Grecques',
        'languageSchools': 'Écoles de Langue Grecques',
        'vocationalSchools': 'Écoles Professionnelles Grecques',
        'conservatories': 'Conservatoires Grecs',
        'foundationPrograms': 'Programmes Préparatoires Grecs'
    },
    'es': {
        'universities': 'Universidades Griegas',
        'languageSchools': 'Escuelas de Idiomas Griegas',
        'vocationalSchools': 'Escuelas Profesionales Griegas',
        'conservatories': 'Conservatorios Griegos',
        'foundationPrograms': 'Programas Preparatorios Griegos'
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
        
        # Додати грецькі переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['GR'] = GREECE_TRANSLATIONS.get(lang_code, GREECE_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Greek jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Greek translations added!")

if __name__ == "__main__":
    main()
