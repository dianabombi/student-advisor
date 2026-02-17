"""
Додавання перекладів для шведської юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Швеції
SWEDEN_TRANSLATIONS = {
    'sk': {
        'universities': 'Švédske Univerzity',
        'languageSchools': 'Švédske Jazykové Školy',
        'vocationalSchools': 'Švédske Stredné Odborné Školy',
        'conservatories': 'Švédske Konzervatóriá',
        'foundationPrograms': 'Švédske Prípravné Programy'
    },
    'cs': {
        'universities': 'Švédské Univerzity',
        'languageSchools': 'Švédské Jazykové Školy',
        'vocationalSchools': 'Švédské Střední Odborné Školy',
        'conservatories': 'Švédská Konzervatoře',
        'foundationPrograms': 'Švédské Přípravné Programy'
    },
    'pl': {
        'universities': 'Szwedzkie Uniwersytety',
        'languageSchools': 'Szwedzkie Szkoły Językowe',
        'vocationalSchools': 'Szwedzkie Szkoły Zawodowe',
        'conservatories': 'Szwedzkie Konserwatoria',
        'foundationPrograms': 'Szwedzkie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Swedish Universities',
        'languageSchools': 'Swedish Language Schools',
        'vocationalSchools': 'Swedish Vocational Schools',
        'conservatories': 'Swedish Conservatories',
        'foundationPrograms': 'Swedish Foundation Programs'
    },
    'de': {
        'universities': 'Schwedische Universitäten',
        'languageSchools': 'Schwedische Sprachschulen',
        'vocationalSchools': 'Schwedische Berufsschulen',
        'conservatories': 'Schwedische Konservatorien',
        'foundationPrograms': 'Schwedische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Шведські Університети',
        'languageSchools': 'Шведські Мовні Школи',
        'vocationalSchools': 'Шведські Професійні Школи',
        'conservatories': 'Шведські Консерваторії',
        'foundationPrograms': 'Шведські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Шведские Университеты',
        'languageSchools': 'Шведские Языковые Школы',
        'vocationalSchools': 'Шведские Профессиональные Школы',
        'conservatories': 'Шведские Консерватории',
        'foundationPrograms': 'Шведские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Svedesi',
        'languageSchools': 'Scuole di Lingua Svedesi',
        'vocationalSchools': 'Scuole Professionali Svedesi',
        'conservatories': 'Conservatori Svedesi',
        'foundationPrograms': 'Programmi Preparatori Svedesi'
    },
    'fr': {
        'universities': 'Universités Suédoises',
        'languageSchools': 'Écoles de Langue Suédoises',
        'vocationalSchools': 'Écoles Professionnelles Suédoises',
        'conservatories': 'Conservatoires Suédois',
        'foundationPrograms': 'Programmes Préparatoires Suédois'
    },
    'es': {
        'universities': 'Universidades Suecas',
        'languageSchools': 'Escuelas de Idiomas Suecas',
        'vocationalSchools': 'Escuelas Profesionales Suecas',
        'conservatories': 'Conservatorios Suecos',
        'foundationPrograms': 'Programas Preparatorios Suecos'
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
        
        # Додати шведські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['SE'] = SWEDEN_TRANSLATIONS.get(lang_code, SWEDEN_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Swedish jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Swedish translations added!")

if __name__ == "__main__":
    main()
