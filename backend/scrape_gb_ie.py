#!/usr/bin/env python3
"""
Scrape universities from English-speaking countries: GB, IE
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from celery_app import celery_app
from tasks.university_scraping import scrape_university_task

# Database setup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/codex_db')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def main():
    db = SessionLocal()
    try:
        from tasks.models import University
        from main import Jurisdiction
        
        # Get English-speaking jurisdictions
        jurisdictions = db.query(Jurisdiction).filter(
            Jurisdiction.code.in_(['GB', 'IE'])
        ).all()
        
        jurisdiction_ids = [j.id for j in jurisdictions]
        
        # Get universities
        universities = db.query(University).filter(
            University.jurisdiction_id.in_(jurisdiction_ids),
            University.is_active == True
        ).all()
        
        print(f"🇬🇧🇮🇪 Found {len(universities)} universities in GB, IE")
        
        # Queue scraping tasks
        for uni in universities:
            jurisdiction_code = next(j.code for j in jurisdictions if j.id == uni.jurisdiction_id)
            print(f"📋 Queuing: [{jurisdiction_code}] {uni.name} (ID: {uni.id})")
            scrape_university_task.delay(uni.id)
        
        print(f"\n✅ Queued {len(universities)} English-speaking universities!")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
