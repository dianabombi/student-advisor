#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration: Add Spanish Job Agencies

Verified Spanish Job Portals:
- Indeed.es - Major job portal (https://www.indeed.es)
- Randstad.es - Leading recruitment agency (https://www.randstad.es)
- Adecco.es - Global recruitment agency (https://www.adecco.es)
- StudentJob.es - Student-focused portal (https://www.studentjob.es)

Cities with universities in Spain:
Barcelona, Madrid, Salamanca, Valencia
"""

import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency

def add_spanish_job_agencies():
    """Add verified Spanish job agencies"""
    db = SessionLocal()
    
    try:
        # Check if ES agencies already exist
        existing = db.query(JobAgency).filter(
            JobAgency.country_code == 'ES'
        ).count()
        
        if existing > 0:
            print(f"Found {existing} existing ES agencies. Deleting...")
            db.query(JobAgency).filter(JobAgency.country_code == 'ES').delete()
            db.commit()
        
        # Spanish cities with universities
        cities = ['Barcelona', 'Madrid', 'Salamanca', 'Valencia']
        
        # Verified agencies
        agencies_template = [
            {
                'name': 'Indeed.es',
                'website_url': 'https://www.indeed.es',
                'description': 'Portal de empleo con miles de ofertas para estudiantes',
                'specialization': 'student_jobs'
            },
            {
                'name': 'Randstad.es',
                'website_url': 'https://www.randstad.es',
                'description': 'Agencia de empleo con trabajos a tiempo parcial',
                'specialization': 'student_jobs'
            },
            {
                'name': 'Adecco.es',
                'website_url': 'https://www.adecco.es',
                'description': 'Agencia de trabajo temporal y empleo',
                'specialization': 'student_jobs'
            },
            {
                'name': 'StudentJob.es',
                'website_url': 'https://www.studentjob.es',
                'description': 'Portal de empleo para estudiantes y jovenes',
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
                    country_code='ES',
                    website_url=template['website_url'],
                    description=template['description'],
                    specialization=template['specialization'],
                    is_active=True
                )
                db.add(agency)
                count += 1
                print(f"Added: {template['name']} - {city}")
        
        db.commit()
        print(f"\nSuccessfully added {count} Spanish job agencies!")
        print(f"Cities: {', '.join(cities)}")
        print(f"Portals: Indeed.es, Randstad.es, Adecco.es, StudentJob.es")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_spanish_job_agencies()
