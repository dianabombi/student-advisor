"""
Додавання перекладів для угорської юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Угорщини
HUNGARY_TRANSLATIONS = {
    'sk': {
        'universities': 'Maďarské Univerzity',
        'languageSchools': 'Maďarské Jazykové Školy',
        'vocationalSchools': 'Maďarské Stredné Odborné Školy',
        'conservatories': 'Maďarské Konzervatóriá',
        'foundationPrograms': 'Maďarské Prípravné Programy'
    },
    'cs': {
        'universities': 'Maďarské Univerzity',
        'languageSchools': 'Maďarské Jazykové Školy',
        'vocationalSchools': 'Maďarské Střední Odborné Školy',
        'conservatories': 'Maďarská Konzervatoře',
        'foundationPrograms': 'Maďarské Přípravné Programy'
    },
    'pl': {
        'universities': 'Węgierskie Uniwersytety',
        'languageSchools': 'Węgierskie Szkoły Językowe',
        'vocationalSchools': 'Węgierskie Szkoły Zawodowe',
        'conservatories': 'Węgierskie Konserwatoria',
        'foundationPrograms': 'Węgierskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Hungarian Universities',
        'languageSchools': 'Hungarian Language Schools',
        'vocationalSchools': 'Hungarian Vocational Schools',
        'conservatories': 'Hungarian Conservatories',
        'foundationPrograms': 'Hungarian Foundation Programs'
    },
    'de': {
        'universities': 'Ungarische Universitäten',
        'languageSchools': 'Ungarische Sprachschulen',
        'vocationalSchools': 'Ungarische Berufsschulen',
        'conservatories': 'Ungarische Konservatorien',
        'foundationPrograms': 'Ungarische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Угорські Університети',
        'languageSchools': 'Угорські Мовні Школи',
        'vocationalSchools': 'Угорські Професійні Школи',
        'conservatories': 'Угорські Консерваторії',
        'foundationPrograms': 'Угорські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Венгерские Университеты',
        'languageSchools': 'Венгерские Языковые Школы',
        'vocationalSchools': 'Венгерские Профессиональные Школы',
        'conservatories': 'Венгерские Консерватории',
        'foundationPrograms': 'Венгерские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Ungheresi',
        'languageSchools': 'Scuole di Lingua Ungheresi',
        'vocationalSchools': 'Scuole Professionali Ungheresi',
        'conservatories': 'Conservatori Ungheresi',
        'foundationPrograms': 'Programmi Preparatori Ungheresi'
    },
    'fr': {
        'universities': 'Universités Hongroises',
        'languageSchools': 'Écoles de Langue Hongroises',
        'vocationalSchools': 'Écoles Professionnelles Hongroises',
        'conservatories': 'Conservatoires Hongrois',
        'foundationPrograms': 'Programmes Préparatoires Hongrois'
    },
    'es': {
        'universities': 'Universidades Húngaras',
        'languageSchools': 'Escuelas de Idiomas Húngaras',
        'vocationalSchools': 'Escuelas Profesionales Húngaras',
        'conservatories': 'Conservatorios Húngaros',
        'foundationPrograms': 'Programas Preparatorios Húngaros'
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
        
        # Додати угорські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['HU'] = HUNGARY_TRANSLATIONS.get(lang_code, HUNGARY_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Hungarian jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Hungarian translations added!")

if __name__ == "__main__":
    main()
