#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add German job agencies (Zenjob, StepStone, Indeed)
"""

import sys
# Add the project root to the python path
sys.path.append('/app')

from main import SessionLocal, JobAgency, University

def normalize_german_city(city):
    """
    Normalize German city names for URLs.
    München -> muenchen
    Köln -> koeln
    Nürnberg -> nuernberg
    """
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue'
    }
    normalized = city
    for char, replacement in replacements.items():
        normalized = normalized.replace(char, replacement)
    
    return normalized.lower()

def add_german_job_agencies():
    """Add German agencies for all cities in DB"""
    db = SessionLocal()
    
    try:
        # Get cities dynamically
        cities = db.query(University.city).filter(University.country == 'DE').distinct().all()
        unique_cities = sorted(list(set([city[0] for city in cities if city[0]])))
        
        print(f"🔍 Found {len(unique_cities)} cities in Germany")
        
        for city in unique_cities:
            url_city = normalize_german_city(city)
            
            # 1. Zenjob (Very popular for students)
            # URL: https://www.zenjob.com/de/jobs/[city]/
            zenjob_url = f"https://www.zenjob.com/de/jobs/{url_city}/"
            
            # 2. StepStone
            # URL: https://www.stepstone.de/jobs/[city]?q=Werkstudent
            stepstone_url = f"https://www.stepstone.de/jobs/{city}?q=Werkstudent"
            
            # 3. Indeed
            # URL: https://de.indeed.com/Jobs?l=[city]&q=Student
            indeed_url = f"https://de.indeed.com/Jobs?l={city}&q=Student"
            
            agencies = [
                {
                    'name': f'Zenjob - {city}',
                    'city': city,
                    'country_code': 'DE',
                    'website_url': zenjob_url,
                    'description': f'Flexible student jobs in {city}',
                    'specialization': 'student_jobs',
                    'is_active': True
                },
                {
                    'name': f'StepStone - {city}',
                    'city': city,
                    'country_code': 'DE',
                    'website_url': stepstone_url,
                    'description': f'Werkstudent jobs in {city}',
                    'specialization': 'student_jobs',
                    'is_active': True
                },
                {
                    'name': f'Indeed.de - {city}',
                    'city': city,
                    'country_code': 'DE',
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
        print("\n✅ Successfully updated German job agencies!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_german_job_agencies()
