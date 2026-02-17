"""
Додавання перекладів для юрисдикції Ватикану
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Ватикану
VATICAN_TRANSLATIONS = {
    'sk': {
        'universities': 'Vatikánske Univerzity',
        'languageSchools': 'Vatikánske Jazykové Školy',
        'vocationalSchools': 'Vatikánske Stredné Odborné Školy',
        'conservatories': 'Vatikánske Konzervatóriá',
        'foundationPrograms': 'Vatikánske Prípravné Programy'
    },
    'cs': {
        'universities': 'Vatikánské Univerzity',
        'languageSchools': 'Vatikánské Jazykové Školy',
        'vocationalSchools': 'Vatikánské Střední Odborné Školy',
        'conservatories': 'Vatikánská Konzervatoře',
        'foundationPrograms': 'Vatikánské Přípravné Programy'
    },
    'pl': {
        'universities': 'Watykańskie Uniwersytety',
        'languageSchools': 'Watykańskie Szkoły Językowe',
        'vocationalSchools': 'Watykańskie Szkoły Zawodowe',
        'conservatories': 'Watykańskie Konserwatoria',
        'foundationPrograms': 'Watykańskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Vatican Universities',
        'languageSchools': 'Vatican Language Schools',
        'vocationalSchools': 'Vatican Vocational Schools',
        'conservatories': 'Vatican Conservatories',
        'foundationPrograms': 'Vatican Foundation Programs'
    },
    'de': {
        'universities': 'Vatikanische Universitäten',
        'languageSchools': 'Vatikanische Sprachschulen',
        'vocationalSchools': 'Vatikanische Berufsschulen',
        'conservatories': 'Vatikanische Konservatorien',
        'foundationPrograms': 'Vatikanische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Ватиканські Університети',
        'languageSchools': 'Ватиканські Мовні Школи',
        'vocationalSchools': 'Ватиканські Професійні Школи',
        'conservatories': 'Ватиканські Консерваторії',
        'foundationPrograms': 'Ватиканські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Ватиканские Университеты',
        'languageSchools': 'Ватиканские Языковые Школы',
        'vocationalSchools': 'Ватиканские Профессиональные Школы',
        'conservatories': 'Ватиканские Консерватории',
        'foundationPrograms': 'Ватиканские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Vaticane',
        'languageSchools': 'Scuole di Lingua Vaticane',
        'vocationalSchools': 'Scuole Professionali Vaticane',
        'conservatories': 'Conservatori Vaticani',
        'foundationPrograms': 'Programmi Preparatori Vaticani'
    },
    'fr': {
        'universities': 'Universités du Vatican',
        'languageSchools': 'Écoles de Langue du Vatican',
        'vocationalSchools': 'Écoles Professionnelles du Vatican',
        'conservatories': 'Conservatoires du Vatican',
        'foundationPrograms': 'Programmes Préparatoires du Vatican'
    },
    'es': {
        'universities': 'Universidades Vaticanas',
        'languageSchools': 'Escuelas de Idiomas Vaticanas',
        'vocationalSchools': 'Escuelas Profesionales Vaticanas',
        'conservatories': 'Conservatorios Vaticanos',
        'foundationPrograms': 'Programas Preparatorios Vaticanos'
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
        
        # Додати ватиканські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['VA'] = VATICAN_TRANSLATIONS.get(lang_code, VATICAN_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Vatican jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Vatican translations added!")

if __name__ == "__main__":
    main()
