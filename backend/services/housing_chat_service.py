#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Housing Chat Service with automatic city detection
Student Advisor Platform - Housing Module
Supports all 11 platform languages with RAG
"""

import os
from typing import List, Dict, Optional
from openai import AsyncOpenAI


class HousingChatService:
    """Conversational housing consultant service with RAG"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    

    def _detect_message_language(self, message: str):
        """
        Detect language from message content
        Returns language code (sk, cs, pl, en, de, fr, es, uk, it, ru, pt) or None
        """
        message_lower = message.lower()
        
        # Check for Cyrillic script (Ukrainian/Russian)
        has_cyrillic = any('\u0400' <= char <= '\u04FF' for char in message)
        
        if has_cyrillic:
            # Ukrainian-specific: і, ї, є, ґ
            ukrainian_chars = ['і', 'ї', 'є', 'ґ']
            ukrainian_words = ['шукаю', 'житло', 'квартиру', 'гуртожиток', 'пиши', 'українською']
            
            if any(char in message_lower for char in ukrainian_chars) or \
               any(word in message_lower for word in ukrainian_words):
                return 'uk'
            
            # Russian-specific: ы, э, ъ
            russian_words = ['ищу', 'жилье', 'квартиру', 'общежитие', 'пиши', 'по-русски']
            if any(word in message_lower for word in russian_words):
                return 'ru'
            
            # Default Cyrillic to Ukrainian (more common on platform)
            return 'uk'
        
        # Check for specific language keywords
        lang_keywords = {
            'sk': ['hľadám', 'bývanie', 'byt', 'slovensky', 'slovenčina'],
            'cs': ['hledám', 'bydlení', 'česky', 'čeština'],
            'pl': ['szukam', 'mieszkania', 'po polsku', 'polski'],
            'de': ['suche', 'wohnung', 'auf deutsch', 'deutsch'],
            'fr': ['cherche', 'logement', 'en français', 'français'],
            'es': ['busco', 'vivienda', 'en español', 'español'],
            'it': ['cerco', 'alloggio', 'in italiano', 'italiano'],
            'pt': ['procuro', 'moradia', 'em português', 'português'],
        }
        
        for lang, keywords in lang_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return lang
        
        # No clear language detected
        return None


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
        
        print(f"🚀 Housing chat called: message='{message[:50]}...', jurisdiction='{jurisdiction}', db={'YES' if db else 'NO'}")
        
        
        # AUTOMATIC CITY DETECTION - Extract city from user message if not provided
        print(f"🚦 Condition check: db={bool(db)}, city={repr(city)}, not city={not city}")
        if db and not city:
            print("🔍 Calling _extract_city_from_message")
            city = self._extract_city_from_message(message, jurisdiction)
            if city:
                print(f"Auto-detected city: {city}")
            else:
                # Fallback: Try to extract city from conversation history
                print("🔍 City not found in current message, checking conversation history...")
                for msg in reversed(conversation_history):
                    if msg.get("role") == "user":
                        history_city = self._extract_city_from_message(msg.get("content", ""), jurisdiction)
                        if history_city:
                            city = history_city
                            print(f"✅ Found city in history: {city}")
                            break
        else:
            print(f"❌ Skipping city detection: db={bool(db)}, not city={not city}")
        
        # Retrieve agencies context from database if city available
        agencies_context = ""
        if db and city:
            # Use the provided jurisdiction for agency search
            agencies_context = self._get_agencies_context(db, city, jurisdiction)
            print(f"Retrieved {len(agencies_context)} chars of agency context for {city} (Country: {jurisdiction})")
        
        # AUTOMATIC LANGUAGE DETECTION - Override frontend language if message is in different language
        detected_language = self._detect_message_language(message)
        if detected_language and detected_language != language:
            print(f"🌍 Language auto-detected: {language} → {detected_language} (from message content)")
            language = detected_language
        
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
            print(f"Error in housing chat: {e}")
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
        # Validate country code (now supports ALL planned jurisdictions + micro-states)
        # SK, CZ, PL, DE, AT, CH, GB, IE, FR, BE, NL, IT, ES, PT, DK, SE, NO, FI, GR, HU, SI, HR, LU
        # LI (Liechtenstein), VA (Vatican), SM (San Marino), MC (Monaco), AD (Andorra)
        supported_codes = [
            'SK', 'CZ', 'PL', 'DE', 'AT', 'CH', 'GB', 'IE', 'FR', 
            'BE', 'NL', 'IT', 'ES', 'PT', 'DK', 'SE', 'NO', 'FI', 
            'GR', 'HU', 'SI', 'HR', 'LU',
            'LI', 'VA', 'SM', 'MC', 'AD'  # Micro-states
        ]
        if country_code not in supported_codes:
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
        
        print(f"🔍 City detection: message='{message[:60]}', country='{country_code}'")
        
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
            
            # CZECH CITIES - official names with multilingual variants (ALL 11 LANGUAGES)
            # Praha: cs, sk, pl, en, de, fr, es, uk, it, ru, pt
            'Praha': [
                'prah', 'prague', 'praga', 'прага', 'праз', 'праги', 'праге', 'прагу', 'прагою',
                'praze', 'prahu', 'prahy', 'pragi', 'prago', 'pragę', 'pragą', 'praze',
                'praga', 'pragu', 'prague', 'prag', 'pragu', 'praghe', 'prague',
                'праги', 'праге', 'прагой', 'прагу', 'прагою', 'празі', 'празе'
            ],
            # Brno: cs, sk, pl, en, de, fr, es, uk, it, ru, pt
            'Brno': [
                'brno', 'брно', 'брні', 'брне', 'брну', 'брном', 'brunn', 'brünn',
                'brně', 'brna', 'brnu', 'brnem', 'brnie', 'brną', 'brnie',
                'брне', 'брну', 'брном', 'брної', 'брні'
            ],
            # Olomouc: cs, sk, pl, en, de, fr, es, uk, it, ru, pt
            'Olomouc': [
                'olomouc', 'оломоуць', 'оломоуц', 'оломоуці', 'оломоуце', 'olmütz', 'olomoucz',
                'olomouci', 'olomoucem', 'olomouce', 'ołomuniec', 'ołomuńcu',
                'оломоуці', 'оломоуце', 'оломоуцем', 'оломоуцу'
            ],
            # Ostrava: cs, sk, pl, en, de, fr, es, uk, it, ru, pt
            'Ostrava': [
                'ostrava', 'ostrawa', 'острава', 'остраві', 'остраве', 'остраву', 'остравою',
                'ostravě', 'ostravy', 'ostravu', 'ostravi', 'ostravo', 'ostravie', 'ostrawę',
                'остраві', 'остраве', 'остравой', 'остраву', 'остравою', 'mährisch-ostrau'
            ],
            # Plzeň: cs, sk, pl, en, de, fr, es, uk, it, ru, pt
            'Plzeň': [
                'plzeň', 'plzen', 'pilsen', 'пльзень', 'пльзені', 'пльзене', 'пльзеню',
                'plzni', 'plzně', 'plzní', 'pilznie', 'pilzno', 'pilzna',
                'пльзені', 'пльзене', 'пльзенем', 'пльзеню'
            ],
            # Liberec: cs, sk, pl, en, de, fr, es, uk, it, ru, pt
            'Liberec': [
                'liberec', 'reichenberg', 'ліберець', 'либерец', 'ліберці', 'ліберце', 'ліберцю',
                'liberci', 'libercem', 'liberce', 'libercu', 'libercie',
                'ліберці', 'ліберце', 'ліберцем', 'ліберцю'
            ],
            # Hradec Králové: cs, sk, pl, en, de, fr, es, uk, it, ru, pt
            'Hradec Králové': [
                'hradec', 'králové', 'hradec králové', 'königgrätz', 'градець кралове', 'градец кралове',
                'hradci králové', 'hradcem králové', 'hradce králové', 'hradcu králové',
                'градці кралове', 'градце кралове', 'градцем кралове', 'градцю кралове'
            ],
            # České Budějovice: cs, sk, pl, en, de, fr, es, uk, it, ru, pt
            'České Budějovice': [
                'české budějovice', 'ceske budejovice', 'budweis', 'ческе будейовіце', 'ческе будеёвице',
                'českých budějovicích', 'českými budějovicemi', 'czeskie budziejowice',
                'ческе будейовіце', 'ческе будейовице', 'ческе будеёвице', 'ческих будейовицах'
            ],
            # Pardubice: cs, sk, pl, en, de, fr, es, uk, it, ru, pt
            'Pardubice': [
                'pardubice', 'pardubitz', 'пардубіце', 'пардубице', 'пардубіці', 'пардубіце',
                'pardubicích', 'pardubicemi', 'pardubic', 'pardubitz',
                'пардубіці', 'пардубіце', 'пардубицем', 'пардубіцю'
            ],
            
            # POLISH CITIES - official names with multilingual variants (ALL 11 LANGUAGES)
            # Warszawa: pl, en, de, fr, es, uk, it, ru, pt
            'Warszawa': [
                'warszawa', 'warsaw', 'varsovie', 'warschau', 'varsavia', 'варшава', 'varsovia',
                'warszawy', 'warszawie', 'warszawą', 'варшаві', 'варшаву', 'варшавою', 'варшаве'
            ],
            # Kraków: pl, en, de, fr, es, uk, it, ru, pt
            'Kraków': [
                'kraków', 'krakow', 'cracow', 'cracovie', 'krakau', 'cracovia', 'краків', 'краков',
                'cracóvia', 'krakowa', 'krakowie', 'krakowem', 'кракова', 'кракові', 'кракову'
            ],
            # Wrocław: pl, en, de, fr, es, uk, it, ru, pt
            'Wrocław': [
                'wrocław', 'wroclaw', 'breslau', 'vratislav', 'вроцлав',
                'wrocławia', 'wrocławiu', 'wrocławiem', 'вроцлаві', 'вроцлава'
            ],
            # Poznań: pl, en, de, fr, es, uk, it, ru, pt
            'Poznań': [
                'poznań', 'poznan', 'posen', 'познань',
                'poznania', 'poznaniu', 'poznaniem', 'познані'
            ],
            # Gdańsk: pl, en, de, fr, es, uk, it, ru, pt
            'Gdańsk': [
                'gdańsk', 'gdansk', 'danzig', 'гданськ', 'гданьск', 'gdánsk',
                'gdańska', 'gdańsku', 'gdańskiem', 'гданську', 'гданська'
            ],
            
            # GERMAN CITIES - official names with multilingual variants
            # München: de, en, fr, it, es, pt, pl
            'München': [
                'münchen', 'munchen', 'munich', 'monaco', 'monachium', 'мюнхен', 'munique',
                'мюнхена', 'мюнхене', 'мюнхену', 'мюнхені'
            ],
            # Köln: de, en, fr, it, es, pt, pl
            'Köln': [
                'köln', 'koln', 'cologne', 'colonia', 'colônia', 'кельн', 'кьольн', 
                'кельна', 'кельне', 'кельну', 'кьольні'
            ],
            # Nürnberg: de, en, fr, it, es, pt, pl
            'Nürnberg': [
                'nürnberg', 'nurnberg', 'nuremberg', 'norymberga', 'нюрнберг', 'norinberg',
                'нюрнберга', 'нюрнберге', 'нюрнбергу', 'нюрнберзі', 'norymberdze'
            ],
            # Frankfurt: de, en, fr, it, es, pt, pl
            'Frankfurt': [
                'frankfurt', 'francfort', 'frankfort', 'francoforte', 'франкфурт',
                'франкфурта', 'франкфурте', 'франкфурту', 'франкфурті'
            ],
            # Hamburg: de, en, fr, it, es, pt, pl
            'Hamburg': [
                'hamburg', 'hambourg', 'hamburgo', 'amburg', 'амбург', 'гамбург',
                'гамбурга', 'гамбурге', 'гамбургу', 'гамбурзі'
            ],
            # Berlin: de, en, fr, it, es, pt, pl
            'Berlin': [
                'berlin', 'berlino', 'berlim', 'берлін', 'берлин',
                'берліна', 'берліні', 'берліну', 'берлина', 'берлине'
            ],
            # Aachen: de, en, fr, it, es, pt, pl
            'Aachen': [
                'aachen', 'aix-la-chapelle', 'aix la chapelle', 'akwizgran', 'ахен',
                'ахена', 'ахене', 'ахену', 'ахені'
            ],
            
            # AUSTRIAN CITIES
            # Wien: de, en, fr, it, es, pt, pl
            'Wien': [
                'wien', 'vienna', 'vienne', 'viena', 'wiedeń', 'відень',
                'відня', 'відні', 'віднем', 'vienne', 'viedni', 'vídni', 'вене'
            ],
            # Graz: de, en, fr...
            'Graz': [
                'graz', 'gratz', 'hradec', 'грац', 'граца', 'граце', 'грацу'
            ],
            # Salzburg: de, en, fr...
            'Salzburg': [
                'salzburg', 'salzbourg', 'szalzburg', 'зальцбург', 'зальцбурга'
            ],
            # Innsbruck: de...
            'Innsbruck': [
                'innsbruck', 'innspruck', 'insbruck', 'інсбрук'
            ],
            # Linz: de...
            'Linz': [
                'linz', 'lince', 'лінц', 'линц'
            ],
            
            # SWISS CITIES
            # Zurich: de, en, fr, it...
            'Zurich': [
                'zurich', 'zürich', 'zuerich', 'zurigo', 'zurych', 'цюрих', 'цюриха'
            ],
            # Geneva: de, en, fr, it...
            'Geneva': [
                'geneva', 'genève', 'geneve', 'genf', 'ginevra', 'żenewa', 'женева', 'женев'
            ],
            # Bern: de, en, fr, it...
            'Bern': [
                'bern', 'berne', 'berna', 'берн'
            ],
            # Basel: de, en, fr, it...
            'Basel': [
                'basel', 'bâle', 'bale', 'basilea', 'bazylea', 'базель', 'базеле'
            ],
            # Lausanne: de, en, fr, it...
            'Lausanne': [
                'lausanne', 'lozan', 'lozanna', 'лозанна', 'лозанне'
            ],
            # St. Gallen: de, en, fr...
            'St. Gallen': [
                'st. gallen', 'st gallen', 'sankt gallen', 'saint-gall', 'san gallo', 'санкт-галлен'
            ],
            
            # DUTCH CITIES (NL) - All 11 platform languages: sk, cs, pl, en, de, fr, es, uk, it, ru, pt
            'Amsterdam': [
                'amsterdam', 'ams', 'a\'dam',
                # Ukrainian (uk)
                'амстердам', 'амстердамі', 'амстердаме', 'амстердаму', 'амстердамом',
                # Russian (ru)
                'амстердам', 'амстердаме', 'амстердаму', 'амстердамом',
                # Polish (pl)
                'amsterdamie', 'amsterdamu',
                # Spanish (es)
                'ámsterdam',
                # Portuguese (pt)
                'amsterdã', 'amesterdão', 'amesterdã'
            ],
            'Rotterdam': [
                'rotterdam', 'r\'dam', 'rdam', 'r-dam',
                # Ukrainian (uk)
                'роттердам', 'роттердамі', 'роттердаме', 'роттердаму',
                # Russian (ru)
                'роттердам', 'роттердаме', 'роттердаму',
                # Polish (pl)
                'rotterdamie', 'rotterdamu',
                # Portuguese (pt)
                'roterdão', 'roterdã'
            ],
            'Utrecht': [
                'utrecht',
                # Ukrainian (uk)
                'утрехт', 'утрехті', 'утрехте', 'утрехту',
                # Russian (ru)
                'утрехт', 'утрехте', 'утрехту',
                # Polish (pl)
                'utrechcie', 'utrechtu'
            ],
            'Leiden': [
                'leiden', 'leyden',
                # Ukrainian (uk)
                'лейден', 'лейдені', 'лейдене', 'лейдену',
                # Russian (ru)
                'лейден', 'лейдене', 'лейдену',
                # Polish (pl)
                'lejdzie', 'lejdą'
            ],
            'Groningen': [
                'groningen',
                # Ukrainian (uk)
                'гронінген', 'гронінгені', 'гронінгене', 'гронінгену',
                # Russian (ru)
                'гронинген', 'гронингене', 'гронингену',
                # Polish (pl)
                'groningen', 'groningenie'
            ],
            'Delft': [
                'delft',
                # Ukrainian (uk)
                'делфт', 'делфті', 'делфте', 'делфту',
                # Russian (ru)
                'делфт', 'делфте', 'делфту',
                # Polish (pl)
                'delfcie', 'delftu'
            ],
            'The Hague': [
                'the hague', 'den haag', 'haag', "'s-gravenhage", 's-gravenhage', 'gravenhage',
                # Ukrainian (uk)
                'гаага', 'гаазі', 'гаазе', 'гаагу', 'ден-гааг', 'ден гааг',
                # Russian (ru)
                'гаага', 'гааге', 'гаагу', 'ден-хааг', 'ден хааг',
                # French (fr)
                'la haye', 'lahaye',
                # German (de)
                'den haag',
                # Polish (pl)
                'hadze', 'haga', 'hadze'
            ],
            'Eindhoven': [
                'eindhoven',
                # Ukrainian (uk)
                'ейндховен', 'ейндховені', 'ейндховене', 'ейндховену', 'айндховен',
                # Russian (ru)
                'эйндховен', 'эйндховене', 'эйндховену', 'айндховен',
                # Polish (pl)
                'eindhoven', 'eindhovenie'
            ],
            'Maastricht': [
                'maastricht', 'maestricht',
                # Ukrainian (uk)
                'маастрихт', 'маастрихті', 'маастрихте', 'маастрихту',
                # Russian (ru)
                'маастрихт', 'маастрихте', 'маастрихту',
                # French (fr)
                'maestricht', 'mastricht',
                # Polish (pl)
                'maastricht', 'maastrichcie'
            ],
            'Tilburg': [
                'tilburg',
                # Ukrainian (uk)
                'тілбург', 'тілбурзі', 'тілбурге', 'тілбургу',
                # Russian (ru)
                'тилбург', 'тилбурге', 'тилбургу',
                # Polish (pl)
                'tilburgu', 'tilburgie'
            ],
            'Nijmegen': [
                'nijmegen', 'nimwegen',
                # Ukrainian (uk)
                'неймеген', 'неймегені', 'неймегене', 'неймегену', 'німеген',
                # Russian (ru)
                'неймеген', 'неймегене', 'неймегену', 'нимеген',
                # German (de)
                'nimwegen',
                # Polish (pl)
                'nijmegen', 'nijmegenie'
            ],
            'Wageningen': [
                'wageningen',
                # Ukrainian (uk)
                'вагенінген', 'вагенінгені', 'вагенінгене', 'вагенінгену',
                # Russian (ru)
                'вагенинген', 'вагенингене', 'вагенингену',
                # Polish (pl)
                'wageningen', 'wageningenie'
            ],
            'Enschede': [
                'enschede',
                # Ukrainian (uk)
                'енсхеде', 'енсхеді', 'енсхеде', 'енсхеду',
                # Russian (ru)
                'энсхеде', 'энсхеде', 'энсхеду',
                # Polish (pl)
                'enschede', 'enschedzie'
            ],

            # ITALIAN CITIES (IT) - All 11 platform languages
            'Rome': [
                'rome', 'roma',
                # Ukrainian (uk)
                'рим', 'римі', 'римом', 'риму',
                # Russian (ru)
                'рим', 'риме', 'римом', 'риму',
                # Polish (pl)
                'rzym', 'rzymie', 'rzymu',
                # German (de)
                'rom',
                # French (fr)
                'rome',
                # Spanish (es)
                'roma'
            ],
            'Milan': [
                'milan', 'milano',
                # Ukrainian (uk)
                'мілан', 'мілані', 'міланом', 'мілану',
                # Russian (ru)
                'милан', 'милане', 'миланом', 'милану',
                # Polish (pl)
                'mediolan', 'mediolanie', 'mediolanu',
                # German (de)
                'mailand',
                # French (fr)
                'milan'
            ],
            'Florence': [
                'florence', 'firenze',
                # Ukrainian (uk)
                'флоренція', 'флоренції', 'флоренцією',
                # Russian (ru)
                'флоренция', 'флоренции', 'флоренцией',
                # Polish (pl)
                'florencja', 'florencji', 'florencję',
                # German (de)
                'florenz',
                # French (fr)
                'florence'
            ],
            'Bologna': [
                'bologna',
                # Ukrainian (uk)
                'болонья', 'болоньї', 'болонью',
                # Russian (ru)
                'болонья', 'болоньи', 'болонью',
                # Polish (pl)
                'bolonia', 'bolonii', 'bolonię'
            ],
            'Venice': [
                'venice', 'venezia',
                # Ukrainian (uk)
                'венеція', 'венеції', 'венецією',
                # Russian (ru)
                'венеция', 'венеции', 'венецией',
                # Polish (pl)
                'wenecja', 'wenecji', 'wenecję',
                # German (de)
                'venedig',
                # French (fr)
                'venise'
            ],
            'Padua': [
                'padua', 'padova',
                # Ukrainian (uk)
                'падуя', 'падуї', 'падуєю',
                # Russian (ru)
                'падуя', 'падуи', 'падуей',
                # Polish (pl)
                'padwa', 'padwie', 'padwę'
            ],
            'Pisa': [
                'pisa',
                # Ukrainian (uk)
                'піза', 'пізі', 'пізою',
                # Russian (ru)
                'пиза', 'пизе', 'пизой',
                # Polish (pl)
                'piza', 'pizie', 'pizę'
            ],

            # SPANISH CITIES (ES) - All 11 platform languages
            'Madrid': [
                'madrid',
                # Ukrainian (uk)
                'мадрид', 'мадриді', 'мадридом', 'мадриду',
                # Russian (ru)
                'мадрид', 'мадриде', 'мадридом', 'мадриду',
                # Polish (pl)
                'madryt', 'madrycie', 'madrytu'
            ],
            'Barcelona': [
                'barcelona',
                # Ukrainian (uk)
                'барселона', 'барселоні', 'барселоною', 'барселону',
                # Russian (ru)
                'барселона', 'барселоне', 'барселоной', 'барселону',
                # Polish (pl)
                'barcelona', 'barcelonie', 'barcelonę'
            ],
            'Valencia': [
                'valencia', 'valència',
                # Ukrainian (uk)
                'валенсія', 'валенсії', 'валенсією', 'валенсію',
                # Russian (ru)
                'валенсия', 'валенсии', 'валенсией', 'валенсию',
                # Polish (pl)
                'walencja', 'walencji', 'walencję'
            ],
            'Salamanca': [
                'salamanca',
                # Ukrainian (uk)
                'саламанка', 'саламанці', 'саламанкою', 'саламанку',
                # Russian (ru)
                'саламанка', 'саламанке', 'саламанкой', 'саламанку',
                # Polish (pl)
                'salamanka', 'salamance', 'salamankę'
            ],

            # PORTUGUESE CITIES (PT) - All 11 platform languages
            'Lisbon': [
                'lisbon', 'lisboa',
                # Ukrainian (uk)
                'лісабон', 'лісабоні', 'лісабоном', 'лісабону',
                # Russian (ru)
                'лиссабон', 'лиссабоне', 'лиссабоном', 'лиссабону',
                # Polish (pl)
                'lizbona', 'lizbonie', 'lizbonę',
                # German (de)
                'lissabon'
            ],
            'Porto': [
                'porto',
                # Ukrainian (uk)
                'порту', 'порто',
                # Russian (ru)
                'порту', 'порто'
            ],
            'Coimbra': [
                'coimbra',
                # Ukrainian (uk)
                'коїмбра', 'коїмбрі',
                # Russian (ru)
                'коимбра', 'коимбре'
            ],
            'Braga': [
                'braga',
                # Ukrainian (uk)
                'брага', 'бразі',
                # Russian (ru)
                'брага', 'браге'
            ],
            'Aveiro': [
                'aveiro',
                # Ukrainian (uk)
                'авейру', 'авейро',
                # Russian (ru)
                'авейру', 'авейро'
            ],

            # SWEDISH CITIES (SE) - All 11 platform languages
            'Stockholm': [
                'stockholm',
                # Ukrainian (uk)
                'стокгольм', 'стокгольмі', 'стокгольмом',
                # Russian (ru)
                'стокгольм', 'стокгольме', 'стокгольмом',
                # Polish (pl)
                'sztokholm', 'sztokholmie', 'sztokholmu'
            ],
            'Gothenburg': [
                'gothenburg', 'göteborg',
                # Ukrainian (uk)
                'гетеборг', 'гетеборзі', 'гетеборгом',
                # Russian (ru)
                'гетеборг', 'гетеборге', 'гетеборгом',
                # Polish (pl)
                'göteborg', 'göteborgu'
            ],
            'Uppsala': [
                'uppsala',
                # Ukrainian (uk)
                'уппсала', 'уппсалі',
                # Russian (ru)
                'уппсала', 'уппсале'
            ],
            'Lund': [
                'lund',
                # Ukrainian (uk)
                'лунд', 'лунді',
                # Russian (ru)
                'лунд', 'лунде'
            ],
            'Linköping': [
                'linköping', 'linkoping',
                # Ukrainian (uk)
                'лінчепінг', 'лінчепінгу',
                # Russian (ru)
                'линчепинг', 'линчепинге'
            ],

            # DANISH CITIES (DK)
            'Copenhagen': ['copenhagen', 'københavn', 'копенгаген', 'копенгагені', 'копенгагеном', 'копенгаген', 'копенгагене', 'копенгагеном', 'kopenhaga', 'kopenhadze'],
            'Aarhus': ['aarhus', 'орхус', 'орхусі'],
            'Odense': ['odense', 'оденсе', 'оденсі'],
            'Aalborg': ['aalborg', 'ольборг', 'ольборзі'],
            'Roskilde': ['roskilde', 'роскілле', 'роскіллі'],
            'Kolding': ['kolding', 'колдінг', 'колдінгу'],
            'Lyngby': ['lyngby', 'люнгбю', 'люнгбі'],

            # NORWEGIAN CITIES (NO)
            'Oslo': ['oslo', 'осло', 'ослі', 'ослом', 'осло', 'осле', 'ослом'],
            'Bergen': ['bergen', 'берген', 'бергені', 'бергеном'],
            'Trondheim': ['trondheim', 'тронгейм', 'тронгеймі'],
            'Stavanger': ['stavanger', 'ставангер', 'ставангері'],
            'Tromsø': ['tromsø', 'tromso', 'тромсе', 'тромсі'],
            'Ås': ['ås', 'as', 'ос', 'осі'],

            # FINNISH CITIES (FI)
            'Helsinki': ['helsinki', 'гельсінкі', 'хельсинки'],
            'Espoo': ['espoo', 'еспоо'],
            'Tampere': ['tampere', 'тампере', 'тампері'],
            'Turku': ['turku', 'турку'],
            'Oulu': ['oulu', 'оулу'],
            'Jyväskylä': ['jyväskylä', 'jyvaskyla', 'ювяскюля', 'ювяскюлі'],
            'Joensuu': ['joensuu', 'йоенсуу'],

            # GREEK CITIES (GR)
            'Athens': ['athens', 'athína', 'αθήνα', 'афіни', 'афінах', 'афінами', 'афины', 'афинах', 'афинами'],
            'Thessaloniki': ['thessaloniki', 'θεσσαλονίκη', 'салоніки', 'салонікі'],
            'Heraklion': ['heraklion', 'ηράκλειο', 'іракліон', 'іракліоні'],
            'Volos': ['volos', 'βόλος', 'волос', 'волосі'],
            'Ioannina': ['ioannina', 'ιωάννινα', 'яніна', 'яніні'],

            # HUNGARIAN CITIES (HU)
            'Budapest': ['budapest', 'будапешт', 'будапешті', 'будапештом', 'будапешт', 'будапеште', 'будапештом'],
            'Debrecen': ['debrecen', 'дебрецен', 'дебрецені'],
            'Szeged': ['szeged', 'сегед', 'сегеді'],
            'Pécs': ['pécs', 'pecs', 'печ', 'печі'],

            # SLOVENIAN CITIES (SI)
            'Ljubljana': ['ljubljana', 'любляна', 'люблян', 'любляною', 'любляна', 'любляне', 'любляной'],
            'Maribor': ['maribor', 'марібор', 'маріборі'],
            'Koper': ['koper', 'копер', 'коперу'],
            'Nova Gorica': ['nova gorica', 'нова горіца', 'нова гориця'],

            # CROATIAN CITIES (HR)
            'Zagreb': ['zagreb', 'загреб', 'загребі', 'загребом', 'загреб', 'загребе', 'загребом'],
            'Split': ['split', 'спліт', 'спліті'],
            'Rijeka': ['rijeka', 'рієка', 'рієці'],
            'Osijek': ['osijek', 'осієк', 'осієку'],

            # MICRO-STATES
            # Liechtenstein (LI)
            'Vaduz': ['vaduz', 'вадуц', 'вадуці'],
            'Bendern': ['bendern', 'бендерн', 'бендерні'],
            # Vatican (VA)
            'Vatican City': ['vatican', 'vatican city', 'ватикан', 'ватикані'],
            # San Marino (SM)
            'San Marino': ['san marino', 'сан маріно', 'сан-маріно'],
            # Monaco (MC)
            'Monaco': ['monaco', 'монако', 'монако'],
            # Andorra (AD)
            'Andorra la Vella': ['andorra', 'andorra la vella', 'андорра', 'андоррі'],
            'Sant Julià de Lòria': ['sant julia', 'sant julià de lòria', 'сант жуліа'],

            # UNITED KINGDOM CITIES (GB) - All 11 platform languages
            # London: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'London': [
                'london', 'londýn', 'londýne', 'londine', 'londyn', 'londynie', 'londres', 'londra', 'londen',
                'лондон', 'лондоні', 'лондоном', 'лондону', 'лондоне', 'лондона'
            ],
            # Edinburgh: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Edinburgh': [
                'edinburgh', 'edinburg', 'edinburgu', 'edinburghu', 'edinburge', 'edynburg', 'edynburgu', 'edynburgu',
                'édimbourg', 'edimburgo', 'edinburgo', 'edimburgo',
                'единбург', 'единбурзі', 'единбургом', 'единбургу', 'единбурге',
                'едінбург', 'едінбурзі', 'едінбургом', 'едінбургу', 'едінбурзе'
            ],
            # Manchester: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Manchester': [
                'manchester', 'manchestri', 'manchestre', 'manchesteru', 'mančester', 'mančestri', 'mančesteru',
                'manczester', 'manczestru', 'manczesterze', 'mánchester', 'mancester',
                'манчестер', 'манчестері', 'манчестером', 'манчестеру', 'манчестере', 'манчестера'
            ],
            # Birmingham: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Birmingham': [
                'birmingham', 'birminghame', 'birminghamu', 'birmingeme', 'birmingemu', 'birmingem', 'birmingemu',
                'birmingam', 'birmingão',
                'бірмінгем', 'бірмінгемі', 'бірмінгемом', 'бірмінгему', 'бірмінгемі',
                'бирмингем', 'бирмингеме', 'бирмингемом', 'бирмингему', 'бирмингема'
            ],
            # Glasgow: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Glasgow': [
                'glasgow', 'glasgowe', 'glasgowu', 'glazgow', 'glazgów', 'glazgowie', 'glasgovia',
                'глазго', 'глазгов', 'глазгові', 'глазговом', 'глазгову', 'глазгове', 'глазгова'
            ],
            # Bristol: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Bristol': [
                'bristol', 'bristole', 'bristolu', 'bristoli', 'brystol', 'brystolu', 'brístol',
                'брістоль', 'брістолі', 'брістолем', 'брістолю', 'брістолі',
                'бристоль', 'бристоле', 'бристолем', 'бристолю', 'бристоля'
            ],
            # Leeds: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Leeds': [
                'leeds', 'leedse', 'leedsu', 'lids', 'lídz', 'lídzu', 'lids',
                'лідс', 'лідсі', 'лідсом', 'лідсу', 'лідсі',
                'лидс', 'лидсе', 'лидсом', 'лидсу', 'лидса'
            ],
            # Liverpool: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Liverpool': [
                'liverpool', 'liverpoole', 'liverpoolu', 'liverpule', 'liverpulu', 'liverpul', 'liverpúl', 'liverpullu',
                'ливерпуль', 'ливерпулі', 'ливерпулем', 'ливерпулю', 'ливерпулі', 'ливерпуля',
                'ліверпуль', 'ліверпулі', 'ліверпулем', 'ліверпулю', 'ліверпулі'
            ],
            # Oxford: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Oxford': [
                'oxford', 'oxforde', 'oxfordu', 'oxferdu', 'oksford', 'oksfordu', 'oksfordzie', 'oxónia',
                'оксфорд', 'оксфорді', 'оксфордом', 'оксфорду', 'оксфорде', 'оксфорда'
            ],
            # Cambridge: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Cambridge': [
                'cambridge', 'cambridgi', 'cambridgu', 'kembridž', 'kembridži', 'kembridžu',
                'kembrydż', 'kembrydżu', 'kembrydżu', 'cambrígia',
                'кембридж', 'кембриджі', 'кембриджем', 'кембриджу', 'кембридже', 'кембриджа'
            ],
            # Newcastle: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Newcastle': [
                'newcastle', 'newcastli', 'newcastlu', 'ňjukásl', 'ňjukaslu', 'niukasl', 'niukaslu',
                'newcastle upon tyne', 'newcastle-upon-tyne',
                'ньюкасл', 'ньюкаслі', 'ньюкаслом', 'ньюкаслу', 'ньюкасле', 'ньюкасла'
            ],
            # Sheffield: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Sheffield': [
                'sheffield', 'sheffilde', 'sheffieldu', 'šefíld', 'šefíldu', 'šeffield', 'cheffield',
                'шеффілд', 'шеффілді', 'шеффілдом', 'шеффілду', 'шеффілді',
                'шеффилд', 'шеффилде', 'шеффилдом', 'шеффилду', 'шеффилда'
            ],
            # Nottingham: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Nottingham': [
                'nottingham', 'nottinghame', 'nottinghamu', 'notingeme', 'notingemu', 'notingem', 'notingemu',
                'notyngham', 'notynghamu', 'nótingem',
                'ноттінгем', 'ноттінгемі', 'ноттінгемом', 'ноттінгему', 'ноттінгемі',
                'ноттингем', 'ноттингеме', 'ноттингемом', 'ноттингему', 'ноттингема'
            ],
            # Southampton: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Southampton': [
                'southampton', 'southamptone', 'southamptonu', 'sautgempton', 'sautgemptonu',
                'sauthempton', 'sauthemptonu', 'sautémpton',
                'саутгемптон', 'саутгемптоні', 'саутгемптоном', 'саутгемптону', 'саутгемптоні',
                'саутхемптон', 'саутхемптоне', 'саутхемптоном', 'саутхемптону', 'саутхемптона'
            ],
            # Cardiff: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Cardiff': [
                'cardiff', 'cardiffe', 'cardiffu', 'kardif', 'kardifu', 'kardiff', 'kardiffu', 'caerdydd',
                'кардіфф', 'кардіффі', 'кардіффом', 'кардіффу', 'кардіффі',
                'кардифф', 'кардиффе', 'кардиффом', 'кардиффу', 'кардиффа'
            ],
            # Belfast: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Belfast': [
                'belfast', 'belfaste', 'belfastu', 'belfást', 'béal feirste',
                'белфаст', 'белфасті', 'белфастом', 'белфасту', 'белфасте', 'белфаста'
            ],
            # Aberdeen: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Aberdeen': [
                'aberdeen', 'aberdeene', 'aberdeenu', 'aberdín', 'aberdínu', 'aberdyn', 'aberdynu',
                'абердін', 'абердіні', 'абердіном', 'абердіну', 'абердіні',
                'абердин', 'абердине', 'абердином', 'абердину', 'абердина'
            ],
            # Leicester: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Leicester': [
                'leicester', 'leicestri', 'leicestru', 'lester', 'lestru', 'lajster', 'lajstru',
                'лестер', 'лестері', 'лестером', 'лестеру', 'лестере', 'лестера'
            ],
            # Coventry: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Coventry': [
                'coventry', 'coventri', 'coventru', 'koventri', 'koventru', 'kowentry', 'kowentru',
                'ковентрі', 'ковентрі', 'ковентрі', 'ковентрі',
                'ковентри', 'ковентри', 'ковентри', 'ковентри'
            ],
            # York: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'York': [
                'york', 'yorku', 'yorke', 'jork', 'jorku', 'jorque',
                'йорк', 'йорку', 'йорком', 'йорке', 'йорка'
            ],
            
            # IRISH CITIES (IE)
            # Dublin
            'Dublin': [
                'dublin', 'dublín', 'dublina', 'дублін'
            ],
            # Cork
            'Cork': [
                'cork', 'corcaigh', 'kork', 'корк'
            ],
            # Galway
            'Galway': [
                'galway', 'gaillimh', 'golwe', 'голвей'
            ],
            # Limerick
            'Limerick': [
                'limerick', 'luimneach', 'лимерик'
            ],
            # Maynooth
            'Maynooth': [
                'maynooth', 'maigh nuad', 'майнкут'
            ],
            
            # FRENCH CITIES (FR) - All 11 platform languages
            # Paris: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Paris': [
                'paris', 'paríž', 'paříž', 'parížu', 'paryż', 'paryżu', 'paryżem', 'parigi',
                'parís', 'lutetia',
                'париж', 'парижі', 'парижем', 'парижу', 'париже', 'парижа'
            ],
            # Lyon: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Lyon': [
                'lyon', 'lyonu', 'lyone', 'lion', 'lugdunum', 'lione',
                'ліон', 'ліоні', 'ліоном', 'ліону',
                'лион', 'лионе', 'лионом', 'лиону', 'лиона'
            ],
            # Marseille: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Marseille': [
                'marseille', 'marseilles', 'marsiglia', 'marsella', 'marselha',
                'марсель', 'марселі', 'марселем', 'марселю', 'марселе', 'марселя'
            ],
            # Toulouse: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Toulouse': [
                'toulouse', 'tolosa', 'tolouse', 'tuluza',
                'тулуза', 'тулузі', 'тулузою', 'тулузу', 'тулузе', 'тулузи'
            ],
            # Nice: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Nice': [
                'nice', 'nizza', 'nica', 'niça',
                'ніцца', 'ніцці', 'ніццою', 'ніцці',
                'ницца', 'ницце', 'ниццой', 'ниццу', 'ниццы'
            ],
            # Nantes: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Nantes': [
                'nantes', 'nant', 'нант', 'нанті', 'нантом', 'нанту', 'нанте', 'нанта'
            ],
            # Strasbourg: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Strasbourg': [
                'strasbourg', 'strasburgu', 'strasburg', 'strasburgu', 'straßburg', 'strassburg',
                'estrasburgo', 'strasburgo',
                'страсбург', 'страсбурзі', 'страсбургом', 'страсбургу', 'страсбурге',
                'штрасбург', 'штрасбурзі', 'штрасбургом'
            ],
            # Montpellier: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Montpellier': [
                'montpellier', 'montpellier', 'монпельє', 'монпельєрі', 'монпельєром',
                'монпелье', 'монпелье', 'монпельере'
            ],
            # Bordeaux: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Bordeaux': [
                'bordeaux', 'bordó', 'бордо', 'бордо', 'бордо'
            ],
            # Lille: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Lille': [
                'lille', 'rijsel', 'lila', 'ліль', 'лілі', 'ліллю',
                'лилль', 'лилле', 'лиллю', 'лилля'
            ],
            # Rennes: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Rennes': [
                'rennes', 'ренн', 'ренні', 'ренном', 'ренну', 'ренне', 'ренна'
            ],
            # Grenoble: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Grenoble': [
                'grenoble', 'grenoblu', 'гренобль', 'гренобл', 'гренобл', 'гренобля'
            ],
            # Aix-en-Provence: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Aix-en-Provence': [
                'aix-en-provence', 'aix en provence', 'aix', 'екс-ан-прованс', 'екс-ан-провансі',
                'экс-ан-прованс', 'экс-ан-провансе'
            ],
            # Cergy: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Cergy': [
                'cergy', 'cergy-pontoise', 'сержі', 'сержи', 'сержи'
            ],
            # Jouy-en-Josas: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Jouy-en-Josas': [
                'jouy-en-josas', 'jouy en josas', 'jouy', 'жуї-ан-жоза', 'жуи-ан-жоза'
            ],
            # Palaiseau: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Palaiseau': [
                'palaiseau', 'палезо', 'палезо'
            ],
            
            # SPANISH CITIES (ES) - All 11 platform languages
            # Madrid: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Madrid': [
                'madrid', 'madridu', 'madride', 'мадрид', 'мадриді', 'мадридом', 'мадриду', 'мадриде', 'мадрида'
            ],
            # Barcelona: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Barcelona': [
                'barcelona', 'barcelony', 'barcelone', 'barcellona', 'барселона', 'барселоні', 'барселоною', 'барселону', 'барселоне', 'барселоны'
            ],
            # Valencia: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Valencia': [
                'valencia', 'valencie', 'valencii', 'valence', 'валенсія', 'валенсії', 'валенсією', 'валенсію',
                'валенсия', 'валенсии', 'валенсией', 'валенсию', 'валенсии'
            ],
            # Sevilla: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Sevilla': [
                'sevilla', 'sevilly', 'seville', 'siviglia', 'севілья', 'севільї', 'севільєю', 'севілью',
                'севилья', 'севильи', 'севильей', 'севилью', 'севильи'
            ],
            # Zaragoza: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Zaragoza': [
                'zaragoza', 'saragossa', 'saragosse', 'сарагоса', 'сарагосі', 'сарагосою', 'сарагосу', 'сарагосе', 'сарагосы'
            ],
            # Málaga: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Málaga': [
                'málaga', 'malaga', 'malagi', 'малага', 'малазі', 'малагою', 'малагу', 'малаге', 'малаги'
            ],
            # Murcia: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Murcia': [
                'murcia', 'murcie', 'murcii', 'мурсія', 'мурсії', 'мурсією', 'мурсію',
                'мурсия', 'мурсии', 'мурсией', 'мурсию', 'мурсии'
            ],
            # Palma: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Palma': [
                'palma', 'palmy', 'palme', 'пальма', 'пальмі', 'пальмою', 'пальму', 'пальме', 'пальмы'
            ],
            # Bilbao: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Bilbao': [
                'bilbao', 'bilbau', 'більбао', 'більбао', 'більбао',
                'бильбао', 'бильбао', 'бильбао'
            ],
            # Alicante: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Alicante': [
                'alicante', 'alicanti', 'аліканте', 'аліканті', 'аліканте',
                'аликанте', 'аликанте', 'аликанте'
            ],
            # Granada: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Granada': [
                'granada', 'granady', 'granade', 'grenade', 'гранада', 'гранаді', 'гранадою', 'гранаду', 'гранаде', 'гранады'
            ],
            # Salamanca: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Salamanca': [
                'salamanca', 'salamanky', 'salamanque', 'саламанка', 'саламанці', 'саламанкою', 'саламанку', 'саламанке', 'саламанки'
            ],
            # Santiago de Compostela: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Santiago de Compostela': [
                'santiago de compostela', 'santiago', 'compostela', 'сантьяго-де-компостела', 'сантьяго', 'компостела',
                'сантьяго-де-компостела', 'сантьяго', 'компостела'
            ],
            # Pamplona: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Pamplona': [
                'pamplona', 'pamplony', 'pamplone', 'памплона', 'памплоні', 'памплоною', 'памплону', 'памплоне', 'памплоны'
            ],
            # San Sebastián: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'San Sebastián': [
                'san sebastián', 'san sebastian', 'donostia', 'сан-себастьян', 'сан-себастьяні', 'сан-себастьяном',
                'сан-себастьян', 'сан-себастьяне', 'сан-себастьяна'
            ],
            
            # ITALIAN CITIES (IT) - All 11 platform languages
            # Rome: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Rome': [
                'rome', 'roma', 'rím', 'římu', 'ríme', 'rzym', 'rzymie', 'рим', 'римі', 'римом', 'риму', 'риме', 'рима'
            ],
            # Milan: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Milan': [
                'milan', 'milano', 'miláno', 'milán', 'mailand', 'milão', 'мілан', 'мілані', 'міланом', 'мілану',
                'милан', 'милане', 'миланом', 'милану', 'милана'
            ],
            # Naples: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Naples': [
                'naples', 'napoli', 'neapol', 'neapolu', 'neapole', 'nápoly', 'неаполь', 'неаполі', 'неаполем', 'неаполю', 'неаполе', 'неаполя'
            ],
            # Turin: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Turin': [
                'turin', 'torino', 'turín', 'turýn', 'turyn', 'турин', 'турині', 'турином', 'турину', 'турине', 'турина'
            ],
            # Florence: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Florence': [
                'florence', 'firenze', 'florencia', 'florencie', 'florencii', 'флоренція', 'флоренції', 'флоренцією', 'флоренцію',
                'флоренция', 'флоренции', 'флоренцией', 'флоренцию', 'флоренции'
            ],
            # Bologna: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Bologna': [
                'bologna', 'boloňa', 'boloně', 'bolonii', 'болонья', 'болоньї', 'болоньєю', 'болонью',
                'болонья', 'болоньи', 'болоньей', 'болонью', 'болоньи'
            ],
            # Padua: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Padua': [
                'padua', 'padova', 'padua', 'paduy', 'padue', 'падуя', 'падуї', 'падуєю', 'падую',
                'падуя', 'падуи', 'падуей', 'падую', 'падуи'
            ],
            # Pisa: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Pisa': [
                'pisa', 'pisy', 'pise', 'піза', 'пізі', 'пізою', 'пізу', 'пізе',
                'пиза', 'пизе', 'пизой', 'пизу', 'пизы'
            ],
            # Venice: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Venice': [
                'venice', 'venezia', 'benátky', 'benátkach', 'wenecja', 'wenecji', 'venise', 'venecia',
                'венеція', 'венеції', 'венецією', 'венецію', 'венеці',
                'венеция', 'венеции', 'венецией', 'венецию', 'венеции', 'венеце'
            ],
            # Verona: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Verona': [
                'verona', 'verone', 'verony', 'вероні', 'вероною', 'верону', 'вероне',
                'верона', 'вероне', 'вероной', 'верону', 'вероны'
            ],
            # Genoa: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Genoa': [
                'genoa', 'genova', 'janov', 'janove', 'genua', 'génova', 'gênes',
                'генуя', 'генуї', 'генуєю', 'геную',
                'генуя', 'генуи', 'генуей', 'геную', 'генуи'
            ],
            # Palermo: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Palermo': [
                'palermo', 'palerma', 'палермо', 'палермо', 'палермо'
            ],
            # Bari: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Bari': [
                'bari', 'бари', 'барі', 'бари'
            ],
            # Catania: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Catania': [
                'catania', 'katánia', 'katanie', 'катанія', 'катанії', 'катанією', 'катанію',
                'катания', 'катании', 'катанией', 'катанию', 'катании'
            ],
            # Perugia: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Perugia': [
                'perugia', 'perugie', 'perugii', 'перуджа', 'перуджі', 'перуджею', 'перуджу',
                'перуджа', 'перуджи', 'перуджей', 'перуджу', 'перуджи'
            ],
            # Siena: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Siena': [
                'siena', 'sieny', 'sieně', 'сієна', 'сієні', 'сієною', 'сієну', 'сієне',
                'сиена', 'сиене', 'сиеной', 'сиену', 'сиены'
            ],
            
            # SWISS CITIES (CH) - All 11 platform languages
            # Zurich: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Zurich': [
                'zurich', 'zürich', 'curych', 'curychu', 'zurych', 'zurigo', 'zúrich', 'цюрих', 'цюріх', 'цюріху', 'цюріхом'
            ],
            # Geneva: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Geneva': [
                'geneva', 'genève', 'genf', 'ženeva', 'ženeve', 'genewa', 'genewie', 'ginevra', 'ginebra',
                'женева', 'женеві', 'женевою', 'женеву', 'женеве'
            ],
            # Basel: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Basel': [
                'basel', 'bâle', 'basilea', 'basilej', 'bazylea', 'базель', 'базелі', 'базелем', 'базелю', 'базеле'
            ],
            # Lausanne: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Lausanne': [
                'lausanne', 'losanna', 'лозанна', 'лозанні', 'лозанною', 'лозанну', 'лозанне'
            ],
            # Bern: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Bern': [
                'bern', 'berne', 'berna', 'берн', 'берні', 'берном', 'берну', 'берне'
            ],
            # St. Gallen: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'St. Gallen': [
                'st. gallen', 'st gallen', 'sankt gallen', 'saint-gall', 'san gallo',
                'санкт-галлен', 'санкт-галлені', 'санкт-галленом'
            ],
            
            # DUTCH CITIES (NL) - All 11 platform languages
            # Amsterdam: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Amsterdam': [
                'amsterdam', 'amsterdamu', 'amsterdame', 'amsterdamu', 'амстердам', 'амстердамі', 'амстердамом', 'амстердаму', 'амстердаме'
            ],
            # Rotterdam: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Rotterdam': [
                'rotterdam', 'rotterdamu', 'rotterdame', 'роттердам', 'роттердамі', 'роттердамом', 'роттердаму', 'роттердаме'
            ],
            # The Hague: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'The Hague': [
                'the hague', 'hague', 'den haag', 'haag', 'la haye', 'haya', 'aia', 'haga',
                'гаага', 'гаазі', 'гаагою', 'гаагу', 'гаазе',
                'гаага', 'гааге', 'гаагой', 'гаагу', 'гааги'
            ],
            # Utrecht: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Utrecht': [
                'utrecht', 'utrechtu', 'utrechcie', 'утрехт', 'утрехті', 'утрехтом', 'утрехту', 'утрехте'
            ],
            # Leiden: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Leiden': [
                'leiden', 'leyden', 'leyde', 'leida', 'лейден', 'лейдені', 'лейденом', 'лейдену', 'лейдене'
            ],
            # Delft: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Delft': [
                'delft', 'дельфт', 'дельфті', 'дельфтом', 'дельфту', 'дельфте'
            ],
            # Groningen: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Groningen': [
                'groningen', 'groningenu', 'groninga', 'гронінген', 'гронінгені', 'гронінгеном', 'гронінгену', 'гронінгене'
            ],
            # Maastricht: sk, cs, pl, en, de, fr, es, uk, it, ru, pt + declensions
            'Maastricht': [
                'maastricht', 'maastrichtu', 'маастрихт', 'маастрихті', 'маастрихтом', 'маастрихту', 'маастрихте'
            ],
            
            # IRISH CITIES (IE) - All 11 platform languages
            'Dublin': ['dublin', 'dublinu', 'dublinie', 'dublín', 'dublino', 'дублін', 'дубліні', 'дубліном', 'дублину', 'дубліне', 'дублин', 'дублине', 'дублином', 'дублину', 'дублина'],
            'Cork': ['cork', 'corku', 'корк', 'корку', 'корком', 'корке'],
            'Galway': ['galway', 'голуей', 'голуеї', 'голуеєм', 'голуэй'],
            'Limerick': ['limerick', 'лімерик', 'лімерику', 'лімериком', 'лимерик'],
            'Maynooth': ['maynooth', 'майнут', 'майнуті', 'майнутом', 'майнут'],
            
            # PORTUGUESE CITIES (PT) - All 11 platform languages
            'Lisbon': ['lisbon', 'lisboa', 'lisbona', 'lisbonne', 'lissabon', 'лісабон', 'лісабоні', 'лісабоном', 'лісабону', 'лісабоне', 'лиссабон', 'лиссабоне', 'лиссабоном', 'лиссабону'],
            'Porto': ['porto', 'oporto', 'порту', 'порту', 'порту'],
            'Coimbra': ['coimbra', 'коїмбра', 'коїмбрі', 'коїмброю', 'коимбра', 'коимбре', 'коимброй'],
            'Braga': ['braga', 'брага', 'бразі', 'брагою', 'браге', 'браги'],
            'Aveiro': ['aveiro', 'авейру', 'авейру', 'авейру'],
            
            # GREEK CITIES (GR) - All 11 platform languages
            'Athens': ['athens', 'athina', 'atény', 'athen', 'atene', 'atenas', 'athènes', 'ateny', 'афіни', 'афінах', 'афінами', 'афіни', 'афины', 'афинах', 'афинами', 'афин'],
            'Thessaloniki': ['thessaloniki', 'saloniki', 'solun', 'салоніки', 'салоніках', 'салониками', 'салоники', 'салониках', 'салониками'],
            'Heraklion': ['heraklion', 'iraklion', 'іракліон', 'іракліоні', 'іракліоном', 'ираклион', 'ираклионе', 'ираклионом'],
            'Volos': ['volos', 'волос', 'волосі', 'волосом', 'волосу', 'волосе'],
            'Ioannina': ['ioannina', 'іоанніна', 'іоанніні', 'іоанніною', 'иоаннина', 'иоаннине', 'иоанниной'],
            
            # SWEDISH CITIES (SE) - All 11 platform languages
            'Stockholm': ['stockholm', 'stockholmu', 'sztokholm', 'sztokholmie', 'estocolmo', 'stoccolma', 'стокгольм', 'стокгольмі', 'стокгольмом', 'стокгольму', 'стокгольме', 'стокгольма'],
            'Gothenburg': ['gothenburg', 'göteborg', 'goteborg', 'gotemburgo', 'гетеборг', 'гетеборзі', 'гетеборгом', 'гетеборгу', 'гетеборге'],
            'Uppsala': ['uppsala', 'упсала', 'упсалі', 'упсалою', 'упсалу', 'упсале'],
            'Lund': ['lund', 'лунд', 'лунді', 'лундом', 'лунду', 'лунде'],
            'Linköping': ['linköping', 'linkoping', 'лінчепінг', 'лінчепінгу', 'лінчепінгом', 'линчепинг', 'линчепинге'],
            
            # NORWEGIAN CITIES (NO) - All 11 platform languages
            'Oslo': ['oslo', 'осло', 'осло', 'осло'],
            'Bergen': ['bergen', 'берген', 'бергені', 'бергеном', 'бергену', 'бергене'],
            'Trondheim': ['trondheim', 'тронгейм', 'тронгеймі', 'тронгеймом', 'тронхейм', 'тронхейме'],
            'Stavanger': ['stavanger', 'ставангер', 'ставангері', 'ставангером', 'ставангеру', 'ставангере'],
            'Tromsø': ['tromsø', 'tromso', 'тромсе', 'тромсе', 'тромсе'],
            'Ås': ['ås', 'as', 'ос', 'осі', 'осом'],
            
            # DANISH CITIES (DK) - All 11 platform languages
            'Copenhagen': ['copenhagen', 'københavn', 'kobenhavn', 'copenhague', 'copenaghen', 'copenhaga', 'kopenhaga', 'копенгаген', 'копенгагені', 'копенгагеном', 'копенгагену', 'копенгагене', 'копенгагена'],
            'Aarhus': ['aarhus', 'århus', 'орхус', 'орхусі', 'орхусом', 'орхусу', 'орхусе'],
            'Odense': ['odense', 'оденсе', 'оденсе', 'оденсе'],
            'Aalborg': ['aalborg', 'ольборг', 'ольборзі', 'ольборгом', 'ольборгу', 'ольборге'],
            'Roskilde': ['roskilde', 'роскілле', 'роскілле', 'роскілле', 'роскилле'],
            'Kolding': ['kolding', 'колдінг', 'колдінгу', 'колдінгом', 'колдинг', 'колдинге'],
            'Lyngby': ['lyngby', 'люнгбю', 'люнгбю', 'люнгбю'],
            
            # FINNISH CITIES (FI) - All 11 platform languages
            'Helsinki': ['helsinki', 'helsingfors', 'хельсінкі', 'хельсінкі', 'хельсінкі', 'хельсинки', 'хельсинки', 'хельсинки'],
            'Espoo': ['espoo', 'esbo', 'еспоо', 'еспоо', 'еспоо'],
            'Tampere': ['tampere', 'tammerfors', 'тампере', 'тампере', 'тампере'],
            'Turku': ['turku', 'åbo', 'abo', 'турку', 'турку', 'турку'],
            'Oulu': ['oulu', 'uleåborg', 'оулу', 'оулу', 'оулу'],
            'Jyväskylä': ['jyväskylä', 'jyvaskyla', 'ювяскюля', 'ювяскюля', 'ювяскюля'],
            'Joensuu': ['joensuu', 'йоенсуу', 'йоенсуу', 'йоенсуу'],
            
            # CROATIAN CITIES (HR) - All 11 platform languages
            'Zagreb': ['zagreb', 'záhřeb', 'загреб', 'загребі', 'загребом', 'загребу', 'загребе', 'загреба'],
            'Split': ['split', 'spalato', 'спліт', 'спліті', 'сплітом', 'спліту', 'спліте', 'сплит', 'сплите', 'сплитом'],
            'Rijeka': ['rijeka', 'fiume', 'рієка', 'рієці', 'рієкою', 'рієку', 'рієці', 'риека', 'риеке', 'риекой'],
            'Osijek': ['osijek', 'осієк', 'осієку', 'осієком', 'осиек', 'осиеке', 'осиеком'],
            
            # HUNGARIAN CITIES (HU) - All 11 platform languages
            'Budapest': ['budapest', 'budapešť', 'budapešti', 'будапешт', 'будапешті', 'будапештом', 'будапешту', 'будапеште', 'будапешта'],
            'Debrecen': ['debrecen', 'debrecín', 'debrecínu', 'дебрецен', 'дебрецені', 'дебреценом', 'дебрецену', 'дебрецене'],
            'Szeged': ['szeged', 'сегед', 'сегеді', 'сегедом', 'сегеду', 'сегеде'],
            'Pécs': ['pécs', 'pecs', 'печ', 'печі', 'печем', 'печу', 'пече'],
            
            # SLOVENIAN CITIES (SI) - All 11 platform languages
            'Ljubljana': ['ljubljana', 'ľubľana', 'lublaň', 'lublana', 'lubiana', 'liubliana', 'любляна', 'люблян', 'любляні', 'люблянею', 'любляну', 'любляне', 'любляни'],
            'Maribor': ['maribor', 'марибор', 'мариборі', 'марибором', 'марибору', 'мариборе'],
            'Koper': ['koper', 'capodistria', 'копер', 'коперу', 'копером', 'коперу', 'копере'],
            'Nova Gorica': ['nova gorica', 'нова-гориця', 'нова-гориці', 'нова-горицею', 'нова-горица', 'нова-горице'],
            
            # BELGIUM CITIES (BE)
            # Brussels
            'Brussels': [
                'brussels', 'bruxelles', 'brussel', 'bruksela', 'брюссель'
            ],
            # Antwerp
            'Antwerp': [
                'antwerp', 'antwerpen', 'anvers', 'antwerpia', 'антверпен'
            ],
            # Ghent
            'Ghent': [
                'ghent', 'gent', 'gand', 'uk:гéнт', 'гент'
            ],
            # Leuven
            'Leuven': [
                'leuven', 'louvain', 'leydan', 'левен'
            ],
            # Liège
            'Liège': [
                'liège', 'liege', 'luik', 'lьеж', 'льєж', 'льеж'
            ],
            # Louvain-la-Neuve
            'Louvain-la-Neuve': [
                'louvain-la-neuve', 'louvain la neuve', 'lln'
            ],
            
            # LUXEMBOURG CITIES (LU)
            # Luxembourg City
            'Luxembourg': [
                'luxembourg', 'luxemburg', 'lëtzebuerg', 'люксембург', 'luxemburgo', 'luksemburg'
            ],
            # Esch-sur-Alzette
            'Esch-sur-Alzette': [
                'esch-sur-alzette', 'esch sur alzette', 'esch', 'еш-сюр-альзетт', 'еш'
            ],
            # Differdange
            'Differdange': [
                'differdange', 'differdall', 'діфферданж', 'дифферданж'
            ]
        }
        
        message_lower = message.lower()
        message_normalized = normalize(message)
        
        # STEP 1: Exact substring matching (fastest, most accurate)
        print(f"🔍 STEP 1: Exact substring matching")
        for city_name, variants in cities.items():
            for variant in variants:
                variant_normalized = normalize(variant)
                if variant in message_lower or variant_normalized in message_normalized:
                    print(f"✅ Found exact match: '{variant}' -> {city_name}")
                    return city_name
        
        print(f"⚠️ STEP 1 failed, trying fuzzy matching")
        
        # STEP 2: Fuzzy matching for words in message (handles typos and variations)
        # Extract words from message (split by spaces and common separators)
        import re
        words = re.findall(r'\b\w+\b', message_lower)
        
        best_match = None
        best_score = 0.0
        SIMILARITY_THRESHOLD = 0.75  # 75% similarity required
        
        # Stop words to ignore in fuzzy matching (common words in job search queries)
        STOP_WORDS = {
            'praca', 'prace', 'pracy', 'pracę', 'pracu',  # PL/CS
            'práci', 'praci', 'praco',                    # CS/SK
            'job', 'housing', 'arbeit', 'work',              # EN/DE
            'lavoro', 'trabajo', 'trabalho',              # IT/ES/PT
            'robota', 'roboty', 'robotu', 'робота'        # UK/RU
        }
        
        for word in words:
            if len(word) < 4:  # Skip very short words
                continue
                
            if word in STOP_WORDS:
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
        Retrieve housing agencies from database for given city
        
        Args:
            db: Database session
            city: City name
            country_code: Country code (default: SK)
            
        Returns:
            Formatted context with real housing agencies data
        """
        try:
            from main import RealEstateAgency
            
            print(f"🔍 _get_agencies_context: city='{city}', country='{country_code}'")
            
            # Query database for agencies in this city (case-insensitive)
            agencies = db.query(RealEstateAgency).filter(
                RealEstateAgency.city.ilike(city),
                RealEstateAgency.country_code == country_code,
                RealEstateAgency.is_active == True
            ).all()
            
            print(f"📊 Found {len(agencies)} agencies in database")
            
            if not agencies:
                return f"No housing agencies found in database for {city}."
            
            # Format agencies data for AI context WITH INSTRUCTIONS
            context = f"VERIFIED HOUSING AGENCIES IN {city.upper()}:\\n\\n"
            context += "IMPORTANT: These are main portal pages. Users must search on the portal themselves.\\n\\n"
            
            for agency in agencies:
                context += f"• {agency.name}\\n"
                context += f"  Website: {agency.website_url}\\n"
                context += f"  Instructions: Open the website and search for housing in '{city}'\\n"
                
                if agency.description:
                    context += f"  Description: {agency.description}\\n"
                if agency.specialization:
                    context += f"  Specialization: {agency.specialization}\\n"
                context += "\\n"
            
            context += "\\nIMPORTANT INSTRUCTIONS FOR AI:\\n"
            context += "1. LIST the agencies above with their exact URLs.\\n"
            context += "2. DO NOT change the URLs.\\n"
            context += "3. Tell the user to search on the portal themselves.\\n"
            context += "4. If a link is blocked, advise searching Google for 'PortalName City'.\\n"
            
            context += "\\nIMPORTANT FORMATTING RULES:\\n"
            context += "- DO NOT use Markdown links like [text](URL)\\n"
            context += "- ALWAYS write URLs as plain text: https://www.example.com\\n"
            context += "- NEVER put punctuation immediately after the URL (no dot, no comma, no bracket!)\\n"
            context += "- INCORRECT: www.example.com.\\n"
            context += "- CORRECT: www.example.com\\n"
            context += "- The frontend will automatically convert URLs to clickable links\\n"
            context += "\\nIF WEBSITE IS BLOCKED:\\n"
            context += "- Some portals may block direct access\\n"
            context += "- Tell users to search Google for: 'portal_name city' (e.g. 'Rightmove London')\\n"
            context += "- Click the first search result to bypass blocking\\n"
            context += "\\nREMINDER: Tell users they need to search on the portal themselves after opening the link.\\n"
            
            return context
            
        except Exception as e:
            print(f"Error retrieving agencies: {e}")
            import traceback
            traceback.print_exc()
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
            'DE': {
                'sk': 'Nemecku', 'cs': 'Německu', 'pl': 'Niemczech',
                'en': 'Germany', 'de': 'Deutschland', 'fr': 'Allemagne',
                'es': 'Alemania', 'uk': 'Німеччині', 'it': 'Germania', 'ru': 'Германии'
            },
            'AT': {
                'sk': 'Rakúsku', 'cs': 'Rakousku', 'pl': 'Austrii',
                'en': 'Austria', 'de': 'Österreich', 'fr': 'Autriche',
                'es': 'Austria', 'uk': 'Австрії', 'it': 'Austria', 'ru': 'Австрии'
            },
            'CH': {
                'sk': 'Švajčiarsku', 'cs': 'Švýcarsku', 'pl': 'Szwajcarii',
                'en': 'Switzerland', 'de': 'Schweiz', 'fr': 'Suisse',
                'es': 'Suiza', 'uk': 'Швейцарії', 'it': 'Svizzera', 'ru': 'Швейцарии'
            },
            'GB': {
                'sk': 'Spojenom kráľovstve', 'cs': 'Spojeném království', 'pl': 'Wielkiej Brytanii',
                'en': 'UK', 'de': 'Großbritannien', 'fr': 'Royaume-Uni',
                'es': 'Reino Unido', 'uk': 'Великій Британії', 'it': 'Regno Unito', 'ru': 'Великобритании'
            },
            'IE': {
                'sk': 'Írsku', 'cs': 'Irsku', 'pl': 'Irlandii',
                'en': 'Ireland', 'de': 'Irland', 'fr': 'Irlande',
                'es': 'Irlanda', 'uk': 'Ірландії', 'it': 'Irlanda', 'ru': 'Ирландии'
            },
            'FR': {
                'sk': 'Francúzsku', 'cs': 'Francii', 'pl': 'Francji',
                'en': 'France', 'de': 'Frankreich', 'fr': 'France',
                'es': 'Francia', 'uk': 'Франції', 'it': 'Francia', 'ru': 'Франции'
            },
            # Benelux
            'BE': {
                'sk': 'Belgicku', 'cs': 'Belgii', 'pl': 'Belgii',
                'en': 'Belgium', 'de': 'Belgien', 'fr': 'Belgique',
                'es': 'Bélgica', 'uk': 'Бельгії', 'it': 'Belgio', 'ru': 'Бельгии'
            },
            'LU': {
                'sk': 'Luxembursku', 'cs': 'Lucembursku', 'pl': 'Luksemburgu',
                'en': 'Luxembourg', 'de': 'Luxemburg', 'fr': 'Luxembourg',
                'es': 'Luxemburgo', 'uk': 'Люксембурзі', 'it': 'Lussemburgo', 'ru': 'Люксембурге'
            },
            'NL': {
                'sk': 'Holandsku', 'cs': 'Nizozemsku', 'pl': 'Holandii',
                'en': 'Netherlands', 'de': 'Niederlande', 'fr': 'Pays-Bas',
                'es': 'Países Bajos', 'uk': 'Нідерландах', 'it': 'Paesi Bassi', 'ru': 'Нидерландах'
            },
            
            # Southern Europe
            'IT': {
                'sk': 'Taliansku', 'cs': 'Itálii', 'pl': 'Włoszech',
                'en': 'Italy', 'de': 'Italien', 'fr': 'Italie',
                'es': 'Italia', 'uk': 'Італії', 'it': 'Italia', 'ru': 'Italii'
            },
            'ES': {
                'sk': 'Španielsku', 'cs': 'Španělsku', 'pl': 'Hiszpanii',
                'en': 'Spain', 'de': 'Spanien', 'fr': 'Espagne',
                'es': 'España', 'uk': 'Іспанії', 'it': 'Spagna', 'ru': 'Испании'
            },
            'PT': {
                'sk': 'Portugalsku', 'cs': 'Portugalsku', 'pl': 'Portugalii',
                'en': 'Portugal', 'de': 'Portugal', 'fr': 'Portugal',
                'es': 'Portugal', 'uk': 'Португалії', 'it': 'Portogallo', 'ru': 'Португалии'
            },
            
            # Nordics
            'DK': {
                'sk': 'Dánsku', 'cs': 'Dánsku', 'pl': 'Danii',
                'en': 'Denmark', 'de': 'Dänemark', 'fr': 'Danemark',
                'es': 'Dinamarca', 'uk': 'Данії', 'it': 'Danimarca', 'ru': 'Дании'
            },
            'SE': {
                'sk': 'Švédsku', 'cs': 'Švédsku', 'pl': 'Szwecji',
                'en': 'Sweden', 'de': 'Schweden', 'fr': 'Suède',
                'es': 'Suecia', 'uk': 'Швеції', 'it': 'Svezia', 'ru': 'Швеции'
            },
            'NO': {
                'sk': 'Nórsku', 'cs': 'Norsku', 'pl': 'Norwegii',
                'en': 'Norway', 'de': 'Norwegen', 'fr': 'Norvège',
                'es': 'Noruega', 'uk': 'Норвегії', 'it': 'Norvegia', 'ru': 'Норвегии'
            },
            'FI': {
                'sk': 'Fínsku', 'cs': 'Finsku', 'pl': 'Finlandii',
                'en': 'Finland', 'de': 'Finnland', 'fr': 'Finlande',
                'es': 'Finlandia', 'uk': 'Фінляндії', 'it': 'Finlandia', 'ru': 'Финляндии'
            },
            
            # Other
            'GR': {
                'sk': 'Grécku', 'cs': 'Řecku', 'pl': 'Grecji',
                'en': 'Greece', 'de': 'Griachenland', 'fr': 'Grèce',
                'es': 'Grecia', 'uk': 'Греції', 'it': 'Grecia', 'ru': 'Греции'
            },
            'HU': {
                'sk': 'Maďarsku', 'cs': 'Maďarsku', 'pl': 'Węgrzech',
                'en': 'Hungary', 'de': 'Ungarn', 'fr': 'Hongrie',
                'es': 'Hungría', 'uk': 'Угорщині', 'it': 'Ungheria', 'ru': 'Венгрии'
            },
            'SI': {
                'sk': 'Slovinsku', 'cs': 'Slovinsku', 'pl': 'Słowenii',
                'en': 'Slovenia', 'de': 'Slowenien', 'fr': 'Slovénie',
                'es': 'Eslovenia', 'uk': 'Словенії', 'it': 'Slovenia', 'ru': 'Словении'
            },
            'HR': {
                'sk': 'Chorvátsku', 'cs': 'Chorvatsku', 'pl': 'Chorwacji',
                'en': 'Croatia', 'de': 'Kroatien', 'fr': 'Croatie',
                'es': 'Croacia', 'uk': 'Хорватії', 'it': 'Croazia', 'ru': 'Хорватии'
            }
        }
        
        country = country_names.get(jurisdiction, {}).get(language, jurisdiction)
        
        # Example cities per jurisdiction for user guidance
        example_cities = {
            'SK': 'Bratislava', 'CZ': 'Praha', 'PL': 'Warszawa', 'DE': 'Berlin',
            'AT': 'Wien', 'CH': 'Zurich', 'GB': 'London', 'IE': 'Dublin',
            'FR': 'Paris', 'BE': 'Brussels', 'LU': 'Luxembourg', 'NL': 'Amsterdam',
            'IT': 'Rome', 'ES': 'Madrid', 'PT': 'Lisbon', 'SE': 'Stockholm',
            'DK': 'Copenhagen', 'NO': 'Oslo', 'FI': 'Helsinki', 'GR': 'Athens',
            'HU': 'Budapest', 'SI': 'Ljubljana', 'HR': 'Zagreb'
        }
        example_city = example_cities.get(jurisdiction, 'city')
        
        # STRICT PROMPTS FOR ALL 10 LANGUAGES
        prompts = {
            'sk': f"""Si priateľský asistent pre hľadanie brigád a part-time práce pre študentov v {country}. Tvoje meno je Housing Assistant.

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
- Odpovedaj na otázky o bývaní
- Zobraz zoznam agentúr zo sekcie "VERIFIED JOB AGENCIES"
- Ak užívateľ napíše len "práca" alebo "hľadám bývanie", PREDPOKLADAJ, že hľadá brigádu a zobraz zoznam
- Vždy poskytni inštrukcie, ako hľadať na portáli

