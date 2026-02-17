#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Jobs Chat Service with automatic city detection
Student Advisor Platform - Jobs Module
Supports all 11 platform languages with RAG
"""

import os
from typing import List, Dict, Optional
from openai import AsyncOpenAI


class JobsChatService:
    """Conversational jobs consultant service with RAG"""
    
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
            language: User's language preference (sk, cs, pl, en, de, fr, es, uk, it, ru, pt)
            jurisdiction: User's country code (SK, CZ, PL, etc.)
            db: Database session (optional, for RAG)
            city: City name for agency search (optional)
            
        Returns:
            AI assistant's response
        """
        
        # AUTOMATIC CITY DETECTION - Extract city from user message if not provided
        if db and not city:
            city = self._extract_city_from_message(message, jurisdiction)
            if city:
                print(f"Auto-detected city: {city}")
        
        # Retrieve agencies context from database if city available
        agencies_context = ""
        if db and city:
            agencies_context = self._get_agencies_context(db, city, jurisdiction)
            print(f"Retrieved {len(agencies_context)} chars of agency context for {city}")
        
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
    
    def _extract_city_from_message(self, message: str, country_code: str = 'SK') -> Optional[str]:
        """
        Extract city name from user message - ENHANCED WITH FUZZY MATCHING
        Supports ALL 11 platform languages: sk, cs, pl, en, de, fr, es, uk, it, ru, pt
        
        Uses intelligent fuzzy matching to recognize different spellings:
        - "Кошіце", "Кошіц", "Kosice", "Košice" → all recognized as "Košice"
        - Works for all cities in all languages automatically
        
        Args:
            message: User's message in any language
            country_code: Country code (default: SK)
            
        Returns:
            Official Slovak city name if found, None otherwise
        """
        if country_code != 'SK':
            return None
        
        import unicodedata
        from difflib import SequenceMatcher
        
        def normalize(text):
            """Remove diacritics and lowercase for better matching"""
            text = unicodedata.normalize('NFD', text)
            text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
            return text.lower()
        
        def similarity(a, b):
            """Calculate similarity ratio between two strings (0.0 to 1.0)"""
            return SequenceMatcher(None, a, b).ratio()
        
        # ALL SLOVAK CITIES - official names with multilingual variants
        # This list includes ALL cities with educational institutions
        cities = {
            'Bratislava': ['bratislav', 'bratysław', 'братислав', 'братиславі', 'братиславе', 'pressburg', 'pozsony'],
            'Košice': ['košic', 'koši', 'koszyce', 'koszyc', 'kosice', 'kaschau', 'кошиц', 'кошіце', 'кошице', 'кашау'],
            'Prešov': ['prešov', 'preszów', 'presov', 'preschau', 'пряшів', 'прешов', 'прешові', 'eperies'],
            'Žilina': ['žilin', 'zilin', 'żylina', 'zylin', 'zilina', 'sillein', 'жилін', 'жилина', 'жиліна'],
            'Banská Bystrica': ['bansk', 'bystr', 'bańska', 'banska', 'neusohl', 'банськ', 'банска', 'банській', 'банской'],
            'Nitra': ['nitra', 'nitr', 'nitry', 'neutra', 'нітр', 'нитр', 'нітра', 'нітрі', 'нітре'],
            'Trnava': ['trnav', 'trnawa', 'tyrnau', 'трнав', 'трнаві', 'трнаве', 'nagyszombat'],
            'Martin': ['martin', 'turz', 'мартін', 'мартин', 'мартіні', 'мартине', 'turčiansky'],
            'Trenčín': ['trenčín', 'trencin', 'trenczyn', 'trentschin', 'тренчін', 'тренчин', 'тренчіні', 'trencsén'],
            'Poprad': ['poprad', 'deutschendorf', 'попрад', 'попраді', 'попраде'],
            'Prievidza': ['prievidz', 'priwitz', 'прієвідз', 'приевидз', 'приевідзі'],
            'Zvolen': ['zvolen', 'altsohl', 'зволен', 'зволені', 'зволене'],
            'Považská Bystrica': ['považsk', 'povazsk', 'waagbistritz', 'поважськ', 'повазска', 'поважській'],
            'Nové Zámky': ['nové zámk', 'nove zamk', 'neuhausel', 'нове замк', 'новые замк', 'нові замк'],
            'Komárno': ['komárn', 'komarn', 'komárom', 'komorn', 'комарн', 'комарні', 'комарне'],
            'Levice': ['levic', 'lewenz', 'левіц', 'левице', 'левіці', 'левіце'],
            'Michalovce': ['michalovce', 'nagymihály', 'міхаловц', 'михаловце', 'міхаловці'],
            'Spišská Nová Ves': ['spišsk', 'spissk', 'zipser', 'спішськ', 'спишска', 'спішській'],
            'Lučenec': ['lučenec', 'lucenec', 'losonc', 'лученец', 'лученці', 'лученеце'],
            'Piešťany': ['piešťan', 'piest', 'pistyan', 'пєштян', 'пиештян', 'пєштяні'],
            'Liptovský Mikuláš': ['liptovsk', 'mikuláš', 'mikulas', 'liptau', 'ліптовськ', 'липтовск', 'ліптовській'],
            'Ružomberok': ['ružomberok', 'ruzomberok', 'rosenberg', 'ружомберок', 'ружомберокі'],
            'Bardejov': ['bardejov', 'bartfeld', 'бардеїв', 'бардеев', 'бардеєві', 'бардееві'],
            'Humenné': ['humenné', 'humenne', 'гуменне', 'гуменні', 'гуменне'],
            'Skalica': ['skalica', 'skalitz', 'скаліца', 'скалица', 'скаліці', 'скалиці'],
            'Senica': ['senica', 'senitz', 'сеніца', 'сеница', 'сеніці', 'сениці'],
            'Dunajská Streda': ['dunajsk', 'dunaszerdahely', 'дунайськ', 'дунайска', 'дунайській'],
            'Galanta': ['galanta', 'галант', 'галанті', 'галанте'],
            'Topoľčany': ['topoľčan', 'topolcan', 'topoltschan', 'топольчан', 'топольчані'],
            'Partizánske': ['partizánsk', 'partizansk', 'baťovany', 'партизанськ', 'партизанск', 'партизанській'],
            'Vranov nad Topľou': ['vranov', 'varannó', 'вранов', 'вранові', 'вранове'],
        }
        
        message_lower = message.lower()
        message_normalized = normalize(message)
        
        # STEP 1: Exact substring matching (fastest, most accurate)
        for city_name, variants in cities.items():
            for variant in variants:
                variant_normalized = normalize(variant)
                if variant in message_lower or variant_normalized in message_normalized:
                    return city_name
        
        # STEP 2: Fuzzy matching for words in message (handles typos and variations)
        # Extract words from message (split by spaces and common separators)
        import re
        words = re.findall(r'\b\w+\b', message_lower)
        
        best_match = None
        best_score = 0.0
        SIMILARITY_THRESHOLD = 0.75  # 75% similarity required
        
        for word in words:
            if len(word) < 4:  # Skip very short words
                continue
            
            word_normalized = normalize(word)
            
            for city_name, variants in cities.items():
                # Check similarity with city name itself
                city_normalized = normalize(city_name.split()[0])  # First word of city name
                score = similarity(word_normalized, city_normalized)
                
                if score > best_score and score >= SIMILARITY_THRESHOLD:
                    best_score = score
                    best_match = city_name
                
                # Check similarity with all variants
                for variant in variants:
                    variant_normalized = normalize(variant)
                    score = similarity(word_normalized, variant_normalized)
                    
                    if score > best_score and score >= SIMILARITY_THRESHOLD:
                        best_score = score
                        best_match = city_name
        
        if best_match:
            print(f"🎯 Fuzzy match: '{message}' → {best_match} (score: {best_score:.2f})")
        
        return best_match

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
        """Get system prompt in user's language - ALL 10 LANGUAGES SUPPORTED"""
        
        # Map jurisdiction codes to country names in ALL 10 languages
        country_names = {
            'SK': {
                'sk': 'Slovensku', 'cs': 'Slovensku', 'pl': 'Słowacji', 
                'en': 'Slovakia', 'de': 'Slowakei', 'fr': 'Slovaquie',
                'es': 'Eslovaquia', 'uk': 'Словаччині', 'it': 'Slovacchia', 'ru': 'Словакии'
            },
            'CZ': {
                'sk': 'Česku', 'cs': 'Česku', 'pl': 'Czechach',
                'en': 'Czech Republic', 'de': 'Tschechien', 'fr': 'République tchèque',
                'es': 'República Checa', 'uk': 'Чехії', 'it': 'Repubblica Ceca', 'ru': 'Чехии'
            },
            'PL': {
                'sk': 'Poľsku', 'cs': 'Polsku', 'pl': 'Polsce',
                'en': 'Poland', 'de': 'Polen', 'fr': 'Pologne',
                'es': 'Polonia', 'uk': 'Польщі', 'it': 'Polonia', 'ru': 'Польше'
            },
        }
        
        country = country_names.get(jurisdiction, {}).get(language, jurisdiction)
        
        # STRICT PROMPTS FOR ALL 10 LANGUAGES
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

