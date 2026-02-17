"""
Додавання перекладів для австрійської юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Австрії
AUSTRIA_TRANSLATIONS = {
    'sk': {
        'universities': 'Rakúske Univerzity',
        'languageSchools': 'Rakúske Jazykové Školy',
        'vocationalSchools': 'Rakúske Stredné Odborné Školy',
        'conservatories': 'Rakúske Konzervatóriá',
        'foundationPrograms': 'Rakúske Prípravné Programy'
    },
    'cs': {
        'universities': 'Rakouské Univerzity',
        'languageSchools': 'Rakouské Jazykové Školy',
        'vocationalSchools': 'Rakouské Střední Odborné Školy',
        'conservatories': 'Rakouská Konzervatoře',
        'foundationPrograms': 'Rakouské Přípravné Programy'
    },
    'pl': {
        'universities': 'Austriackie Uniwersytety',
        'languageSchools': 'Austriackie Szkoły Językowe',
        'vocationalSchools': 'Austriackie Szkoły Zawodowe',
        'conservatories': 'Austriackie Konserwatoria',
        'foundationPrograms': 'Austriackie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Austrian Universities',
        'languageSchools': 'Austrian Language Schools',
        'vocationalSchools': 'Austrian Vocational Schools',
        'conservatories': 'Austrian Conservatories',
        'foundationPrograms': 'Austrian Foundation Programs'
    },
    'de': {
        'universities': 'Österreichische Universitäten',
        'languageSchools': 'Österreichische Sprachschulen',
        'vocationalSchools': 'Österreichische Berufsschulen',
        'conservatories': 'Österreichische Konservatorien',
        'foundationPrograms': 'Österreichische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Австрійські Університети',
        'languageSchools': 'Австрійські Мовні Школи',
        'vocationalSchools': 'Австрійські Професійні Школи',
        'conservatories': 'Австрійські Консерваторії',
        'foundationPrograms': 'Австрійські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Австрийские Университеты',
        'languageSchools': 'Австрийские Языковые Школы',
        'vocationalSchools': 'Австрийские Профессиональные Школы',
        'conservatories': 'Австрийские Консерватории',
        'foundationPrograms': 'Австрийские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Austriache',
        'languageSchools': 'Scuole di Lingua Austriache',
        'vocationalSchools': 'Scuole Professionali Austriache',
        'conservatories': 'Conservatori Austriaci',
        'foundationPrograms': 'Programmi Preparatori Austriaci'
    },
    'fr': {
        'universities': 'Universités Autrichiennes',
        'languageSchools': 'Écoles de Langue Autrichiennes',
        'vocationalSchools': 'Écoles Professionnelles Autrichiennes',
        'conservatories': 'Conservatoires Autrichiens',
        'foundationPrograms': 'Programmes Préparatoires Autrichiens'
    },
    'es': {
        'universities': 'Universidades Austriacas',
        'languageSchools': 'Escuelas de Idiomas Austriacas',
        'vocationalSchools': 'Escuelas Profesionales Austriacas',
        'conservatories': 'Conservatorios Austriacos',
        'foundationPrograms': 'Programas Preparatorios Austriacos'
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
        
        # Додати австрійські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['AT'] = AUSTRIA_TRANSLATIONS.get(lang_code, AUSTRIA_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Austrian jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Austrian translations added!")

if __name__ == "__main__":
    main()
