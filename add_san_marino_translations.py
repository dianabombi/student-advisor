"""
Додавання перекладів для юрисдикції Сан-Марино
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Сан-Марино
SAN_MARINO_TRANSLATIONS = {
    'sk': {
        'universities': 'Sanmarínske Univerzity',
        'languageSchools': 'Sanmarínske Jazykové Školy',
        'vocationalSchools': 'Sanmarínske Stredné Odborné Školy',
        'conservatories': 'Sanmarínske Konzervatóriá',
        'foundationPrograms': 'Sanmarínske Prípravné Programy'
    },
    'cs': {
        'universities': 'Sanmarínské Univerzity',
        'languageSchools': 'Sanmarínské Jazykové Školy',
        'vocationalSchools': 'Sanmarínské Střední Odborné Školy',
        'conservatories': 'Sanmarínská Konzervatoře',
        'foundationPrograms': 'Sanmarínské Přípravné Programy'
    },
    'pl': {
        'universities': 'Sanmaryńskie Uniwersytety',
        'languageSchools': 'Sanmaryńskie Szkoły Językowe',
        'vocationalSchools': 'Sanmaryńskie Szkoły Zawodowe',
        'conservatories': 'Sanmaryńskie Konserwatoria',
        'foundationPrograms': 'Sanmaryńskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'San Marino Universities',
        'languageSchools': 'San Marino Language Schools',
        'vocationalSchools': 'San Marino Vocational Schools',
        'conservatories': 'San Marino Conservatories',
        'foundationPrograms': 'San Marino Foundation Programs'
    },
    'de': {
        'universities': 'San-marinesische Universitäten',
        'languageSchools': 'San-marinesische Sprachschulen',
        'vocationalSchools': 'San-marinesische Berufsschulen',
        'conservatories': 'San-marinesische Konservatorien',
        'foundationPrograms': 'San-marinesische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Санмаринські Університети',
        'languageSchools': 'Санмаринські Мовні Школи',
        'vocationalSchools': 'Санмаринські Професійні Школи',
        'conservatories': 'Санмаринські Консерваторії',
        'foundationPrograms': 'Санмаринські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Санмаринские Университеты',
        'languageSchools': 'Санмаринские Языковые Школы',
        'vocationalSchools': 'Санмаринские Профессиональные Школы',
        'conservatories': 'Санмаринские Консерватории',
        'foundationPrograms': 'Санмаринские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università di San Marino',
        'languageSchools': 'Scuole di Lingua di San Marino',
        'vocationalSchools': 'Scuole Professionali di San Marino',
        'conservatories': 'Conservatori di San Marino',
        'foundationPrograms': 'Programmi Preparatori di San Marino'
    },
    'fr': {
        'universities': 'Universités de Saint-Marin',
        'languageSchools': 'Écoles de Langue de Saint-Marin',
        'vocationalSchools': 'Écoles Professionnelles de Saint-Marin',
        'conservatories': 'Conservatoires de Saint-Marin',
        'foundationPrograms': 'Programmes Préparatoires de Saint-Marin'
    },
    'es': {
        'universities': 'Universidades de San Marino',
        'languageSchools': 'Escuelas de Idiomas de San Marino',
        'vocationalSchools': 'Escuelas Profesionales de San Marino',
        'conservatories': 'Conservatorios de San Marino',
        'foundationPrograms': 'Programas Preparatorios de San Marino'
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
        
        # Додати санмаринські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['SM'] = SAN_MARINO_TRANSLATIONS.get(lang_code, SAN_MARINO_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding San Marino jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll San Marino translations added!")

if __name__ == "__main__":
    main()
