"""
Додавання перекладів для британської юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Великої Британії
UK_TRANSLATIONS = {
    'sk': {
        'universities': 'Britské Univerzity',
        'languageSchools': 'Britské Jazykové Školy',
        'vocationalSchools': 'Britské Stredné Odborné Školy',
        'conservatories': 'Britské Konzervatóriá',
        'foundationPrograms': 'Britské Prípravné Programy'
    },
    'cs': {
        'universities': 'Britské Univerzity',
        'languageSchools': 'Britské Jazykové Školy',
        'vocationalSchools': 'Britské Střední Odborné Školy',
        'conservatories': 'Britská Konzervatoře',
        'foundationPrograms': 'Britské Přípravné Programy'
    },
    'pl': {
        'universities': 'Brytyjskie Uniwersytety',
        'languageSchools': 'Brytyjskie Szkoły Językowe',
        'vocationalSchools': 'Brytyjskie Szkoły Zawodowe',
        'conservatories': 'Brytyjskie Konserwatoria',
        'foundationPrograms': 'Brytyjskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'British Universities',
        'languageSchools': 'British Language Schools',
        'vocationalSchools': 'British Vocational Schools',
        'conservatories': 'British Conservatories',
        'foundationPrograms': 'British Foundation Programs'
    },
    'de': {
        'universities': 'Britische Universitäten',
        'languageSchools': 'Britische Sprachschulen',
        'vocationalSchools': 'Britische Berufsschulen',
        'conservatories': 'Britische Konservatorien',
        'foundationPrograms': 'Britische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Британські Університети',
        'languageSchools': 'Британські Мовні Школи',
        'vocationalSchools': 'Британські Професійні Школи',
        'conservatories': 'Британські Консерваторії',
        'foundationPrograms': 'Британські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Британские Университеты',
        'languageSchools': 'Британские Языковые Школы',
        'vocationalSchools': 'Британские Профессиональные Школы',
        'conservatories': 'Британские Консерватории',
        'foundationPrograms': 'Британские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Britanniche',
        'languageSchools': 'Scuole di Lingua Britanniche',
        'vocationalSchools': 'Scuole Professionali Britanniche',
        'conservatories': 'Conservatori Britannici',
        'foundationPrograms': 'Programmi Preparatori Britannici'
    },
    'fr': {
        'universities': 'Universités Britanniques',
        'languageSchools': 'Écoles de Langue Britanniques',
        'vocationalSchools': 'Écoles Professionnelles Britanniques',
        'conservatories': 'Conservatoires Britanniques',
        'foundationPrograms': 'Programmes Préparatoires Britanniques'
    },
    'es': {
        'universities': 'Universidades Británicas',
        'languageSchools': 'Escuelas de Idiomas Británicas',
        'vocationalSchools': 'Escuelas Profesionales Británicas',
        'conservatories': 'Conservatorios Británicos',
        'foundationPrograms': 'Programas Preparatorios Británicos'
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
        
        # Додати британські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['GB'] = UK_TRANSLATIONS.get(lang_code, UK_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding UK jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll UK translations added!")

if __name__ == "__main__":
    main()
