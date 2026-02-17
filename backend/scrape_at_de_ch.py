#!/usr/bin/env python3
"""
Scrape universities for German-speaking jurisdictions (AT, DE, CH)
"""
import sys
sys.path.append('/app')

from main import SessionLocal
from tasks.university_scraping import scrape_university_task
from sqlalchemy import text

def scrape_german_speaking():
    """Scrape all universities in AT, DE, CH"""
    db = SessionLocal()
    try:
        query = text("""
            SELECT u.id, u.name, j.code as jurisdiction
            FROM universities u
            JOIN jurisdictions j ON u.jurisdiction_id = j.id
            WHERE j.code IN ('AT', 'DE', 'CH')
            AND u.website_url IS NOT NULL
            AND u.website_url != ''
            ORDER BY j.code, u.name
        """)
        
        result = db.execute(query)
        universities = result.fetchall()
        
        print(f"🇦🇹🇩🇪🇨🇭 Found {len(universities)} universities in AT, DE, CH")
        
        queued = 0
        for uni in universities:
            print(f"📋 Queuing: [{uni.jurisdiction}] {uni.name} (ID: {uni.id})")
            scrape_university_task.delay(uni.id)
            queued += 1
        
        print(f"\n✅ Queued {queued} German-speaking universities!")
        return queued
        
    finally:
        db.close()

if __name__ == "__main__":
    scrape_german_speaking()
