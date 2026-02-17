#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Housing and Jobs translations to all 10 languages
Adds translations for the new Housing and Jobs modules
"""

import json
import os

# Define translations for all 10 languages
TRANSLATIONS = {
    'sk': {
        'housing': {
            'title': 'Nájsť bývanie',
            'subtitle': 'Nájdi ideálne bývanie pre štúdium',
            'agencies': 'Agentúry',
            'chatConsultant': 'Chat konzultant',
            'selectCity': 'Vyber mesto',
            'cityDescription': 'Vyber mesto, kde hľadáš bývanie',
            'comingSoon': 'Čoskoro dostupné',
            'useChat': 'Zatiaľ použite chat konzultanta',
            'chatTitle': 'Chat s konzultantom',
            'chatDescription': 'Povedz, aké bývanie hľadáš',
            'placeholder': 'Napíš svoju otázku...',
            'send': 'Odoslať',
            'infoTitle': 'Užitočné informácie',
            'info': 'Náš AI pomôže nájsť najlepšie možnosti bývania',
            'welcome': 'Ahoj {{name}}! Pomôžem ti nájsť bývanie.',
            'error': 'Prepáčte, nastala chyba.'
        },
        'jobs': {
            'title': 'Brigády pre študentov',
            'subtitle': 'Nájdi ideálnu part-time prácu'
        }
    },
    'cs': {
        'housing': {
            'title': 'Najít bydlení',
            'subtitle': 'Najdi ideální bydlení pro studium',
            'agencies': 'Agentury',
            'chatConsultant': 'Chat konzultant',
            'selectCity': 'Vyber město',
            'cityDescription': 'Vyber město, kde hledáš bydlení',
            'comingSoon': 'Brzy dostupné',
            'useChat': 'Zatím použijte chat konzultanta',
            'chatTitle': 'Chat s konzultantem',
            'chatDescription': 'Řekni, jaké bydlení hledáš',
            'placeholder': 'Napiš svou otázku...',
            'send': 'Odeslat',
            'infoTitle': 'Užitečné informace',
            'info': 'Naše AI pomůže najít nejlepší možnosti bydlení',
            'welcome': 'Ahoj {{name}}! Pomůžu ti najít bydlení.',
            'error': 'Promiňte, nastala chyba.'
        },
        'jobs': {
            'title': 'Brigády pro studenty',
            'subtitle': 'Najdi ideální part-time práci'
        }
    },
    'pl': {
        'housing': {
            'title': 'Znaleźć mieszkanie',
            'subtitle': 'Znajdź idealne mieszkanie do nauki',
            'agencies': 'Agencje',
            'chatConsultant': 'Chat konsultant',
            'selectCity': 'Wybierz miasto',
            'cityDescription': 'Wybierz miasto, w którym szukasz mieszkania',
            'comingSoon': 'Wkrótce dostępne',
            'useChat': 'Na razie użyj chat konsultanta',
            'chatTitle': 'Chat z konsultantem',
            'chatDescription': 'Powiedz, jakiego mieszkania szukasz',
            'placeholder': 'Napisz swoje pytanie...',
            'send': 'Wyślij',
            'infoTitle': 'Przydatne informacje',
            'info': 'Nasza AI pomoże znaleźć najlepsze opcje mieszkania',
            'welcome': 'Cześć {{name}}! Pomogę ci znaleźć mieszkanie.',
            'error': 'Przepraszamy, wystąpił błąd.'
        },
        'jobs': {
            'title': 'Praca dorywcza dla studentów',
            'subtitle': 'Znajdź idealną pracę part-time'
        }
    },
    'en': {
        'housing': {
            'title': 'Find Housing',
            'subtitle': 'Find the perfect housing for your studies',
            'agencies': 'Agencies',
            'chatConsultant': 'Chat Consultant',
            'selectCity': 'Select City',
            'cityDescription': 'Select the city where you are looking for housing',
            'comingSoon': 'Coming Soon',
            'useChat': 'For now, use the chat consultant',
            'chatTitle': 'Chat with Consultant',
            'chatDescription': 'Tell us what housing you are looking for',
            'placeholder': 'Write your question...',
            'send': 'Send',
            'infoTitle': 'Useful Information',
            'info': 'Our AI will help find the best housing options',
            'welcome': 'Hi {{name}}! I will help you find housing.',
            'error': 'Sorry, an error occurred.'
        },
        'jobs': {
            'title': 'Student Jobs',
            'subtitle': 'Find the perfect part-time job'
        }
    },
    'de': {
        'housing': {
            'title': 'Unterkunft finden',
            'subtitle': 'Finde die perfekte Unterkunft für dein Studium',
            'agencies': 'Agenturen',
            'chatConsultant': 'Chat Berater',
            'selectCity': 'Stadt wählen',
            'cityDescription': 'Wähle die Stadt, in der du eine Unterkunft suchst',
            'comingSoon': 'Demnächst verfügbar',
            'useChat': 'Verwende vorerst den Chat-Berater',
            'chatTitle': 'Chat mit Berater',
            'chatDescription': 'Sag uns, welche Unterkunft du suchst',
            'placeholder': 'Schreibe deine Frage...',
            'send': 'Senden',
            'infoTitle': 'Nützliche Informationen',
            'info': 'Unsere KI hilft dir, die besten Unterkunftsoptionen zu finden',
            'welcome': 'Hallo {{name}}! Ich helfe dir, eine Unterkunft zu finden.',
            'error': 'Entschuldigung, ein Fehler ist aufgetreten.'
        },
        'jobs': {
            'title': 'Studentenjobs',
            'subtitle': 'Finde den perfekten Teilzeitjob'
        }
    },
    'fr': {
        'housing': {
            'title': 'Trouver un logement',
            'subtitle': 'Trouve le logement parfait pour tes études',
            'agencies': 'Agences',
            'chatConsultant': 'Consultant Chat',
            'selectCity': 'Sélectionner la ville',
            'cityDescription': 'Sélectionne la ville où tu cherches un logement',
            'comingSoon': 'Bientôt disponible',
            'useChat': 'Pour l\'instant, utilise le consultant chat',
            'chatTitle': 'Chat avec le consultant',
            'chatDescription': 'Dis-nous quel logement tu cherches',
            'placeholder': 'Écris ta question...',
            'send': 'Envoyer',
            'infoTitle': 'Informations utiles',
            'info': 'Notre IA aidera à trouver les meilleures options de logement',
            'welcome': 'Salut {{name}}! Je vais t\'aider à trouver un logement.',
            'error': 'Désolé, une erreur s\'est produite.'
        },
        'jobs': {
            'title': 'Jobs étudiants',
            'subtitle': 'Trouve le job à temps partiel parfait'
        }
    },
    'es': {
        'housing': {
            'title': 'Encontrar alojamiento',
            'subtitle': 'Encuentra el alojamiento perfecto para tus estudios',
            'agencies': 'Agencias',
            'chatConsultant': 'Consultor de Chat',
            'selectCity': 'Seleccionar ciudad',
            'cityDescription': 'Selecciona la ciudad donde buscas alojamiento',
            'comingSoon': 'Próximamente disponible',
            'useChat': 'Por ahora, usa el consultor de chat',
            'chatTitle': 'Chat con consultor',
            'chatDescription': 'Dinos qué alojamiento buscas',
            'placeholder': 'Escribe tu pregunta...',
            'send': 'Enviar',
            'infoTitle': 'Información útil',
            'info': 'Nuestra IA ayudará a encontrar las mejores opciones de alojamiento',
            'welcome': 'Hola {{name}}! Te ayudaré a encontrar alojamiento.',
            'error': 'Lo siento, ocurrió un error.'
        },
        'jobs': {
            'title': 'Trabajos para estudiantes',
            'subtitle': 'Encuentra el trabajo a tiempo parcial perfecto'
        }
    },
    'uk': {
        'housing': {
            'title': 'Знайти житло',
            'subtitle': 'Знайди ідеальне житло для навчання',
            'agencies': 'Агенції',
            'chatConsultant': 'Чат консультант',
            'selectCity': 'Вибери місто',
            'cityDescription': 'Вибери місто, де шукаєш житло',
            'comingSoon': 'Скоро буде доступно',
            'useChat': 'Поки що використовуй чат консультант',
            'chatTitle': 'Чат з консультантом',
            'chatDescription': 'Розкажи, яке житло шукаєш',
            'placeholder': 'Напиши своє питання...',
            'send': 'Відправити',
            'infoTitle': 'Корисна інформація',
            'info': 'Наш AI допоможе знайти найкращі варіанти житла',
            'welcome': 'Привіт {{name}}! Я допоможу знайти житло.',
            'error': 'Вибачте, сталася помилка.'
        },
        'jobs': {
            'title': 'Підробіток для студентів',
            'subtitle': 'Знайди ідеальну part-time роботу'
        }
    },
    'it': {
        'housing': {
            'title': 'Trova alloggio',
            'subtitle': 'Trova l\'alloggio perfetto per i tuoi studi',
            'agencies': 'Agenzie',
            'chatConsultant': 'Consulente Chat',
            'selectCity': 'Seleziona città',
            'cityDescription': 'Seleziona la città dove cerchi alloggio',
            'comingSoon': 'Prossimamente disponibile',
            'useChat': 'Per ora, usa il consulente chat',
            'chatTitle': 'Chat con consulente',
            'chatDescription': 'Dicci quale alloggio stai cercando',
            'placeholder': 'Scrivi la tua domanda...',
            'send': 'Invia',
            'infoTitle': 'Informazioni utili',
            'info': 'La nostra IA aiuterà a trovare le migliori opzioni di alloggio',
            'welcome': 'Ciao {{name}}! Ti aiuterò a trovare un alloggio.',
            'error': 'Spiacente, si è verificato un errore.'
        },
        'jobs': {
            'title': 'Lavori per studenti',
            'subtitle': 'Trova il lavoro part-time perfetto'
        }
    },
    'ru': {
        'housing': {
            'title': 'Найти жилье',
            'subtitle': 'Найди идеальное жилье для учебы',
            'agencies': 'Агентства',
            'chatConsultant': 'Чат консультант',
            'selectCity': 'Выбери город',
            'cityDescription': 'Выбери город, где ищешь жилье',
            'comingSoon': 'Скоро будет доступно',
            'useChat': 'Пока используй чат консультант',
            'chatTitle': 'Чат с консультантом',
            'chatDescription': 'Расскажи, какое жилье ищешь',
            'placeholder': 'Напиши свой вопрос...',
            'send': 'Отправить',
            'infoTitle': 'Полезная информация',
            'info': 'Наш AI поможет найти лучшие варианты жилья',
            'welcome': 'Привет {{name}}! Я помогу найти жилье.',
            'error': 'Извините, произошла ошибка.'
        },
        'jobs': {
            'title': 'Подработка для студентов',
            'subtitle': 'Найди идеальную part-time работу'
        }
    }
}

def add_translations():
    """Add housing and jobs translations to all language files"""
    
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    locales_dir = os.path.join(frontend_dir, 'locales')
    
    if not os.path.exists(locales_dir):
        print(f"❌ Locales directory not found: {locales_dir}")
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
                print(f"[!] File not found: {lang_file}, creating new...")
                os.makedirs(os.path.dirname(lang_file), exist_ok=True)
                data = {}
            
            # Add housing and jobs translations
            data['housing'] = translations['housing']
            data['jobs'] = translations['jobs']
            
            # Write back to file
            with open(lang_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"[+] Updated {lang_code}/common.json")
            success_count += 1
            
        except Exception as e:
            print(f"[-] Error updating {lang_code}: {e}")
            error_count += 1
    
    print(f"\n{'='*50}")
    print(f"[+] Successfully updated: {success_count} files")
    if error_count > 0:
        print(f"[-] Errors: {error_count} files")
    print(f"{'='*50}")
    print("\nAdded translations for:")
    print("  - housing.title, subtitle, agencies, chatConsultant, etc.")
    print("  - jobs.title, subtitle")
    print("\nLanguages: SK, CS, PL, EN, DE, FR, ES, UK, IT, RU")


if __name__ == "__main__":
    print("Adding Housing & Jobs translations to all 10 languages...\n")
    add_translations()
    print("\nDone! Translations added successfully.")
