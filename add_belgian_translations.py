"""
Додавання перекладів для бельгійської юрисдикції
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для Бельгії
BELGIUM_TRANSLATIONS = {
    'sk': {
        'universities': 'Belgické Univerzity',
        'languageSchools': 'Belgické Jazykové Školy',
        'vocationalSchools': 'Belgické Stredné Odborné Školy',
        'conservatories': 'Belgické Konzervatóriá',
        'foundationPrograms': 'Belgické Prípravné Programy'
    },
    'cs': {
        'universities': 'Belgické Univerzity',
        'languageSchools': 'Belgické Jazykové Školy',
        'vocationalSchools': 'Belgické Střední Odborné Školy',
        'conservatories': 'Belgická Konzervatoře',
        'foundationPrograms': 'Belgické Přípravné Programy'
    },
    'pl': {
        'universities': 'Belgijskie Uniwersytety',
        'languageSchools': 'Belgijskie Szkoły Językowe',
        'vocationalSchools': 'Belgijskie Szkoły Zawodowe',
        'conservatories': 'Belgijskie Konserwatoria',
        'foundationPrograms': 'Belgijskie Programy Przygotowawcze'
    },
    'en': {
        'universities': 'Belgian Universities',
        'languageSchools': 'Belgian Language Schools',
        'vocationalSchools': 'Belgian Vocational Schools',
        'conservatories': 'Belgian Conservatories',
        'foundationPrograms': 'Belgian Foundation Programs'
    },
    'de': {
        'universities': 'Belgische Universitäten',
        'languageSchools': 'Belgische Sprachschulen',
        'vocationalSchools': 'Belgische Berufsschulen',
        'conservatories': 'Belgische Konservatorien',
        'foundationPrograms': 'Belgische Vorbereitungsprogramme'
    },
    'uk': {
        'universities': 'Бельгійські Університети',
        'languageSchools': 'Бельгійські Мовні Школи',
        'vocationalSchools': 'Бельгійські Професійні Школи',
        'conservatories': 'Бельгійські Консерваторії',
        'foundationPrograms': 'Бельгійські Підготовчі Програми'
    },
    'ru': {
        'universities': 'Бельгийские Университеты',
        'languageSchools': 'Бельгийские Языковые Школы',
        'vocationalSchools': 'Бельгийские Профессиональные Школы',
        'conservatories': 'Бельгийские Консерватории',
        'foundationPrograms': 'Бельгийские Подготовительные Программы'
    },
    'it': {
        'universities': 'Università Belghe',
        'languageSchools': 'Scuole di Lingua Belghe',
        'vocationalSchools': 'Scuole Professionali Belghe',
        'conservatories': 'Conservatori Belgi',
        'foundationPrograms': 'Programmi Preparatori Belgi'
    },
    'fr': {
        'universities': 'Universités Belges',
        'languageSchools': 'Écoles de Langue Belges',
        'vocationalSchools': 'Écoles Professionnelles Belges',
        'conservatories': 'Conservatoires Belges',
        'foundationPrograms': 'Programmes Préparatoires Belges'
    },
    'es': {
        'universities': 'Universidades Belgas',
        'languageSchools': 'Escuelas de Idiomas Belgas',
        'vocationalSchools': 'Escuelas Profesionales Belgas',
        'conservatories': 'Conservatorios Belgas',
        'foundationPrograms': 'Programas Preparatorios Belgas'
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
        
        # Додати бельгійські переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        data['jurisdictions']['BE'] = BELGIUM_TRANSLATIONS.get(lang_code, BELGIUM_TRANSLATIONS['en'])
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Adding Belgian jurisdiction translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll Belgian translations added!")

if __name__ == "__main__":
    main()
