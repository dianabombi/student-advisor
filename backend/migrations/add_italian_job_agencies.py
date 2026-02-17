#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration: Add Italian Job Agencies
Following the established pattern for Jobs AI

Verified Italian Job Portals:
- Indeed.it - Major job portal (https://it.indeed.com)
- Randstad.it - Leading recruitment agency (https://www.randstad.it)
- Adecco.it - Global recruitment agency (https://www.adecco.it)
- Manpower.it - Major employment agency (https://www.manpower.it)

Cities with universities in Italy:
Bologna, Florence, Milan, Padua, Pisa, Rome, Venice
"""

import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency

def add_italian_job_agencies():
    """Add verified Italian job agencies"""
    db = SessionLocal()
    
    try:
        # Check if IT agencies already exist
        existing = db.query(JobAgency).filter(
            JobAgency.country_code == 'IT'
        ).count()
        
        if existing > 0:
            print(f"Found {existing} existing IT agencies. Deleting...")
            db.query(JobAgency).filter(JobAgency.country_code == 'IT').delete()
            db.commit()
        
        # Italian cities with universities
        cities = [
            'Bologna', 'Florence', 'Milan', 'Padua', 'Pisa', 'Rome', 'Venice'
        ]
        
        # Verified agencies (main portal URLs only)
        agencies_template = [
            {
                'name': 'Indeed.it',
                'website_url': 'https://it.indeed.com',
                'description': 'Portale di lavoro con migliaia di offerte per studenti',
                'specialization': 'student_jobs'
            },
            {
                'name': 'Randstad.it',
                'website_url': 'https://www.randstad.it',
                'description': 'Agenzia per il lavoro con opportunità part-time',
                'specialization': 'student_jobs'
            },
            {
                'name': 'Adecco.it',
                'website_url': 'https://www.adecco.it',
                'description': 'Agenzia del lavoro per privati e studenti',
                'specialization': 'student_jobs'
            },
            {
                'name': 'Manpower.it',
                'website_url': 'https://www.manpower.it',
                'description': 'Agenzia per il lavoro con offerte part-time',
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
                    country_code='IT',
                    website_url=template['website_url'],
                    description=template['description'],
                    specialization=template['specialization'],
                    is_active=True
                )
                db.add(agency)
                count += 1
                print(f"Added: {template['name']} - {city}")
        
        db.commit()
        print(f"\nSuccessfully added {count} Italian job agencies!")
        print(f"Cities: {', '.join(cities)}")
        print(f"Portals: Indeed.it, Randstad.it, Adecco.it, Manpower.it")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_italian_job_agencies()
