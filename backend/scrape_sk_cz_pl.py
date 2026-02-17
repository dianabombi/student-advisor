#!/usr/bin/env python3
"""
Scrape universities for specific jurisdictions (SK, CZ, PL)
"""
import sys
sys.path.append('/app')

from main import SessionLocal, University
from tasks.university_scraping import scrape_university_task
from sqlalchemy import text

def scrape_jurisdictions(jurisdiction_codes):
    """Scrape all universities in specified jurisdictions"""
    db = SessionLocal()
    try:
        # Get universities for these jurisdictions
        query = text("""
            SELECT u.id, u.name, j.code as jurisdiction
            FROM universities u
            JOIN jurisdictions j ON u.jurisdiction_id = j.id
            WHERE j.code IN :codes
            AND u.website_url IS NOT NULL
            AND u.website_url != ''
            ORDER BY j.code, u.name
        """)
        
        result = db.execute(query, {"codes": tuple(jurisdiction_codes)})
        universities = result.fetchall()
        
        print(f"🎯 Found {len(universities)} universities in {', '.join(jurisdiction_codes)}")
        
        queued = 0
        for uni in universities:
            print(f"📋 Queuing: [{uni.jurisdiction}] {uni.name} (ID: {uni.id})")
            scrape_university_task.delay(uni.id)
            queued += 1
        
        print(f"\n✅ Queued {queued} universities for scraping!")
        return queued
        
    finally:
        db.close()

if __name__ == "__main__":
    jurisdictions = ['SK', 'CZ', 'PL']
    scrape_jurisdictions(jurisdictions)
