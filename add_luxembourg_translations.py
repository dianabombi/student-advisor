"""
Додавання перекладів для люксембурзької юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Люксембургу
LUXEMBOURG_TRANSLATIONS = {
    'sk': {
        'universities': 'Luxemburské Univerzity',
        'languageSchools': 'Luxemburské Jazykové Školy',
        'vocationalSchools': 'Luxemburské Stredné Odborné Školy',
        'conservatories': 'Luxemburské Konzervatóriá',
        'foundationPrograms': 'Luxemburské Prípravné Programy'
    },
    'cs': {
        'universities': 'Lucemburské Univerzity',
        'languageSchools': 'Lucemburské Jazykové Školy',
        'vocationalSchools': 'Lucemburské Střední Odborné Školy',
        'conservatories': 'Lucemburská Konzervatoře',
        'foundationPrograms': 'Lucemburské Přípravné Programy'
    },
    'pl': {
        'universities': 'Luksemburskie Uniwersytety',
        'languageSchools': 'Luksemburskie Szkoły Językowe',
        'vocationalSchools': 'Luksemburskie Szkoły Zawodowe',
        'conservatories': 'Luksemburskie Konserwatoria',
        'foundationPrograms': 'Luksemburskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Luxembourg Universities',
        'languageSchools': 'Luxembourg Language Schools',
        'vocationalSchools': 'Luxembourg Vocational Schools',
        'conservatories': 'Luxembourg Conservatories',
        'foundationPrograms': 'Luxembourg Foundation Programs'
    },
    'de': {
        'universities': 'Luxemburgische Universitäten',
        'languageSchools': 'Luxemburgische Sprachschulen',
        'vocationalSchools': 'Luxemburgische Berufsschulen',
        'conservatories': 'Luxemburgische Konservatorien',
        'foundationPrograms': 'Luxemburgische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Люксембурзькі Університети',
        'languageSchools': 'Люксембурзькі Мовні Школи',
        'vocationalSchools': 'Люксембурзькі Професійні Школи',
        'conservatories': 'Люксембурзькі Консерваторії',
        'foundationPrograms': 'Люксембурзькі Підготовчі Програми'
    },
    'ru': {
        'universities': 'Люксембургские Университеты',
        'languageSchools': 'Люксембургские Языковые Школы',
        'vocationalSchools': 'Люксембургские Профессиональные Школы',
        'conservatories': 'Люксембургские Консерватории',
        'foundationPrograms': 'Люксембургские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Lussemburghesi',
        'languageSchools': 'Scuole di Lingua Lussemburghesi',
        'vocationalSchools': 'Scuole Professionali Lussemburghesi',
        'conservatories': 'Conservatori Lussemburghesi',
        'foundationPrograms': 'Programmi Preparatori Lussemburghesi'
    },
    'fr': {
        'universities': 'Universités Luxembourgeoises',
        'languageSchools': 'Écoles de Langue Luxembourgeoises',
        'vocationalSchools': 'Écoles Professionnelles Luxembourgeoises',
        'conservatories': 'Conservatoires Luxembourgeois',
        'foundationPrograms': 'Programmes Préparatoires Luxembourgeois'
    },
    'es': {
        'universities': 'Universidades Luxemburguesas',
        'languageSchools': 'Escuelas de Idiomas Luxemburguesas',
        'vocationalSchools': 'Escuelas Profesionales Luxemburguesas',
        'conservatories': 'Conservatorios Luxemburgueses',
        'foundationPrograms': 'Programas Preparatorios Luxemburgueses'
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
        
        # Додати люксембурзькі переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['LU'] = LUXEMBOURG_TRANSLATIONS.get(lang_code, LUXEMBOURG_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Luxembourg jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Luxembourg translations added!")

if __name__ == "__main__":
    main()
