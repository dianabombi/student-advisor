"""
Додавання перекладів для італійської юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Італії
ITALY_TRANSLATIONS = {
    'sk': {
        'universities': 'Talianske Univerzity',
        'languageSchools': 'Talianske Jazykové Školy',
        'vocationalSchools': 'Talianske Stredné Odborné Školy',
        'conservatories': 'Talianske Konzervatóriá',
        'foundationPrograms': 'Talianske Prípravné Programy'
    },
    'cs': {
        'universities': 'Italské Univerzity',
        'languageSchools': 'Italské Jazykové Školy',
        'vocationalSchools': 'Italské Střední Odborné Školy',
        'conservatories': 'Italská Konzervatoře',
        'foundationPrograms': 'Italské Přípravné Programy'
    },
    'pl': {
        'universities': 'Włoskie Uniwersytety',
        'languageSchools': 'Włoskie Szkoły Językowe',
        'vocationalSchools': 'Włoskie Szkoły Zawodowe',
        'conservatories': 'Włoskie Konserwatoria',
        'foundationPrograms': 'Włoskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Italian Universities',
        'languageSchools': 'Italian Language Schools',
        'vocationalSchools': 'Italian Vocational Schools',
        'conservatories': 'Italian Conservatories',
        'foundationPrograms': 'Italian Foundation Programs'
    },
    'de': {
        'universities': 'Italienische Universitäten',
        'languageSchools': 'Italienische Sprachschulen',
        'vocationalSchools': 'Italienische Berufsschulen',
        'conservatories': 'Italienische Konservatorien',
        'foundationPrograms': 'Italienische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Італійські Університети',
        'languageSchools': 'Італійські Мовні Школи',
        'vocationalSchools': 'Італійські Професійні Школи',
        'conservatories': 'Італійські Консерваторії',
        'foundationPrograms': 'Італійські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Итальянские Университеты',
        'languageSchools': 'Итальянские Языковые Школы',
        'vocationalSchools': 'Итальянские Профессиональные Школы',
        'conservatories': 'Итальянские Консерватории',
        'foundationPrograms': 'Итальянские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Italiane',
        'languageSchools': 'Scuole di Lingua Italiane',
        'vocationalSchools': 'Scuole Professionali Italiane',
        'conservatories': 'Conservatori Italiani',
        'foundationPrograms': 'Programmi Preparatori Italiani'
    },
    'fr': {
        'universities': 'Universités Italiennes',
        'languageSchools': 'Écoles de Langue Italiennes',
        'vocationalSchools': 'Écoles Professionnelles Italiennes',
        'conservatories': 'Conservatoires Italiens',
        'foundationPrograms': 'Programmes Préparatoires Italiens'
    },
    'es': {
        'universities': 'Universidades Italianas',
        'languageSchools': 'Escuelas de Idiomas Italianas',
        'vocationalSchools': 'Escuelas Profesionales Italianas',
        'conservatories': 'Conservatorios Italianos',
        'foundationPrograms': 'Programas Preparatorios Italianos'
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
        
        # Додати італійські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['IT'] = ITALY_TRANSLATIONS.get(lang_code, ITALY_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Italian jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Italian translations added!")

if __name__ == "__main__":
    main()
