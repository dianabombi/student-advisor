"""
Додавання перекладів для ліхтенштейнської юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Ліхтенштейну
LIECHTENSTEIN_TRANSLATIONS = {
    'sk': {
        'universities': 'Lichtenštajnské Univerzity',
        'languageSchools': 'Lichtenštajnské Jazykové Školy',
        'vocationalSchools': 'Lichtenštajnské Stredné Odborné Školy',
        'conservatories': 'Lichtenštajnské Konzervatóriá',
        'foundationPrograms': 'Lichtenštajnské Prípravné Programy'
    },
    'cs': {
        'universities': 'Lichtenštejnské Univerzity',
        'languageSchools': 'Lichtenštejnské Jazykové Školy',
        'vocationalSchools': 'Lichtenštejnské Střední Odborné Školy',
        'conservatories': 'Lichtenštejnská Konzervatoře',
        'foundationPrograms': 'Lichtenštejnské Přípravné Programy'
    },
    'pl': {
        'universities': 'Liechtensteińskie Uniwersytety',
        'languageSchools': 'Liechtensteińskie Szkoły Językowe',
        'vocationalSchools': 'Liechtensteińskie Szkoły Zawodowe',
        'conservatories': 'Liechtensteińskie Konserwatoria',
        'foundationPrograms': 'Liechtensteińskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Liechtenstein Universities',
        'languageSchools': 'Liechtenstein Language Schools',
        'vocationalSchools': 'Liechtenstein Vocational Schools',
        'conservatories': 'Liechtenstein Conservatories',
        'foundationPrograms': 'Liechtenstein Foundation Programs'
    },
    'de': {
        'universities': 'Liechtensteinische Universitäten',
        'languageSchools': 'Liechtensteinische Sprachschulen',
        'vocationalSchools': 'Liechtensteinische Berufsschulen',
        'conservatories': 'Liechtensteinische Konservatorien',
        'foundationPrograms': 'Liechtensteinische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Ліхтенштейнські Університети',
        'languageSchools': 'Ліхтенштейнські Мовні Школи',
        'vocationalSchools': 'Ліхтенштейнські Професійні Школи',
        'conservatories': 'Ліхтенштейнські Консерваторії',
        'foundationPrograms': 'Ліхтенштейнські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Лихтенштейнские Университеты',
        'languageSchools': 'Лихтенштейнские Языковые Школы',
        'vocationalSchools': 'Лихтенштейнские Профессиональные Школы',
        'conservatories': 'Лихтенштейнские Консерватории',
        'foundationPrograms': 'Лихтенштейнские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università del Liechtenstein',
        'languageSchools': 'Scuole di Lingua del Liechtenstein',
        'vocationalSchools': 'Scuole Professionali del Liechtenstein',
        'conservatories': 'Conservatori del Liechtenstein',
        'foundationPrograms': 'Programmi Preparatori del Liechtenstein'
    },
    'fr': {
        'universities': 'Universités du Liechtenstein',
        'languageSchools': 'Écoles de Langue du Liechtenstein',
        'vocationalSchools': 'Écoles Professionnelles du Liechtenstein',
        'conservatories': 'Conservatoires du Liechtenstein',
        'foundationPrograms': 'Programmes Préparatoires du Liechtenstein'
    },
    'es': {
        'universities': 'Universidades de Liechtenstein',
        'languageSchools': 'Escuelas de Idiomas de Liechtenstein',
        'vocationalSchools': 'Escuelas Profesionales de Liechtenstein',
        'conservatories': 'Conservatorios de Liechtenstein',
        'foundationPrograms': 'Programas Preparatorios de Liechtenstein'
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
        
        # Додати ліхтенштейнські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['LI'] = LIECHTENSTEIN_TRANSLATIONS.get(lang_code, LIECHTENSTEIN_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Liechtenstein jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Liechtenstein translations added!")

if __name__ == "__main__":
    main()
