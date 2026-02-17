"""
Додавання перекладів для фінської юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Фінляндії
FINLAND_TRANSLATIONS = {
    'sk': {
        'universities': 'Fínske Univerzity',
        'languageSchools': 'Fínske Jazykové Školy',
        'vocationalSchools': 'Fínske Stredné Odborné Školy',
        'conservatories': 'Fínske Konzervatóriá',
        'foundationPrograms': 'Fínske Prípravné Programy'
    },
    'cs': {
        'universities': 'Finské Univerzity',
        'languageSchools': 'Finské Jazykové Školy',
        'vocationalSchools': 'Finské Střední Odborné Školy',
        'conservatories': 'Finská Konzervatoře',
        'foundationPrograms': 'Finské Přípravné Programy'
    },
    'pl': {
        'universities': 'Fińskie Uniwersytety',
        'languageSchools': 'Fińskie Szkoły Językowe',
        'vocationalSchools': 'Fińskie Szkoły Zawodowe',
        'conservatories': 'Fińskie Konserwatoria',
        'foundationPrograms': 'Fińskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Finnish Universities',
        'languageSchools': 'Finnish Language Schools',
        'vocationalSchools': 'Finnish Vocational Schools',
        'conservatories': 'Finnish Conservatories',
        'foundationPrograms': 'Finnish Foundation Programs'
    },
    'de': {
        'universities': 'Finnische Universitäten',
        'languageSchools': 'Finnische Sprachschulen',
        'vocationalSchools': 'Finnische Berufsschulen',
        'conservatories': 'Finnische Konservatorien',
        'foundationPrograms': 'Finnische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Фінські Університети',
        'languageSchools': 'Фінські Мовні Школи',
        'vocationalSchools': 'Фінські Професійні Школи',
        'conservatories': 'Фінські Консерваторії',
        'foundationPrograms': 'Фінські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Финские Университеты',
        'languageSchools': 'Финские Языковые Школы',
        'vocationalSchools': 'Финские Профессиональные Школы',
        'conservatories': 'Финские Консерватории',
        'foundationPrograms': 'Финские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Finlandesi',
        'languageSchools': 'Scuole di Lingua Finlandesi',
        'vocationalSchools': 'Scuole Professionali Finlandesi',
        'conservatories': 'Conservatori Finlandesi',
        'foundationPrograms': 'Programmi Preparatori Finlandesi'
    },
    'fr': {
        'universities': 'Universités Finlandaises',
        'languageSchools': 'Écoles de Langue Finlandaises',
        'vocationalSchools': 'Écoles Professionnelles Finlandaises',
        'conservatories': 'Conservatoires Finlandais',
        'foundationPrograms': 'Programmes Préparatoires Finlandais'
    },
    'es': {
        'universities': 'Universidades Finlandesas',
        'languageSchools': 'Escuelas de Idiomas Finlandesas',
        'vocationalSchools': 'Escuelas Profesionales Finlandesas',
        'conservatories': 'Conservatorios Finlandeses',
        'foundationPrograms': 'Programas Preparatorios Finlandeses'
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
        
        # Додати фінські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['FI'] = FINLAND_TRANSLATIONS.get(lang_code, FINLAND_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Finnish jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Finnish translations added!")

if __name__ == "__main__":
    main()
