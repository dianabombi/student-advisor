"""
Додавання перекладів для юрисдикції Андорри
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Андорри
ANDORRA_TRANSLATIONS = {
    'sk': {
        'universities': 'Andorrské Univerzity',
        'languageSchools': 'Andorrské Jazykové Školy',
        'vocationalSchools': 'Andorrské Stredné Odborné Školy',
        'conservatories': 'Andorrské Konzervatóriá',
        'foundationPrograms': 'Andorrské Prípravné Programy'
    },
    'cs': {
        'universities': 'Andorrské Univerzity',
        'languageSchools': 'Andorrské Jazykové Školy',
        'vocationalSchools': 'Andorrské Střední Odborné Školy',
        'conservatories': 'Andorrská Konzervatoře',
        'foundationPrograms': 'Andorrské Přípravné Programy'
    },
    'pl': {
        'universities': 'Andorskie Uniwersytety',
        'languageSchools': 'Andorskie Szkoły Językowe',
        'vocationalSchools': 'Andorskie Szkoły Zawodowe',
        'conservatories': 'Andorskie Konserwatoria',
        'foundationPrograms': 'Andorskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Andorran Universities',
        'languageSchools': 'Andorran Language Schools',
        'vocationalSchools': 'Andorran Vocational Schools',
        'conservatories': 'Andorran Conservatories',
        'foundationPrograms': 'Andorran Foundation Programs'
    },
    'de': {
        'universities': 'Andorranische Universitäten',
        'languageSchools': 'Andorranische Sprachschulen',
        'vocationalSchools': 'Andorranische Berufsschulen',
        'conservatories': 'Andorranische Konservatorien',
        'foundationPrograms': 'Andorranische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Андоррські Університети',
        'languageSchools': 'Андоррські Мовні Школи',
        'vocationalSchools': 'Андоррські Професійні Школи',
        'conservatories': 'Андоррські Консерваторії',
        'foundationPrograms': 'Андоррські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Андоррские Университеты',
        'languageSchools': 'Андоррские Языковые Школы',
        'vocationalSchools': 'Андоррские Профессиональные Школы',
        'conservatories': 'Андоррские Консерватории',
        'foundationPrograms': 'Андоррские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università di Andorra',
        'languageSchools': 'Scuole di Lingua di Andorra',
        'vocationalSchools': 'Scuole Professionali di Andorra',
        'conservatories': 'Conservatori di Andorra',
        'foundationPrograms': 'Programmi Preparatori di Andorra'
    },
    'fr': {
        'universities': 'Universités d\'Andorre',
        'languageSchools': 'Écoles de Langue d\'Andorre',
        'vocationalSchools': 'Écoles Professionnelles d\'Andorre',
        'conservatories': 'Conservatoires d\'Andorre',
        'foundationPrograms': 'Programmes Préparatoires d\'Andorre'
    },
    'es': {
        'universities': 'Universidades de Andorra',
        'languageSchools': 'Escuelas de Idiomas de Andorra',
        'vocationalSchools': 'Escuelas Profesionales de Andorra',
        'conservatories': 'Conservatorios de Andorra',
        'foundationPrograms': 'Programas Preparatorios de Andorra'
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
        
        # Додати андоррські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['AD'] = ANDORRA_TRANSLATIONS.get(lang_code, ANDORRA_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Andorra jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Andorra translations added!")

if __name__ == "__main__":
    main()
