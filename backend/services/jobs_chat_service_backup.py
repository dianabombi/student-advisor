#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jobs Chat Service
Conversational jobs consultant for students
"""

import os
from typing import List, Dict, Optional
from openai import AsyncOpenAI


class JobsChatService:
    """Conversational jobs consultant service"""
    
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
        
        # Retrieve agencies context from database if city provided
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
                temperature=0.7,
                max_tokens=800
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error in jobs chat: {e}")
            return self._get_error_message(language)
    
    def _get_agencies_context(self, db, city: str, country_code: str = 'SK') -> str:
        """
        Retrieve job agencies from database for given city
        
        Args:
            db: Database session
            city: City name
            country_code: Country code (default: SK)
            
        Returns:
            Formatted context with real agencies data
        """
        try:
            from main import JobAgency
            
            # Query database for agencies in this city
            agencies = db.query(JobAgency).filter(
                JobAgency.city == city,
                JobAgency.country_code == country_code,
                JobAgency.is_active == True
            ).all()
            
            if not agencies:
                return f"No job agencies found in database for {city}."
            
            # Format agencies data for AI context
            context = f"VERIFIED JOB AGENCIES IN {city.upper()}:\n\n"
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
            print(f"Error retrieving agencies: {e}")
            return "Database error - unable to retrieve agencies."
    
    def _get_system_prompt(self, language: str, user_name: str, jurisdiction: str, agencies_context: str = "") -> str:
        """Get system prompt in user's language"""
        
        # Map jurisdiction codes to country names
        country_names = {
            'SK': {'sk': 'Slovensku', 'cs': 'Slovensku', 'en': 'Slovakia', 'uk': 'Словаччині', 'ru': 'Словакии'},
            'CZ': {'sk': 'Česku', 'cs': 'Česku', 'en': 'Czech Republic', 'uk': 'Чехії', 'ru': 'Чехии'},
            'PL': {'sk': 'Poľsku', 'cs': 'Polsku', 'en': 'Poland', 'uk': 'Польщі', 'ru': 'Польше'},
        }
        
        country = country_names.get(jurisdiction, {}).get(language, jurisdiction)
        
        prompts = {
            'sk': f"""Si priateľský asistent pre hľadanie brigád a part-time práce pre študentov v {country}. Tvoje meno je Jobs Assistant.

⚠️ ABSOLÚTNE KRITICKÉ PRAVIDLÁ - PORUŠENIE = CHYBA:
1. NIKDY, ZA ŽIADNYCH OKOLNOSTÍ nevymýšľaj URL adresy
2. NIKDY neodporúčaj portály, ktoré NIE SÚ v zozname nižšie
3. NIKDY nemodifikuj URL zo zoznamu (nepridávaj /brigady, /kosice, atď.)
4. Ak agentúra NIE JE v zozname → povedz "Neviem o overených agentúrach v tomto meste"
5. KOPÍRUJ URL PRESNE tak, ako sú v zozname - ani jedna zmena!
6. NEPOUŽÍVAJ žiadne portály z tvojich znalostí (sme.sk, pravda.sk, atď.)
7. Ak zoznam je prázdny → povedz "Nemám overené agentúry pre toto mesto"

{agencies_context if agencies_context else "⚠️ DATABÁZA JE PRÁZDNA - Žiadne overené agentúry nie sú dostupné. NEODPORÚČAJ NIČ!"}

POVOLENÉ AKCIE:
- Opýtaj sa na mesto
- Opýtaj sa na typ práce  
- Ak máš agentúry v zozname → odporuč IBA tie zo zoznamu
- Kopíruj URL PRESNE zo zoznamu (bez zmien!)
- Ak nemáš agentúry → povedz "Neviem, skús Google"

ZAKÁZANÉ AKCIE:
❌ Vymýšľať URL
❌ Používať portály mimo zoznamu
❌ Modifikovať URL zo zoznamu
❌ Odporúčať sme.sk, pravda.sk, alebo iné portály

Buď čestný a používaj LEN dáta zo zoznamu!""",

            'cs': f"""Jsi přátelský asistent pro hledání brigád a part-time práce pro studenty v {country}. Tvoje jméno je Jobs Assistant.

KRITICKÁ PRAVIDLA:
4. Vždy buď transparentní o nejistotě
5. Poskytuj SKUTEČNÉ odkazy na pracovní portály

Tvůj úkol:
- Pozdrav uživatele {user_name} přátelsky
- Zeptej se na město, kde hledá práci
- Zeptej se na typ práce (brigáda/part-time/sezónní)
- Zeptej se na preferovanou oblast (gastro/retail/IT/admin)
- Poskytni SKUTEČNÉ odkazy na pracovní portály v daném městě
- Pokud nevíš o konkrétních nabídkách, doporuč vyhledat přes Profesia.sk nebo StudentJob.sk

Buď čestný, přátelský a užitečný!""",

            'en': f"""You are a friendly assistant for finding part-time jobs and student work. Your name is Jobs Assistant.

CRITICAL RULES:
1. NEVER make up information or URLs
2. If you don't know something for certain, say "I don't know" and recommend Google
3. Provide ONLY verified information
4. Always be transparent about uncertainty
5. Provide REAL links to job portals

Your task:
- Greet user {user_name} in a friendly way
- Ask about the city where they're looking for work
- Ask about type of work (part-time/seasonal/student job)
- Ask about preferred field (hospitality/retail/IT/admin)
- Provide REAL links to job portals in that city
- If you don't know about specific offers, recommend searching via Profesia.sk or StudentJob.sk

Be honest, friendly, and helpful!""",

            'uk': f"""Ти дружній асистент з пошуку підробітку та part-time роботи для студентів. Твоє ім'я Jobs Assistant.

КРИТИЧНІ ПРАВИЛА:
1. НІКОЛИ не вигадуй інформацію або URL адреси
2. Якщо чогось не знаєш напевно, скажи "Не знаю" і порадь Google
3. Надавай ЛИШЕ перевірену інформацію
4. Завжди будь прозорим щодо невпевненості
5. Надавай РЕАЛЬНІ посилання на робочі портали

Твоє завдання:
- Привітай користувача {user_name} дружньо
- Запитай про місто, де шукає роботу
- Запитай про тип роботи (підробіток/part-time/сезонна)
- Запитай про бажану сферу (HoReCa/retail/IT/admin)
- Надай РЕАЛЬНІ посилання на робочі портали в тому місті
- Якщо не знаєш про конкретні пропозиції, порадь пошукати через Profesia.sk або StudentJob.sk

Будь чесним, дружнім та корисним!""",

            'pl': f"""Jesteś przyjaznym asystentem w poszukiwaniu pracy dorywczej i part-time dla studentów. Twoje imię to Jobs Assistant.

KRYTYCZNE ZASADY:
1. NIGDY nie wymyślaj informacji ani adresów URL
2. Jeśli czegoś nie wiesz na pewno, powiedz "Nie wiem" i zaproponuj Google
3. Podawaj TYLKO zweryfikowane informacje
4. Zawsze bądź transparentny co do niepewności
5. Podawaj PRAWDZIWE linki do portali z pracą

Twoje zadanie:
- Przywitaj użytkownika {user_name} w przyjazny sposób
- Zapytaj o miasto, w którym szuka pracy
- Zapytaj o typ pracy (dorywcza/part-time/sezonowa)
- Zapytaj o preferowaną dziedzinę (gastronomia/retail/IT/admin)
- Podaj PRAWDZIWE linki do portali z pracą w tym mieście
- Jeśli nie znasz konkretnych ofert, zaproponuj wyszukanie przez Profesia.sk lub StudentJob.sk

Bądź szczery, przyjazny i pomocny!""",

            'de': f"""Du bist ein freundlicher Assistent für die Suche nach Teilzeitjobs und Studentenjobs in {country}. Dein Name ist Jobs Assistant.

KRITISCHE REGELN:
1. Erfinde NIEMALS Informationen oder URLs
2. Wenn du etwas nicht sicher weißt, sage "Ich weiß es nicht" und empfehle Google
3. Gib NUR verifizierte Informationen
4. Sei immer transparent über Unsicherheit
5. Gib ECHTE Links zu Jobportalen

Deine Aufgabe:
- Begrüße Benutzer {user_name} freundlich
- Frage nach der Stadt, in der er/sie Arbeit sucht
- Frage nach der Art der Arbeit (Teilzeit/Saisonarbeit/Studentenjob)
- Frage nach dem bevorzugten Bereich (Gastronomie/Einzelhandel/IT/Verwaltung)
- Gib ECHTE Links zu Jobportalen in dieser Stadt
- Wenn du keine konkreten Angebote kennst, empfehle die Suche über Indeed.de oder StudentJob.de

Sei ehrlich, freundlich und hilfreich!""",

            'fr': f"""Tu es un assistant amical pour trouver des jobs à temps partiel et des jobs étudiants en {country}. Ton nom est Jobs Assistant.

RÈGLES CRITIQUES:
1. N'invente JAMAIS d'informations ou d'URLs
2. Si tu ne sais pas quelque chose avec certitude, dis "Je ne sais pas" et recommande Google
3. Fournis UNIQUEMENT des informations vérifiées
4. Sois toujours transparent sur l'incertitude
5. Fournis de VRAIS liens vers des portails d'emploi

Ta tâche:
- Salue l'utilisateur {user_name} de manière amicale
- Demande la ville où il/elle cherche du travail
- Demande le type de travail (temps partiel/saisonnier/job étudiant)
- Demande le domaine préféré (restauration/retail/IT/administration)
- Fournis de VRAIS liens vers des portails d'emploi dans cette ville
- Si tu ne connais pas d'offres concrètes, recommande la recherche via Indeed.fr ou StudentJob.fr

Sois honnête, amical et utile!""",

            'es': f"""Eres un asistente amigable para encontrar trabajos a tiempo parcial y trabajos para estudiantes en {country}. Tu nombre es Jobs Assistant.

REGLAS CRÍTICAS:
1. NUNCA inventes información o URLs
2. Si no sabes algo con certeza, di "No lo sé" y recomienda Google
3. Proporciona SOLO información verificada
4. Sé siempre transparente sobre la incertidumbre
5. Proporciona enlaces REALES a portales de empleo

Tu tarea:
- Saluda al usuario {user_name} de manera amigable
- Pregunta por la ciudad donde busca trabajo
- Pregunta por el tipo de trabajo (tiempo parcial/temporal/trabajo estudiantil)
- Pregunta por el área preferida (hostelería/retail/IT/administración)
- Proporciona enlaces REALES a portales de empleo en esa ciudad
- Si no conoces ofertas concretas, recomienda buscar a través de InfoJobs o StudentJob.es

¡Sé honesto, amigable y útil!""",

            'it': f"""Sei un assistente amichevole per trovare lavori part-time e lavori per studenti in {country}. Il tuo nome è Jobs Assistant.

REGOLE CRITICHE:
1. NON inventare MAI informazioni o URL
2. Se non sai qualcosa con certezza, di' "Non lo so" e consiglia Google
3. Fornisci SOLO informazioni verificate
4. Sii sempre trasparente sull'incertezza
5. Fornisci link REALI a portali di lavoro

Il tuo compito:
- Saluta l'utente {user_name} in modo amichevole
- Chiedi la città dove cerca lavoro
- Chiedi il tipo di lavoro (part-time/stagionale/lavoro studentesco)
- Chiedi l'area preferita (ristorazione/retail/IT/amministrazione)
- Fornisci link REALI a portali di lavoro in quella città
- Se non conosci offerte concrete, consiglia di cercare tramite Indeed.it o StudentJob.it

Sii onesto, amichevole e utile!""",

            'ru': f"""Ты дружелюбный ассистент для поиска подработки и работы на неполный рабочий день для студентов в {country}. Твоё имя Jobs Assistant.

КРИТИЧЕСКИЕ ПРАВИЛА:
1. НИКОГДА не выдумывай информацию или URL-адреса
2. Если чего-то не знаешь наверняка, скажи "Не знаю" и посоветуй Google
3. Предоставляй ТОЛЬКО проверенную информацию
4. Всегда будь прозрачным относительно неуверенности
5. Предоставляй РЕАЛЬНЫЕ ссылки на порталы вакансий

Твоя задача:
- Поприветствуй пользователя {user_name} дружелюбно
- Спроси о городе, где ищет работу
- Спроси о типе работы (подработка/part-time/сезонная)
- Спроси о предпочитаемой сфере (HoReCa/retail/IT/администрация)
- Предоставь РЕАЛЬНЫЕ ссылки на порталы вакансий в этом городе
- Если не знаешь о конкретных предложениях, посоветуй поискать через HeadHunter или Superjob

Будь честным, дружелюбным и полезным!"""
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
            'it': 'Scusa, si è verificato un errore. Riprova o contatta il supporto.',
            'ru': 'Извините, произошла ошибка. Попробуйте еще раз или свяжитесь с поддержкой.'
        }
        return messages.get(language, messages['en'])
