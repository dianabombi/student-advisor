#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Monaco job agencies - replace broken portals with working ones
"""

import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency

db = SessionLocal()

try:
    # Delete all Monaco agencies
    monaco_agencies = db.query(JobAgency).filter(
        JobAgency.country_code == 'MC'
    ).all()
    
    for agency in monaco_agencies:
        print(f"❌ Deleting: {agency.name} ({agency.website_url})")
        db.delete(agency)
    
    # Add working Monaco job portals
    new_agencies = [
        {
            'name': 'Emploi-Monaco.com - Monaco',
            'city': 'Monaco',
            'country_code': 'MC',
            'website_url': 'https://www.emploi-monaco.com',
            'description': 'Principal site d\'emploi de la Principauté de Monaco',
            'specialization': 'Emplois étudiants',
            'is_active': True
        },
        {
            'name': 'Monte-Carlo.mc - Monaco',
            'city': 'Monaco',
            'country_code': 'MC',
            'website_url': 'https://www.monte-carlo.mc',
            'description': 'Portail officiel de Monaco avec offres d\'emploi',
            'specialization': 'Emplois étudiants',
            'is_active': True
        },
        {
            'name': 'Indeed.fr - Monaco',
            'city': 'Monaco',
            'country_code': 'MC',
            'website_url': 'https://fr.indeed.com',
            'description': 'Portail international d\'emploi',
            'specialization': 'Emplois étudiants',
            'is_active': True
        }
    ]
    
    for data in new_agencies:
        agency = JobAgency(**data)
        db.add(agency)
        print(f"✅ Added: {data['name']}")
    
    db.commit()
    print(f"\n✅ Successfully updated Monaco job agencies")
    print(f"   Deleted: {len(monaco_agencies)} old portals")
    print(f"   Added: {len(new_agencies)} working portals")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
