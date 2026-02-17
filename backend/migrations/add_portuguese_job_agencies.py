#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration: Add Portuguese Job Agencies

Verified Portuguese Job Portals:
- Indeed.pt - Major job portal (https://www.indeed.pt)
- Randstad.pt - Leading recruitment agency (https://www.randstad.pt)
- Adecco.pt - Global recruitment agency (https://www.adecco.pt)
- Net-Empregos.com - Portuguese job portal (https://www.net-empregos.com)

Cities with universities in Portugal:
Aveiro, Braga, Coimbra, Lisbon, Porto
"""

import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency

def add_portuguese_job_agencies():
    """Add verified Portuguese job agencies"""
    db = SessionLocal()
    
    try:
        # Check if PT agencies already exist
        existing = db.query(JobAgency).filter(
            JobAgency.country_code == 'PT'
        ).count()
        
        if existing > 0:
            print(f"Found {existing} existing PT agencies. Deleting...")
            db.query(JobAgency).filter(JobAgency.country_code == 'PT').delete()
            db.commit()
        
        # Portuguese cities with universities
        cities = ['Aveiro', 'Braga', 'Coimbra', 'Lisbon', 'Porto']
        
        # Verified agencies
        agencies_template = [
            {
                'name': 'Indeed.pt',
                'website_url': 'https://www.indeed.pt',
                'description': 'Portal de emprego com milhares de ofertas para estudantes',
                'specialization': 'student_jobs'
            },
            {
                'name': 'Randstad.pt',
                'website_url': 'https://www.randstad.pt',
                'description': 'Agência de emprego com trabalho temporário e part-time',
                'specialization': 'student_jobs'
            },
            {
                'name': 'Adecco.pt',
                'website_url': 'https://www.adecco.pt',
                'description': 'Recrutamento e trabalho temporário',
                'specialization': 'student_jobs'
            },
            {
                'name': 'Net-Empregos.com',
                'website_url': 'https://www.net-empregos.com',
                'description': 'Portal de emprego português',
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
                    country_code='PT',
                    website_url=template['website_url'],
                    description=template['description'],
                    specialization=template['specialization'],
                    is_active=True
                )
                db.add(agency)
                count += 1
                print(f"Added: {template['name']} - {city}")
        
        db.commit()
        print(f"\nSuccessfully added {count} Portuguese job agencies!")
        print(f"Cities: {', '.join(cities)}")
        print(f"Portals: Indeed.pt, Randstad.pt, Adecco.pt, Net-Empregos.com")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    add_portuguese_job_agencies()
