#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Housing Chat Service
Conversational housing consultant for students
"""

import os
from typing import List, Dict, Optional
from openai import AsyncOpenAI


class HousingChatService:
    """Conversational housing consultant service"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    async def chat(
        self,
        message: str,
        conversation_history: List[Dict],
        user_name: str,
        language: str = 'sk',
        jurisdiction: str = 'SK',
        db = None,
        city: str = None
    ) -> str:
        """
        Process user message and generate AI response with RAG
        
        Args:
            message: User's message
            conversation_history: Previous messages in conversation
            user_name: User's name for personalization
            language: User's language preference
            jurisdiction: User's country code (SK, CZ, PL, etc.)
            db: Database session (optional, for RAG)
            city: City name for agency search (optional)
            
        Returns:
            AI assistant's response
        """
        
        print(f"🔍 DEBUG: db={db is not None}, city={city}, jurisdiction={jurisdiction}")
        
        # AUTO-DETECT CITY if not provided (like Jobs AI)
        if db and not city:
            print(f"🔍 Attempting city detection...")
            try:
                from services.jobs_chat_service import JobsChatService
                jobs_service = JobsChatService()
                city = jobs_service._extract_city_from_message(message, jurisdiction)
                if city:
                    print(f"🏠 Auto-detected city: {city}")
                else:
                    print(f"⚠️ City detection returned None")
            except Exception as e:
                print(f"⚠️ City detection error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"⚠️ Skipping city detection: db={db is not None}, city={city}")
        
        # Retrieve housing agencies context from database if city provided
        agencies_context = ""
        if db and city:
            agencies_context = self._get_agencies_context(db, city, jurisdiction)
        
        # System prompt - defines AI behavior with RAG context
        system_prompt = self._get_system_prompt(language, user_name, jurisdiction, agencies_context)
        
        # Build messages for OpenAI
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,  # Balanced between creative and factual
                max_tokens=800
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error in housing chat: {e}")
            return self._get_error_message(language)
    
    def _get_agencies_context(self, db, city: str, country_code: str = 'SK') -> str:
        """
        Retrieve housing agencies from database for given city
        
        Args:
            db: Database session
            city: City name
            country_code: Country code (default: SK)
            
        Returns:
            Formatted context with real agencies data
        """
        try:
            from main import RealEstateAgency
            
            # Query database for housing agencies in this city
            agencies = db.query(RealEstateAgency).filter(
                RealEstateAgency.city == city,
                RealEstateAgency.country_code == country_code,
                RealEstateAgency.is_active == True
            ).all()
            
            if not agencies:
                return f"No housing agencies found in database for {city}."
            
            # Format agencies data for AI context
            context = f"VERIFIED HOUSING AGENCIES IN {city.upper()}:\n\n"
            for agency in agencies:
                context += f"• {agency.name}\n"
                context += f"  Website: {agency.website_url}\n"
                if agency.description:
                    context += f"  Description: {agency.description}\n"
                if agency.specialization:
                    context += f"  Specialization: {agency.specialization}\n"
                if agency.phone:
                    context += f"  Phone: {agency.phone}\n"
                if agency.email:
                    context += f"  Email: {agency.email}\n"
                context += "\n"
            
            return context
            
        except Exception as e:
            print(f"Error retrieving housing agencies: {e}")
            return "Database error - unable to retrieve agencies."
    
    def _get_system_prompt(self, language: str, user_name: str, jurisdiction: str, agencies_context: str = "") -> str:
        """Get system prompt in user's language"""
        
        # Map jurisdiction codes to country names in multiple languages
        country_names = {
            'SK': {'sk': 'Slovensku', 'cs': 'Slovensku', 'en': 'Slovakia', 'uk': 'Словаччині', 'ru': 'Словакии'},
            'CZ': {'sk': 'Česku', 'cs': 'Česku', 'en': 'Czech Republic', 'uk': 'Чехії', 'ru': 'Чехии'},
            'PL': {'sk': 'Poľsku', 'cs': 'Polsku', 'en': 'Poland', 'uk': 'Польщі', 'ru': 'Польше'},
            'DE': {'sk': 'Nemecku', 'cs': 'Německu', 'en': 'Germany', 'uk': 'Німеччині', 'ru': 'Германии'},
            'AT': {'sk': 'Rakúsku', 'cs': 'Rakousku', 'en': 'Austria', 'uk': 'Австрії', 'ru': 'Австрии'},
            'CH': {'sk': 'Švajčiarsku', 'cs': 'Švýcarsku', 'en': 'Switzerland', 'uk': 'Швейцарії', 'ru': 'Швейцарии'},
            'FR': {'sk': 'Francúzsku', 'cs': 'Francii', 'en': 'France', 'uk': 'Франції', 'ru': 'Франции'},
            'IT': {'sk': 'Taliansku', 'cs': 'Itálii', 'en': 'Italy', 'uk': 'Італії', 'ru': 'Италии'},
            'ES': {'sk': 'Španielsku', 'cs': 'Španělsku', 'en': 'Spain', 'uk': 'Іспанії', 'ru': 'Испании'},
            'PT': {'sk': 'Portugalsku', 'cs': 'Portugalsku', 'en': 'Portugal', 'uk': 'Португалії', 'ru': 'Португалии'},
            'GB': {'sk': 'Veľkej Británii', 'cs': 'Velké Británii', 'en': 'United Kingdom', 'uk': 'Великій Британії', 'ru': 'Великобритании'},
            'IE': {'sk': 'Írsku', 'cs': 'Irsku', 'en': 'Ireland', 'uk': 'Ірландії', 'ru': 'Ирландии'},
            'NL': {'sk': 'Holandsku', 'cs': 'Nizozemsku', 'en': 'Netherlands', 'uk': 'Нідерландах', 'ru': 'Нидерландах'},
            'BE': {'sk': 'Belgicku', 'cs': 'Belgii', 'en': 'Belgium', 'uk': 'Бельгії', 'ru': 'Бельгии'},
            'LU': {'sk': 'Luxembursku', 'cs': 'Lucembursku', 'en': 'Luxembourg', 'uk': 'Люксембурзі', 'ru': 'Люксембурге'},
            'SE': {'sk': 'Švédsku', 'cs': 'Švédsku', 'en': 'Sweden', 'uk': 'Швеції', 'ru': 'Швеции'},
            'DK': {'sk': 'Dánsku', 'cs': 'Dánsku', 'en': 'Denmark', 'uk': 'Данії', 'ru': 'Дании'},
            'NO': {'sk': 'Nórsku', 'cs': 'Norsku', 'en': 'Norway', 'uk': 'Норвегії', 'ru': 'Норвегии'},
            'FI': {'sk': 'Fínsku', 'cs': 'Finsku', 'en': 'Finland', 'uk': 'Фінляндії', 'ru': 'Финляндии'},
            'GR': {'sk': 'Grécku', 'cs': 'Řecku', 'en': 'Greece', 'uk': 'Греції', 'ru': 'Греции'},
            'HU': {'sk': 'Maďarsku', 'cs': 'Maďarsku', 'en': 'Hungary', 'uk': 'Угорщині', 'ru': 'Венгрии'},
            'SI': {'sk': 'Slovinsku', 'cs': 'Slovinsku', 'en': 'Slovenia', 'uk': 'Словенії', 'ru': 'Словении'},
            'HR': {'sk': 'Chorvátsku', 'cs': 'Chorvatsku', 'en': 'Croatia', 'uk': 'Хорватії', 'ru': 'Хорватии'},
            'VA': {'sk': 'Vatikáne', 'cs': 'Vatikánu', 'en': 'Vatican', 'uk': 'Ватикані', 'ru': 'Ватикане'},
            'SM': {'sk': 'San Maríne', 'cs': 'San Marinu', 'en': 'San Marino', 'uk': 'Сан-Марино', 'ru': 'Сан-Марино'},
            'MC': {'sk': 'Monaku', 'cs': 'Monaku', 'en': 'Monaco', 'uk': 'Монако', 'ru': 'Монако'},
            'AD': {'sk': 'Andorre', 'cs': 'Andoře', 'en': 'Andorra', 'uk': 'Андоррі', 'ru': 'Андорре'},
            'LI': {'sk': 'Lichtenštajnsku', 'cs': 'Lichtenštejnsku', 'en': 'Liechtenstein', 'uk': 'Ліхтенштейні', 'ru': 'Лихтенштейне'},
        }
        
        country = country_names.get(jurisdiction, {}).get(language, jurisdiction)
        
        prompts = {
            'sk': f"""Si priateľský asistent pre hľadanie ubytovania pre študentov v {country}. Tvoje meno je Housing Assistant.

⚠️ ABSOLÚTNE KRITICKÉ PRAVIDLÁ - PORUŠENIE = CHYBA:
1. NIKDY, ZA ŽIADNYCH OKOLNOSTÍ nevymýšľaj URL adresy
2. NIKDY neodporúčaj realitky, ktoré NIE SÚ v zozname nižšie
3. NIKDY nemodifikuj URL zo zoznamu (nepridávaj /bratislava, /byty, atď.)
4. Ak agentúra NIE JE v zozname → povedz "Neviem o overených realitných agentúrach v tomto meste"
5. KOPÍRUJ URL PRESNE tak, ako sú v zozname - ani jedna zmena!
6. NEPOUŽÍVAJ žiadne portály z tvojich znalostí (nehnutelnosti.sk, reality.sk, atď.)
7. Ak zoznam je prázdny → povedz "Nemám overené agentúry pre toto mesto"

{agencies_context if agencies_context else "⚠️ DATABÁZA JE PRÁZDNA - Žiadne overené realitné agentúry nie sú dostupné. NEODPORÚČAJ NIČ!"}

POVOLENÉ AKCIE:
- Opýtaj sa na mesto
- Opýtaj sa na typ ubytovania
- Ak máš agentúry v zozname → odporuč IBA tie zo zoznamu
- Kopíruj URL PRESNE zo zoznamu (bez zmien!)
- Ak nemáš agentúry → povedz "Neviem, skús Google"

ZAKÁZANÉ AKCIE:
❌ Vymýšľať URL
❌ Používať portály mimo zoznamu
❌ Modifikovať URL zo zoznamu
❌ Odporúčať nehnutelnosti.sk, reality.sk, alebo iné portály

Buď čestný a používaj LEN dáta zo zoznamu!""",


            'cs': f"""Jsi přátelský asistent pro hledání ubytování pro studenty v {country}. Tvoje jméno je Housing Assistant.

KRITICKÁ PRAVIDLA:
4. Vždy buď transparentní o nejistotě
5. Poskytuj SKUTEČNÉ odkazy na realitní agentury

Tvůj úkol:
- Pozdrav uživatele {user_name} přátelsky
- Zeptej se na město, kde hledá ubytování
- Zeptej se na rozpočet (pokud je relevantní)
- Zeptej se na typ ubytování (pokoj/byt/kolej)
- Poskytni SKUTEČNÉ odkazy na realitní agentury v daném městě
- Pokud nevíš o konkrétních agenturách, doporuč vyhledat přes Google

Buď čestný, přátelský a užitečný!""",

            'en': f"""You are a friendly housing search assistant for students. Your name is Housing Assistant.

CRITICAL RULES:
1. NEVER make up information or URLs
2. If you don't know something for certain, say "I don't know" and recommend Google
3. Provide ONLY verified information
4. Always be transparent about uncertainty
5. Provide REAL links to real estate agencies

Your task:
- Greet user {user_name} in a friendly way
- Ask about the city where they're looking for accommodation
- Ask about budget (if relevant)
- Ask about type of accommodation (room/apartment/dormitory)
- Provide REAL links to real estate agencies in that city
- If you don't know about specific agencies, recommend searching via Google

Be honest, friendly, and helpful!""",

            'uk': f"""Ти дружній асистент з пошуку житла для студентів. Твоє ім'я Housing Assistant.

КРИТИЧНІ ПРАВИЛА:
1. НІКОЛИ не вигадуй інформацію або URL адреси
2. Якщо чогось не знаєш напевно, скажи "Не знаю" і порадь Google
3. Надавай ЛИШЕ перевірену інформацію
4. Завжди будь прозорим щодо невпевненості
5. Надавай РЕАЛЬНІ посилання на агентства нерухомості

Твоє завдання:
- Привітай користувача {user_name} дружньо
- Запитай про місто, де шукає житло
- Запитай про бюджет (якщо релевантно)
- Запитай про тип житла (кімната/квартира/гуртожиток)
- Надай РЕАЛЬНІ посилання на агентства нерухомості в тому місті
- Якщо не знаєш про конкретні агентства, порадь пошукати через Google

Будь чесним, дружнім та корисним!""",

            'pl': f"""Jesteś przyjaznym asystentem w poszukiwaniu zakwaterowania dla studentów. Twoje imię to Housing Assistant.

KRYTYCZNE ZASADY:
1. NIGDY nie wymyślaj informacji ani adresów URL
2. Jeśli czegoś nie wiesz na pewno, powiedz "Nie wiem" i zaproponuj Google
3. Podawaj TYLKO zweryfikowane informacje
4. Zawsze bądź transparentny co do niepewności
5. Podawaj PRAWDZIWE linki do agencji nieruchomości

Twoje zadanie:
- Przywitaj użytkownika {user_name} w przyjazny sposób
- Zapytaj o miasto, w którym szuka zakwaterowania
- Zapytaj o budżet (jeśli istotne)
- Zapytaj o typ zakwaterowania (pokój/mieszkanie/akademik)
- Podaj PRAWDZIWE linki do agencji nieruchomości w tym mieście
- Jeśli nie znasz konkretnych agencji, zaproponuj wyszukanie przez Google

Bądź szczery, przyjazny i pomocny!"""
        }
        
        return prompts.get(language, prompts['en'])
    
    def _get_error_message(self, language: str) -> str:
        """Get error message in user's language"""
        messages = {
            'sk': 'Prepáčte, nastala chyba. Skúste to prosím znova alebo kontaktujte podporu.',
            'cs': 'Promiňte, nastala chyba. Zkuste to prosím znovu nebo kontaktujte podporu.',
            'en': 'Sorry, an error occurred. Please try again or contact support.',
            'uk': 'Вибачте, сталася помилка. Спробуйте ще раз або зв\'яжіться з підтримкою.',
            'pl': 'Przepraszamy, wystąpił błąd. Spróbuj ponownie lub skontaktuj się z pomocą techniczną.',
            'de': 'Entschuldigung, ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut oder kontaktieren Sie den Support.',
            'fr': 'Désolé, une erreur s\'est produite. Veuillez réessayer ou contacter le support.',
            'es': 'Lo siento, ocurrió un error. Por favor, inténtalo de nuevo o contacta con soporte.',
            'it': 'Spiacente, si è verificato un errore. Riprova o contatta il supporto.',
            'ru': 'Извините, произошла ошибка. Пожалуйста, попробуйте снова или свяжитесь с поддержкой.'
        }
        return messages.get(language, messages['en'])
