"""
Додавання перекладів для швейцарської юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Швейцарії
SWITZERLAND_TRANSLATIONS = {
    'sk': {
        'universities': 'Švajčiarske Univerzity',
        'languageSchools': 'Švajčiarske Jazykové Školy',
        'vocationalSchools': 'Švajčiarske Stredné Odborné Školy',
        'conservatories': 'Švajčiarske Konzervatóriá',
        'foundationPrograms': 'Švajčiarske Prípravné Programy'
    },
    'cs': {
        'universities': 'Švýcarské Univerzity',
        'languageSchools': 'Švýcarské Jazykové Školy',
        'vocationalSchools': 'Švýcarské Střední Odborné Školy',
        'conservatories': 'Švýcarská Konzervatoře',
        'foundationPrograms': 'Švýcarské Přípravné Programy'
    },
    'pl': {
        'universities': 'Szwajcarskie Uniwersytety',
        'languageSchools': 'Szwajcarskie Szkoły Językowe',
        'vocationalSchools': 'Szwajcarskie Szkoły Zawodowe',
        'conservatories': 'Szwajcarskie Konserwatoria',
        'foundationPrograms': 'Szwajcarskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Swiss Universities',
        'languageSchools': 'Swiss Language Schools',
        'vocationalSchools': 'Swiss Vocational Schools',
        'conservatories': 'Swiss Conservatories',
        'foundationPrograms': 'Swiss Foundation Programs'
    },
    'de': {
        'universities': 'Schweizer Universitäten',
        'languageSchools': 'Schweizer Sprachschulen',
        'vocationalSchools': 'Schweizer Berufsschulen',
        'conservatories': 'Schweizer Konservatorien',
        'foundationPrograms': 'Schweizer Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Швейцарські Університети',
        'languageSchools': 'Швейцарські Мовні Школи',
        'vocationalSchools': 'Швейцарські Професійні Школи',
        'conservatories': 'Швейцарські Консерваторії',
        'foundationPrograms': 'Швейцарські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Швейцарские Университеты',
        'languageSchools': 'Швейцарские Языковые Школы',
        'vocationalSchools': 'Швейцарские Профессиональные Школы',
        'conservatories': 'Швейцарские Консерватории',
        'foundationPrograms': 'Швейцарские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Svizzere',
        'languageSchools': 'Scuole di Lingua Svizzere',
        'vocationalSchools': 'Scuole Professionali Svizzere',
        'conservatories': 'Conservatori Svizzeri',
        'foundationPrograms': 'Programmi Preparatori Svizzeri'
    },
    'fr': {
        'universities': 'Universités Suisses',
        'languageSchools': 'Écoles de Langue Suisses',
        'vocationalSchools': 'Écoles Professionnelles Suisses',
        'conservatories': 'Conservatoires Suisses',
        'foundationPrograms': 'Programmes Préparatoires Suisses'
    },
    'es': {
        'universities': 'Universidades Suizas',
        'languageSchools': 'Escuelas de Idiomas Suizas',
        'vocationalSchools': 'Escuelas Profesionales Suizas',
        'conservatories': 'Conservatorios Suizos',
        'foundationPrograms': 'Programas Preparatorios Suizos'
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
        
        # Додати швейцарські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['CH'] = SWITZERLAND_TRANSLATIONS.get(lang_code, SWITZERLAND_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Swiss jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Swiss translations added!")

if __name__ == "__main__":
    main()