ZAKÁZANÉ AKCIE:
❌ Vymýšľať URL
❌ Používať portály mimo zoznamu
❌ Modifikovať URL zo zoznamu
❌ Odporúčať sme.sk, pravda.sk, alebo iné portály

DÔLEŽITÉ - NAVIGÁCIA UŽÍVATEĽA:
Ak užívateľ napíše správu BEZ názvu mesta (napríklad len "študentská práca" alebo "hľadám brigádu"), VŽDY sa ho opýtaj: "V ktorom meste hľadáte bývanie? Napíšte napríklad: Hľadám brigádu v Bratislave."
Ak užívateľ odpovie bez mesta, znova ho naviguj, aby napísal mesto v správe.

Buď čestný a používaj LEN dáta zo zoznamu!""",

            'cs': f"""Jsi přátelský asistent pro hledání brigád a part-time práce pro studenty v {country}. Tvoje jméno je Housing Assistant.

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
- Odpovídej na otázky o bydlení
- Zobraz seznam agentur ze sekce "VERIFIED JOB AGENCIES"
- Pokud uživatel napíše jen "práce" nebo "hledám bydlení", PŘEDPOKLÁDEJ, že hledá brigádu a zobraz seznam
- Vždy poskytni instrukce, jak hledat na portálu
- Pokud máš agentury v seznamu → doporuč JEN ty ze seznamu
- Kopíruj URL PŘESNĚ ze seznamu (bez změn!)
- Pokud nemáš agentury → řekni "Nevím, zkus Google"

