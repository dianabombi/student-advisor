"""
Додавання перекладів для ірландської юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Ірландії
IRELAND_TRANSLATIONS = {
    'sk': {
        'universities': 'Írske Univerzity',
        'languageSchools': 'Írske Jazykové Školy',
        'vocationalSchools': 'Írske Stredné Odborné Školy',
        'conservatories': 'Írske Konzervatóriá',
        'foundationPrograms': 'Írske Prípravné Programy'
    },
    'cs': {
        'universities': 'Irské Univerzity',
        'languageSchools': 'Irské Jazykové Školy',
        'vocationalSchools': 'Irské Střední Odborné Školy',
        'conservatories': 'Irská Konzervatoře',
        'foundationPrograms': 'Irské Přípravné Programy'
    },
    'pl': {
        'universities': 'Irlandzkie Uniwersytety',
        'languageSchools': 'Irlandzkie Szkoły Językowe',
        'vocationalSchools': 'Irlandzkie Szkoły Zawodowe',
        'conservatories': 'Irlandzkie Konserwatoria',
        'foundationPrograms': 'Irlandzkie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Irish Universities',
        'languageSchools': 'Irish Language Schools',
        'vocationalSchools': 'Irish Vocational Schools',
        'conservatories': 'Irish Conservatories',
        'foundationPrograms': 'Irish Foundation Programs'
    },
    'de': {
        'universities': 'Irische Universitäten',
        'languageSchools': 'Irische Sprachschulen',
        'vocationalSchools': 'Irische Berufsschulen',
        'conservatories': 'Irische Konservatorien',
        'foundationPrograms': 'Irische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Ірландські Університети',
        'languageSchools': 'Ірландські Мовні Школи',
        'vocationalSchools': 'Ірландські Професійні Школи',
        'conservatories': 'Ірландські Консерваторії',
        'foundationPrograms': 'Ірландські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Ирландские Университеты',
        'languageSchools': 'Ирландские Языковые Школы',
        'vocationalSchools': 'Ирландские Профессиональные Школы',
        'conservatories': 'Ирландские Консерватории',
        'foundationPrograms': 'Ирландские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Irlandesi',
        'languageSchools': 'Scuole di Lingua Irlandesi',
        'vocationalSchools': 'Scuole Professionali Irlandesi',
        'conservatories': 'Conservatori Irlandesi',
        'foundationPrograms': 'Programmi Preparatori Irlandesi'
    },
    'fr': {
        'universities': 'Universités Irlandaises',
        'languageSchools': 'Écoles de Langue Irlandaises',
        'vocationalSchools': 'Écoles Professionnelles Irlandaises',
        'conservatories': 'Conservatoires Irlandais',
        'foundationPrograms': 'Programmes Préparatoires Irlandais'
    },
    'es': {
        'universities': 'Universidades Irlandesas',
        'languageSchools': 'Escuelas de Idiomas Irlandesas',
        'vocationalSchools': 'Escuelas Profesionales Irlandesas',
        'conservatories': 'Conservatorios Irlandeses',
        'foundationPrograms': 'Programas Preparatorios Irlandeses'
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
        
        # Додати ірландські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['IE'] = IRELAND_TRANSLATIONS.get(lang_code, IRELAND_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Irish jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Irish translations added!")

if __name__ == "__main__":
    main()
