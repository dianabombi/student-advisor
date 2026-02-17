"""
Додавання перекладів для норвезької юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Норвегії
NORWAY_TRANSLATIONS = {
    'sk': {
        'universities': 'Nórske Univerzity',
        'languageSchools': 'Nórske Jazykové Školy',
        'vocationalSchools': 'Nórske Stredné Odborné Školy',
        'conservatories': 'Nórske Konzervatóriá',
        'foundationPrograms': 'Nórske Prípravné Programy'
    },
    'cs': {
        'universities': 'Norské Univerzity',
        'languageSchools': 'Norské Jazykové Školy',
        'vocationalSchools': 'Norské Střední Odborné Školy',
        'conservatories': 'Norská Konzervatoře',
        'foundationPrograms': 'Norské Přípravné Programy'
    },
    'pl': {
        'universities': 'Norweskie Uniwersytety',
        'languageSchools': 'Norweskie Szkoły Językowe',
        'vocationalSchools': 'Norweskie Szkoły Zawodowe',
        'conservatories': 'Norweskie Konserwatoria',
        'foundationPrograms': 'Norweskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Norwegian Universities',
        'languageSchools': 'Norwegian Language Schools',
        'vocationalSchools': 'Norwegian Vocational Schools',
        'conservatories': 'Norwegian Conservatories',
        'foundationPrograms': 'Norwegian Foundation Programs'
    },
    'de': {
        'universities': 'Norwegische Universitäten',
        'languageSchools': 'Norwegische Sprachschulen',
        'vocationalSchools': 'Norwegische Berufsschulen',
        'conservatories': 'Norwegische Konservatorien',
        'foundationPrograms': 'Norwegische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Норвезькі Університети',
        'languageSchools': 'Норвезькі Мовні Школи',
        'vocationalSchools': 'Норвезькі Професійні Школи',
        'conservatories': 'Норвезькі Консерваторії',
        'foundationPrograms': 'Норвезькі Підготовчі Програми'
    },
    'ru': {
        'universities': 'Норвежские Университеты',
        'languageSchools': 'Норвежские Языковые Школы',
        'vocationalSchools': 'Норвежские Профессиональные Школы',
        'conservatories': 'Норвежские Консерватории',
        'foundationPrograms': 'Норвежские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Norvegesi',
        'languageSchools': 'Scuole di Lingua Norvegesi',
        'vocationalSchools': 'Scuole Professionali Norvegesi',
        'conservatories': 'Conservatori Norvegesi',
        'foundationPrograms': 'Programmi Preparatori Norvegesi'
    },
    'fr': {
        'universities': 'Universités Norvégiennes',
        'languageSchools': 'Écoles de Langue Norvégiennes',
        'vocationalSchools': 'Écoles Professionnelles Norvégiennes',
        'conservatories': 'Conservatoires Norvégiens',
        'foundationPrograms': 'Programmes Préparatoires Norvégiens'
    },
    'es': {
        'universities': 'Universidades Noruegas',
        'languageSchools': 'Escuelas de Idiomas Noruegas',
        'vocationalSchools': 'Escuelas Profesionales Noruegas',
        'conservatories': 'Conservatorios Noruegos',
        'foundationPrograms': 'Programas Preparatorios Noruegos'
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
        
        # Додати норвезькі переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['NO'] = NORWAY_TRANSLATIONS.get(lang_code, NORWAY_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Norwegian jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Norwegian translations added!")

if __name__ == "__main__":
    main()
