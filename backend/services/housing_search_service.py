#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Housing Search Service
Professional housing consultant for students
Searches for accommodation at universities and real estate agencies
"""

import os
import re
from typing import Dict, List, Optional
import openai
from sqlalchemy.orm import Session


class HousingSearchAgent:
    """Professional Housing Consultant for Students"""
    
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key
        
    async def search_housing(
        self,
        university_name: str,
        university_website: str,
        city: str,
        country: str,
        language: str = 'sk'
    ) -> Dict:
        """
        Search for housing options for a student
        
        Args:
            university_name: Name of the university
            university_website: University website URL
            city: City where university is located
            country: Country code (SK, CZ, PL, etc.)
            language: User's language preference
            
        Returns:
            Dict with housing information and links
        """
        
        # Step 1: Check if university provides accommodation
        university_housing = await self._check_university_housing(
            university_name, university_website, language
        )
        
        # Step 2: Find real estate agencies in the city
        real_estate_agencies = await self._find_real_estate_agencies(
            city, country, language
        )
        
        # Step 3: Generate response with links
        response = self._generate_response(
            university_name,
            city,
            university_housing,
            real_estate_agencies,
            language
        )
        
        return response
    
    async def _check_university_housing(
        self,
        university_name: str,
        university_website: str,
        language: str
    ) -> Dict:
        """
        Use AI to determine if university provides student accommodation.
        IMPORTANT: Never fabricate information. Only provide verified data.
        """
        
        prompt = f"""You are an HONEST housing search assistant for students.

CRITICAL RULES:
1. NEVER make up information or URLs
2. If you don't know something for certain, say "I don't know"
3. Only provide information you are confident about
4. Always be transparent about uncertainty

Task: Based on your training data, do you have VERIFIED information about student housing at {university_name}?

University website: {university_website}

Respond in JSON format:
{{
    "has_verified_info": true/false,
    "has_housing": true/false/null,
    "housing_page_url": "ONLY if you know the exact URL, otherwise use main website",
    "description": "Brief HONEST description in {language} language",
    "confidence": "high/medium/low",
    "recommendation": "What student should do next"
}}

If you DON'T have verified information, set has_verified_info to false and recommend checking the university website directly.