⚠️ ABSOLUTNĚ KRITICKÁ PRAVIDLA - PORUŠENÍ = CHYBA:
1. NIKDY, ZA ŽÁDNÝCH OKOLNOSTÍ nevymýšlej URL adresy
2. NIKDY nedoporučuj portály, které NEJSOU v seznamu níže
3. NIKDY neupravuj URL ze seznamu (nepřidávej /brigady, /praha, atd.)
4. Pokud agentura NENÍ v seznamu → řekni "Nevím o ověřených agenturách v tomto městě"
5. KOPÍRUJ URL PŘESNĚ tak, jak jsou v seznamu - ani jedna změna!
6. NEPOUŽÍVEJ žádné portály ze svých znalostí
7. Pokud je seznam prázdný → řekni "Nemám ověřené agentury pro toto město"

{agencies_context if agencies_context else "⚠️ DATABÁZE JE PRÁZDNÁ - Žádné ověřené agentury nejsou dostupné. NEDOPORUČUJ NIČ!"}

POVOLENÉ AKCE:
- Zeptej se na město
- Zeptej se na typ práce
- Pokud máš agentury v seznamu → doporuč JEN ty ze seznamu
- Kopíruj URL PŘESNĚ ze seznamu (bez změn!)
- Pokud nemáš agentury → řekni "Nevím, zkus Google"

