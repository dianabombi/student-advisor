"""
Додавання перекладів для юрисдикції Словенії
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Словенії
SLOVENIA_TRANSLATIONS = {
    'sk': {
        'universities': 'Slovinské Univerzity',
        'languageSchools': 'Slovinské Jazykové Školy',
        'vocationalSchools': 'Slovinské Stredné Odborné Školy',
        'conservatories': 'Slovinské Konzervatóriá',
        'foundationPrograms': 'Slovinské Prípravné Programy'
    },
    'cs': {
        'universities': 'Slovinské Univerzity',
        'languageSchools': 'Slovinské Jazykové Školy',
        'vocationalSchools': 'Slovinské Střední Odborné Školy',
        'conservatories': 'Slovinská Konzervatoře',
        'foundationPrograms': 'Slovinské Přípravné Programy'
    },
    'pl': {
        'universities': 'Słoweńskie Uniwersytety',
        'languageSchools': 'Słoweńskie Szkoły Językowe',
        'vocationalSchools': 'Słoweńskie Szkoły Zawodowe',
        'conservatories': 'Słoweńskie Konserwatoria',
        'foundationPrograms': 'Słoweńskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Slovenian Universities',
        'languageSchools': 'Slovenian Language Schools',
        'vocationalSchools': 'Slovenian Vocational Schools',
        'conservatories': 'Slovenian Conservatories',
        'foundationPrograms': 'Slovenian Foundation Programs'
    },
    'de': {
        'universities': 'Slowenische Universitäten',
        'languageSchools': 'Slowenische Sprachschulen',
        'vocationalSchools': 'Slowenische Berufsschulen',
        'conservatories': 'Slowenische Konservatorien',
        'foundationPrograms': 'Slowenische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Словенські Університети',
        'languageSchools': 'Словенські Мовні Школи',
        'vocationalSchools': 'Словенські Професійні Школи',
        'conservatories': 'Словенські Консерваторії',
        'foundationPrograms': 'Словенські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Словенские Университеты',
        'languageSchools': 'Словенские Языковые Школы',
        'vocationalSchools': 'Словенские Профессиональные Школы',
        'conservatories': 'Словенские Консерватории',
        'foundationPrograms': 'Словенские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Slovene',
        'languageSchools': 'Scuole di Lingua Slovene',
        'vocationalSchools': 'Scuole Professionali Slovene',
        'conservatories': 'Conservatori Sloveni',
        'foundationPrograms': 'Programmi Preparatori Sloveni'
    },
    'fr': {
        'universities': 'Universités Slovènes',
        'languageSchools': 'Écoles de Langue Slovènes',
        'vocationalSchools': 'Écoles Professionnelles Slovènes',
        'conservatories': 'Conservatoires Slovènes',
        'foundationPrograms': 'Programmes Préparatoires Slovènes'
    },
    'es': {
        'universities': 'Universidades Eslovenas',
        'languageSchools': 'Escuelas de Idiomas Eslovenas',
        'vocationalSchools': 'Escuelas Profesionales Eslovenas',
        'conservatories': 'Conservatorios Eslovenos',
        'foundationPrograms': 'Programas Preparatorios Eslovenos'
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
        
        # Додати словенські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['SI'] = SLOVENIA_TRANSLATIONS.get(lang_code, SLOVENIA_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Slovenia jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Slovenia translations added!")

if __name__ == "__main__":
    main()
