"""
Додавання перекладів для юрисдикції Монако
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Монако
MONACO_TRANSLATIONS = {
    'sk': {
        'universities': 'Monacké Univerzity',
        'languageSchools': 'Monacké Jazykové Školy',
        'vocationalSchools': 'Monacké Stredné Odborné Školy',
        'conservatories': 'Monacké Konzervatóriá',
        'foundationPrograms': 'Monacké Prípravné Programy'
    },
    'cs': {
        'universities': 'Monacké Univerzity',
        'languageSchools': 'Monacké Jazykové Školy',
        'vocationalSchools': 'Monacké Střední Odborné Školy',
        'conservatories': 'Monacká Konzervatoře',
        'foundationPrograms': 'Monacké Přípravné Programy'
    },
    'pl': {
        'universities': 'Monakijskie Uniwersytety',
        'languageSchools': 'Monakijskie Szkoły Językowe',
        'vocationalSchools': 'Monakijskie Szkoły Zawodowe',
        'conservatories': 'Monakijskie Konserwatoria',
        'foundationPrograms': 'Monakijskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Monaco Universities',
        'languageSchools': 'Monaco Language Schools',
        'vocationalSchools': 'Monaco Vocational Schools',
        'conservatories': 'Monaco Conservatories',
        'foundationPrograms': 'Monaco Foundation Programs'
    },
    'de': {
        'universities': 'Monegassische Universitäten',
        'languageSchools': 'Monegassische Sprachschulen',
        'vocationalSchools': 'Monegassische Berufsschulen',
        'conservatories': 'Monegassische Konservatorien',
        'foundationPrograms': 'Monegassische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Монакські Університети',
        'languageSchools': 'Монакські Мовні Школи',
        'vocationalSchools': 'Монакські Професійні Школи',
        'conservatories': 'Монакські Консерваторії',
        'foundationPrograms': 'Монакські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Монакские Университеты',
        'languageSchools': 'Монакские Языковые Школы',
        'vocationalSchools': 'Монакские Профессиональные Школы',
        'conservatories': 'Монакские Консерватории',
        'foundationPrograms': 'Монакские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università di Monaco',
        'languageSchools': 'Scuole di Lingua di Monaco',
        'vocationalSchools': 'Scuole Professionali di Monaco',
        'conservatories': 'Conservatori di Monaco',
        'foundationPrograms': 'Programmi Preparatori di Monaco'
    },
    'fr': {
        'universities': 'Universités de Monaco',
        'languageSchools': 'Écoles de Langue de Monaco',
        'vocationalSchools': 'Écoles Professionnelles de Monaco',
        'conservatories': 'Conservatoires de Monaco',
        'foundationPrograms': 'Programmes Préparatoires de Monaco'
    },
    'es': {
        'universities': 'Universidades de Mónaco',
        'languageSchools': 'Escuelas de Idiomas de Mónaco',
        'vocationalSchools': 'Escuelas Profesionales de Mónaco',
        'conservatories': 'Conservatorios de Mónaco',
        'foundationPrograms': 'Programas Preparatorios de Mónaco'
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
        
        # Додати монакські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['MC'] = MONACO_TRANSLATIONS.get(lang_code, MONACO_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Monaco jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Monaco translations added!")

if __name__ == "__main__":
    main()
