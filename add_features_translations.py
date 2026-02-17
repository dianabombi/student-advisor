#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add feature4 and feature5 translations to all 10 languages
"""

import json
import os

# Define translations for feature4 (Housing) and feature5 (Jobs)
TRANSLATIONS = {
    'sk': {
        'feature4': {
            'title': 'Hľadanie Ubytovania',
            'description': 'Nájdite perfektné ubytovanie pre vaše štúdium'
        },
        'feature5': {
            'title': 'Brigády pre Študentov',
            'description': 'Objavte part-time pracovné príležitosti počas štúdia'
        }
    },
    'cs': {
        'feature4': {
            'title': 'Hledání Ubytování',
            'description': 'Najděte perfektní ubytování pro vaše studium'
        },
        'feature5': {
            'title': 'Brigády pro Studenty',
            'description': 'Objevte part-time pracovní příležitosti během studia'
        }
    },
    'pl': {
        'feature4': {
            'title': 'Szukanie Zakwaterowania',
            'description': 'Znajdź idealne zakwaterowanie na czas studiów'
        },
        'feature5': {
            'title': 'Praca dla Studentów',
            'description': 'Odkryj możliwości pracy w niepełnym wymiarze podczas studiów'
        }
    },
    'en': {
        'feature4': {
            'title': 'Housing Search',
            'description': 'Find the perfect accommodation for your studies'
        },
        'feature5': {
            'title': 'Student Jobs',
            'description': 'Discover part-time work opportunities during your studies'
        }
    },
    'de': {
        'feature4': {
            'title': 'Wohnungssuche',
            'description': 'Finden Sie die perfekte Unterkunft für Ihr Studium'
        },
        'feature5': {
            'title': 'Studentenjobs',
            'description': 'Entdecken Sie Teilzeitmöglichkeiten während des Studiums'
        }
    },
    'fr': {
        'feature4': {
            'title': 'Recherche de Logement',
            'description': 'Trouvez le logement parfait pour vos études'
        },
        'feature5': {
            'title': 'Jobs Étudiants',
            'description': 'Découvrez des opportunités de travail à temps partiel pendant vos études'
        }
    },
    'es': {
        'feature4': {
            'title': 'Búsqueda de Alojamiento',
            'description': 'Encuentra el alojamiento perfecto para tus estudios'
        },
        'feature5': {
            'title': 'Trabajos para Estudiantes',
            'description': 'Descubre oportunidades de trabajo a tiempo parcial durante tus estudios'
        }
    },
    'uk': {
        'feature4': {
            'title': 'Пошук Житла',
            'description': 'Знайдіть ідеальне житло для навчання'
        },
        'feature5': {
            'title': 'Підробіток для Студентів',
            'description': 'Відкрийте можливості роботи на неповний робочий день під час навчання'
        }
    },
    'it': {
        'feature4': {
            'title': 'Ricerca Alloggio',
            'description': 'Trova l\'alloggio perfetto per i tuoi studi'
        },
        'feature5': {
            'title': 'Lavori per Studenti',
            'description': 'Scopri opportunità di lavoro part-time durante gli studi'
        }
    },
    'ru': {
        'feature4': {
            'title': 'Поиск Жилья',
            'description': 'Найдите идеальное жилье для учебы'
        },
        'feature5': {
            'title': 'Подработка для Студентов',
            'description': 'Откройте возможности работы на неполный рабочий день во время учебы'
        }
    }
}

def add_translations():
    """Add feature4 and feature5 translations to all language files"""
    
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    locales_dir = os.path.join(frontend_dir, 'locales')
    
    if not os.path.exists(locales_dir):
        print(f"[-] Locales directory not found: {locales_dir}")
        return
    
    success_count = 0
    error_count = 0
    
    for lang_code, translations in TRANSLATIONS.items():
        lang_file = os.path.join(locales_dir, lang_code, 'common.json')
        
        try:
            # Read existing translations (handle UTF-8 BOM)
            if os.path.exists(lang_file):
                with open(lang_file, 'r', encoding='utf-8-sig') as f:
                    data = json.load(f)
            else:
                print(f"[!] File not found: {lang_file}")
                continue
            
            # Add feature4 and feature5 translations
            if 'student' not in data:
                data['student'] = {}
            if 'features' not in data['student']:
                data['student']['features'] = {}
            
            data['student']['features']['feature4'] = translations['feature4']
            data['student']['features']['feature5'] = translations['feature5']
            
            # Write back to file
            with open(lang_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"[+] Updated {lang_code}/common.json")
            print(f"    Feature 4: {translations['feature4']['title']}")
            print(f"    Feature 5: {translations['feature5']['title']}")
            success_count += 1
            
        except Exception as e:
            print(f"[-] Error updating {lang_code}: {e}")
            error_count += 1
    
    print(f"\n{'='*50}")
    print(f"[+] Successfully updated: {success_count} files")
    if error_count > 0:
        print(f"[-] Errors: {error_count} files")
    print(f"{'='*50}")


if __name__ == "__main__":
    print("Adding feature4 and feature5 translations to all 10 languages...\n")
    add_translations()
    print("\nDone! Translations added successfully.")
