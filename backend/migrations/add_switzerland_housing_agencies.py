#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Swiss real estate agencies and university accommodation
"""

import sys
sys.path.append('/app')

from main import SessionLocal, RealEstateAgency

db = SessionLocal()

try:
    cities = ['Zurich', 'Geneva', 'Basel', 'Lausanne', 'Bern', 'St. Gallen']
    
    portals = [
        {'name_template': 'Homegate - {}', 'url': 'https://www.homegate.ch',
         'description': 'Le plus grand portail immobilier suisse', 'specialization': 'Location et vente'},
        {'name_template': 'ImmoScout24 - {}', 'url': 'https://www.immoscout24.ch',
         'description': 'Portail immobilier leader en Suisse', 'specialization': 'Location'},
        {'name_template': 'Comparis - {}', 'url': 'https://www.comparis.ch',
         'description': 'Comparateur immobilier suisse', 'specialization': 'Location et vente'}
    ]
    
    student_accommodation = {
        'Zurich': [{'name': 'WOKO Zürich', 'url': 'https://www.woko.ch',
                   'description': 'Student housing cooperative Zurich', 'specialization': 'Student housing'}],
        'Geneva': [{'name': 'FMEL Geneva', 'url': 'https://www.fmel.ch',
                   'description': 'Student housing foundation Geneva', 'specialization': 'Student housing'}]
    }
    
    added_count = 0
    for city in cities:
        for portal in portals:
            db.add(RealEstateAgency(name=portal['name_template'].format(city), city=city, country_code='CH',
                                   website_url=portal['url'], description=portal['description'],
                                   specialization=portal['specialization'], is_verified=True, is_active=True))
            added_count += 1
            print(f"✅ Added: {portal['name_template'].format(city)}")
    
    for city, accommodations in student_accommodation.items():
        for acc in accommodations:
            db.add(RealEstateAgency(name=acc['name'], city=city, country_code='CH',
                                   website_url=acc['url'], description=acc['description'],
                                   specialization=acc['specialization'], is_verified=True, is_active=True))
            added_count += 1
            print(f"✅ Added: {acc['name']}")
    
    db.commit()
    print(f"\n✅ Successfully added {added_count} housing agencies for Switzerland")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
