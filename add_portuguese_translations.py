"""
Додавання перекладів для португальської юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Португалії
PORTUGAL_TRANSLATIONS = {
    'sk': {
        'universities': 'Portugalské Univerzity',
        'languageSchools': 'Portugalské Jazykové Školy',
        'vocationalSchools': 'Portugalské Stredné Odborné Školy',
        'conservatories': 'Portugalské Konzervatóriá',
        'foundationPrograms': 'Portugalské Prípravné Programy'
    },
    'cs': {
        'universities': 'Portugalské Univerzity',
        'languageSchools': 'Portugalské Jazykové Školy',
        'vocationalSchools': 'Portugalské Střední Odborné Školy',
        'conservatories': 'Portugalská Konzervatoře',
        'foundationPrograms': 'Portugalské Přípravné Programy'
    },
    'pl': {
        'universities': 'Portugalskie Uniwersytety',
        'languageSchools': 'Portugalskie Szkoły Językowe',
        'vocationalSchools': 'Portugalskie Szkoły Zawodowe',
        'conservatories': 'Portugalskie Konserwatoria',
        'foundationPrograms': 'Portugalskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Portuguese Universities',
        'languageSchools': 'Portuguese Language Schools',
        'vocationalSchools': 'Portuguese Vocational Schools',
        'conservatories': 'Portuguese Conservatories',
        'foundationPrograms': 'Portuguese Foundation Programs'
    },
    'de': {
        'universities': 'Portugiesische Universitäten',
        'languageSchools': 'Portugiesische Sprachschulen',
        'vocationalSchools': 'Portugiesische Berufsschulen',
        'conservatories': 'Portugiesische Konservatorien',
        'foundationPrograms': 'Portugiesische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Португальські Університети',
        'languageSchools': 'Португальські Мовні Школи',
        'vocationalSchools': 'Португальські Професійні Школи',
        'conservatories': 'Португальські Консерваторії',
        'foundationPrograms': 'Португальські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Португальские Университеты',
        'languageSchools': 'Португальские Языковые Школы',
        'vocationalSchools': 'Португальские Профессиональные Школы',
        'conservatories': 'Португальские Консерватории',
        'foundationPrograms': 'Португальские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Portoghesi',
        'languageSchools': 'Scuole di Lingua Portoghesi',
        'vocationalSchools': 'Scuole Professionali Portoghesi',
        'conservatories': 'Conservatori Portoghesi',
        'foundationPrograms': 'Programmi Preparatori Portoghesi'
    },
    'fr': {
        'universities': 'Universités Portugaises',
        'languageSchools': 'Écoles de Langue Portugaises',
        'vocationalSchools': 'Écoles Professionnelles Portugaises',
        'conservatories': 'Conservatoires Portugais',
        'foundationPrograms': 'Programmes Préparatoires Portugais'
    },
    'es': {
        'universities': 'Universidades Portuguesas',
        'languageSchools': 'Escuelas de Idiomas Portuguesas',
        'vocationalSchools': 'Escuelas Profesionales Portuguesas',
        'conservatories': 'Conservatorios Portugueses',
        'foundationPrograms': 'Programas Preparatorios Portugueses'
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
        
        # Додати португальські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['PT'] = PORTUGAL_TRANSLATIONS.get(lang_code, PORTUGAL_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Portuguese jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Portuguese translations added!")

if __name__ == "__main__":
    main()
