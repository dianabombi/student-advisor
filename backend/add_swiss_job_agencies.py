#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Swiss job agencies (Jobs.ch, Students.ch)
"""

import sys
import unicodedata

# Add the project root to the python path
sys.path.append('/app')

from main import SessionLocal, JobAgency, University

def normalize_city_for_url(city):
    """Normalize city name for URLs"""
    # Handle St. Gallen -> st-gallen
    normalized = city.lower().replace('.', '').replace(' ', '-')
    # Remove accents
    normalized = unicodedata.normalize('NFKD', normalized).encode('ASCII', 'ignore').decode('utf-8')
    return normalized

def add_swiss_job_agencies():
    """Add Swiss agencies for all cities in DB"""
    db = SessionLocal()
    
    try:
        # Get cities dynamically
        cities = db.query(University.city).filter(University.country == 'CH').distinct().all()
        unique_cities = sorted(list(set([city[0] for city in cities if city[0]])))
        
        print(f"🔍 Found {len(unique_cities)} cities in Switzerland")
        
        for city in unique_cities:
            url_city = normalize_city_for_url(city)
            
            # 1. Jobs.ch (Biggest portal)
            # URL: https://www.jobs.ch/en/vacancies/?location=[City]
            jobs_ch_url = f"https://www.jobs.ch/en/vacancies/?location={city}"
            
            # 2. Students.ch (Student focus)
            # URL: https://www.students.ch/jobs/search?q=&l=[City]
            students_ch_url = f"https://www.students.ch/jobs/search?q=&l={city}"
            
            # 3. Indeed.ch
            # URL: https://ch.indeed.com/jobs?q=Student&l=[City]
            indeed_url = f"https://ch.indeed.com/jobs?q=Student&l={city}"
            
            agencies = [
                {
                    'name': f'Jobs.ch - {city}',
                    'city': city,
                    'country_code': 'CH',
                    'website_url': jobs_ch_url,
                    'description': f'Leading job portal in {city}',
                    'specialization': 'student_jobs',
                    'is_active': True
                },
                {
                    'name': f'Students.ch - {city}',
                    'city': city,
                    'country_code': 'CH',
                    'website_url': students_ch_url,
                    'description': f'Student jobs in {city}',
                    'specialization': 'student_jobs',
                    'is_active': True
                },
                {
                    'name': f'Indeed.ch - {city}',
                    'city': city,
                    'country_code': 'CH',
                    'website_url': indeed_url,
                    'description': f'Student jobs in {city}',
                    'specialization': 'student_jobs',
                    'is_active': True
                }
            ]
            
            for data in agencies:
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
        print("\n✅ Successfully updated Swiss job agencies!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_swiss_job_agencies()
