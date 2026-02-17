"""
Додавання перекладів для нідерландської юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Нідерландів
NETHERLANDS_TRANSLATIONS = {
    'sk': {
        'universities': 'Holandské Univerzity',
        'languageSchools': 'Holandské Jazykové Školy',
        'vocationalSchools': 'Holandské Stredné Odborné Školy',
        'conservatories': 'Holandské Konzervatóriá',
        'foundationPrograms': 'Holandské Prípravné Programy'
    },
    'cs': {
        'universities': 'Nizozemské Univerzity',
        'languageSchools': 'Nizozemské Jazykové Školy',
        'vocationalSchools': 'Nizozemské Střední Odborné Školy',
        'conservatories': 'Nizozemská Konzervatoře',
        'foundationPrograms': 'Nizozemské Přípravné Programy'
    },
    'pl': {
        'universities': 'Holenderskie Uniwersytety',
        'languageSchools': 'Holenderskie Szkoły Językowe',
        'vocationalSchools': 'Holenderskie Szkoły Zawodowe',
        'conservatories': 'Holenderskie Konserwatoria',
        'foundationPrograms': 'Holenderskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Dutch Universities',
        'languageSchools': 'Dutch Language Schools',
        'vocationalSchools': 'Dutch Vocational Schools',
        'conservatories': 'Dutch Conservatories',
        'foundationPrograms': 'Dutch Foundation Programs'
    },
    'de': {
        'universities': 'Niederländische Universitäten',
        'languageSchools': 'Niederländische Sprachschulen',
        'vocationalSchools': 'Niederländische Berufsschulen',
        'conservatories': 'Niederländische Konservatorien',
        'foundationPrograms': 'Niederländische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Нідерландські Університети',
        'languageSchools': 'Нідерландські Мовні Школи',
        'vocationalSchools': 'Нідерландські Професійні Школи',
        'conservatories': 'Нідерландські Консерваторії',
        'foundationPrograms': 'Нідерландські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Нидерландские Университеты',
        'languageSchools': 'Нидерландские Языковые Школы',
        'vocationalSchools': 'Нидерландские Профессиональные Школы',
        'conservatories': 'Нидерландские Консерватории',
        'foundationPrograms': 'Нидерландские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Olandesi',
        'languageSchools': 'Scuole di Lingua Olandesi',
        'vocationalSchools': 'Scuole Professionali Olandesi',
        'conservatories': 'Conservatori Olandesi',
        'foundationPrograms': 'Programmi Preparatori Olandesi'
    },
    'fr': {
        'universities': 'Universités Néerlandaises',
        'languageSchools': 'Écoles de Langue Néerlandaises',
        'vocationalSchools': 'Écoles Professionnelles Néerlandaises',
        'conservatories': 'Conservatoires Néerlandais',
        'foundationPrograms': 'Programmes Préparatoires Néerlandais'
    },
    'es': {
        'universities': 'Universidades Holandesas',
        'languageSchools': 'Escuelas de Idiomas Holandesas',
        'vocationalSchools': 'Escuelas Profesionales Holandesas',
        'conservatories': 'Conservatorios Holandeses',
        'foundationPrograms': 'Programas Preparatorios Holandeses'
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
        
        # Додати нідерландські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['NL'] = NETHERLANDS_TRANSLATIONS.get(lang_code, NETHERLANDS_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Dutch jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Dutch translations added!")

if __name__ == "__main__":
    main()
