#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Jobs Chat Service with automatic city detection
This replaces the existing jobs_chat_service.py
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
            language: User's language preference
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
                print(f"🏙️ Auto-detected city: {city}")
        
        # Retrieve agencies context from database if city available
        agencies_context = ""
        if db and city:
            agencies_context = self._get_agencies_context(db, city, jurisdiction)
            print(f"📋 Retrieved {len(agencies_context)} chars of agency context for {city}")
        
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
        Extract city name from user message - AUTOMATIC DETECTION
        Supports all Slovak cities with educational institutions
        
        Args:
            message: User's message
            country_code: Country code (default: SK)
            
        Returns:
            City name if found, None otherwise
        """
        if country_code != 'SK':
            return None
        
        # ALL SLOVAK CITIES WITH EDUCATIONAL INSTITUTIONS
        # Pattern -> Official City Name
        slovak_cities = {
            # Major cities
            'bratislav': 'Bratislava',
            'košic': 'Košice',
            'koši': 'Košice',
            'prešov': 'Prešov',
            'žilin': 'Žilina',
            'zilin': 'Žilina',
            'bansk': 'Banská Bystrica',
            'nitra': 'Nitra',
            'trnav': 'Trnava',
            'martin': 'Martin',
            'trenčín': 'Trenčín',
            'trencin': 'Trenčín',
            
            # Medium cities
            'poprad': 'Poprad',
            'prievidz': 'Prievidza',
            'zvolen': 'Zvolen',
            'považsk': 'Považská Bystrica',
            'povazsk': 'Považská Bystrica',
            'nové zámk': 'Nové Zámky',
            'nove zamk': 'Nové Zámky',
            'komárn': 'Komárno',
            'komarn': 'Komárno',
            'levic': 'Levice',
            'michalovce': 'Michalovce',
            'spišsk': 'Spišská Nová Ves',
            'spissk': 'Spišská Nová Ves',
            'lučenec': 'Lučenec',
            'lucenec': 'Lučenec',
            'piešťan': 'Piešťany',
            'piest': 'Piešťany',
            'liptovsk': 'Liptovský Mikuláš',
            
            # Smaller cities with universities
            'ružomberok': 'Ružomberok',
            'ruzomberok': 'Ružomberok',
            'bardejov': 'Bardejov',
            'humenné': 'Humenné',
            'humenne': 'Humenné',
            'skalica': 'Skalica',
            'senica': 'Senica',
            'dunajsk': 'Dunajská Streda',
            'galanta': 'Galanta',
            'topoľčan': 'Topoľčany',
            'topolcan': 'Topoľčany',
            'partizánsk': 'Partizánske',
            'partizansk': 'Partizánske',
            'vranov': 'Vranov nad Topľou',
        }
        
        message_lower = message.lower()
        
        # Check for city mentions
        for pattern, city in slovak_cities.items():
            if pattern in message_lower:
                return city
        
        return None
    
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
        }
        
        return prompts.get(language, prompts['sk'])
    
    def _get_error_message(self, language: str) -> str:
        messages = {
            'sk': 'Prepáčte, nastala chyba. Skúste to prosím znova.',
        }
        return messages.get(language, messages['sk'])