Respond ONLY with valid JSON, no other text."""

        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an HONEST housing search assistant. NEVER fabricate information. If uncertain, admit it and suggest alternatives."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Lower temperature for more factual responses
                max_tokens=600
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            import json
            result = json.loads(result_text)
            
            # If AI doesn't have verified info, be honest
            if not result.get('has_verified_info', False):
                return {
                    "has_housing": None,
                    "housing_page_url": university_website,
                    "description": self._get_honest_fallback_text(language, university_name),
                    "confidence": "low",
                    "recommendation": self._get_google_search_recommendation(language, university_name)
                }
            
            return result
            
        except Exception as e:
            print(f"Error checking university housing: {e}")
            # Honest fallback response
            return {
                "has_housing": None,
                "housing_page_url": university_website,
                "description": self._get_honest_fallback_text(language, university_name),
                "confidence": "low",
                "recommendation": self._get_google_search_recommendation(language, university_name)
            }
    
    async def _find_real_estate_agencies(
        self,
        city: str,
        country: str,
        language: str
    ) -> List[Dict]:
        """
        Get real estate agencies from database by city
        """
        try:
            # Import here to avoid circular dependency
            from main import RealEstateAgency, get_db
            
            # Get database session
            db = next(get_db())
            
            # Query agencies for this city
            agencies = db.query(RealEstateAgency).filter(
                RealEstateAgency.city == city,
                RealEstateAgency.country_code == country,
                RealEstateAgency.is_active == True
            ).all()
            
            # Convert to dict format
            result = []
            for agency in agencies:
                result.append({
                    'name': agency.name,
                    'website': agency.website_url,
                    'description': agency.description or f"Real estate agency in {city}",
                    'phone': agency.phone,
                    'email': agency.email,
                    'specialization': agency.specialization
                })
            
            # If we have agencies from database, return them
            if result:
                print(f"✅ Found {len(result)} agencies in database for {city}")
                return result
            
            # Fallback to hardcoded list if no agencies in database
            print(f"⚠️ No agencies in database for {city}, using fallback")
            return self._get_fallback_agencies(city, country, language)
            
        except Exception as e:
            print(f"Error finding real estate agencies: {e}")
            # Fallback response
            return self._get_fallback_agencies(city, country, language)
    
    def _generate_response(
        self,
        university_name: str,
        city: str,
        university_housing: Dict,
        agencies: List[Dict],
        language: str
    ) -> Dict:
        """
        Generate final response with all housing options
        """
        
        translations = {
            'sk': {
                'title': '🏠 Možnosti ubytovania',
                'university_section': '🎓 Univerzitné ubytovanie',
                'check_here': 'Skontrolujte tu',
                'agencies_section': '🏢 Realitné agentúry v meste',
                'visit': 'Navštíviť',
                'recommendation': '💡 Odporúčanie: Najprv skontrolujte možnosti univerzitného ubytovania, pretože sú zvyčajne cenovo výhodnejšie.'
            },
            'cs': {
                'title': '🏠 Možnosti ubytování',
                'university_section': '🎓 Univerzitní ubytování',
                'check_here': 'Zkontrolujte zde',
                'agencies_section': '🏢 Realitní agentury ve městě',
                'visit': 'Navštívit',
                'recommendation': '💡 Doporučení: Nejprve zkontrolujte možnosti univerzitního ubytování, protože jsou obvykle cenově výhodnější.'
            },
            'en': {
                'title': '🏠 Housing Options',
                'university_section': '🎓 University Accommodation',
                'check_here': 'Check here',
                'agencies_section': '🏢 Real Estate Agencies in the City',
                'visit': 'Visit',
                'recommendation': '💡 Recommendation: First check university accommodation options as they are usually more affordable.'
            },
            'uk': {
                'title': '🏠 Варіанти житла',
                'university_section': '🎓 Університетське житло',
                'check_here': 'Перевірте тут',
                'agencies_section': '🏢 Агентства нерухомості в місті',
                'visit': 'Відвідати',
                'recommendation': '💡 Рекомендація: Спочатку перевірте можливості університетського житла, оскільки вони зазвичай дешевші.'
            },
            'pl': {
                'title': '🏠 Opcje zakwaterowania',
                'university_section': '🎓 Zakwaterowanie uniwersyteckie',
                'check_here': 'Sprawdź tutaj',
                'agencies_section': '🏢 Agencje nieruchomości w mieście',
                'visit': 'Odwiedź',
                'recommendation': '💡 Rekomendacja: Najpierw sprawdź opcje zakwaterowania uniwersyteckiego, ponieważ są zazwyczaj tańsze.'
            },
            'de': {
                'title': '🏠 Unterkunftsmöglichkeiten',
                'university_section': '🎓 Universitätsunterkunft',
                'check_here': 'Hier prüfen',
                'agencies_section': '🏢 Immobilienagenturen in der Stadt',
                'visit': 'Besuchen',
                'recommendation': '💡 Empfehlung: Prüfen Sie zuerst die Universitätsunterkunft, da diese in der Regel günstiger ist.'
            },
            'fr': {
                'title': '🏠 Options de logement',
                'university_section': '🎓 Logement universitaire',
                'check_here': 'Vérifier ici',
                'agencies_section': '🏢 Agences immobilières de la ville',
                'visit': 'Visiter',
                'recommendation': '💡 Recommandation: Vérifiez d\'abord les options de logement universitaire car elles sont généralement plus abordables.'
            },
            'es': {
                'title': '🏠 Opciones de alojamiento',
                'university_section': '🎓 Alojamiento universitario',
                'check_here': 'Consultar aquí',
                'agencies_section': '🏢 Agencias inmobiliarias de la ciudad',
                'visit': 'Visitar',
                'recommendation': '💡 Recomendación: Primero consulte las opciones de alojamiento universitario ya que suelen ser más económicas.'
            },
            'it': {
                'title': '🏠 Opzioni di alloggio',
                'university_section': '🎓 Alloggio universitario',
                'check_here': 'Controlla qui',
                'agencies_section': '🏢 Agenzie immobiliari della città',
                'visit': 'Visita',
                'recommendation': '💡 Raccomandazione: Controlla prima le opzioni di alloggio universitario perché sono solitamente più convenienti.'
            },
            'ru': {
                'title': '🏠 Варианты жилья',
                'university_section': '🎓 Университетское жилье',
                'check_here': 'Проверьте здесь',
                'agencies_section': '🏢 Агентства недвижимости в городе',
                'visit': 'Посетить',
                'recommendation': '💡 Рекомендация: Сначала проверьте варианты университетского жилья, так как они обычно дешевле.'
            }
        }
        
        t = translations.get(language, translations['en'])
        
        return {
            'title': t['title'],
            'university_housing': {
                'available': university_housing.get('has_housing', True),
                'url': university_housing.get('housing_page_url', ''),
                'description': university_housing.get('description', ''),
                'label': t['university_section']
            },
            'real_estate_agencies': [
                {
                    'name': agency['name'],
                    'url': agency['website'],
                    'description': agency['description']
                }
                for agency in agencies
            ],
            'agencies_label': t['agencies_section'],
            'visit_label': t['visit'],
            'recommendation': t['recommendation']
        }
    
    def _get_fallback_housing_text(self, language: str) -> str:
        """Fallback text when AI fails"""
        texts = {
            'sk': 'Univerzita pravdepodobne poskytuje študentské ubytovanie. Skontrolujte oficiálnu stránku univerzity.',
            'cs': 'Univerzita pravděpodobně poskytuje studentské ubytování. Zkontrolujte oficiální stránku univerzity.',
            'en': 'The university likely provides student accommodation. Check the official university website.',
            'uk': 'Університет ймовірно надає студентське житло. Перевірте офіційний сайт університету.',
            'pl': 'Uniwersytet prawdopodobnie zapewnia zakwaterowanie dla studentów. Sprawdź oficjalną stronę uniwersytetu.',
            'de': 'Die Universität bietet wahrscheinlich Studentenunterkünfte an. Überprüfen Sie die offizielle Website der Universität.',
            'fr': 'L\'université propose probablement un logement étudiant. Consultez le site officiel de l\'université.',
            'es': 'La universidad probablemente ofrece alojamiento para estudiantes. Consulte el sitio web oficial de la universidad.',
            'it': 'L\'università probabilmente offre alloggi per studenti. Controlla il sito ufficiale dell\'università.',
            'ru': 'Университет, вероятно, предоставляет студенческое жилье. Проверьте официальный сайт университета.'
        }
        return texts.get(language, texts['en'])
    
    def _get_fallback_agencies(self, city: str, country: str, language: str) -> List[Dict]:
        """Fallback agencies when AI fails"""
        
        # Common real estate platforms by country
        fallback_data = {
            'SK': [
                {'name': 'Nehnuteľnosti.sk', 'website': 'https://www.nehnutelnosti.sk', 'description': 'Najväčší portál s nehnuteľnosťami na Slovensku'},
                {'name': 'Reality.sk', 'website': 'https://www.reality.sk', 'description': 'Populárny realitný portál'},
                {'name': 'Topreality.sk', 'website': 'https://www.topreality.sk', 'description': 'Realitná kancelária s ponukou bytov'}
            ],
            'CZ': [
                {'name': 'Sreality.cz', 'website': 'https://www.sreality.cz', 'description': 'Největší realitní portál v ČR'},
                {'name': 'Bezrealitky.cz', 'website': 'https://www.bezrealitky.cz', 'description': 'Inzeráty bez realitních kanceláří'},
                {'name': 'Reality.cz', 'website': 'https://www.reality.cz', 'description': 'Realitní portál'}
            ],
            'PL': [
                {'name': 'OLX.pl', 'website': 'https://www.olx.pl/nieruchomosci', 'description': 'Popularna platforma ogłoszeniowa'},
                {'name': 'Otodom.pl', 'website': 'https://www.otodom.pl', 'description': 'Największy portal nieruchomości w Polsce'},
                {'name': 'Gratka.pl', 'website': 'https://www.gratka.pl', 'description': 'Portal z ofertami nieruchomości'}
            ],
            'SI': [
                {'name': 'Nepremicnine.net', 'website': 'https://www.nepremicnine.net', 'description': 'Največji portal za nepremičnine v Sloveniji'},
                {'name': 'Bolha.com', 'website': 'https://www.bolha.com', 'description': 'Oglasna platforma'},
            ],
            'HU': [
                {'name': 'Ingatlan.com', 'website': 'https://www.ingatlan.com', 'description': 'Legnagyobb ingatlan portál Magyarországon'},
                {'name': 'Jofogas.hu', 'website': 'https://www.jofogas.hu', 'description': 'Hirdetési platform'},
            ]
        }
        
        return fallback_data.get(country, fallback_data['SK'])
    
    def _get_honest_fallback_text(self, language: str, university_name: str) -> str:
        """Honest fallback text when AI doesn't have verified information"""
        texts = {
            'sk': f'Prepáčte, nemám overené informácie o ubytovaní na {university_name}. Odporúčam navštíviť oficiálnu stránku univerzity alebo kontaktovať ich priamo.',
            'cs': f'Promiňte, nemám ověřené informace o ubytování na {university_name}. Doporučuji navštívit oficiální stránku univerzity nebo je kontaktovat přímo.',
            'en': f'Sorry, I don\'t have verified information about accommodation at {university_name}. I recommend visiting the official university website or contacting them directly.',
            'uk': f'Вибачте, я не маю перевіреної інформації про житло в {university_name}. Рекомендую відвідати офіційний сайт університету або зв\'язатися з ними безпосередньо.',
            'pl': f'Przepraszam, nie mam zweryfikowanych informacji o zakwaterowaniu na {university_name}. Polecam odwiedzić oficjalną stronę uniwersytetu lub skontaktować się z nimi bezpośrednio.',
            'de': f'Entschuldigung, ich habe keine verifizierten Informationen über die Unterkunft an der {university_name}. Ich empfehle, die offizielle Website der Universität zu besuchen oder sie direkt zu kontaktieren.',
            'fr': f'Désolé, je n\'ai pas d\'informations vérifiées sur le logement à {university_name}. Je recommande de visiter le site officiel de l\'université ou de les contacter directement.',
            'es': f'Lo siento, no tengo información verificada sobre el alojamiento en {university_name}. Recomiendo visitar el sitio web oficial de la universidad o contactarlos directamente.',
            'it': f'Spiacente, non ho informazioni verificate sull\'alloggio presso {university_name}. Consiglio di visitare il sito ufficiale dell\'università o di contattarli direttamente.',
            'ru': f'Извините, у меня нет проверенной информации о жилье в {university_name}. Рекомендую посетить официальный сайт университета или связаться с ними напрямую.'
        }
        return texts.get(language, texts['en'])
    
    def _get_google_search_recommendation(self, language: str, university_name: str) -> str:
        """Recommendation to search via Google when AI doesn't know"""
        search_query = f"{university_name} student accommodation"
        google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        
        texts = {
            'sk': f'💡 Skúste vyhľadať "{university_name} študentské ubytovanie" cez Google: {google_url}',
            'cs': f'💡 Zkuste vyhledat "{university_name} studentské ubytování" přes Google: {google_url}',
            'en': f'💡 Try searching "{university_name} student accommodation" via Google: {google_url}',
            'uk': f'💡 Спробуйте пошукати "{university_name} студентське житло" через Google: {google_url}',
            'pl': f'💡 Spróbuj wyszukać "{university_name} zakwaterowanie studenckie" przez Google: {google_url}',
            'de': f'💡 Versuchen Sie "{university_name} Studentenunterkunft" über Google zu suchen: {google_url}',
            'fr': f'💡 Essayez de rechercher "{university_name} logement étudiant" via Google: {google_url}',
            'es': f'💡 Intenta buscar "{university_name} alojamiento estudiantil" a través de Google: {google_url}',
            'it': f'💡 Prova a cercare "{university_name} alloggio studenti" tramite Google: {google_url}',
            'ru': f'💡 Попробуйте поискать "{university_name} студенческое жилье" через Google: {google_url}'
        }
        return texts.get(language, texts['en'])