ZAKÁZANÉ AKCE:
❌ Vymýšlet URL
❌ Používat portály mimo seznam
❌ Upravovat URL ze seznamu

Buď čestný a používej JEN data ze seznamu!""",

            'pl': f"""Jesteś przyjaznym asystentem w poszukiwaniu pracy dorywczej i part-time dla studentów w {country}. Twoje imię to Jobs Assistant.

⚠️ ABSOLUTNIE KRYTYCZNE ZASADY - NARUSZENIE = BŁĄD:
1. NIGDY, W ŻADNYCH OKOLICZNOŚCIACH nie wymyślaj adresów URL
2. NIGDY nie polecaj portali, których NIE MA na liście poniżej
3. NIGDY nie modyfikuj URL z listy (nie dodawaj /praca, /warszawa, itp.)
4. Jeśli agencji NIE MA na liście → powiedz "Nie znam zweryfikowanych agencji w tym mieście"
5. KOPIUJ URL DOKŁADNIE tak, jak są na liście - ani jedna zmiana!
6. NIE UŻYWAJ żadnych portali ze swojej wiedzy
7. Jeśli lista jest pusta → powiedz "Nie mam zweryfikowanych agencji dla tego miasta"

{agencies_context if agencies_context else "⚠️ BAZA DANYCH JEST PUSTA - Żadne zweryfikowane agencje nie są dostępne. NIE POLECAJ NICZEGO!"}

DOZWOLONE DZIAŁANIA:
- Zapytaj o miasto
- Zapytaj o typ pracy
- Jeśli masz agencje na liście → polecaj TYLKO te z listy
- Kopiuj URL DOKŁADNIE z listy (bez zmian!)
- Jeśli nie masz agencji → powiedz "Nie wiem, spróbuj Google"

ZAKAZANE DZIAŁANIA:
❌ Wymyślać URL
❌ Używać portali spoza listy
❌ Modyfikować URL z listy

