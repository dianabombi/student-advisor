"""
Додавання перекладів для данської юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Данії
DENMARK_TRANSLATIONS = {
    'sk': {
        'universities': 'Dánske Univerzity',
        'languageSchools': 'Dánske Jazykové Školy',
        'vocationalSchools': 'Dánske Stredné Odborné Školy',
        'conservatories': 'Dánske Konzervatóriá',
        'foundationPrograms': 'Dánske Prípravné Programy'
    },
    'cs': {
        'universities': 'Dánské Univerzity',
        'languageSchools': 'Dánské Jazykové Školy',
        'vocationalSchools': 'Dánské Střední Odborné Školy',
        'conservatories': 'Dánská Konzervatoře',
        'foundationPrograms': 'Dánské Přípravné Programy'
    },
    'pl': {
        'universities': 'Duńskie Uniwersytety',
        'languageSchools': 'Duńskie Szkoły Językowe',
        'vocationalSchools': 'Duńskie Szkoły Zawodowe',
        'conservatories': 'Duńskie Konserwatoria',
        'foundationPrograms': 'Duńskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Danish Universities',
        'languageSchools': 'Danish Language Schools',
        'vocationalSchools': 'Danish Vocational Schools',
        'conservatories': 'Danish Conservatories',
        'foundationPrograms': 'Danish Foundation Programs'
    },
    'de': {
        'universities': 'Dänische Universitäten',
        'languageSchools': 'Dänische Sprachschulen',
        'vocationalSchools': 'Dänische Berufsschulen',
        'conservatories': 'Dänische Konservatorien',
        'foundationPrograms': 'Dänische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Данські Університети',
        'languageSchools': 'Данські Мовні Школи',
        'vocationalSchools': 'Данські Професійні Школи',
        'conservatories': 'Данські Консерваторії',
        'foundationPrograms': 'Данські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Датские Университеты',
        'languageSchools': 'Датские Языковые Школы',
        'vocationalSchools': 'Датские Профессиональные Школы',
        'conservatories': 'Датские Консерватории',
        'foundationPrograms': 'Датские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Danesi',
        'languageSchools': 'Scuole di Lingua Danesi',
        'vocationalSchools': 'Scuole Professionali Danesi',
        'conservatories': 'Conservatori Danesi',
        'foundationPrograms': 'Programmi Preparatori Danesi'
    },
    'fr': {
        'universities': 'Universités Danoises',
        'languageSchools': 'Écoles de Langue Danoises',
        'vocationalSchools': 'Écoles Professionnelles Danoises',
        'conservatories': 'Conservatoires Danois',
        'foundationPrograms': 'Programmes Préparatoires Danois'
    },
    'es': {
        'universities': 'Universidades Danesas',
        'languageSchools': 'Escuelas de Idiomas Danesas',
        'vocationalSchools': 'Escuelas Profesionales Danesas',
        'conservatories': 'Conservatorios Daneses',
        'foundationPrograms': 'Programas Preparatorios Daneses'
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
        
        # Додати данські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['DK'] = DENMARK_TRANSLATIONS.get(lang_code, DENMARK_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Danish jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Danish translations added!")

if __name__ == "__main__":
    main()
