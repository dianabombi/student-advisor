#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add UK job agencies (Reed, Indeed, Totaljobs)
"""

import sys
import unicodedata

# Add the project root to the python path
sys.path.append('/app')

from main import SessionLocal, JobAgency, University

def normalize_city_for_url(city):
    """Normalize city name for URLs"""
    # Simple normalization
    normalized = city.lower().replace(' ', '-')
    return normalized

def add_uk_job_agencies():
    """Add UK agencies for all cities in DB"""
    db = SessionLocal()
    
    try:
        # Get cities dynamically (GB or UK)
        cities = db.query(University.city).filter(University.country.in_(['GB', 'UK'])).distinct().all()
        unique_cities = sorted(list(set([city[0] for city in cities if city[0]])))
        
        print(f"🔍 Found {len(unique_cities)} cities in UK")
        
        for city in unique_cities:
            url_city = normalize_city_for_url(city)
            
            # 1. Reed.co.uk (Major portal)
            # URL: https://www.reed.co.uk/jobs/[city]?keywords=student
            reed_url = f"https://www.reed.co.uk/jobs/{url_city}?keywords=student"
            
            # 2. Totaljobs
            # URL: https://www.totaljobs.com/jobs/student/in-[city]
            # e.g. in-london
            totaljobs_url = f"https://www.totaljobs.com/jobs/student/in-{url_city}"
            
            # 3. Indeed.co.uk
            # URL: https://uk.indeed.com/jobs?q=Student&l=[City]
            indeed_url = f"https://uk.indeed.com/jobs?q=Student&l={city}"
            
            agencies = [
                {
                    'name': f'Reed.co.uk - {city}',
                    'city': city,
                    'country_code': 'GB', # Usually GB in DB, but let's stick to what DB uses. I'll use GB as standard ISO.
                    'website_url': reed_url,
                    'description': f'Jobs in {city}',
                    'specialization': 'student_jobs',
                    'is_active': True
                },
                {
                    'name': f'Totaljobs - {city}',
                    'city': city,
                    'country_code': 'GB',
                    'website_url': totaljobs_url,
                    'description': f'Student jobs in {city}',
                    'specialization': 'student_jobs',
                    'is_active': True
                },
                {
                    'name': f'Indeed UK - {city}',
                    'city': city,
                    'country_code': 'GB',
                    'website_url': indeed_url,
                    'description': f'Student jobs in {city}',
                    'specialization': 'student_jobs',
                    'is_active': True
                }
            ]
            
            for data in agencies:
                # Check existance by name AND city
                existing = db.query(JobAgency).filter(
                    JobAgency.name == data['name'],
                    JobAgency.city == data['city']
                ).first()
                
                if existing:
                    print(f"⚠️ Exists: {data['name']}")
                else:
                    agency = JobAgency(**data)
                    db.add(agency)
                    print(f"✅ Added: {data['name']}")
        
        db.commit()
        print("\n✅ Successfully updated UK job agencies!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_uk_job_agencies()
