#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

# Student-specific translations for all languages
student_translations = {
    'en': {
        "student": {
            "hero": {
                "title": "Your Gateway to Educational Opportunities",
                "subtitle": "Discover universities, get AI-powered guidance, and plan your academic future",
                "getStarted": "Get Started",
                "exploreUniversities": "Explore Universities"
            },
            "features": {
                "title": "Why Choose Student Platform?",
                "feature1": {
                    "title": "University Search",
                    "description": "Find and compare universities across multiple countries"
                },
                "feature2": {
                    "title": "AI Guidance",
                    "description": "Get personalized recommendations and application support"
                },
                "feature3": {
                    "title": "Global Reach",
                    "description": "Access information about universities worldwide"
                }
            },
            "universities": {
                "title": "Slovak Universities",
                "viewAll": "View All Universities"
            },
            "cta": {
                "title": "Ready to Start Your Journey?",
                "subtitle": "Join thousands of students finding their perfect university",
                "button": "Create Free Account"
            }
        },
        "auth_buttons": {
            "loginButton": "Login",
            "registerButton": "Register"
        }
    },
    'sk': {
        "student": {
            "hero": {
                "title": "Vaša brána k vzdelávacím príležitostiam",
                "subtitle": "Objavte univerzity, získajte AI poradenstvo a naplánujte svoju akademickú budúcnosť",
                "getStarted": "Začať",
                "exploreUniversities": "Preskúmať Univerzity"
            },
            "features": {
                "title": "Prečo si vybrať Student Platform?",
                "feature1": {
                    "title": "Vyhľadávanie Univerzít",
                    "description": "Nájdite a porovnajte univerzity v mnohých krajinách"
                },
                "feature2": {
                    "title": "AI Poradenstvo",
                    "description": "Získajte personalizované odporúčania a podporu pri prihlasovaní"
                },
                "feature3": {
                    "title": "Globálny Dosah",
                    "description": "Prístup k informáciám o univerzitách po celom svete"
                }
            },
            "universities": {
                "title": "Slovenské Univerzity",
                "viewAll": "Zobraziť Všetky Univerzity"
            },
            "cta": {
                "title": "Pripravení Začať Svoju Cestu?",
                "subtitle": "Pripojte sa k tisíckam študentov hľadajúcich svoju ideálnu univerzitu",
                "button": "Vytvoriť Bezplatný Účet"
            }
        },
        "auth_buttons": {
            "loginButton": "Prihlásenie",
            "registerButton": "Registrácia"
        }
    },
    'cs': {
        "student": {
            "hero": {
                "title": "Vaše brána k vzdělávacím příležitostem",
                "subtitle": "Objevte univerzity, získejte AI poradenství a naplánujte svou akademickou budoucnost",
                "getStarted": "Začít",
                "exploreUniversities": "Prozkoumat Univerzity"
            },
            "features": {
                "title": "Proč si vybrat Student Platform?",
                "feature1": {
                    "title": "Vyhledávání Univerzit",
                    "description": "Najděte a porovnejte univerzity v mnoha zemích"
                },
                "feature2": {
                    "title": "AI Poradenství",
                    "description": "Získejte personalizovaná doporučení a podporu při přihlašování"
                },
                "feature3": {
                    "title": "Globální Dosah",
                    "description": "Přístup k informacím o univerzitách po celém světě"
                }
            },
            "universities": {
                "title": "Slovenské Univerzity",
                "viewAll": "Zobrazit Všechny Univerzity"
            },
            "cta": {
                "title": "Připraveni Začít Svou Cestu?",
                "subtitle": "Připojte se k tisícům studentů hledajících svou ideální univerzitu",
                "button": "Vytvořit Bezplatný Účet"
            }
        },
        "auth_buttons": {
            "loginButton": "Přihlášení",
            "registerButton": "Registrace"
        }
    },
    'pl': {
        "student": {
            "hero": {
                "title": "Twoja Brama do Możliwości Edukacyjnych",
                "subtitle": "Odkryj uniwersytety, uzyskaj wsparcie AI i zaplanuj swoją akademicką przyszłość",
                "getStarted": "Rozpocznij",
                "exploreUniversities": "Przeglądaj Uniwersytety"
            },
            "features": {
                "title": "Dlaczego Wybrać Student Platform?",
                "feature1": {
                    "title": "Wyszukiwanie Uniwersytetów",
                    "description": "Znajdź i porównaj uniwersytety w wielu krajach"
                },
                "feature2": {
                    "title": "Wsparcie AI",
                    "description": "Otrzymaj spersonalizowane rekomendacje i wsparcie aplikacyjne"
                },
                "feature3": {
                    "title": "Globalny Zasięg",
                    "description": "Dostęp do informacji o uniwersytetach na całym świecie"
                }
            },
            "universities": {
                "title": "Słowackie Uniwersytety",
                "viewAll": "Zobacz Wszystkie Uniwersytety"
            },
            "cta": {
                "title": "Gotowy Rozpocząć Swoją Podróż?",
                "subtitle": "Dołącz do tysięcy studentów szukających idealnego uniwersytetu",
                "button": "Utwórz Darmowe Konto"
            }
        },
        "auth_buttons": {
            "loginButton": "Logowanie",
            "registerButton": "Rejestracja"
        }
    },
    'de': {
        "student": {
            "hero": {
                "title": "Ihr Tor zu Bildungsmöglichkeiten",
                "subtitle": "Entdecken Sie Universitäten, erhalten Sie KI-gestützte Beratung und planen Sie Ihre akademische Zukunft",
                "getStarted": "Loslegen",
                "exploreUniversities": "Universitäten Erkunden"
            },
            "features": {
                "title": "Warum Student Platform Wählen?",
                "feature1": {
                    "title": "Universitätssuche",
                    "description": "Finden und vergleichen Sie Universitäten in vielen Ländern"
                },
                "feature2": {
                    "title": "KI-Beratung",
                    "description": "Erhalten Sie personalisierte Empfehlungen und Bewerbungsunterstützung"
                },
                "feature3": {
                    "title": "Globale Reichweite",
                    "description": "Zugang zu Informationen über Universitäten weltweit"
                }
            },
            "universities": {
                "title": "Slowakische Universitäten",
                "viewAll": "Alle Universitäten Anzeigen"
            },
            "cta": {
                "title": "Bereit, Ihre Reise zu Beginnen?",
                "subtitle": "Schließen Sie sich Tausenden von Studenten an, die ihre perfekte Universität finden",
                "button": "Kostenloses Konto Erstellen"
            }
        },
        "auth_buttons": {
            "loginButton": "Anmelden",
            "registerButton": "Registrieren"
        }
    },
    'fr': {
        "student": {
            "hero": {
                "title": "Votre Porte vers les Opportunités Éducatives",
                "subtitle": "Découvrez des universités, obtenez des conseils IA et planifiez votre avenir académique",
                "getStarted": "Commencer",
                "exploreUniversities": "Explorer les Universités"
            },
            "features": {
                "title": "Pourquoi Choisir Student Platform?",
                "feature1": {
                    "title": "Recherche d'Universités",
                    "description": "Trouvez et comparez des universités dans plusieurs pays"
                },
                "feature2": {
                    "title": "Conseils IA",
                    "description": "Obtenez des recommandations personnalisées et un soutien aux candidatures"
                },
                "feature3": {
                    "title": "Portée Mondiale",
                    "description": "Accédez aux informations sur les universités du monde entier"
                }
            },
            "universities": {
                "title": "Universités Slovaques",
                "viewAll": "Voir Toutes les Universités"
            },
            "cta": {
                "title": "Prêt à Commencer Votre Voyage?",
                "subtitle": "Rejoignez des milliers d'étudiants à la recherche de leur université idéale",
                "button": "Créer un Compte Gratuit"
            }
        },
        "auth_buttons": {
            "loginButton": "Connexion",
            "registerButton": "Inscription"
        }
    },
    'es': {
        "student": {
            "hero": {
                "title": "Su Puerta a las Oportunidades Educativas",
                "subtitle": "Descubra universidades, obtenga orientación con IA y planifique su futuro académico",
                "getStarted": "Comenzar",
                "exploreUniversities": "Explorar Universidades"
            },
            "features": {
                "title": "¿Por Qué Elegir Student Platform?",
                "feature1": {
                    "title": "Búsqueda de Universidades",
                    "description": "Encuentre y compare universidades en múltiples países"
                },
                "feature2": {
                    "title": "Orientación IA",
                    "description": "Obtenga recomendaciones personalizadas y apoyo en solicitudes"
                },
                "feature3": {
                    "title": "Alcance Global",
                    "description": "Acceso a información sobre universidades en todo el mundo"
                }
            },
            "universities": {
                "title": "Universidades Eslovacas",
                "viewAll": "Ver Todas las Universidades"
            },
            "cta": {
                "title": "¿Listo para Comenzar su Viaje?",
                "subtitle": "Únase a miles de estudiantes que buscan su universidad perfecta",
                "button": "Crear Cuenta Gratuita"
            }
        },
        "auth_buttons": {
            "loginButton": "Iniciar Sesión",
            "registerButton": "Registrarse"
        }
    },
    'it': {
        "student": {
            "hero": {
                "title": "La Tua Porta verso le Opportunità Educative",
                "subtitle": "Scopri università, ottieni consulenza IA e pianifica il tuo futuro accademico",
                "getStarted": "Inizia",
                "exploreUniversities": "Esplora le Università"
            },
            "features": {
                "title": "Perché Scegliere Student Platform?",
                "feature1": {
                    "title": "Ricerca Università",
                    "description": "Trova e confronta università in diversi paesi"
                },
                "feature2": {
                    "title": "Consulenza IA",
                    "description": "Ottieni raccomandazioni personalizzate e supporto nelle candidature"
                },
                "feature3": {
                    "title": "Portata Globale",
                    "description": "Accesso a informazioni sulle università in tutto il mondo"
                }
            },
            "universities": {
                "title": "Università Slovacche",
                "viewAll": "Vedi Tutte le Università"
            },
            "cta": {
                "title": "Pronto a Iniziare il Tuo Viaggio?",
                "subtitle": "Unisciti a migliaia di studenti che cercano la loro università ideale",
                "button": "Crea Account Gratuito"
            }
        },
        "auth_buttons": {
            "loginButton": "Accedi",
            "registerButton": "Registrati"
        }
    },
    'uk': {
        "student": {
            "hero": {
                "title": "Ваші Ворота до Освітніх Можливостей",
                "subtitle": "Відкрийте університети, отримайте AI-консультації та сплануйте своє академічне майбутнє",
                "getStarted": "Почати",
                "exploreUniversities": "Досліджувати Університети"
            },
            "features": {
                "title": "Чому Обрати Student Platform?",
                "feature1": {
                    "title": "Пошук Університетів",
                    "description": "Знайдіть та порівняйте університети в багатьох країнах"
                },
                "feature2": {
                    "title": "AI Консультації",
                    "description": "Отримайте персоналізовані рекомендації та підтримку при вступі"
                },
                "feature3": {
                    "title": "Глобальний Охоплення",
                    "description": "Доступ до інформації про університети по всьому світу"
                }
            },
            "universities": {
                "title": "Словацькі Університети",
                "viewAll": "Переглянути Всі Університети"
            },
            "cta": {
                "title": "Готові Розпочати Свою Подорож?",
                "subtitle": "Приєднуйтесь до тисяч студентів, які шукають свій ідеальний університет",
                "button": "Створити Безкоштовний Обліковий Запис"
            }
        },
        "auth_buttons": {
            "loginButton": "Вхід",
            "registerButton": "Реєстрація"
        }
    },
    'ru': {
        "student": {
            "hero": {
                "title": "Ваши Ворота к Образовательным Возможностям",
                "subtitle": "Откройте университеты, получите AI-консультации и спланируйте свое академическое будущее",
                "getStarted": "Начать",
                "exploreUniversities": "Исследовать Университеты"
            },
            "features": {
                "title": "Почему Выбрать Student Platform?",
                "feature1": {
                    "title": "Поиск Университетов",
                    "description": "Найдите и сравните университеты во многих странах"
                },
                "feature2": {
                    "title": "AI Консультации",
                    "description": "Получите персонализированные рекомендации и поддержку при поступлении"
                },
                "feature3": {
                    "title": "Глобальный Охват",
                    "description": "Доступ к информации об университетах по всему миру"
                }
            },
            "universities": {
                "title": "Словацкие Университеты",
                "viewAll": "Просмотреть Все Университеты"
            },
            "cta": {
                "title": "Готовы Начать Свой Путь?",
                "subtitle": "Присоединяйтесь к тысячам студентов, ищущих свой идеальный университет",
                "button": "Создать Бесплатный Аккаунт"
            }
        },
        "auth_buttons": {
            "loginButton": "Вход",
            "registerButton": "Регистрация"
        }
    }
}

# Process each language
base_path = r"C:\Users\info\OneDrive\Dokumenty\Student\frontend\locales"
for lang, translations in student_translations.items():
    file_path = os.path.join(base_path, lang, "common.json")
    
    # Read existing file
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add student section
    data['student'] = translations['student']
    
    # Add auth buttons
    if 'auth' not in data:
        data['auth'] = {}
    data['auth']['loginButton'] = translations['auth_buttons']['loginButton']
    data['auth']['registerButton'] = translations['auth_buttons']['registerButton']
    
    # Write back with UTF-8
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Updated {lang}/common.json")

print("\n🎉 All translation files updated with Student sections!")
