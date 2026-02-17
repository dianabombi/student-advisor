#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add French job agencies (Welcome to the Jungle, Indeed.fr, StudentJob.fr)
"""

import sys
import unicodedata

# Add the project root to the python path
sys.path.append('/app')

from main import SessionLocal, JobAgency, University

def normalize_city_for_url(city):
    """Normalize city name for URLs"""
    normalized = city.lower().replace(' ', '-')
    normalized = unicodedata.normalize('NFKD', normalized).encode('ASCII', 'ignore').decode('utf-8')
    return normalized

def add_french_job_agencies():
    """Add French agencies for all cities in DB"""
    db = SessionLocal()
    
    try:
        # Get cities dynamically for FR
        cities = db.query(University.city).filter(University.country == 'FR').distinct().all()
        unique_cities = sorted(list(set([city[0] for city in cities if city[0]])))
        
        print(f"🔍 Found {len(unique_cities)} cities in France")
        
        for city in unique_cities:
            url_city = normalize_city_for_url(city)
            
            # 1. Welcome to the Jungle
            # URL: https://www.welcometothejungle.com/fr/jobs?query=student&aroundQuery=[city]
            wtj_url = f"https://www.welcometothejungle.com/fr/jobs?query=student&aroundQuery={city}"
            
            # 2. StudentJob.fr
            # URL: https://www.studentjob.fr/boulots-etudiants/[city]
            # e.g. boulots-etudiants/paris
            studentjob_url = f"https://www.studentjob.fr/boulots-etudiants/{url_city}"
            
            # 3. Indeed.fr
            # URL: https://fr.indeed.com/emplois?q=Etudiant&l=[City]
            indeed_url = f"https://fr.indeed.com/emplois?q=Etudiant&l={city}"
            
            agencies = [
                {
                    'name': f'Welcome to the Jungle - {city}',
                    'city': city,
                    'country_code': 'FR',
                    'website_url': wtj_url,
                    'description': f'Jobs in {city}',
                    'specialization': 'startups_student_jobs',
                },
                {
                    'name': f'StudentJob.fr - {city}',
                    'city': city,
                    'country_code': 'FR',
                    'website_url': studentjob_url,
                    'description': f'Part-time jobs in {city}',
                    'specialization': 'student_jobs',
                },
                {
                    'name': f'Indeed France - {city}',
                    'city': city,
                    'country_code': 'FR',
                    'website_url': indeed_url,
                    'description': f'Student jobs in {city}',
                    'specialization': 'student_jobs',
                }
            ]
            
            for data in agencies:
                existing = db.query(JobAgency).filter(
                    JobAgency.name == data['name'],
                    JobAgency.city == data['city']
                ).first()
                
                if existing:
                    print(f"🔄 Updating: {data['name']}")
                    existing.website_url = data['website_url']
                    existing.is_active = True
                else:
                    agency = JobAgency(**data)
                    agency.is_active = True
                    db.add(agency)
                    print(f"✅ Added: {data['name']}")
        
        db.commit()
        print("\n✅ Successfully updated French job agencies!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_french_job_agencies()
