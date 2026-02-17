#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
University Website Scraper
Scrapes official university websites to collect admission, program, and contact information
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import argparse
import logging
from typing import Dict, List, Optional
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class UniversityScraper:
    """Scrape university websites for key information"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_university(self, url: str, university_name: str) -> Dict:
        """
        Scrape a university website for key information
        
        Returns dict with:
        - programs: List of programs found
        - contact_info: Contact details
        - admission_info: Admission requirements
        - general_info: General description
        """
        logger.info(f"Scraping {university_name} at {url}")
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract data
            data = {
                'url': url,
                'university_name': university_name,
                'scraped_at': datetime.utcnow().isoformat(),
                'programs': self._extract_programs(soup, url),
                'contact_info': self._extract_contact(soup),
                'admission_info': self._extract_admission(soup),
                'general_info': self._extract_general_info(soup),
                'language_info': self._extract_language_info(soup),
            }
            
            logger.info(f"Successfully scraped {university_name}")
            return data
            
        except requests.RequestException as e:
            logger.error(f"Failed to scrape {university_name}: {e}")
            return {
                'url': url,
                'university_name': university_name,
                'error': str(e),
                'scraped_at': datetime.utcnow().isoformat()
            }
    
    def _extract_programs(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract program names from the page"""
        programs = []
        
        # Look for common program indicators
        keywords = ['program', 'študijný', 'bakalár', 'magister', 'faculty', 'fakulta']
        
        # Find links and headings that might be programs
        for element in soup.find_all(['a', 'h2', 'h3', 'h4']):
            text = element.get_text(strip=True)
            if any(keyword in text.lower() for keyword in keywords):
                if len(text) > 10 and len(text) < 200:  # Reasonable length
                    programs.append(text)
        
        # Remove duplicates and limit
        programs = list(dict.fromkeys(programs))[:20]
        return programs
    
    def _extract_contact(self, soup: BeautifulSoup) -> Dict:
        """Extract contact information"""
        contact = {}
        
        # Look for email
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        import re
        emails = re.findall(email_pattern, soup.get_text())
        if emails:
            contact['email'] = emails[0]
        
        # Look for phone
        phone_pattern = r'\+?\d{1,4}[\s-]?\(?\d{1,4}\)?[\s-]?\d{1,4}[\s-]?\d{1,4}'
        phones = re.findall(phone_pattern, soup.get_text())
        if phones:
            contact['phone'] = phones[0]
        
        return contact
    
    def _extract_admission(self, soup: BeautifulSoup) -> str:
        """Extract admission information"""
        keywords = ['prijímanie', 'admission', 'prihlás', 'apply', 'vstup']
        
        for element in soup.find_all(['p', 'div', 'section']):
            text = element.get_text(strip=True)
            if any(keyword in text.lower() for keyword in keywords):
                if len(text) > 50 and len(text) < 500:
                    return text[:500]  # Limit length
        
        return "Visit official website for admission information"
    
    def _extract_general_info(self, soup: BeautifulSoup) -> str:
        """Extract general description"""
        # Try meta description first
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content']
        
        # Try first paragraph
        first_p = soup.find('p')
        if first_p:
            text = first_p.get_text(strip=True)
            if len(text) > 50:
                return text[:500]
        
        return "University information"
    
    def _extract_language_info(self, soup: BeautifulSoup) -> str:
        """Extract language of instruction info"""
        keywords = ['jazyk', 'language', 'english', 'slovenčina', 'slovak']
        
        for element in soup.find_all(['p', 'li', 'span']):
            text = element.get_text(strip=True)
            if any(keyword in text.lower() for keyword in keywords):
                if 'english' in text.lower() or 'anglick' in text.lower():
                    return "Slovak and English"
        
        return "Slovak"


def scrape_all_universities(db_connection_string: str):
    """Scrape all universities from database"""
    from main import University, Base
    
    engine = create_engine(db_connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Get all active universities
        universities = session.query(University).filter_by(is_active=True).all()
        
        scraper = UniversityScraper()
        results = []
        
        for university in universities:
            if not university.website_url:
                logger.warning(f"No website URL for {university.name}")
                continue
            
            # Scrape the university
            data = scraper.scrape_university(
                university.website_url,
                university.name
            )
            results.append(data)
            
            # Update university with scraped data
            if 'error' not in data:
                if data.get('contact_info', {}).get('email'):
                    university.contact_email = data['contact_info']['email']
                if data.get('contact_info', {}).get('phone'):
                    university.contact_phone = data['contact_info']['phone']
                
                university.last_updated = datetime.utcnow()
            
            # Be polite - wait between requests
            time.sleep(2)
        
        session.commit()
        logger.info(f"Scraped {len(results)} universities")
        
        return results
        
    except Exception as e:
        logger.error(f"Error scraping universities: {e}")
        session.rollback()
        raise
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(description='Scrape university websites')
    parser.add_argument('--all', action='store_true', help='Scrape all universities')
    parser.add_argument('--university-id', type=int, help='Scrape specific university by ID')
    parser.add_argument('--db-url', type=str, 
                       default=os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/codex_db'),
                       help='Database connection string')
    
    args = parser.parse_args()
    
    if args.all:
        logger.info("Scraping all universities...")
        results = scrape_all_universities(args.db_url)
        logger.info(f"Completed scraping {len(results)} universities")
        
        # Print summary
        for result in results:
            if 'error' in result:
                print(f"❌ {result['university_name']}: {result['error']}")
            else:
                print(f"✅ {result['university_name']}: {len(result.get('programs', []))} programs found")
    
    elif args.university_id:
        logger.info(f"Scraping university ID {args.university_id}...")
        # TODO: Implement single university scraping
        logger.error("Single university scraping not yet implemented")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
