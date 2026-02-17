const fs = require('fs');
const path = require('path');

// Pricing translations for all languages
const pricingTranslations = {
    sk: {
        "pricing": {
            "title": "Vyberte si svoj plán",
            "subtitle": "Začnite s bezplatným plánom alebo si vyberte prémiové funkcie",
            "guarantee": "💳 Bezpečná platba • 🔒 Zrušiteľné kedykoľvek • ✅ Bez skrytých poplatkov",
            "free": {
                "name": "FREE",
                "price": "€0",
                "period": "/mesiac",
                "description": "Základný prístup",
                "features": {
                    "browse": "Prehliadanie univerzít",
                    "links": "Odkazy na oficiálne stránky",
                    "info": "Základné informácie",
                    "noAI": "Bez AI konzultanta"
                },
                "button": "Začať zadarmo",
                "currentPlan": "Aktuálny plán"
            },
            "basic": {
                "name": "BASIC",
                "price": "€10",
                "period": "/mesiac",
                "description": "Pre aktívnych študentov",
                "badge": "Populárne",
                "features": {
                    "allFree": "Všetko z FREE +",
                    "aiConsultations": "25 AI konzultácií/deň",
                    "detailed": "Detailné odpovede",
                    "housing": "Hľadanie ubytovania",
                    "jobs": "Brigády pre študentov"
                },
                "button": "Vybrať BASIC"
            },
            "standard": {
                "name": "STANDARD",
                "price": "€20",
                "period": "/mesiac",
                "description": "Pre náročných",
                "features": {
                    "allBasic": "Všetko z BASIC +",
                    "aiConsultations": "50 AI konzultácií/deň",
                    "plans": "Pokrokové plány vstupu",
                    "advice": "Personalizované rady",
                    "templates": "Šablóny dokumentov"
                },
                "button": "Vybrať STANDARD"
            },
            "premium": {
                "name": "PREMIUM",
                "price": "€30",
                "period": "/mesiac",
                "description": "Kompletná podpora",
                "badge": "⭐ Najlepšie",
                "features": {
                    "allStandard": "Všetko zo STANDARD +",
                    "aiConsultations": "100 AI konzultácií/deň",
                    "expert": "Expertné konzultácie",
                    "support": "Prioritná podpora 24/7",
                    "personalPlan": "Osobný vstupný plán"
                },
                "button": "Vybrať PREMIUM"
            }
        }
    },
    cs: {
        "pricing": {
            "title": "Vyberte si svůj plán",
            "subtitle": "Začněte s bezplatným plánem nebo si vyberte prémiové funkce",
            "guarantee": "💳 Bezpečná platba • 🔒 Zrušitelné kdykoli • ✅ Bez skrytých poplatků",
            "free": {
                "name": "FREE",
                "price": "€0",
                "period": "/měsíc",
                "description": "Základní přístup",
                "features": {
                    "browse": "Prohlížení univerzit",
                    "links": "Odkazy na oficiální stránky",
                    "info": "Základní informace",
                    "noAI": "Bez AI konzultanta"
                },
                "button": "Začít zdarma",
                "currentPlan": "Aktuální plán"
            },
            "basic": {
                "name": "BASIC",
                "price": "€10",
                "period": "/měsíc",
                "description": "Pro aktivní studenty",
                "badge": "Populární",
                "features": {
                    "allFree": "Vše z FREE +",
                    "aiConsultations": "25 AI konzultací/den",
                    "detailed": "Podrobné odpovědi",
                    "housing": "Hledání ubytování",
                    "jobs": "Brigády pro studenty"
                },
                "button": "Vybrat BASIC"
            },
            "standard": {
                "name": "STANDARD",
                "price": "€20",
                "period": "/měsíc",
                "description": "Pro náročné",
                "features": {
                    "allBasic": "Vše z BASIC +",
                    "aiConsultations": "50 AI konzultací/den",
                    "plans": "Pokročilé plány přijetí",
                    "advice": "Personalizované rady",
                    "templates": "Šablony dokumentů"
                },
                "button": "Vybrat STANDARD"
            },
            "premium": {
                "name": "PREMIUM",
                "price": "€30",
                "period": "/měsíc",
                "description": "Kompletní podpora",
                "badge": "⭐ Nejlepší",
                "features": {
                    "allStandard": "Vše ze STANDARD +",
                    "aiConsultations": "100 AI konzultací/den",
                    "expert": "Expertní konzultace",
                    "support": "Prioritní podpora 24/7",
                    "personalPlan": "Osobní plán přijetí"
                },
                "button": "Vybrat PREMIUM"
            }
        }
    },
    pl: {
        "pricing": {
            "title": "Wybierz swój plan",
            "subtitle": "Zacznij od darmowego planu lub wybierz funkcje premium",
            "guarantee": "💳 Bezpieczna płatność • 🔒 Anuluj w dowolnym momencie • ✅ Bez ukrytych opłat",
            "free": {
                "name": "FREE",
                "price": "€0",
                "period": "/miesiąc",
                "description": "Podstawowy dostęp",
                "features": {
                    "browse": "Przeglądanie uniwersytetów",
                    "links": "Linki do oficjalnych stron",
                    "info": "Podstawowe informacje",
                    "noAI": "Bez konsultanta AI"
                },
                "button": "Rozpocznij za darmo",
                "currentPlan": "Aktualny plan"
            },
            "basic": {
                "name": "BASIC",
                "price": "€10",
                "period": "/miesiąc",
                "description": "Dla aktywnych studentów",
                "badge": "Popularne",
                "features": {
                    "allFree": "Wszystko z FREE +",
                    "aiConsultations": "25 konsultacji AI/dzień",
                    "detailed": "Szczegółowe odpowiedzi",
                    "housing": "Wyszukiwanie zakwaterowania",
                    "jobs": "Praca dla studentów"
                },
                "button": "Wybierz BASIC"
            },
            "standard": {
                "name": "STANDARD",
                "price": "€20",
                "period": "/miesiąc",
                "description": "Dla wymagających",
                "features": {
                    "allBasic": "Wszystko z BASIC +",
                    "aiConsultations": "50 konsultacji AI/dzień",
                    "plans": "Zaawansowane plany przyjęcia",
                    "advice": "Spersonalizowane porady",
                    "templates": "Szablony dokumentów"
                },
                "button": "Wybierz STANDARD"
            },
            "premium": {
                "name": "PREMIUM",
                "price": "€30",
                "period": "/miesiąc",
                "description": "Pełne wsparcie",
                "badge": "⭐ Najlepsze",
                "features": {
                    "allStandard": "Wszystko ze STANDARD +",
                    "aiConsultations": "100 konsultacji AI/dzień",
                    "expert": "Konsultacje eksperckie",
                    "support": "Priorytetowe wsparcie 24/7",
                    "personalPlan": "Osobisty plan przyjęcia"
                },
                "button": "Wybierz PREMIUM"
            }
        }
    },
    uk: {
        "pricing": {
            "title": "Оберіть свій план",
            "subtitle": "Почніть з безкоштовного плану або оберіть преміум функції",
            "guarantee": "💳 Безпечна оплата • 🔒 Скасування в будь-який час • ✅ Без прихованих платежів",
            "free": {
                "name": "FREE",
                "price": "€0",
                "period": "/місяць",
                "description": "Базовий доступ",
                "features": {
                    "browse": "Перегляд університетів",
                    "links": "Посилання на офіційні сайти",
                    "info": "Базова інформація",
                    "noAI": "Без AI консультанта"
                },
                "button": "Почати безкоштовно",
                "currentPlan": "Поточний план"
            },
            "basic": {
                "name": "BASIC",
                "price": "€10",
                "period": "/місяць",
                "description": "Для активних студентів",
                "badge": "Популярне",
                "features": {
                    "allFree": "Все з FREE +",
                    "aiConsultations": "25 AI консультацій/день",
                    "detailed": "Детальні відповіді",
                    "housing": "Пошук житла",
                    "jobs": "Робота для студентів"
                },
                "button": "Обрати BASIC"
            },
            "standard": {
                "name": "STANDARD",
                "price": "€20",
                "period": "/місяць",
                "description": "Для вимогливих",
                "features": {
                    "allBasic": "Все з BASIC +",
                    "aiConsultations": "50 AI консультацій/день",
                    "plans": "Покрокові плани вступу",
                    "advice": "Персоналізовані поради",
                    "templates": "Шаблони документів"
                },
                "button": "Обрати STANDARD"
            },
            "premium": {
                "name": "PREMIUM",
                "price": "€30",
                "period": "/місяць",
                "description": "Повна підтримка",
                "badge": "⭐ Найкраще",
                "features": {
                    "allStandard": "Все зі STANDARD +",
                    "aiConsultations": "100 AI консультацій/день",
                    "expert": "Експертні консультації",
                    "support": "Пріоритетна підтримка 24/7",
                    "personalPlan": "Особистий план вступу"
                },
                "button": "Обрати PREMIUM"
            }
        }
    },
    en: {
        "pricing": {
            "title": "Choose Your Plan",
            "subtitle": "Start with a free plan or choose premium features",
            "guarantee": "💳 Secure payment • 🔒 Cancel anytime • ✅ No hidden fees",
            "free": {
                "name": "FREE",
                "price": "€0",
                "period": "/month",
                "description": "Basic access",
                "features": {
                    "browse": "Browse universities",
                    "links": "Links to official websites",
                    "info": "Basic information",
                    "noAI": "No AI consultant"
                },
                "button": "Start for free",
                "currentPlan": "Current plan"
            },
            "basic": {
                "name": "BASIC",
                "price": "€10",
                "period": "/month",
                "description": "For active students",
                "badge": "Popular",
                "features": {
                    "allFree": "Everything from FREE +",
                    "aiConsultations": "25 AI consultations/day",
                    "detailed": "Detailed answers",
                    "housing": "Housing search",
                    "jobs": "Student jobs"
                },
                "button": "Choose BASIC"
            },
            "standard": {
                "name": "STANDARD",
                "price": "€20",
                "period": "/month",
                "description": "For demanding users",
                "features": {
                    "allBasic": "Everything from BASIC +",
                    "aiConsultations": "50 AI consultations/day",
                    "plans": "Advanced admission plans",
                    "advice": "Personalized advice",
                    "templates": "Document templates"
                },
                "button": "Choose STANDARD"
            },
            "premium": {
                "name": "PREMIUM",
                "price": "€30",
                "period": "/month",
                "description": "Complete support",
                "badge": "⭐ Best",
                "features": {
                    "allStandard": "Everything from STANDARD +",
                    "aiConsultations": "100 AI consultations/day",
                    "expert": "Expert consultations",
                    "support": "Priority support 24/7",
                    "personalPlan": "Personal admission plan"
                },
                "button": "Choose PREMIUM"
            }
        }
    },
    de: {
        "pricing": {
            "title": "Wählen Sie Ihren Plan",
            "subtitle": "Beginnen Sie mit einem kostenlosen Plan oder wählen Sie Premium-Funktionen",
            "guarantee": "💳 Sichere Zahlung • 🔒 Jederzeit kündbar • ✅ Keine versteckten Gebühren",
            "free": {
                "name": "FREE",
                "price": "€0",
                "period": "/Monat",
                "description": "Grundzugang",
                "features": {
                    "browse": "Universitäten durchsuchen",
                    "links": "Links zu offiziellen Websites",
                    "info": "Grundlegende Informationen",
                    "noAI": "Kein KI-Berater"
                },
                "button": "Kostenlos starten",
                "currentPlan": "Aktueller Plan"
            },
            "basic": {
                "name": "BASIC",
                "price": "€10",
                "period": "/Monat",
                "description": "Für aktive Studenten",
                "badge": "Beliebt",
                "features": {
                    "allFree": "Alles von FREE +",
                    "aiConsultations": "25 KI-Beratungen/Tag",
                    "detailed": "Detaillierte Antworten",
                    "housing": "Wohnungssuche",
                    "jobs": "Studentenjobs"
                },
                "button": "BASIC wählen"
            },
            "standard": {
                "name": "STANDARD",
                "price": "€20",
                "period": "/Monat",
                "description": "Für Anspruchsvolle",
                "features": {
                    "allBasic": "Alles von BASIC +",
                    "aiConsultations": "50 KI-Beratungen/Tag",
                    "plans": "Erweiterte Zulassungspläne",
                    "advice": "Personalisierte Beratung",
                    "templates": "Dokumentvorlagen"
                },
                "button": "STANDARD wählen"
            },
            "premium": {
                "name": "PREMIUM",
                "price": "€30",
                "period": "/Monat",
                "description": "Vollständige Unterstützung",
                "badge": "⭐ Beste",
                "features": {
                    "allStandard": "Alles von STANDARD +",
                    "aiConsultations": "100 KI-Beratungen/Tag",
                    "expert": "Expertenberatungen",
                    "support": "Prioritäts-Support 24/7",
                    "personalPlan": "Persönlicher Zulassungsplan"
                },
                "button": "PREMIUM wählen"
            }
        }
    },
    fr: {
        "pricing": {
            "title": "Choisissez votre plan",
            "subtitle": "Commencez avec un plan gratuit ou choisissez des fonctionnalités premium",
            "guarantee": "💳 Paiement sécurisé • 🔒 Annulez à tout moment • ✅ Pas de frais cachés",
            "free": {
                "name": "FREE",
                "price": "€0",
                "period": "/mois",
                "description": "Accès de base",
                "features": {
                    "browse": "Parcourir les universités",
                    "links": "Liens vers les sites officiels",
                    "info": "Informations de base",
                    "noAI": "Pas de consultant IA"
                },
                "button": "Commencer gratuitement",
                "currentPlan": "Plan actuel"
            },
            "basic": {
                "name": "BASIC",
                "price": "€10",
                "period": "/mois",
                "description": "Pour les étudiants actifs",
                "badge": "Populaire",
                "features": {
                    "allFree": "Tout de FREE +",
                    "aiConsultations": "25 consultations IA/jour",
                    "detailed": "Réponses détaillées",
                    "housing": "Recherche de logement",
                    "jobs": "Jobs étudiants"
                },
                "button": "Choisir BASIC"
            },
            "standard": {
                "name": "STANDARD",
                "price": "€20",
                "period": "/mois",
                "description": "Pour les exigeants",
                "features": {
                    "allBasic": "Tout de BASIC +",
                    "aiConsultations": "50 consultations IA/jour",
                    "plans": "Plans d'admission avancés",
                    "advice": "Conseils personnalisés",
                    "templates": "Modèles de documents"
                },
                "button": "Choisir STANDARD"
            },
            "premium": {
                "name": "PREMIUM",
                "price": "€30",
                "period": "/mois",
                "description": "Support complet",
                "badge": "⭐ Meilleur",
                "features": {
                    "allStandard": "Tout de STANDARD +",
                    "aiConsultations": "100 consultations IA/jour",
                    "expert": "Consultations d'experts",
                    "support": "Support prioritaire 24/7",
                    "personalPlan": "Plan d'admission personnel"
                },
                "button": "Choisir PREMIUM"
            }
        }
    },
    es: {
        "pricing": {
            "title": "Elige tu plan",
            "subtitle": "Comienza con un plan gratuito o elige funciones premium",
            "guarantee": "💳 Pago seguro • 🔒 Cancela en cualquier momento • ✅ Sin tarifas ocultas",
            "free": {
                "name": "FREE",
                "price": "€0",
                "period": "/mes",
                "description": "Acceso básico",
                "features": {
                    "browse": "Explorar universidades",
                    "links": "Enlaces a sitios oficiales",
                    "info": "Información básica",
                    "noAI": "Sin consultor IA"
                },
                "button": "Comenzar gratis",
                "currentPlan": "Plan actual"
            },
            "basic": {
                "name": "BASIC",
                "price": "€10",
                "period": "/mes",
                "description": "Para estudiantes activos",
                "badge": "Popular",
                "features": {
                    "allFree": "Todo de FREE +",
                    "aiConsultations": "25 consultas IA/día",
                    "detailed": "Respuestas detalladas",
                    "housing": "Búsqueda de alojamiento",
                    "jobs": "Trabajos para estudiantes"
                },
                "button": "Elegir BASIC"
            },
            "standard": {
                "name": "STANDARD",
                "price": "€20",
                "period": "/mes",
                "description": "Para exigentes",
                "features": {
                    "allBasic": "Todo de BASIC +",
                    "aiConsultations": "50 consultas IA/día",
                    "plans": "Planes de admisión avanzados",
                    "advice": "Consejos personalizados",
                    "templates": "Plantillas de documentos"
                },
                "button": "Elegir STANDARD"
            },
            "premium": {
                "name": "PREMIUM",
                "price": "€30",
                "period": "/mes",
                "description": "Soporte completo",
                "badge": "⭐ Mejor",
                "features": {
                    "allStandard": "Todo de STANDARD +",
                    "aiConsultations": "100 consultas IA/día",
                    "expert": "Consultas expertas",
                    "support": "Soporte prioritario 24/7",
                    "personalPlan": "Plan de admisión personal"
                },
                "button": "Elegir PREMIUM"
            }
        }
    },
    it: {
        "pricing": {
            "title": "Scegli il tuo piano",
            "subtitle": "Inizia con un piano gratuito o scegli funzionalità premium",
            "guarantee": "💳 Pagamento sicuro • 🔒 Annulla in qualsiasi momento • ✅ Nessun costo nascosto",
            "free": {
                "name": "FREE",
                "price": "€0",
                "period": "/mese",
                "description": "Accesso base",
                "features": {
                    "browse": "Sfoglia università",
                    "links": "Link ai siti ufficiali",
                    "info": "Informazioni di base",
                    "noAI": "Nessun consulente IA"
                },
                "button": "Inizia gratis",
                "currentPlan": "Piano attuale"
            },
            "basic": {
                "name": "BASIC",
                "price": "€10",
                "period": "/mese",
                "description": "Per studenti attivi",
                "badge": "Popolare",
                "features": {
                    "allFree": "Tutto da FREE +",
                    "aiConsultations": "25 consulenze IA/giorno",
                    "detailed": "Risposte dettagliate",
                    "housing": "Ricerca alloggio",
                    "jobs": "Lavori per studenti"
                },
                "button": "Scegli BASIC"
            },
            "standard": {
                "name": "STANDARD",
                "price": "€20",
                "period": "/mese",
                "description": "Per esigenti",
                "features": {
                    "allBasic": "Tutto da BASIC +",
                    "aiConsultations": "50 consulenze IA/giorno",
                    "plans": "Piani di ammissione avanzati",
                    "advice": "Consigli personalizzati",
                    "templates": "Modelli di documenti"
                },
                "button": "Scegli STANDARD"
            },
            "premium": {
                "name": "PREMIUM",
                "price": "€30",
                "period": "/mese",
                "description": "Supporto completo",
                "badge": "⭐ Migliore",
                "features": {
                    "allStandard": "Tutto da STANDARD +",
                    "aiConsultations": "100 consulenze IA/giorno",
                    "expert": "Consulenze esperte",
                    "support": "Supporto prioritario 24/7",
                    "personalPlan": "Piano di ammissione personale"
                },
                "button": "Scegli PREMIUM"
            }
        }
    },
    pt: {
        "pricing": {
            "title": "Escolha o seu plano",
            "subtitle": "Comece com um plano gratuito ou escolha recursos premium",
            "guarantee": "💳 Pagamento seguro • 🔒 Cancele a qualquer momento • ✅ Sem taxas ocultas",
            "free": {
                "name": "FREE",
                "price": "€0",
                "period": "/mês",
                "description": "Acesso básico",
                "features": {
                    "browse": "Navegar universidades",
                    "links": "Links para sites oficiais",
                    "info": "Informações básicas",
                    "noAI": "Sem consultor IA"
                },
                "button": "Começar grátis",
                "currentPlan": "Plano atual"
            },
            "basic": {
                "name": "BASIC",
                "price": "€10",
                "period": "/mês",
                "description": "Para estudantes ativos",
                "badge": "Popular",
                "features": {
                    "allFree": "Tudo do FREE +",
                    "aiConsultations": "25 consultas IA/dia",
                    "detailed": "Respostas detalhadas",
                    "housing": "Busca de alojamento",
                    "jobs": "Trabalhos para estudantes"
                },
                "button": "Escolher BASIC"
            },
            "standard": {
                "name": "STANDARD",
                "price": "€20",
                "period": "/mês",
                "description": "Para exigentes",
                "features": {
                    "allBasic": "Tudo do BASIC +",
                    "aiConsultations": "50 consultas IA/dia",
                    "plans": "Planos de admissão avançados",
                    "advice": "Conselhos personalizados",
                    "templates": "Modelos de documentos"
                },
                "button": "Escolher STANDARD"
            },
            "premium": {
                "name": "PREMIUM",
                "price": "€30",
                "period": "/mês",
                "description": "Suporte completo",
                "badge": "⭐ Melhor",
                "features": {
                    "allStandard": "Tudo do STANDARD +",
                    "aiConsultations": "100 consultas IA/dia",
                    "expert": "Consultas especializadas",
                    "support": "Suporte prioritário 24/7",
                    "personalPlan": "Plano de admissão pessoal"
                },
                "button": "Escolher PREMIUM"
            }
        }
    },
    ru: {
        "pricing": {
            "title": "Выберите свой план",
            "subtitle": "Начните с бесплатного плана или выберите премиум функции",
            "guarantee": "💳 Безопасная оплата • 🔒 Отмена в любое время • ✅ Без скрытых платежей",
            "free": {
                "name": "FREE",
                "price": "€0",
                "period": "/месяц",
                "description": "Базовый доступ",
                "features": {
                    "browse": "Просмотр университетов",
                    "links": "Ссылки на официальные сайты",
                    "info": "Базовая информация",
                    "noAI": "Без AI консультанта"
                },
                "button": "Начать бесплатно",
                "currentPlan": "Текущий план"
            },
            "basic": {
                "name": "BASIC",
                "price": "€10",
                "period": "/месяц",
                "description": "Для активных студентов",
                "badge": "Популярное",
                "features": {
                    "allFree": "Все из FREE +",
                    "aiConsultations": "25 AI консультаций/день",
                    "detailed": "Подробные ответы",
                    "housing": "Поиск жилья",
                    "jobs": "Работа для студентов"
                },
                "button": "Выбрать BASIC"
            },
            "standard": {
                "name": "STANDARD",
                "price": "€20",
                "period": "/месяц",
                "description": "Для требовательных",
                "features": {
                    "allBasic": "Все из BASIC +",
                    "aiConsultations": "50 AI консультаций/день",
                    "plans": "Продвинутые планы поступления",
                    "advice": "Персонализированные советы",
                    "templates": "Шаблоны документов"
                },
                "button": "Выбрать STANDARD"
            },
            "premium": {
                "name": "PREMIUM",
                "price": "€30",
                "period": "/месяц",
                "description": "Полная поддержка",
                "badge": "⭐ Лучшее",
                "features": {
                    "allStandard": "Все из STANDARD +",
                    "aiConsultations": "100 AI консультаций/день",
                    "expert": "Экспертные консультации",
                    "support": "Приоритетная поддержка 24/7",
                    "personalPlan": "Личный план поступления"
                },
                "button": "Выбрать PREMIUM"
            }
        }
    }
};

// Languages to update
const languages = ['cs', 'pl', 'uk', 'en', 'de', 'fr', 'es', 'it', 'pt', 'ru'];

// Update each language file
languages.forEach(lang => {
    const filePath = path.join(__dirname, `student_${lang}.json`);

    try {
        // Read existing file
        const fileContent = fs.readFileSync(filePath, 'utf8');
        const data = JSON.parse(fileContent);

        // Add pricing translations
        data.student.pricing = pricingTranslations[lang].pricing;

        // Write back to file
        fs.writeFileSync(filePath, JSON.stringify(data, null, 4), 'utf8');
        console.log(`✅ Updated ${lang} translations`);
    } catch (error) {
        console.error(`❌ Error updating ${lang}:`, error.message);
    }
});

console.log('\n🎉 All pricing translations added successfully!');
