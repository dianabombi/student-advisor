#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add job agencies for Andorra la Vella (capital city)
Currently only Sant Julià de Lòria has agencies
"""

import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency

db = SessionLocal()

try:
    # Add agencies for Andorra la Vella
    new_agencies = [
        {
            'name': 'Govern.ad - Andorra la Vella',
            'city': 'Andorra la Vella',
            'country_code': 'AD',
            'website_url': 'https://www.govern.ad/treball',
            'description': 'Portal oficial d\'ocupació del Govern d\'Andorra',
            'specialization': 'Treballs per a estudiants',
            'is_active': True
        },
        {
            'name': 'InfoJobs.net - Andorra la Vella',
            'city': 'Andorra la Vella',
            'country_code': 'AD',
            'website_url': 'https://www.infojobs.net',
            'description': 'Portal de treball espanyol (utilitzat a Andorra)',
            'specialization': 'Treballs per a estudiants',
            'is_active': True
        },
        {
            'name': 'Buscofeina.ad - Andorra la Vella',
            'city': 'Andorra la Vella',
            'country_code': 'AD',
            'website_url': 'https://www.buscofeina.ad',
            'description': 'Portal de treball andorrà',
            'specialization': 'Treballs per a estudiants',
            'is_active': True
        }
    ]
    
    for data in new_agencies:
        agency = JobAgency(**data)
        db.add(agency)
        print(f"✅ Added: {data['name']}")
    
    db.commit()
    print(f"\n✅ Successfully added {len(new_agencies)} agencies for Andorra la Vella")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
