"""
Оновлення перекладів для юрисдикційно-залежних заголовків
Додає переклади для SK, CZ, PL юрисдикцій
"""

import json
import os

LOCALES_DIR = "c:/Users/info/OneDrive/Dokumenty/STUDENT/frontend/locales"

# Переклади для кожної юрисдикції
TRANSLATIONS = {
    'sk': {
        'SK': {
            'universities': 'Slovenské Univerzity',
            'languageSchools': 'Slovenské Jazykové Školy',
            'vocationalSchools': 'Slovenské Stredné Odborné Školy',
            'conservatories': 'Slovenské Konzervatóriá',
            'foundationPrograms': 'Slovenské Prípravné Programy'
        },
        'CZ': {
            'universities': 'České Univerzity',
            'languageSchools': 'České Jazykové Školy',
            'vocationalSchools': 'České Střední Odborné Školy',
            'conservatories': 'České Konzervatoře',
            'foundationPrograms': 'České Přípravné Programy'
        },
        'PL': {
            'universities': 'Poľské Univerzity',
            'languageSchools': 'Poľské Jazykové Školy',
            'vocationalSchools': 'Poľské Stredné Odborné Školy',
            'conservatories': 'Poľské Konzervatóriá',
            'foundationPrograms': 'Poľské Prípravné Programy'
        }
    },
    'cs': {
        'SK': {
            'universities': 'Slovenské Univerzity',
            'languageSchools': 'Slovenské Jazykové Školy',
            'vocationalSchools': 'Slovenské Střední Odborné Školy',
            'conservatories': 'Slovenská Konzervatoře',
            'foundationPrograms': 'Slovenské Přípravné Programy'
        },
        'CZ': {
            'universities': 'České Univerzity',
            'languageSchools': 'České Jazykové Školy',
            'vocationalSchools': 'České Střední Odborné Školy',
            'conservatories': 'České Konzervatoře',
            'foundationPrograms': 'České Přípravné Programy'
        },
        'PL': {
            'universities': 'Polské Univerzity',
            'languageSchools': 'Polské Jazykové Školy',
            'vocationalSchools': 'Polské Střední Odborné Školy',
            'conservatories': 'Polská Konzervatoře',
            'foundationPrograms': 'Polské Přípravné Programy'
        }
    },
    'pl': {
        'SK': {
            'universities': 'Słowackie Uniwersytety',
            'languageSchools': 'Słowackie Szkoły Językowe',
            'vocationalSchools': 'Słowackie Szkoły Zawodowe',
            'conservatories': 'Słowackie Konserwatoria',
            'foundationPrograms': 'Słowackie Programy Przygotowawcze'
        },
        'CZ': {
            'universities': 'Czeskie Uniwersytety',
            'languageSchools': 'Czeskie Szkoły Językowe',
            'vocationalSchools': 'Czeskie Szkoły Zawodowe',
            'conservatories': 'Czeskie Konserwatoria',
            'foundationPrograms': 'Czeskie Programy Przygotowawcze'
        },
        'PL': {
            'universities': 'Polskie Uniwersytety',
            'languageSchools': 'Polskie Szkoły Językowe',
            'vocationalSchools': 'Polskie Szkoły Zawodowe',
            'conservatories': 'Polskie Konserwatoria',
            'foundationPrograms': 'Polskie Programy Przygotowawcze'
        }
    },
    'en': {
        'SK': {
            'universities': 'Slovak Universities',
            'languageSchools': 'Slovak Language Schools',
            'vocationalSchools': 'Slovak Vocational Schools',
            'conservatories': 'Slovak Conservatories',
            'foundationPrograms': 'Slovak Foundation Programs'
        },
        'CZ': {
            'universities': 'Czech Universities',
            'languageSchools': 'Czech Language Schools',
            'vocationalSchools': 'Czech Vocational Schools',
            'conservatories': 'Czech Conservatories',
            'foundationPrograms': 'Czech Foundation Programs'
        },
        'PL': {
            'universities': 'Polish Universities',
            'languageSchools': 'Polish Language Schools',
            'vocationalSchools': 'Polish Vocational Schools',
            'conservatories': 'Polish Conservatories',
            'foundationPrograms': 'Polish Foundation Programs'
        }
    },
    'uk': {
        'SK': {
            'universities': 'Словацькі Університети',
            'languageSchools': 'Словацькі Мовні Школи',
            'vocationalSchools': 'Словацькі Професійні Школи',
            'conservatories': 'Словацькі Консерваторії',
            'foundationPrograms': 'Словацькі Підготовчі Програми'
        },
        'CZ': {
            'universities': 'Чеські Університети',
            'languageSchools': 'Чеські Мовні Школи',
            'vocationalSchools': 'Чеські Професійні Школи',
            'conservatories': 'Чеські Консерваторії',
            'foundationPrograms': 'Чеські Підготовчі Програми'
        },
        'PL': {
            'universities': 'Польські Університети',
            'languageSchools': 'Польські Мовні Школи',
            'vocationalSchools': 'Польські Професійні Школи',
            'conservatories': 'Польські Консерваторії',
            'foundationPrograms': 'Польські Підготовчі Програми'
        }
    }
}

# Додати переклади для інших мов (de, fr, es, it, ru)
for lang in ['de', 'fr', 'es', 'it', 'ru']:
    TRANSLATIONS[lang] = TRANSLATIONS['en']  # Використовуємо англійські як базу

def update_locale_file(lang_code):
    """Оновити файл перекладів для мови"""
    file_path = os.path.join(LOCALES_DIR, lang_code, 'common.json')
    
    if not os.path.exists(file_path):
        print(f"Skipping {lang_code} - file not found")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Додати юрисдикційні переклади
        if 'jurisdictions' not in data:
            data['jurisdictions'] = {}
        
        for jurisdiction in ['SK', 'CZ', 'PL']:
            if jurisdiction not in data['jurisdictions']:
                data['jurisdictions'][jurisdiction] = {}
            
            data['jurisdictions'][jurisdiction] = TRANSLATIONS.get(lang_code, TRANSLATIONS['en'])[jurisdiction]
        
        # Зберегти
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Updated {lang_code}/common.json")
        
    except Exception as e:
        print(f"Error updating {lang_code}: {e}")

def main():
    print("Updating jurisdiction-dependent translations...")
    
    languages = ['sk', 'cs', 'pl', 'en', 'de', 'fr', 'es', 'uk', 'it', 'ru']
    
    for lang in languages:
        update_locale_file(lang)
    
    print("\nAll translations updated!")
    print("\nNext step: Update page.tsx to use jurisdiction-dependent translations")

if __name__ == "__main__":
    main()
