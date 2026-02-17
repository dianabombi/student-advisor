"""
Додавання перекладів для юрисдикції Хорватії
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Хорватії
CROATIA_TRANSLATIONS = {
    'sk': {
        'universities': 'Chorvátske Univerzity',
        'languageSchools': 'Chorvátske Jazykové Školy',
        'vocationalSchools': 'Chorvátske Stredné Odborné Školy',
        'conservatories': 'Chorvátske Konzervatóriá',
        'foundationPrograms': 'Chorvátske Prípravné Programy'
    },
    'cs': {
        'universities': 'Chorvatské Univerzity',
        'languageSchools': 'Chorvatské Jazykové Školy',
        'vocationalSchools': 'Chorvatské Střední Odborné Školy',
        'conservatories': 'Chorvatská Konzervatoře',
        'foundationPrograms': 'Chorvatské Přípravné Programy'
    },
    'pl': {
        'universities': 'Chorwackie Uniwersytety',
        'languageSchools': 'Chorwackie Szkoły Językowe',
        'vocationalSchools': 'Chorwackie Szkoły Zawodowe',
        'conservatories': 'Chorwackie Konserwatoria',
        'foundationPrograms': 'Chorwackie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Croatian Universities',
        'languageSchools': 'Croatian Language Schools',
        'vocationalSchools': 'Croatian Vocational Schools',
        'conservatories': 'Croatian Conservatories',
        'foundationPrograms': 'Croatian Foundation Programs'
    },
    'de': {
        'universities': 'Kroatische Universitäten',
        'languageSchools': 'Kroatische Sprachschulen',
        'vocationalSchools': 'Kroatische Berufsschulen',
        'conservatories': 'Kroatische Konservatorien',
        'foundationPrograms': 'Kroatische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Хорватські Університети',
        'languageSchools': 'Хорватські Мовні Школи',
        'vocationalSchools': 'Хорватські Професійні Школи',
        'conservatories': 'Хорватські Консерваторії',
        'foundationPrograms': 'Хорватські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Хорватские Университеты',
        'languageSchools': 'Хорватские Языковые Школы',
        'vocationalSchools': 'Хорватские Профессиональные Школы',
        'conservatories': 'Хорватские Консерватории',
        'foundationPrograms': 'Хорватские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Croate',
        'languageSchools': 'Scuole di Lingua Croate',
        'vocationalSchools': 'Scuole Professionali Croate',
        'conservatories': 'Conservatori Croati',
        'foundationPrograms': 'Programmi Preparatori Croati'
    },
    'fr': {
        'universities': 'Universités Croates',
        'languageSchools': 'Écoles de Langue Croates',
        'vocationalSchools': 'Écoles Professionnelles Croates',
        'conservatories': 'Conservatoires Croates',
        'foundationPrograms': 'Programmes Préparatoires Croates'
    },
    'es': {
        'universities': 'Universidades Croatas',
        'languageSchools': 'Escuelas de Idiomas Croatas',
        'vocationalSchools': 'Escuelas Profesionales Croatas',
        'conservatories': 'Conservatorios Croatas',
        'foundationPrograms': 'Programas Preparatorios Croatas'
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
        
        # Додати хорватські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['HR'] = CROATIA_TRANSLATIONS.get(lang_code, CROATIA_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Croatia jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Croatia translations added!")

if __name__ == "__main__":
    main()
