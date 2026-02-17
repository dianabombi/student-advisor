#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Irish job agencies (Jobs.ie, IrishJobs.ie, Indeed.ie)
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

def add_irish_job_agencies():
    """Add Irish agencies for all cities in DB"""
    db = SessionLocal()
    
    try:
        # Get cities dynamically
        cities = db.query(University.city).filter(University.country == 'IE').distinct().all()
        unique_cities = sorted(list(set([city[0] for city in cities if city[0]])))
        
        print(f"🔍 Found {len(unique_cities)} cities in Ireland")
        
        for city in unique_cities:
            url_city = normalize_city_for_url(city)
            
            # 1. Jobs.ie
            # URL: https://www.jobs.ie/jobs/[city]?keyword=student
            jobs_ie_url = f"https://www.jobs.ie/jobs/{url_city}?keyword=student"
            
            # 2. IrishJobs.ie
            # URL: https://www.irishjobs.ie/jobs/student/in-[city]
            # e.g. in-dublin
            irishjobs_url = f"https://www.irishjobs.ie/jobs/student/in-{url_city}"
            
            # 3. Indeed.ie
            # URL: https://ie.indeed.com/jobs?q=Student&l=[City]
            indeed_url = f"https://ie.indeed.com/jobs?q=Student&l={city}"
            
            agencies = [
                {
                    'name': f'Jobs.ie - {city}',
                    'city': city,
                    'country_code': 'IE',
                    'website_url': jobs_ie_url,
                    'description': f'Jobs in {city}',
                    'specialization': 'student_jobs',
                },
                {
                    'name': f'IrishJobs.ie - {city}',
                    'city': city,
                    'country_code': 'IE',
                    'website_url': irishjobs_url,
                    'description': f'Student jobs in {city}',
                    'specialization': 'student_jobs',
                },
                {
                    'name': f'Indeed Ireland - {city}',
                    'city': city,
                    'country_code': 'IE',
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
        print("\n✅ Successfully updated Irish job agencies!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_irish_job_agencies()