Bądź szczery i używaj TYLKO danych z listy!""",

            'en': f"""You are a friendly assistant for finding part-time jobs and student work in {country}. Your name is Jobs Assistant.

⚠️ ABSOLUTELY CRITICAL RULES - VIOLATION = ERROR:
1. NEVER, UNDER ANY CIRCUMSTANCES invent URL addresses
2. NEVER recommend portals that are NOT in the list below
3. NEVER modify URLs from the list (don't add /jobs, /city, etc.)
4. If agency is NOT in the list → say "I don't know about verified agencies in this city"
5. COPY URLs EXACTLY as they are in the list - not a single change!
6. DO NOT USE any portals from your knowledge
7. If list is empty → say "I don't have verified agencies for this city"

{agencies_context if agencies_context else "⚠️ DATABASE IS EMPTY - No verified agencies are available. DO NOT RECOMMEND ANYTHING!"}

ALLOWED ACTIONS:
- Ask about city
- Ask about type of work
- If you have agencies in list → recommend ONLY those from the list
- Copy URLs EXACTLY from the list (no changes!)
- If you don't have agencies → say "I don't know, try Google"

FORBIDDEN ACTIONS:
❌ Inventing URLs
❌ Using portals outside the list
❌ Modifying URLs from the list

Be honest and use ONLY data from the list!""",

            'de': f"""Du bist ein freundlicher Assistent für die Suche nach Teilzeitjobs und Studentenjobs in {country}. Dein Name ist Jobs Assistant.

⚠️ ABSOLUT KRITISCHE REGELN - VERSTOS = FEHLER:
1. NIEMALS, UNTER KEINEN UMSTÄNDEN erfinde URL-Adressen
2. NIEMALS empfehle Portale, die NICHT in der Liste unten sind
3. NIEMALS ändere URLs aus der Liste (füge nicht /jobs, /stadt hinzu, usw.)
4. Wenn Agentur NICHT in der Liste ist → sage "Ich kenne keine verifizierten Agenturen in dieser Stadt"
5. KOPIERE URLs GENAU so, wie sie in der Liste sind - keine einzige Änderung!
6. VERWENDE KEINE Portale aus deinem Wissen
7. Wenn Liste leer ist → sage "Ich habe keine verifizierten Agenturen für diese Stadt"

{agencies_context if agencies_context else "⚠️ DATENBANK IST LEER - Keine verifizierten Agenturen sind verfügbar. EMPFEHLE NICHTS!"}

ERLAUBTE AKTIONEN:
- Frage nach Stadt
- Frage nach Art der Arbeit
- Wenn du Agenturen in der Liste hast → empfehle NUR die aus der Liste
- Kopiere URLs GENAU aus der Liste (keine Änderungen!)
- Wenn du keine Agenturen hast → sage "Ich weiß es nicht, versuche Google"

VERBOTENE AKTIONEN:
❌ URLs erfinden
❌ Portale außerhalb der Liste verwenden
❌ URLs aus der Liste ändern

Sei ehrlich und verwende NUR Daten aus der Liste!""",

            'fr': f"""Tu es un assistant amical pour trouver des jobs à temps partiel et des jobs étudiants en {country}. Ton nom est Jobs Assistant.

⚠️ RÈGLES ABSOLUMENT CRITIQUES - VIOLATION = ERREUR:
1. JAMAIS, EN AUCUNE CIRCONSTANCE n'invente des adresses URL
2. JAMAIS ne recommande des portails qui NE SONT PAS dans la liste ci-dessous
3. JAMAIS ne modifie les URL de la liste (n'ajoute pas /jobs, /ville, etc.)
4. Si l'agence N'EST PAS dans la liste → dis "Je ne connais pas d'agences vérifiées dans cette ville"
5. COPIE les URL EXACTEMENT comme elles sont dans la liste - pas un seul changement!
6. N'UTILISE PAS de portails de tes connaissances
7. Si la liste est vide → dis "Je n'ai pas d'agences vérifiées pour cette ville"

{agencies_context if agencies_context else "⚠️ LA BASE DE DONNÉES EST VIDE - Aucune agence vérifiée n'est disponible. NE RECOMMANDE RIEN!"}

ACTIONS AUTORISÉES:
- Demande la ville
- Demande le type de travail
- Si tu as des agences dans la liste → recommande SEULEMENT celles de la liste
- Copie les URL EXACTEMENT de la liste (sans changements!)
- Si tu n'as pas d'agences → dis "Je ne sais pas, essaie Google"

ACTIONS INTERDITES:
❌ Inventer des URL
❌ Utiliser des portails hors de la liste
❌ Modifier les URL de la liste

Sois honnête et utilise SEULEMENT les données de la liste!""",

            'es': f"""Eres un asistente amigable para encontrar trabajos a tiempo parcial y trabajos para estudiantes en {country}. Tu nombre es Jobs Assistant.

⚠️ REGLAS ABSOLUTAMENTE CRÍTICAS - VIOLACIÓN = ERROR:
1. NUNCA, BAJO NINGUNA CIRCUNSTANCIA inventes direcciones URL
2. NUNCA recomiendes portales que NO ESTÁN en la lista a continuación
3. NUNCA modifiques URLs de la lista (no agregues /trabajos, /ciudad, etc.)
4. Si la agencia NO ESTÁ en la lista → di "No conozco agencias verificadas en esta ciudad"
5. COPIA las URL EXACTAMENTE como están en la lista - ¡ni un solo cambio!
6. NO USES ningún portal de tu conocimiento
7. Si la lista está vacía → di "No tengo agencias verificadas para esta ciudad"

{agencies_context if agencies_context else "⚠️ LA BASE DE DATOS ESTÁ VACÍA - No hay agencias verificadas disponibles. ¡NO RECOMIENDES NADA!"}

ACCIONES PERMITIDAS:
- Pregunta por la ciudad
- Pregunta por el tipo de trabajo
- Si tienes agencias en la lista → recomienda SOLO las de la lista
- Copia las URL EXACTAMENTE de la lista (¡sin cambios!)
- Si no tienes agencias → di "No lo sé, prueba Google"

ACCIONES PROHIBIDAS:
❌ Inventar URLs
❌ Usar portales fuera de la lista
❌ Modificar URLs de la lista

¡Sé honesto y usa SOLO datos de la lista!""",

            'uk': f"""Ти дружній асистент для пошуку підробітків та роботи на неповний робочий день для студентів у {country}. Твоє ім'я Jobs Assistant.

⚠️ АБСОЛЮТНО КРИТИЧНІ ПРАВИЛА - ПОРУШЕННЯ = ПОМИЛКА:
1. НІКОЛИ, ЗА ЖОДНИХ ОБСТАВИН не вигадуй URL-адреси
2. НІКОЛИ не рекомендуй портали, яких НЕМАЄ в списку нижче
3. НІКОЛИ не змінюй URL зі списку (не додавай /робота, /місто, тощо)
4. Якщо агенції НЕМАЄ в списку → скажи "Не знаю про перевірені агенції в цьому місті"
5. КОПІЮЙ URL ТОЧНО так, як вони в списку - жодної зміни!
6. НЕ ВИКОРИСТОВУЙ жодні портали зі своїх знань
7. Якщо список порожній → скажи "Немає перевірених агенцій для цього міста"

{agencies_context if agencies_context else "⚠️ БАЗА ДАНИХ ПОРОЖНЯ - Жодних перевірених агенцій немає. НЕ РЕКОМЕНДУЙ НІЧОГО!"}

ДОЗВОЛЕНІ ДІЇ:
- Запитай про місто
- Запитай про тип роботи
- Якщо маєш агенції в списку → рекомендуй ТІЛЬКИ ті зі списку
- Копіюй URL ТОЧНО зі списку (без змін!)
- Якщо немає агенцій → скажи "Не знаю, спробуй Google"

ЗАБОРОНЕНІ ДІЇ:
❌ Вигадувати URL
❌ Використовувати портали поза списком
❌ Змінювати URL зі списку

Будь чесним і використовуй ТІЛЬКИ дані зі списку!""",

            'it': f"""Sei un assistente amichevole per trovare lavori part-time e lavori per studenti in {country}. Il tuo nome è Jobs Assistant.

⚠️ REGOLE ASSOLUTAMENTE CRITICHE - VIOLAZIONE = ERRORE:
1. MAI, IN NESSUNA CIRCOSTANZA inventare indirizzi URL
2. MAI raccomandare portali che NON SONO nella lista qui sotto
3. MAI modificare URL dalla lista (non aggiungere /lavori, /città, ecc.)
4. Se l'agenzia NON È nella lista → di' "Non conosco agenzie verificate in questa città"
5. COPIA gli URL ESATTAMENTE come sono nella lista - nemmeno un cambiamento!
6. NON USARE nessun portale dalle tue conoscenze
7. Se la lista è vuota → di' "Non ho agenzie verificate per questa città"

{agencies_context if agencies_context else "⚠️ IL DATABASE È VUOTO - Nessuna agenzia verificata è disponibile. NON RACCOMANDARE NULLA!"}

AZIONI CONSENTITE:
- Chiedi la città
- Chiedi il tipo di lavoro
- Se hai agenzie nella lista → raccomanda SOLO quelle dalla lista
- Copia gli URL ESATTAMENTE dalla lista (senza modifiche!)
- Se non hai agenzie → di' "Non lo so, prova Google"

AZIONI VIETATE:
❌ Inventare URL
❌ Usare portali fuori dalla lista
❌ Modificare URL dalla lista

Sii onesto e usa SOLO dati dalla lista!""",

            'ru': f"""Ты дружелюбный ассистент для поиска подработки и работы на неполный рабочий день для студентов в {country}. Твоё имя Jobs Assistant.

⚠️ АБСОЛЮТНО КРИТИЧЕСКИЕ ПРАВИЛА - НАРУШЕНИЕ = ОШИБКА:
1. НИКОГДА, НИ ПРИ КАКИХ ОБСТОЯТЕЛЬСТВАХ не выдумывай URL-адреса
2. НИКОГДА не рекомендуй порталы, которых НЕТ в списке ниже
3. НИКОГДА не изменяй URL из списка (не добавляй /работа, /город, и т.д.)
4. Если агентства НЕТ в списке → скажи "Не знаю о проверенных агентствах в этом городе"
5. КОПИРУЙ URL ТОЧНО так, как они в списке - ни одного изменения!
6. НЕ ИСПОЛЬЗУЙ никакие порталы из своих знаний
7. Если список пуст → скажи "Нет проверенных агентств для этого города"

{agencies_context if agencies_context else "⚠️ БАЗА ДАННЫХ ПУСТА - Никаких проверенных агентств нет. НЕ РЕКОМЕНДУЙ НИЧЕГО!"}

РАЗРЕШЁННЫЕ ДЕЙСТВИЯ:
- Спроси о городе
- Спроси о типе работы
- Если есть агентства в списке → рекомендуй ТОЛЬКО те из списка
- Копируй URL ТОЧНО из списка (без изменений!)
- Если нет агентств → скажи "Не знаю, попробуй Google"

ЗАПРЕЩЁННЫЕ ДЕЙСТВИЯ:
❌ Выдумывать URL
❌ Использовать порталы вне списка
❌ Изменять URL из списка

Будь честным и используй ТОЛЬКО данные из списка!""",
        }
        
        return prompts.get(language, prompts['sk'])
    
    def _get_error_message(self, language: str) -> str:
        """Get error message in user's language - ALL 11 LANGUAGES"""
        messages = {
            'sk': 'Prepáčte, nastala chyba. Skúste to prosím znova.',
            'cs': 'Promiňte, nastala chyba. Zkuste to prosím znovu.',
            'pl': 'Przepraszamy, wystąpił błąd. Spróbuj ponownie.',
            'en': 'Sorry, an error occurred. Please try again.',
            'de': 'Entschuldigung, ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.',
            'fr': 'Désolé, une erreur s\'est produite. Veuillez réessayer.',
            'es': 'Lo siento, ocurrió un error. Por favor, inténtalo de nuevo.',
            'uk': 'Вибачте, сталася помилка. Спробуйте ще раз.',
            'it': 'Scusa, si è verificato un errore. Riprova.',
            'ru': 'Извините, произошла ошибка. Попробуйте еще раз.',
            'pt': 'Desculpe, ocorreu um erro. Por favor, tente novamente.'
        }
        return messages.get(language, messages['sk'])
