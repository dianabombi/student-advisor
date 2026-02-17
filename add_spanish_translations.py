"""
Додавання перекладів для іспанської юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Іспанії
SPAIN_TRANSLATIONS = {
    'sk': {
        'universities': 'Španielske Univerzity',
        'languageSchools': 'Španielske Jazykové Školy',
        'vocationalSchools': 'Španielske Stredné Odborné Školy',
        'conservatories': 'Španielske Konzervatóriá',
        'foundationPrograms': 'Španielske Prípravné Programy'
    },
    'cs': {
        'universities': 'Španělské Univerzity',
        'languageSchools': 'Španělské Jazykové Školy',
        'vocationalSchools': 'Španělské Střední Odborné Školy',
        'conservatories': 'Španělská Konzervatoře',
        'foundationPrograms': 'Španělské Přípravné Programy'
    },
    'pl': {
        'universities': 'Hiszpańskie Uniwersytety',
        'languageSchools': 'Hiszpańskie Szkoły Językowe',
        'vocationalSchools': 'Hiszpańskie Szkoły Zawodowe',
        'conservatories': 'Hiszpańskie Konserwatoria',
        'foundationPrograms': 'Hiszpańskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Spanish Universities',
        'languageSchools': 'Spanish Language Schools',
        'vocationalSchools': 'Spanish Vocational Schools',
        'conservatories': 'Spanish Conservatories',
        'foundationPrograms': 'Spanish Foundation Programs'
    },
    'de': {
        'universities': 'Spanische Universitäten',
        'languageSchools': 'Spanische Sprachschulen',
        'vocationalSchools': 'Spanische Berufsschulen',
        'conservatories': 'Spanische Konservatorien',
        'foundationPrograms': 'Spanische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Іспанські Університети',
        'languageSchools': 'Іспанські Мовні Школи',
        'vocationalSchools': 'Іспанські Професійні Школи',
        'conservatories': 'Іспанські Консерваторії',
        'foundationPrograms': 'Іспанські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Испанские Университеты',
        'languageSchools': 'Испанские Языковые Школы',
        'vocationalSchools': 'Испанские Профессиональные Школы',
        'conservatories': 'Испанские Консерватории',
        'foundationPrograms': 'Испанские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Spagnole',
        'languageSchools': 'Scuole di Lingua Spagnole',
        'vocationalSchools': 'Scuole Professionali Spagnole',
        'conservatories': 'Conservatori Spagnoli',
        'foundationPrograms': 'Programmi Preparatori Spagnoli'
    },
    'fr': {
        'universities': 'Universités Espagnoles',
        'languageSchools': 'Écoles de Langue Espagnoles',
        'vocationalSchools': 'Écoles Professionnelles Espagnoles',
        'conservatories': 'Conservatoires Espagnols',
        'foundationPrograms': 'Programmes Préparatoires Espagnols'
    },
    'es': {
        'universities': 'Universidades Españolas',
        'languageSchools': 'Escuelas de Idiomas Españolas',
        'vocationalSchools': 'Escuelas Profesionales Españolas',
        'conservatories': 'Conservatorios Españoles',
        'foundationPrograms': 'Programas Preparatorios Españoles'
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
        
        # Додати іспанські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['ES'] = SPAIN_TRANSLATIONS.get(lang_code, SPAIN_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Spanish jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Spanish translations added!")

if __name__ == "__main__":
    main()
