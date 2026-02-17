#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update AI Consultant translations to remove "AI" prefix
Changes "AI Consultant" to just "Consultant" in all 10 languages
"""

import json
import os

# Translation updates - removing "AI" from all languages
translations = {
    'sk': {
        'university': {
            'aiConsultant': 'Konzultant',
            'chat': {
                'title': 'Univerzitný konzultant',
                'welcome': 'Ahoj! Som váš konzultant pre {university}. Opýtajte sa ma na prijímanie, požiadavky, programy, poplatky alebo termíny.',
                'placeholder': 'Opýtajte sa na prijímanie, programy, termíny...',
                'send': 'Odoslať',
                'error': 'Prepáčte, nastala chyba. Skúste to prosím znova.'
            }
        }
    },
    'en': {
        'university': {
            'aiConsultant': 'Consultant',
            'chat': {
                'title': 'University Consultant',
                'welcome': 'Hello! I am your consultant for {university}. Ask me about admissions, requirements, programs, fees, or deadlines.',
                'placeholder': 'Ask about admissions, programs, deadlines...',
                'send': 'Send',
                'error': 'Sorry, an error occurred. Please try again.'
            }
        }
    },
    'cs': {
        'university': {
            'aiConsultant': 'Konzultant',
            'chat': {
                'title': 'Univerzitní konzultant',
                'welcome': 'Ahoj! Jsem váš konzultant pro {university}. Zeptejte se mě na přijímání, požadavky, programy, poplatky nebo termíny.',
                'placeholder': 'Zeptejte se na přijímání, programy, termíny...',
                'send': 'Odeslat',
                'error': 'Omlouváme se, došlo k chybě. Zkuste to prosím znovu.'
            }
        }
    },
    'pl': {
        'university': {
            'aiConsultant': 'Konsultant',
            'chat': {
                'title': 'Konsultant uniwersytecki',
                'welcome': 'Cześć! Jestem twoim konsultantem dla {university}. Zapytaj mnie o przyjęcia, wymagania, programy, opłaty lub terminy.',
                'placeholder': 'Zapytaj o przyjęcia, programy, terminy...',
                'send': 'Wyślij',
                'error': 'Przepraszamy, wystąpił błąd. Spróbuj ponownie.'
            }
        }
    },
    'de': {
        'university': {
            'aiConsultant': 'Berater',
            'chat': {
                'title': 'Universitätsberater',
                'welcome': 'Hallo! Ich bin Ihr Berater für {university}. Fragen Sie mich nach Zulassungen, Anforderungen, Programmen, Gebühren oder Fristen.',
                'placeholder': 'Fragen Sie nach Zulassungen, Programmen, Fristen...',
                'send': 'Senden',
                'error': 'Entschuldigung, ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.'
            }
        }
    },
    'fr': {
        'university': {
            'aiConsultant': 'Consultant',
            'chat': {
                'title': 'Consultant universitaire',
                'welcome': 'Bonjour! Je suis votre consultant pour {university}. Posez-moi des questions sur les admissions, les exigences, les programmes, les frais ou les délais.',
                'placeholder': 'Posez des questions sur les admissions, les programmes, les délais...',
                'send': 'Envoyer',
                'error': 'Désolé, une erreur s\'est produite. Veuillez réessayer.'
            }
        }
    },
    'es': {
        'university': {
            'aiConsultant': 'Consultor',
            'chat': {
                'title': 'Consultor universitario',
                'welcome': '¡Hola! Soy tu consultor para {university}. Pregúntame sobre admisiones, requisitos, programas, tarifas o plazos.',
                'placeholder': 'Pregunta sobre admisiones, programas, plazos...',
                'send': 'Enviar',
                'error': 'Lo siento, ocurrió un error. Por favor, inténtalo de nuevo.'
            }
        }
    },
    'it': {
        'university': {
            'aiConsultant': 'Consulente',
            'chat': {
                'title': 'Consulente universitario',
                'welcome': 'Ciao! Sono il tuo consulente per {university}. Chiedimi informazioni su ammissioni, requisiti, programmi, tasse o scadenze.',
                'placeholder': 'Chiedi informazioni su ammissioni, programmi, scadenze...',
                'send': 'Invia',
                'error': 'Spiacenti, si è verificato un errore. Riprova.'
            }
        }
    },
    'uk': {
        'university': {
            'aiConsultant': 'Консультант',
            'chat': {
                'title': 'Університетський консультант',
                'welcome': 'Привіт! Я ваш консультант для {university}. Запитайте мене про вступ, вимоги, програми, вартість або терміни.',
                'placeholder': 'Запитайте про вступ, програми, терміни...',
                'send': 'Надіслати',
                'error': 'Вибачте, сталася помилка. Будь ласка, спробуйте ще раз.'
            }
        }
    },
    'ru': {
        'university': {
            'aiConsultant': 'Консультант',
            'chat': {
                'title': 'Университетский консультант',
                'welcome': 'Привет! Я ваш консультант для {university}. Спросите меня о приеме, требованиях, программах, стоимости или сроках.',
                'placeholder': 'Спросите о приеме, программах, сроках...',
                'send': 'Отправить',
                'error': 'Извините, произошла ошибка. Пожалуйста, попробуйте снова.'
            }
        }
    }
}

def update_translation_file(lang_code, translations_data):
    """Update a single translation file"""
    file_path = f'C:/Users/info/OneDrive/Dokumenty/Student/frontend/locales/{lang_code}/common.json'
    
    try:
        # Read existing file
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        
        # Update university section
        if 'university' not in data:
            data['university'] = {}
        
        data['university'].update(translations_data['university'])
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f'[OK] Updated {lang_code}/common.json')
        return True
        
    except Exception as e:
        print(f'[ERROR] Error updating {lang_code}/common.json: {e}')
        return False

def main():
    """Update all translation files"""
    print('Updating translations to remove "AI" prefix...\n')
    
    success_count = 0
    for lang_code, trans_data in translations.items():
        if update_translation_file(lang_code, trans_data):
            success_count += 1
    
    print(f'\n[OK] Successfully updated {success_count}/{len(translations)} language files')
    print('Changes: "AI Consultant" -> "Consultant" in all languages')

if __name__ == '__main__':
    main()
