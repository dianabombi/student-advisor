#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration: Reset and Add Dutch Job Agencies
Following the Czech pattern (add_czech_job_agencies.py)

Verified Dutch Job Portals:
- StudentJob.nl - Specialized for student jobs (https://www.studentjob.nl)
- Indeed.nl - Major job portal (https://www.indeed.nl)
- Randstad.nl - Leading recruitment agency (https://www.randstad.nl)  
- YoungCapital.nl - Students and young professionals (https://www.youngcapital.nl)

Cities with universities in Netherlands:
Amsterdam, Rotterdam, Utrecht, Leiden, Groningen, Delft, The Hague,
Eindhoven, Maastricht, Tilburg, Nijmegen, Wageningen, Enschede
"""

import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency

def reset_dutch_job_agencies():
    """Delete existing NL agencies and add new verified ones"""
    db = SessionLocal()
    
    try:
        # STEP 1: Delete all existing NL agencies
        deleted = db.query(JobAgency).filter(
            JobAgency.country_code == 'NL'
        ).delete()
        print(f"🗑️ Deleted {deleted} existing NL agencies")
        db.commit()
        
        # STEP 2: Define Dutch cities with universities
        cities = [
            'Amsterdam', 'Rotterdam', 'Utrecht', 'Leiden', 'Groningen',
            'Delft', 'The Hague', 'Eindhoven', 'Maastricht', 'Tilburg',
            'Nijmegen', 'Wageningen', 'Enschede'
        ]
        
        # STEP 3: Define verified agencies (same for all cities - main portal URLs)
        agencies_template = [
            {
                'name': 'StudentJob.nl',
                'website_url': 'https://www.studentjob.nl',
                'description': 'Bijbanen en vakantiewerk voor studenten',
                'specialization': 'student_jobs'
            },
            {
                'name': 'Indeed.nl',
                'website_url': 'https://www.indeed.nl',
                'description': 'Grote vacaturebank met studentenbanen',
                'specialization': 'student_jobs'
            },
            {
                'name': 'Randstad.nl',
                'website_url': 'https://www.randstad.nl',
                'description': 'Uitzendbureau met bijbanen voor studenten',
                'specialization': 'student_jobs'
            },
            {
                'name': 'YoungCapital.nl', 
                'website_url': 'https://www.youngcapital.nl',
                'description': 'Uitzendbureau voor studenten en starters',
                'specialization': 'student_jobs'
            }
        ]
        
        # STEP 4: Add agencies for each city
        count = 0
        for city in cities:
            for template in agencies_template:
                agency = JobAgency(
                    name=f"{template['name']} - {city}",
                    city=city,
                    country_code='NL',
                    website_url=template['website_url'],
                    description=template['description'],
                    specialization=template['specialization'],
                    is_active=True
                )
                db.add(agency)
                count += 1
                print(f"✅ Added: {template['name']} - {city}")
        
        db.commit()
        print(f"\n✅ Successfully added {count} Dutch job agencies!")
        print(f"Cities: {', '.join(cities)}")
        print(f"Portals: StudentJob.nl, Indeed.nl, Randstad.nl, YoungCapital.nl")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    reset_dutch_job_agencies()
