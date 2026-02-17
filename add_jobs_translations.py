#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add comprehensive Jobs page translations to all 10 languages
"""

import json
import os

# Define all translations for Jobs page
TRANSLATIONS = {
    'sk': {
        'title': 'Brigády pre študentov',
        'subtitle': 'Nájdi ideálnu part-time prácu alebo brigádu',
        'searchIn': 'Hľadanie v meste',
        'back': 'Späť',
        'chatTitle': 'Čet s konzultantom',
        'chatSubtitle': 'Povedz mi, akú prácu hľadáš, a pomôžem ti nájsť najlepšie možnosti',
        'placeholder': 'Napíš svoju otázku...',
        'send': 'Odoslať',
        'greeting': 'Ahoj {name}! Som tvoj asistent pre hľadanie brigád a part-time práce.',
        'greetingWithContext': 'Vidím, že si sa zaujímal o {university} v meste {city}. Môžem ti pomôcť nájsť brigády práve v {city}!',
        'howCanHelp': 'Ako ti môžem pomôcť?',
        'error': 'Prepáčte, nastala chyba. Skúste to prosím znova.',
        'popularPortals': 'Populárne portály',
        'jobTypes': 'Typy prác',
        'portals': {
            'profesia': 'Profesia.sk - Brigády',
            'studentjob': 'StudentJob.sk',
            'brigada': 'Brigada.sk',
            'kariera': 'Kariera.sk'
        },
        'types': {
            'parttime': 'Part-time (neúplný úväzok)',
            'brigada': 'Brigády (dočasná práca)',
            'seasonal': 'Sezónna práca',
            'homeoffice': 'Home office (na diaľku)'
        }
    },
    'cs': {
        'title': 'Brigády pro studenty',
        'subtitle': 'Najdi ideální part-time práci nebo brigádu',
        'searchIn': 'Hledání ve městě',
        'back': 'Zpět',
        'chatTitle': 'Chat s konzultantem',
        'chatSubtitle': 'Řekni mi, jakou práci hledáš, a pomůžu ti najít nejlepší možnosti',
        'placeholder': 'Napiš svou otázku...',
        'send': 'Odeslat',
        'greeting': 'Ahoj {name}! Jsem tvůj asistent pro hledání brigád a part-time práce.',
        'greetingWithContext': 'Vidím, že jsi se zajímal o {university} ve městě {city}. Můžu ti pomoci najít brigády právě v {city}!',
        'howCanHelp': 'Jak ti můžu pomoci?',
        'error': 'Promiňte, nastala chyba. Zkuste to prosím znovu.',
        'popularPortals': 'Populární portály',
        'jobTypes': 'Typy prací',
        'portals': {
            'profesia': 'Jobs.cz - Brigády',
            'studentjob': 'StudentJob.cz',
            'brigada': 'Brigada.cz',
            'kariera': 'Prace.cz'
        },
        'types': {
            'parttime': 'Part-time (částečný úvazek)',
            'brigada': 'Brigády (dočasná práce)',
            'seasonal': 'Sezónní práce',
            'homeoffice': 'Home office (na dálku)'
        }
    },
    'pl': {
        'title': 'Praca dla studentów',
        'subtitle': 'Znajdź idealną pracę part-time',
        'searchIn': 'Szukanie w mieście',
        'back': 'Wstecz',
        'chatTitle': 'Czat z konsultantem',
        'chatSubtitle': 'Powiedz mi, jakiej pracy szukasz, a pomogę ci znaleźć najlepsze opcje',
        'placeholder': 'Napisz swoje pytanie...',
        'send': 'Wyślij',
        'greeting': 'Cześć {name}! Jestem twoim asystentem w poszukiwaniu pracy part-time.',
        'greetingWithContext': 'Widzę, że interesowałeś się {university} w mieście {city}. Mogę ci pomóc znaleźć pracę właśnie w {city}!',
        'howCanHelp': 'Jak mogę ci pomóc?',
        'error': 'Przepraszam, wystąpił błąd. Spróbuj ponownie.',
        'popularPortals': 'Popularne portale',
        'jobTypes': 'Rodzaje pracy',
        'portals': {
            'profesia': 'Pracuj.pl - Dla studentów',
            'studentjob': 'StudentJob.pl',
            'brigada': 'OLX Praca',
            'kariera': 'Indeed.pl'
        },
        'types': {
            'parttime': 'Part-time (niepełny etat)',
            'brigada': 'Praca dorywcza',
            'seasonal': 'Praca sezonowa',
            'homeoffice': 'Home office (zdalna)'
        }
    },
    'en': {
        'title': 'Student Jobs',
        'subtitle': 'Find the perfect part-time job',
        'searchIn': 'Searching in',
        'back': 'Back',
        'chatTitle': 'Chat with consultant',
        'chatSubtitle': 'Tell me what job you\'re looking for, and I\'ll help you find the best options',
        'placeholder': 'Type your question...',
        'send': 'Send',
        'greeting': 'Hi {name}! I\'m your assistant for finding part-time jobs.',
        'greetingWithContext': 'I see you were interested in {university} in {city}. I can help you find jobs in {city}!',
        'howCanHelp': 'How can I help you?',
        'error': 'Sorry, an error occurred. Please try again.',
        'popularPortals': 'Popular job portals',
        'jobTypes': 'Job types',
        'portals': {
            'profesia': 'Indeed - Student Jobs',
            'studentjob': 'StudentJob.com',
            'brigada': 'LinkedIn Jobs',
            'kariera': 'Glassdoor'
        },
        'types': {
            'parttime': 'Part-time',
            'brigada': 'Temporary work',
            'seasonal': 'Seasonal work',
            'homeoffice': 'Remote work'
        }
    },
    'de': {
        'title': 'Studentenjobs',
        'subtitle': 'Finde den perfekten Teilzeitjob',
        'searchIn': 'Suche in',
        'back': 'Zurück',
        'chatTitle': 'Chat mit Berater',
        'chatSubtitle': 'Sag mir, welchen Job du suchst, und ich helfe dir, die besten Optionen zu finden',
        'placeholder': 'Schreibe deine Frage...',
        'send': 'Senden',
        'greeting': 'Hallo {name}! Ich bin dein Assistent für die Suche nach Teilzeitjobs.',
        'greetingWithContext': 'Ich sehe, du hast dich für {university} in {city} interessiert. Ich kann dir helfen, Jobs in {city} zu finden!',
        'howCanHelp': 'Wie kann ich dir helfen?',
        'error': 'Entschuldigung, ein Fehler ist aufgetreten. Bitte versuche es erneut.',
        'popularPortals': 'Beliebte Jobportale',
        'jobTypes': 'Jobtypen',
        'portals': {
            'profesia': 'Indeed.de - Studentenjobs',
            'studentjob': 'StudentJob.de',
            'brigada': 'Jobmensa',
            'kariera': 'StepStone'
        },
        'types': {
            'parttime': 'Teilzeit',
            'brigada': 'Aushilfsjobs',
            'seasonal': 'Saisonarbeit',
            'homeoffice': 'Homeoffice (Remote)'
        }
    },
    'fr': {
        'title': 'Jobs étudiants',
        'subtitle': 'Trouve le job à temps partiel parfait',
        'searchIn': 'Recherche dans',
        'back': 'Retour',
        'chatTitle': 'Chat avec consultant',
        'chatSubtitle': 'Dis-moi quel job tu cherches, et je t\'aiderai à trouver les meilleures options',
        'placeholder': 'Écris ta question...',
        'send': 'Envoyer',
        'greeting': 'Salut {name}! Je suis ton assistant pour trouver des jobs à temps partiel.',
        'greetingWithContext': 'Je vois que tu t\'es intéressé à {university} à {city}. Je peux t\'aider à trouver des jobs à {city}!',
        'howCanHelp': 'Comment puis-je t\'aider?',
        'error': 'Désolé, une erreur s\'est produite. Veuillez réessayer.',
        'popularPortals': 'Portails d\'emploi populaires',
        'jobTypes': 'Types d\'emplois',
        'portals': {
            'profesia': 'Indeed.fr - Jobs étudiants',
            'studentjob': 'StudentJob.fr',
            'brigada': 'Jobteaser',
            'kariera': 'Monster.fr'
        },
        'types': {
            'parttime': 'Temps partiel',
            'brigada': 'Travail temporaire',
            'seasonal': 'Travail saisonnier',
            'homeoffice': 'Télétravail'
        }
    },
    'es': {
        'title': 'Trabajos para estudiantes',
        'subtitle': 'Encuentra el trabajo a tiempo parcial perfecto',
        'searchIn': 'Buscando en',
        'back': 'Volver',
        'chatTitle': 'Chat con consultor',
        'chatSubtitle': 'Dime qué trabajo buscas y te ayudaré a encontrar las mejores opciones',
        'placeholder': 'Escribe tu pregunta...',
        'send': 'Enviar',
        'greeting': '¡Hola {name}! Soy tu asistente para encontrar trabajos a tiempo parcial.',
        'greetingWithContext': 'Veo que te interesaste en {university} en {city}. ¡Puedo ayudarte a encontrar trabajos en {city}!',
        'howCanHelp': '¿Cómo puedo ayudarte?',
        'error': 'Lo siento, ocurrió un error. Por favor, inténtalo de nuevo.',
        'popularPortals': 'Portales de empleo populares',
        'jobTypes': 'Tipos de trabajo',
        'portals': {
            'profesia': 'InfoJobs - Estudiantes',
            'studentjob': 'StudentJob.es',
            'brigada': 'Indeed España',
            'kariera': 'Trabajos.com'
        },
        'types': {
            'parttime': 'Tiempo parcial',
            'brigada': 'Trabajo temporal',
            'seasonal': 'Trabajo de temporada',
            'homeoffice': 'Teletrabajo'
        }
    },
    'uk': {
        'title': 'Підробіток для студентів',
        'subtitle': 'Знайди ідеальну part-time роботу',
        'searchIn': 'Пошук в місті',
        'back': 'Назад',
        'chatTitle': 'Чат з консультантом',
        'chatSubtitle': 'Розкажи, яку роботу шукаєш, і я допоможу знайти найкращі варіанти',
        'placeholder': 'Напиши своє питання...',
        'send': 'Відправити',
        'greeting': 'Привіт {name}! Я твій асистент для пошуку підробітку та part-time роботи.',
        'greetingWithContext': 'Бачу, що ти цікавився {university} в місті {city}. Можу допомогти знайти роботу саме в {city}!',
        'howCanHelp': 'Як я можу допомогти?',
        'error': 'Вибачте, сталася помилка. Спробуйте ще раз.',
        'popularPortals': 'Популярні портали',
        'jobTypes': 'Типи робіт',
        'portals': {
            'profesia': 'Robota.ua - Для студентів',
            'studentjob': 'Work.ua',
            'brigada': 'Jooble.ua',
            'kariera': 'Rabota.ua'
        },
        'types': {
            'parttime': 'Part-time (неповний робочий день)',
            'brigada': 'Підробіток (тимчасова робота)',
            'seasonal': 'Сезонна робота',
            'homeoffice': 'Home office (віддалена)'
        }
    },
    'it': {
        'title': 'Lavori per studenti',
        'subtitle': 'Trova il lavoro part-time perfetto',
        'searchIn': 'Ricerca in',
        'back': 'Indietro',
        'chatTitle': 'Chat con consulente',
        'chatSubtitle': 'Dimmi che lavoro cerchi e ti aiuterò a trovare le migliori opzioni',
        'placeholder': 'Scrivi la tua domanda...',
        'send': 'Invia',
        'greeting': 'Ciao {name}! Sono il tuo assistente per trovare lavori part-time.',
        'greetingWithContext': 'Vedo che ti sei interessato a {university} a {city}. Posso aiutarti a trovare lavori a {city}!',
        'howCanHelp': 'Come posso aiutarti?',
        'error': 'Scusa, si è verificato un errore. Riprova.',
        'popularPortals': 'Portali di lavoro popolari',
        'jobTypes': 'Tipi di lavoro',
        'portals': {
            'profesia': 'Indeed Italia - Studenti',
            'studentjob': 'StudentJob.it',
            'brigada': 'InfoJobs.it',
            'kariera': 'Monster.it'
        },
        'types': {
            'parttime': 'Part-time',
            'brigada': 'Lavoro temporaneo',
            'seasonal': 'Lavoro stagionale',
            'homeoffice': 'Lavoro da remoto'
        }
    },
    'ru': {
        'title': 'Подработка для студентов',
        'subtitle': 'Найди идеальную работу на неполный рабочий день',
        'searchIn': 'Поиск в городе',
        'back': 'Назад',
        'chatTitle': 'Чат с консультантом',
        'chatSubtitle': 'Расскажи, какую работу ищешь, и я помогу найти лучшие варианты',
        'placeholder': 'Напиши свой вопрос...',
        'send': 'Отправить',
        'greeting': 'Привет {name}! Я твой ассистент для поиска подработки и работы на неполный рабочий день.',
        'greetingWithContext': 'Вижу, что ты интересовался {university} в городе {city}. Могу помочь найти работу именно в {city}!',
        'howCanHelp': 'Как я могу помочь?',
        'error': 'Извините, произошла ошибка. Попробуйте еще раз.',
        'popularPortals': 'Популярные порталы',
        'jobTypes': 'Типы работ',
        'portals': {
            'profesia': 'HeadHunter - Для студентов',
            'studentjob': 'Superjob',
            'brigada': 'Rabota.ru',
            'kariera': 'Zarplata.ru'
        },
        'types': {
            'parttime': 'Part-time (неполный рабочий день)',
            'brigada': 'Подработка (временная работа)',
            'seasonal': 'Сезонная работа',
            'homeoffice': 'Удаленная работа'
        }
    }
}

def add_jobs_translations():
    """Add Jobs page translations to all language files"""
    
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
            # Read existing translations
            if os.path.exists(lang_file):
                with open(lang_file, 'r', encoding='utf-8-sig') as f:
                    data = json.load(f)
            else:
                print(f"[!] File not found: {lang_file}")
                continue
            
            # Update jobs section
            data['jobs'] = translations
            
            # Write back to file
            with open(lang_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"[+] Updated {lang_code}/common.json with Jobs translations")
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
    print("Adding Jobs page translations to all 10 languages...\n")
    add_jobs_translations()
    print("\nDone! Jobs translations added successfully.")
