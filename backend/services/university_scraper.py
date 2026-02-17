#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced University Scraper
Scrapes applicant-critical information in 11 languages
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from langdetect import detect, DetectorFactory
from urllib.parse import urljoin, urlparse
import re
import time
from sqlalchemy.orm import Session
from datetime import datetime

# Make language detection deterministic
DetectorFactory.seed = 0


class UniversityScraper:
    """Enhanced web scraper for university websites"""
    
    def __init__(self, db: Session):
        self.db = db
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.timeout = 10
        self.max_pages = 50  # Increased from 30 to get more coverage
        
        # URL patterns to EXCLUDE (news, events, blogs)
        self.exclude_patterns = [
            '/aktuality', '/news', '/zpravodaj', '/novinky',
            '/blog', '/article', '/event', '/udalost',
            '/press', '/media', '/tiskove', '/press-release'
        ]
        
        # Applicant-critical keywords in 11 languages
        self.keywords = {
            'tuition': {
                'en': ['tuition', 'fees', 'cost', 'price', 'payment'],
                'sk': ['školné', 'poplatky', 'cena', 'platba'],
                'cs': ['školné', 'poplatky', 'cena', 'platba'],
                'pl': ['czesne', 'opłaty', 'cena', 'płatność'],
                'de': ['studiengebühren', 'kosten', 'preis', 'zahlung'],
                'uk': ['плата', 'вартість', 'ціна', 'оплата'],
                'ru': ['плата', 'стоимость', 'цена', 'оплата'],
                'fr': ['frais', 'coût', 'prix', 'paiement'],
                'es': ['matrícula', 'tasas', 'costo', 'precio'],
                'it': ['tasse', 'costi', 'prezzo', 'pagamento'],
                'pt': ['propinas', 'taxas', 'custo', 'preço', 'pagamento']
            },
            'faculties': {
                'en': ['faculty', 'faculties', 'school', 'department'],
                'sk': ['fakulta', 'fakulty', 'škola', 'katedra'],
                'cs': ['fakulta', 'fakulty', 'škola', 'katedra'],
                'pl': ['wydział', 'wydziały', 'szkoła', 'katedra'],
                'de': ['fakultät', 'fakultäten', 'schule', 'abteilung'],
                'uk': ['факультет', 'факультети', 'школа', 'кафедра'],
                'ru': ['факультет', 'факультеты', 'школа', 'кафедра'],
                'fr': ['faculté', 'facultés', 'école', 'département'],
                'es': ['facultad', 'facultades', 'escuela', 'departamento'],
                'it': ['facoltà', 'scuola', 'dipartimento'],
                'pt': ['faculdade', 'faculdades', 'escola', 'departamento']
            },
            'programs': {
                'en': ['programs', 'programme', 'bachelor', 'master', 'phd', 'courses'],
                'sk': ['programy', 'bakalár', 'magister', 'doktorát', 'kurzy'],
                'cs': ['programy', 'bakalář', 'magistr', 'doktorát', 'kurzy'],
                'pl': ['programy', 'licencjat', 'magister', 'doktorat', 'kursy'],
                'de': ['programme', 'bachelor', 'master', 'doktorat', 'kurse'],
                'uk': ['програми', 'бакалавр', 'магістр', 'докторат', 'курси'],
                'ru': ['программы', 'бакалавр', 'магистр', 'докторат', 'курсы'],
                'fr': ['programmes', 'licence', 'master', 'doctorat', 'cours'],
                'es': ['programas', 'grado', 'máster', 'doctorado', 'cursos'],
                'it': ['programmi', 'laurea', 'magistrale', 'dottorato', 'corsi'],
                'pt': ['programas', 'licenciatura', 'mestrado', 'doutorado', 'cursos']
            },
            'admission': {
                'en': ['admission', 'application', 'apply', 'requirements', 'entrance'],
                'sk': ['prijímanie', 'prihláška', 'požiadavky', 'prijímačky'],
                'cs': ['přijímání', 'přihláška', 'požadavky', 'přijímačky'],
                'pl': ['rekrutacja', 'aplikacja', 'wymagania', 'egzamin'],
                'de': ['zulassung', 'bewerbung', 'anforderungen', 'prüfung'],
                'uk': ['вступ', 'заява', 'вимоги', 'іспит'],
                'ru': ['поступление', 'заявка', 'требования', 'экзамен'],
                'fr': ['admission', 'candidature', 'exigences', 'examen'],
                'es': ['admisión', 'solicitud', 'requisitos', 'examen'],
                'it': ['ammissione', 'domanda', 'requisiti', 'esame'],
                'pt': ['admissão', 'candidatura', 'requisitos', 'exame']
            },
            'dormitory': {
                'en': ['dormitory', 'housing', 'accommodation', 'residence'],
                'sk': ['internát', 'ubytovanie', 'kolej'],
                'cs': ['kolej', 'ubytování', 'internát'],
                'pl': ['akademik', 'zakwaterowanie', 'dom studencki'],
                'de': ['wohnheim', 'unterkunft', 'studentenwohnheim'],
                'uk': ['гуртожиток', 'житло', 'проживання'],
                'ru': ['общежитие', 'жилье', 'проживание'],
                'fr': ['résidence', 'logement', 'hébergement'],
                'es': ['residencia', 'alojamiento', 'vivienda'],
                'it': ['residenza', 'alloggio', 'abitazione'],
                'pt': ['residência', 'alojamento', 'habitação']
            },
            'scholarship': {
                'en': ['scholarship', 'financial aid', 'grant', 'funding'],
                'sk': ['štipendium', 'finančná pomoc', 'grant'],
                'cs': ['stipendium', 'finanční pomoc', 'grant'],
                'pl': ['stypendium', 'pomoc finansowa', 'grant'],
                'de': ['stipendium', 'finanzielle hilfe', 'förderung'],
                'uk': ['стипендія', 'фінансова допомога', 'грант'],
                'ru': ['стипендия', 'финансовая помощь', 'грант'],
                'fr': ['bourse', 'aide financière', 'subvention'],
                'es': ['beca', 'ayuda financiera', 'subvención'],
                'it': ['borsa di studio', 'aiuto finanziario', 'sovvenzione'],
                'pt': ['bolsa', 'ajuda financeira', 'subsídio']
            },
            'deadlines': {
                'en': ['deadline', 'dates', 'calendar', 'schedule'],
                'sk': ['termín', 'dátumy', 'kalendár', 'rozvrh'],
                'cs': ['termín', 'data', 'kalendář', 'rozvrh'],
                'pl': ['termin', 'daty', 'kalendarz', 'harmonogram'],
                'de': ['frist', 'termine', 'kalender', 'zeitplan'],
                'uk': ['термін', 'дати', 'календар', 'розклад'],
                'ru': ['срок', 'даты', 'календарь', 'расписание'],
                'fr': ['délai', 'dates', 'calendrier', 'horaire'],
                'es': ['plazo', 'fechas', 'calendario', 'horario'],
                'it': ['scadenza', 'date', 'calendario', 'orario'],
                'pt': ['prazo', 'datas', 'calendário', 'horário']
            }
        }
        
    async def scrape_university(self, university_id: int, website_url: str) -> Dict:
        """
        Scrape university website for applicant-critical information
        
        Args:
            university_id: University ID
            website_url: University website URL
            
        Returns:
            Dict with scraping results
        """
        from tasks.models import UniversityScrapingStatus, UniversityContent
        
        # Update status to in_progress
        status = self.db.query(UniversityScrapingStatus).filter_by(
            university_id=university_id
        ).first()
        
        if not status:
            status = UniversityScrapingStatus(
                university_id=university_id,
                scraping_status='in_progress'
            )
            self.db.add(status)
        else:
            status.scraping_status = 'in_progress'
        
        self.db.commit()
        
        try:
            pages_scraped = 0
            content_items = []
            
            # 1. Scrape homepage
            homepage_content = await self._scrape_page(website_url, 'general')
            if homepage_content:
                content_items.append({
                    'university_id': university_id,
                    'url': website_url,
                    'title': homepage_content['title'],
                    'content': homepage_content['content'],
                    'content_type': 'general',
                    'language': homepage_content['language']
                })
                pages_scraped += 1
            
            # 2. Find and scrape applicant-critical pages
            key_pages = await self._find_applicant_pages(website_url)
            
            # Scrape up to max_pages
            for page_url, page_type in key_pages[:self.max_pages]:
                page_content = await self._scrape_page(page_url, page_type)
                if page_content and len(page_content['content']) > 200:  # Skip short pages
                    content_items.append({
                        'university_id': university_id,
                        'url': page_url,
                        'title': page_content['title'],
                        'content': page_content['content'],
                        'content_type': page_type,
                        'language': page_content['language']
                    })
                    pages_scraped += 1
                    time.sleep(1)  # Be polite
            
            # Store content in database
            for item in content_items:
                existing = self.db.query(UniversityContent).filter_by(
                    university_id=item['university_id'],
                    url=item['url']
                ).first()
                
                if existing:
                    # Update existing
                    existing.content = item['content']
                    existing.title = item['title']
                    existing.content_type = item['content_type']
                    existing.language = item['language']
                    existing.updated_at = datetime.utcnow()
                else:
                    # Create new
                    content = UniversityContent(**item)
                    self.db.add(content)
            
            self.db.commit()
            
            # Update status to completed
            status.scraping_status = 'completed'
            status.pages_scraped = pages_scraped
            status.last_scraped_at = datetime.utcnow()
            self.db.commit()
            
            return {
                'success': True,
                'pages_scraped': pages_scraped,
                'content_items': len(content_items)
            }
            
        except Exception as e:
            # Rollback any pending transaction
            self.db.rollback()
            
            # Update status to failed
            status.scraping_status = 'failed'
            status.error_message = str(e)
            self.db.commit()
            
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _scrape_page(self, url: str, content_type: str) -> Optional[Dict]:
        """Scrape single page and extract content"""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ''
            
            # Remove script and style elements
            for script in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                script.decompose()
            
            # Extract text content
            text = soup.get_text()
            
            # Clean text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Limit content length to 10000 chars
            if len(text) > 10000:
                text = text[:10000]
            
            # Detect language
            language = self._detect_language(text)
            
            return {
                'title': title_text,
                'content': text,
                'language': language
            }
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    async def _find_applicant_pages(self, base_url: str) -> List[tuple]:
        """Find pages with applicant-critical information using smart URL matching"""
        key_pages = []
        
        # Priority URL patterns (based on 41 questions)
        priority_urls = {
            'tuition': ['/tuition', '/fees', '/costs', '/pricing', '/skolne', '/poplatky'],
            'admission': ['/admission', '/apply', '/application', '/prijimanie', '/prihlaska'],
            'scholarships': ['/scholarship', '/financial-aid', '/funding', '/stipendium'],
            'faculties': ['/faculties', '/schools', '/departments', '/fakulty', '/fakulta'],
            'programs': ['/programs', '/degrees', '/study', '/programy', '/bachelor', '/master'],
            'housing': ['/housing', '/accommodation', '/dormitory', '/kolej', '/internat', '/ubytovanie'],
            'international': ['/international', '/foreign-students', '/international-students'],
            'deadlines': ['/deadlines', '/important-dates', '/calendar', '/terminy'],
            'requirements': ['/requirements', '/documents', '/poziadavky'],
            'language': ['/english-programs', '/language', '/teaching-language']
        }
        
        try:
            response = requests.get(base_url, headers=self.headers, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Find all links
            all_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)
                link_text = link.get_text().lower()
                
                # Skip external links
                if urlparse(full_url).netloc != urlparse(base_url).netloc:
                    continue
                
                # EXCLUDE news/events URLs
                if any(pattern in full_url.lower() for pattern in self.exclude_patterns):
                    continue
                
                all_links.append((full_url, href.lower(), link_text))
            
            # Phase 1: Find HIGH PRIORITY URLs (exact matches)
            for category, url_patterns in priority_urls.items():
                for full_url, href, link_text in all_links:
                    # Check if URL contains priority pattern
                    if any(pattern in href for pattern in url_patterns):
                        if full_url not in [url for url, _ in key_pages]:
                            key_pages.append((full_url, category))
                            print(f"✅ Found {category}: {full_url}")
                            break
            
            # Phase 2: Keyword matching (if not enough pages)
            if len(key_pages) < 20:
                for full_url, href, link_text in all_links:
                    if full_url in [url for url, _ in key_pages]:
                        continue
                    
                    # Check keywords in link text and URL
                    for category, lang_keywords in self.keywords.items():
                        for lang, keywords in lang_keywords.items():
                            if any(keyword in href or keyword in link_text for keyword in keywords):
                                if full_url not in [url for url, _ in key_pages]:
                                    key_pages.append((full_url, category))
                                    break
                        if len(key_pages) >= self.max_pages:
                            break
                    
                    if len(key_pages) >= self.max_pages:
                        break
            
            print(f"📊 Total pages found: {len(key_pages)}")
            
        except Exception as e:
            print(f"Error finding key pages: {e}")
        
        return key_pages[:self.max_pages]
    
    
    def _detect_language(self, text: str) -> str:
        """Detect language of text"""
        try:
            lang = detect(text)
            # Map to supported languages (11 languages)
            lang_map = {
                'sk': 'sk',
                'cs': 'cs',
                'pl': 'pl',
                'en': 'en',
                'de': 'de',
                'fr': 'fr',
                'es': 'es',
                'it': 'it',
                'ru': 'ru',
                'uk': 'uk',
                'pt': 'pt'
            }
            return lang_map.get(lang, 'en')
        except:
            return 'en'
