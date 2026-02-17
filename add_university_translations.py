#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

# University descriptions for all languages
university_descriptions = {
    'en': {
        "universities": {
            "1": {
                "description": "The oldest and largest university in Slovakia, founded in 1919."
            },
            "2": {
                "description": "Leading technical university focused on engineering and technology."
            },
            "3": {
                "description": "Specialized university for economics, business and management."
            },
            "4": {
                "description": "Prominent university in eastern Slovakia with a long tradition."
            },
            "5": {
                "description": "Modern university in central Slovakia with a wide range of programs."
            }
        }
    },
    'sk': {
        "universities": {
            "1": {
                "description": "Najstaršia a najväčšia univerzita na Slovensku, založená v roku 1919."
            },
            "2": {
                "description": "Popredná technická univerzita zameraná na inžinierstvo a technológie."
            },
            "3": {
                "description": "Špecializovaná univerzita pre ekonomiku, obchod a manažment."
            },
            "4": {
                "description": "Významná univerzita vo východnom Slovensku s dlhou tradíciou."
            },
            "5": {
                "description": "Moderná univerzita v strednom Slovensku s širokým spektrom programov."
            }
        }
    },
    'cs': {
        "universities": {
            "1": {
                "description": "Nejstarší a největší univerzita na Slovensku, založená v roce 1919."
            },
            "2": {
                "description": "Přední technická univerzita zaměřená na inženýrství a technologie."
            },
            "3": {
                "description": "Specializovaná univerzita pro ekonomiku, obchod a management."
            },
            "4": {
                "description": "Významná univerzita ve východním Slovensku s dlouhou tradicí."
            },
            "5": {
                "description": "Moderní univerzita ve středním Slovensku s širokým spektrem programů."
            }
        }
    },
    'pl': {
        "universities": {
            "1": {
                "description": "Najstarszy i największy uniwersytet na Słowacji, założony w 1919 roku."
            },
            "2": {
                "description": "Wiodący uniwersytet techniczny skupiony na inżynierii i technologii."
            },
            "3": {
                "description": "Wyspecjalizowany uniwersytet dla ekonomii, biznesu i zarządzania."
            },
            "4": {
                "description": "Wybitny uniwersytet we wschodniej Słowacji z długą tradycją."
            },
            "5": {
                "description": "Nowoczesny uniwersytet w środkowej Słowacji z szeroką gamą programów."
            }
        }
    },
    'de': {
        "universities": {
            "1": {
                "description": "Die älteste und größte Universität in der Slowakei, gegründet 1919."
            },
            "2": {
                "description": "Führende technische Universität mit Schwerpunkt auf Ingenieurwesen und Technologie."
            },
            "3": {
                "description": "Spezialisierte Universität für Wirtschaft, Handel und Management."
            },
            "4": {
                "description": "Bedeutende Universität in der Ostslowakei mit langer Tradition."
            },
            "5": {
                "description": "Moderne Universität in der Mittelslowakei mit breitem Programmangebot."
            }
        }
    },
    'fr': {
        "universities": {
            "1": {
                "description": "La plus ancienne et la plus grande université de Slovaquie, fondée en 1919."
            },
            "2": {
                "description": "Université technique de premier plan axée sur l'ingénierie et la technologie."
            },
            "3": {
                "description": "Université spécialisée en économie, commerce et gestion."
            },
            "4": {
                "description": "Université importante dans l'est de la Slovaquie avec une longue tradition."
            },
            "5": {
                "description": "Université moderne en Slovaquie centrale avec une large gamme de programmes."
            }
        }
    },
    'es': {
        "universities": {
            "1": {
                "description": "La universidad más antigua y grande de Eslovaquia, fundada en 1919."
            },
            "2": {
                "description": "Universidad técnica líder enfocada en ingeniería y tecnología."
            },
            "3": {
                "description": "Universidad especializada en economía, negocios y gestión."
            },
            "4": {
                "description": "Universidad destacada en el este de Eslovaquia con una larga tradición."
            },
            "5": {
                "description": "Universidad moderna en el centro de Eslovaquia con una amplia gama de programas."
            }
        }
    },
    'it': {
        "universities": {
            "1": {
                "description": "L'università più antica e grande della Slovacchia, fondata nel 1919."
            },
            "2": {
                "description": "Università tecnica leader focalizzata su ingegneria e tecnologia."
            },
            "3": {
                "description": "Università specializzata in economia, commercio e gestione."
            },
            "4": {
                "description": "Università importante nella Slovacchia orientale con una lunga tradizione."
            },
            "5": {
                "description": "Università moderna nella Slovacchia centrale con un'ampia gamma di programmi."
            }
        }
    },
    'uk': {
        "universities": {
            "1": {
                "description": "Найстаріший і найбільший університет у Словаччині, заснований у 1919 році."
            },
            "2": {
                "description": "Провідний технічний університет, зосереджений на інженерії та технологіях."
            },
            "3": {
                "description": "Спеціалізований університет з економіки, бізнесу та менеджменту."
            },
            "4": {
                "description": "Видатний університет у східній Словаччині з довгою традицією."
            },
            "5": {
                "description": "Сучасний університет у центральній Словаччині з широким спектром програм."
            }
        }
    },
    'ru': {
        "universities": {
            "1": {
                "description": "Старейший и крупнейший университет в Словакии, основанный в 1919 году."
            },
            "2": {
                "description": "Ведущий технический университет, специализирующийся на инженерии и технологиях."
            },
            "3": {
                "description": "Специализированный университет по экономике, бизнесу и менеджменту."
            },
            "4": {
                "description": "Выдающийся университет в восточной Словакии с долгой традицией."
            },
            "5": {
                "description": "Современный университет в центральной Словакии с широким спектром программ."
            }
        }
    }
}

# Process each language
base_path = r"C:\Users\info\OneDrive\Dokumenty\Student\frontend\locales"
for lang, translations in university_descriptions.items():
    file_path = os.path.join(base_path, lang, "common.json")
    
    # Read existing file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add universities section
    data['universities'] = translations['universities']
    
    # Write back with UTF-8
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Updated {lang}/common.json with university descriptions")

print("\nSUCCESS: All translation files updated with university descriptions!")
