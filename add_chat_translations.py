#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

# Chat modal translations
chat_translations = {
    'en': {
        "chat": {
            "title": "University Consultant",
            "welcome": "Hello! I'm your AI consultant for {university}. Ask me about admission requirements, programs, fees, or deadlines.",
            "placeholder": "Ask about admission, programs, deadlines...",
            "send": "Send",
            "error": "Sorry, I couldn't process your request. Please try again."
        }
    },
    'sk': {
        "chat": {
            "title": "Univerzitný konzultant",
            "welcome": "Ahoj! Som váš AI konzultant pre {university}. Opýtajte sa ma na prijímacie požiadavky, programy, poplatky alebo termíny.",
            "placeholder": "Opýtajte sa na prijímanie, programy, termíny...",
            "send": "Odoslať",
            "error": "Prepáčte, nemohol som spracovať vašu požiadavku. Skúste to prosím znova."
        }
    },
    'cs': {
        "chat": {
            "title": "Univerzitní konzultant",
            "welcome": "Ahoj! Jsem váš AI konzultant pro {university}. Zeptejte se mě na přijímací požadavky, programy, poplatky nebo termíny.",
            "placeholder": "Zeptejte se na přijímání, programy, termíny...",
            "send": "Odeslat",
            "error": "Omlouváme se, nemohl jsem zpracovat váš požadavek. Zkuste to prosím znovu."
        }
    },
    'pl': {
        "chat": {
            "title": "Konsultant uniwersytecki",
            "welcome": "Cześć! Jestem twoim konsultantem AI dla {university}. Zapytaj mnie o wymagania rekrutacyjne, programy, opłaty lub terminy.",
            "placeholder": "Zapytaj o rekrutację, programy, terminy...",
            "send": "Wyślij",
            "error": "Przepraszamy, nie mogłem przetworzyć twojego żądania. Spróbuj ponownie."
        }
    },
    'de': {
        "chat": {
            "title": "Universitätsberater",
            "welcome": "Hallo! Ich bin Ihr KI-Berater für {university}. Fragen Sie mich nach Zulassungsvoraussetzungen, Programmen, Gebühren oder Fristen.",
            "placeholder": "Fragen Sie nach Zulassung, Programmen, Fristen...",
            "send": "Senden",
            "error": "Entschuldigung, ich konnte Ihre Anfrage nicht verarbeiten. Bitte versuchen Sie es erneut."
        }
    },
    'fr': {
        "chat": {
            "title": "Consultant universitaire",
            "welcome": "Bonjour! Je suis votre consultant IA pour {university}. Posez-moi des questions sur les conditions d'admission, les programmes, les frais ou les délais.",
            "placeholder": "Posez des questions sur l'admission, les programmes, les délais...",
            "send": "Envoyer",
            "error": "Désolé, je n'ai pas pu traiter votre demande. Veuillez réessayer."
        }
    },
    'es': {
        "chat": {
            "title": "Consultor universitario",
            "welcome": "¡Hola! Soy tu consultor de IA para {university}. Pregúntame sobre requisitos de admisión, programas, tarifas o plazos.",
            "placeholder": "Pregunte sobre admisión, programas, plazos...",
            "send": "Enviar",
            "error": "Lo siento, no pude procesar su solicitud. Por favor, inténtelo de nuevo."
        }
    },
    'it': {
        "chat": {
            "title": "Consulente universitario",
            "welcome": "Ciao! Sono il tuo consulente IA per {university}. Chiedimi informazioni sui requisiti di ammissione, programmi, tasse o scadenze.",
            "placeholder": "Chiedi informazioni su ammissione, programmi, scadenze...",
            "send": "Invia",
            "error": "Spiacente, non sono riuscito a elaborare la tua richiesta. Riprova."
        }
    },
    'uk': {
        "chat": {
            "title": "Університетський консультант",
            "welcome": "Привіт! Я ваш AI консультант для {university}. Запитайте мене про вимоги до вступу, програми, плату або терміни.",
            "placeholder": "Запитайте про вступ, програми, терміни...",
            "send": "Надіслати",
            "error": "Вибачте, я не зміг обробити ваш запит. Будь ласка, спробуйте ще раз."
        }
    },
    'ru': {
        "chat": {
            "title": "Университетский консультант",
            "welcome": "Привет! Я ваш AI консультант для {university}. Спросите меня о требованиях к поступлению, программах, оплате или сроках.",
            "placeholder": "Спросите о поступлении, программах, сроках...",
            "send": "Отправить",
            "error": "Извините, я не смог обработать ваш запрос. Пожалуйста, попробуйте еще раз."
        }
    }
}

# Process each language
base_path = r"C:\Users\info\OneDrive\Dokumenty\Student\frontend\locales"
for lang, translations in chat_translations.items():
    file_path = os.path.join(base_path, lang, "common.json")
    
    # Read existing file
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    # Add university.chat section
    if 'university' not in data:
        data['university'] = {}
    data['university']['chat'] = translations['chat']
    
    # Write back with UTF-8
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Updated {lang}/common.json with chat translations")

print("\nSUCCESS: All translation files updated with chat modal translations!")