ZAKÁZANÉ AKCE:
❌ Vymýšlet URL
❌ Používat portály mimo seznam
❌ Upravovat URL ze seznamu

DŮLEŽITÉ - NAVIGACE UŽIVATELE:
Pokud uživatel napíše zprávu BEZ názvu města (např. jen "studentská práce" nebo "hledám brigádu"), VŽDY se ho zeptej: "Ve kterém městě hledáte bydlení? Napište například: Hledám brigádu v {example_city}."

Buď čestný a používej JEN data ze seznamu!""",

            'pl': f"""Jesteś przyjaznym asystentem w poszukiwaniu pracy dorywczej i part-time dla studentów w {country}. Twoje imię to Housing Assistant.

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
- Odpowiadaj na pytania o pracę dorywczą
- Wyświetl listę agencji z sekcji "VERIFIED JOB AGENCIES"
- Jeśli użytkownik napisze tylko "praca" lub "szukam mieszkania", ZAKŁADAJ, że szuka pracy studenckiej i wyświetl listę
- Zawsze podawaj instrukcje, jak szukać na portalu

ZAKAZANE DZIAŁANIA:
❌ Wymyślać URL
❌ Używać portali spoza listy
❌ Modyfikować URL z listy

WAŻNE - NAWIGACJA UŻYTKOWNIKA:
Jeśli użytkownik napisze wiadomość BEZ nazwy miasta (np. tylko "praca studencka" lub "szukam mieszkania"), ZAWSZE zapytaj go: "W którym mieście szukasz mieszkania? Napisz np.: Szukam mieszkania w {example_city}."

