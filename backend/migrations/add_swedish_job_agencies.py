#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration: Add Swedish Job Agencies

Verified Swedish Job Portals:
- Arbetsförmedlingen.se - Official Swedish employment service (https://www.arbetsformedlingen.se)
- Manpower.se - Sweden's largest staffing company (https://www.manpower.se)
- Randstad.se - Recruitment agency (https://www.randstad.se)

Cities with universities in Sweden:
Stockholm, Gothenburg, Uppsala, Lund, Linköping
"""

import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency

def add_swedish_job_agencies():
    """Add verified Swedish job agencies"""
    db = SessionLocal()
    
    try:
        # Check if SE agencies already exist
        existing = db.query(JobAgency).filter(
            JobAgency.country_code == 'SE'
        ).count()
        
        if existing > 0:
            print(f"Found {existing} existing SE agencies. Deleting...")
            db.query(JobAgency).filter(JobAgency.country_code == 'SE').delete()
            db.commit()
        
        # Swedish cities with universities
        cities = ['Stockholm', 'Gothenburg', 'Uppsala', 'Lund', 'Linköping']
        
        # Verified agencies
        agencies_template = [
            {
                'name': 'Arbetsförmedlingen.se',
                'website_url': 'https://www.arbetsformedlingen.se',
                'description': 'Sveriges officiella arbetsförmedling',
                'specialization': 'student_jobs'
            },
            {
                'name': 'Manpower.se',
                'website_url': 'https://www.manpower.se',
                'description': 'Sveriges största bemanningsföretag',
                'specialization': 'student_jobs'
            },
            {
                'name': 'Randstad.se',
                'website_url': 'https://www.randstad.se',
                'description': 'Rekryteringsföretag med lediga jobb',
                'specialization': 'student_jobs'
            }
        ]
        
        # Add agencies for each city
        count = 0
        for city in cities:
            for template in agencies_template:
                agency = JobAgency(
                    name=f"{template['name']} - {city}",
                    city=city,
                    country_code='SE',
                    website_url=template['website_url'],
                    description=template['description'],
                    specialization=template['specialization'],
                    is_active=True
                )
                db.add(agency)
                count += 1
                print(f"Added: {template['name']} - {city}")
        
        db.commit()
        print(f"\nSuccessfully added {count} Swedish job agencies!")
        print(f"Cities: {', '.join(cities)}")
        print(f"Portals: Arbetsförmedlingen.se, Manpower.se, Randstad.se")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_swedish_job_agencies()