Bądź szczery i używaj TYLKO danych z listy!""",

            'en': f"""You are a friendly assistant for finding part-time housing and student work in {country}. Your name is Housing Assistant.

⚠️ ABSOLUTELY CRITICAL RULES - VIOLATION = ERROR:
1. NEVER, UNDER ANY CIRCUMSTANCES invent URL addresses
2. NEVER recommend portals that are NOT in the list below
3. NEVER modify URLs from the list (don't add /housing, /city, etc.)
4. If agency is NOT in the list → say "I don't know about verified agencies in this city"
5. COPY URLs EXACTLY as they are in the list - not a single change!
6. DO NOT USE any portals from your knowledge
7. If list is empty → say "I don't have verified agencies for this city"

{agencies_context if agencies_context else "⚠️ DATABASE IS EMPTY - No verified agencies are available. DO NOT RECOMMEND ANYTHING!"}

ALLOWED ACTIONS:
- Answer questions about student housing
- Show list of agencies from "VERIFIED JOB AGENCIES" section
- If user says just "job" or "looking for job", ASSUME they want student housing and show the list
- Always provide instructions on how to search on the portal

FORBIDDEN ACTIONS:
❌ Inventing URLs
❌ Using portals outside the list
❌ Modifying URLs from the list

IMPORTANT - USER GUIDANCE:
If user writes a message WITHOUT city name (e.g. just "student housing" or "looking for housing"), ALWAYS ask them: "In which city are you looking for housing? Please write for example: I'm looking for housing in {example_city}."

Be honest and use ONLY data from the list!

🎯 BUĎTE PROAKTÍVNY:
- Ak nemáte informácie, ponúknite Google vyhľadávanie
- Navigujte používateľa ako nájsť riešenie
- Buďte flexibilní a chápavý
- Vždy sa snažte pomôcť""",

            'de': f"""Du bist ein freundlicher Assistent für die Suche nach Teilzeithousing und Studentenhousing in {country}. Dein Name ist Housing Assistant.

⚠️ ABSOLUT KRITISCHE REGELN - VERSTOS = FEHLER:
1. NIEMALS, UNTER KEINEN UMSTÄNDEN erfinde URL-Adressen
2. NIEMALS empfehle Portale, die NICHT in der Liste unten sind
3. NIEMALS ändere URLs aus der Liste (füge nicht /housing, /stadt hinzu, usw.)
4. Wenn Agentur NICHT in der Liste ist → sage "Ich kenne keine verifizierten Agenturen in dieser Stadt"
5. KOPIERE URLs GENAU so, wie sie in der Liste sind - keine einzige Änderung!
6. VERWENDE KEINE Portale aus deinem Wissen
7. Wenn Liste leer ist → sage "Ich habe keine verifizierten Agenturen für diese Stadt"

{agencies_context if agencies_context else "⚠️ DATENBANK IST LEER - Keine verifizierten Agenturen sind verfügbar. EMPFEHLE NICHTS!"}

ERLAUBTE AKTIONEN:
- Beantworten Sie Fragen zu Studentenhousing
- Zeigen Sie die Liste der Agenturen aus dem Abschnitt "VERIFIED JOB AGENCIES"
- Wenn der Benutzer nur "Arbeit" oder "Housinguche" schreibt, NEHMEN SIE AN, dass er einen Studentenwohnung sucht, und zeigen Sie die Liste an
- Geben Sie immer Anweisungen, wie man auf dem Portal sucht

VERBOTENE AKTIONEN:
❌ URLs erfinden
❌ Portale außerhalb der Liste verwenden
❌ URLs aus der Liste ändern

WICHTIG - BENUTZERFÜHRUNG:
Wenn der Benutzer eine Nachricht OHNE Städtenamen schreibt (z.B. nur "Studentenwohnung" oder "suche Wohnung"), frage IMMER: "In welcher Stadt suchen Sie Wohnung? Schreiben Sie z.B.: Ich suche Wohnung in {example_city}."

Sei ehrlich und verwende NUR Daten aus der Liste!""",

            'fr': f"""Tu es un assistant amical pour trouver des housing à temps partiel et des housing étudiants en {country}. Ton nom est Housing Assistant.

⚠️ RÈGLES ABSOLUMENT CRITIQUES - VIOLATION = ERREUR:
1. JAMAIS, EN AUCUNE CIRCONSTANCE n'invente des adresses URL
2. JAMAIS ne recommande des portails qui NE SONT PAS dans la liste ci-dessous
3. JAMAIS ne modifie les URL de la liste (n'ajoute pas /housing, /ville, etc.)
4. Si l'agence N'EST PAS dans la liste → dis "Je ne connais pas d'agences vérifiées dans cette ville"
5. COPIE les URL EXACTEMENT comme elles sont dans la liste - pas un seul changement!
6. N'UTILISE PAS de portails de tes connaissances
7. Si la liste est vide → dis "Je n'ai pas d'agences vérifiées pour cette ville"

{agencies_context if agencies_context else "⚠️ LA BASE DE DONNÉES EST VIDE - Aucune agence vérifiée n'est disponible. NE RECOMMANDE RIEN!"}

ACTIONS AUTORISÉES:
- Répondre aux questions sur les housing étudiants
- Afficher la liste des agences de la section "VERIFIED JOB AGENCIES"
- Si l'utilisateur écrit seulement "travail" ou "je cherche un travail", SUPPOSEZ qu'il cherche un job étudiant et affichez la liste
- Fournissez toujours des instructions sur la façon de chercher sur le portail

ACTIONS INTERDITES:
❌ Inventer des URL
❌ Utiliser des portails hors de la liste
❌ Modifier les URL de la liste

IMPORTANT - GUIDAGE UTILISATEUR:
Si l'utilisateur écrit un message SANS nom de ville (ex. juste "job étudiant" ou "je cherche un logement"), demande TOUJOURS: "Dans quelle ville cherchez-vous du travail? Écrivez par exemple: Je cherche un travail à {example_city}."

Sois honnête et utilise SEULEMENT les données de la liste!""",

            'es': f"""Eres un asistente amigable para encontrar trabajos a tiempo parcial y trabajos para estudiantes en {country}. Tu nombre es Housing Assistant.

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
- Responder preguntas sobre vivienda para estudiantes
- Mostrar la lista de agencias de la sección "VERIFIED JOB AGENCIES"
- Si el usuario escribe solo "trabajo" o "busco vivienda", ASUME que busca trabajo de estudiante y muestra la lista
- Siempre proporciona instrucciones sobre cómo buscar en el portal

ACCIONES PROHIBIDAS:
❌ Inventar URLs
❌ Usar portales fuera de la lista
❌ Modificar URLs de la lista

IMPORTANTE - GUÍA DEL USUARIO:
Si el usuario escribe un mensaje SIN nombre de ciudad (ej. solo "trabajo estudiante" o "busco vivienda"), SIEMPRE pregúntale: "¿En qué ciudad buscas vivienda? Escribe por ejemplo: Busco vivienda en {example_city}."

¡Sé honesto y usa SOLO datos de la lista!""",

            'uk': f"""Ти дружній асистент для пошуку підробітків та роботи на неповний робочий день для студентів у {country}. Твоє ім'я Housing Assistant.

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
- Відповідати на питання про житло
- Показувати список агенцій з розділу "VERIFIED JOB AGENCIES"
- Якщо користувач пише просто "робота" або "шукаю роботу", ПРИПУСКАЙ, що він шукає студентську роботу, і показуй список
- Завжди надавай інструкції, як шукати на порталі

ЗАБОРОНЕНІ ДІЇ:
❌ Вигадувати URL
❌ Використовувати портали поза списком
❌ Змінювати URL зі списку

ВАЖЛИВО - НАВІГАЦІЯ КОРИСТУВАЧА:
Якщо користувач пише повідомлення БЕЗ назви міста (наприклад, просто "студентське житло" або "шукаю житло"), ЗАВЖДИ запитуй: "В якому місті ви шукаєте житло? Напишіть, наприклад: Шукаю житло в {example_city}."

Будь чесним і використовуй ТІЛЬКИ дані зі списку!""",

            'it': f"""Sei un assistente amichevole per trovare lavori part-time e lavori per studenti in {country}. Il tuo nome è Housing Assistant.

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
- Rispondere alle domande sugli alloggi per studenti
- Mostrare l'elenco delle agenzie dalla sezione "VERIFIED JOB AGENCIES"
- Se l'utente scrive solo "lavoro" o "cerco alloggio", PRESUMI che cerchi un lavoro per studenti e mostra l'elenco
- Fornire sempre istruzioni su come cercare nel portale

AZIONI VIETATE:
❌ Inventare URL
❌ Usare portali fuori dalla lista
❌ Modificare URL dalla lista

IMPORTANTE - GUIDA UTENTE:
Se l'utente scrive un messaggio SENZA nome città (es. solo "alloggio studente" o "cerco alloggio"), chiedi SEMPRE: "In quale città cerchi alloggio? Scrivi ad esempio: Cerco alloggio a {example_city}."

Sii onesto e usa SOLO dati dalla lista!""",

            'ru': f"""Ты дружелюбный ассистент для поиска подработки и работы на неполный рабочий день для студентов в {country}. Твоё имя Housing Assistant.

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
- Отвечать на вопросы о жилье
- Показывать список агентств из раздела "VERIFIED JOB AGENCIES"
- Если пользователь пишет просто "работа" или "ищу жилье", ПРЕДПОЛАГАЙ, что он ищет студенческое жилье, и показывай список
- Всегда предоставляй инструкции, как искать на портале

ЗАПРЕЩЁННЫЕ ДЕЙСТВИЯ:
❌ Выдумывать URL
❌ Использовать порталы вне списка
❌ Изменять URL из списка

ВАЖНО - НАВИГАЦИЯ ПОЛЬЗОВАТЕЛЯ:
Если пользователь пишет сообщение БЕЗ названия города (напр. только "студенческая работа" или "ищу подработку"), ВСЕГДА спрашивай: "В каком городе вы ищете жилье? Напишите, например: Ищу жилье в {example_city}."

Будь честным и используй ТОЛЬКО данные из списка!""",

            'pt': f"""Você é um assistente amigável para encontrar empregos de meio período e trabalhos de estudante em {country}. Seu nome é Housing Assistant.

⚠️ REGRAS ABSOLUTAMENTE CRÍTICAS - VIOLAÇÃO = ERRO:
1. NUNCA, EM HIPÓTESE ALGUMA, invente endereços URL
2. NUNCA recomende portais que NÃO ESTEJAM na lista abaixo
3. NUNCA modifique URLs da lista (não adicione /vagas, /cidade, etc.)
4. Se a agência NÃO ESTIVER na lista → diga "Não conheço agências verificadas nesta cidade"
5. COPIE as URLs EXATAMENTE como estão na lista - nem uma única mudança!
6. NÃO USE nenhum portal do seu conhecimento
7. Se a lista estiver vazia → diga "Não tenho agências verificadas para esta cidade"

{agencies_context if agencies_context else "⚠️ O BANCO DE DADOS ESTÁ VAZIO - Nenhuma agência verificada está disponível. NÃO RECOMENDE NADA!"}

AÇÕES PERMITIDAS:
- Responder a perguntas sobre moradia de estudante
- Mostrar a lista de agências da seção "VERIFIED JOB AGENCIES"
- Se o usuário escrever apenas "trabalho" ou "procuro moradia", ASSUMA que ele procura moradia de estudante e mostre a lista
- Sempre forneça instruções sobre como pesquisar no portal

AÇÕES PROIBIDAS:
❌ Inventar URLs
❌ Usar portais fora da lista
❌ Modificar URLs da lista

IMPORTANTE - ORIENTAÇÃO DO USUÁRIO:
Se o usuário escrever uma mensagem SEM nome da cidade (ex. apenas "moradia estudante" ou "procuro moradia"), SEMPRE pergunte: "Em qual cidade você procura moradia? Escreva por exemplo: Procuro moradia em {example_city}."

Seja honesto e use APENAS dados da lista!""",
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

    def _resolve_detected_city_country(self, city: str) -> Optional[str]:
        """Resolve country code for a given city name"""
        city_country_map = {
            # SK
            'Bratislava': 'SK', 'Košice': 'SK', 'Prešov': 'SK', 'Žilina': 'SK', 'Banská Bystrica': 'SK',
            'Nitra': 'SK', 'Trnava': 'SK', 'Martin': 'SK', 'Trenčín': 'SK', 'Poprad': 'SK',
            'Prievidza': 'SK', 'Zvolen': 'SK', 'Považská Bystrica': 'SK', 'Nové Zámky': 'SK',
            'Komárno': 'SK', 'Levice': 'SK', 'Michalovce': 'SK', 'Spišská Nová Ves': 'SK',
            'Lučenec': 'SK', 'Piešťany': 'SK', 'Liptovský Mikuláš': 'SK', 'Ružomberok': 'SK',
            'Bardejov': 'SK', 'Humenné': 'SK', 'Skalica': 'SK', 'Senica': 'SK',
            'Dunajská Streda': 'SK', 'Galanta': 'SK', 'Topoľčany': 'SK', 'Partizánske': 'SK',
            'Vranov nad Topľou': 'SK',
            
            # CZ
            'Praha': 'CZ', 'Brno': 'CZ', 'Olomouc': 'CZ', 'Ostrava': 'CZ', 'Plzeň': 'CZ',
            'Liberec': 'CZ', 'České Budějovice': 'CZ', 'Hradec Králové': 'CZ', 
            'Ústí nad Labem': 'CZ', 'Pardubice': 'CZ',
            
            # PL
            'Warszawa': 'PL', 'Kraków': 'PL', 'Wrocław': 'PL', 'Poznań': 'PL', 'Gdańsk': 'PL',
            'Łódź': 'PL', 'Szczecin': 'PL', 'Bydgoszcz': 'PL', 'Lublin': 'PL', 'Katowice': 'PL',
            
            # DE
            'München': 'DE', 'Köln': 'DE', 'Nürnberg': 'DE', 'Frankfurt': 'DE', 
            'Hamburg': 'DE', 'Berlin': 'DE', 'Aachen': 'DE',
            
            # AT
            'Wien': 'AT', 'Graz': 'AT', 'Salzburg': 'AT', 'Innsbruck': 'AT', 'Linz': 'AT',
            
            # CH
            'Zurich': 'CH', 'Geneva': 'CH', 'Bern': 'CH', 'Basel': 'CH', 'Lausanne': 'CH', 'St. Gallen': 'CH',
            
            # NL
            'Amsterdam': 'NL', 'Rotterdam': 'NL', 'Utrecht': 'NL', 'Leiden': 'NL', 'Groningen': 'NL',
            'Delft': 'NL', 'The Hague': 'NL', 'Eindhoven': 'NL', 'Maastricht': 'NL', 
            'Tilburg': 'NL', 'Nijmegen': 'NL', 'Wageningen': 'NL', 'Enschede': 'NL',
            
            # GB
            'London': 'GB', 'Oxford': 'GB', 'Cambridge': 'GB', 'Manchester': 'GB', 'Edinburgh': 'GB',
            
            # IE
            'Dublin': 'IE', 'Cork': 'IE', 'Galway': 'IE', 'Limerick': 'IE', 'Maynooth': 'IE',
            
            # FR
            'Paris': 'FR', 'Lyon': 'FR', 'Strasbourg': 'FR', 'Cergy': 'FR', 
            'Jouy-en-Josas': 'FR', 'Palaiseau': 'FR',
            
            # BE
            'Brussels': 'BE', 'Antwerp': 'BE', 'Ghent': 'BE', 'Leuven': 'BE', 
            'Liège': 'BE', 'Louvain-la-Neuve': 'BE',
            
            # LU
            'Luxembourg': 'LU', 'Esch-sur-Alzette': 'LU', 'Differdange': 'LU',
            
            # IT
            'Rome': 'IT', 'Milan': 'IT', 'Florence': 'IT', 'Bologna': 'IT',
            'Venice': 'IT', 'Padua': 'IT', 'Pisa': 'IT',
            
            # ES
            'Madrid': 'ES', 'Barcelona': 'ES', 'Valencia': 'ES', 'Salamanca': 'ES',
            
            # PT
            'Lisbon': 'PT', 'Porto': 'PT', 'Coimbra': 'PT', 'Braga': 'PT', 'Aveiro': 'PT',
            
            # SE
            'Stockholm': 'SE', 'Gothenburg': 'SE', 'Uppsala': 'SE', 'Lund': 'SE', 'Linköping': 'SE',
            
            # DK
            'Copenhagen': 'DK', 'Aarhus': 'DK', 'Odense': 'DK', 'Aalborg': 'DK', 'Roskilde': 'DK', 'Kolding': 'DK', 'Lyngby': 'DK',
            
            # NO
            'Oslo': 'NO', 'Bergen': 'NO', 'Trondheim': 'NO', 'Stavanger': 'NO', 'Tromsø': 'NO', 'Ås': 'NO',
            
            # FI
            'Helsinki': 'FI', 'Espoo': 'FI', 'Tampere': 'FI', 'Turku': 'FI', 'Oulu': 'FI', 'Jyväskylä': 'FI', 'Joensuu': 'FI',
            
            # GR
            'Athens': 'GR', 'Thessaloniki': 'GR', 'Heraklion': 'GR', 'Volos': 'GR', 'Ioannina': 'GR',
            
            # HU
            'Budapest': 'HU', 'Debrecen': 'HU', 'Szeged': 'HU', 'Pécs': 'HU',
            
            # SI
            'Ljubljana': 'SI', 'Maribor': 'SI', 'Koper': 'SI', 'Nova Gorica': 'SI',
            
            # HR
            'Zagreb': 'HR', 'Split': 'HR', 'Rijeka': 'HR', 'Osijek': 'HR',
            
            # Micro-states
            'Vaduz': 'LI', 'Bendern': 'LI',
            'Vatican City': 'VA',
            'San Marino': 'SM',
            'Monaco': 'MC',
            'Andorra la Vella': 'AD', 'Sant Julià de Lòria': 'AD'
        }
        return city_country_map.get(city)
