#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Dutch real estate agencies and university accommodation
"""

import sys
sys.path.append('/app')

from main import SessionLocal, RealEstateAgency

db = SessionLocal()

try:
    cities = ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Leiden', 'Delft', 'Groningen', 'Maastricht']
    
    portals = [
        {'name_template': 'Funda - {}', 'url': 'https://www.funda.nl',
         'description': 'Grootste woningsite van Nederland', 'specialization': 'Huur en koop'},
        {'name_template': 'Pararius - {}', 'url': 'https://www.pararius.nl',
         'description': 'Huurwoningen in Nederland', 'specialization': 'Huur'},
        {'name_template': 'Kamernet - {}', 'url': 'https://www.kamernet.nl',
         'description': 'Kamers en studio\'s voor studenten', 'specialization': 'Studentenkamers'}
    ]
    
    student_accommodation = {
        'Amsterdam': [{'name': 'DUWO Amsterdam', 'url': 'https://www.duwo.nl',
                      'description': 'Student housing Amsterdam', 'specialization': 'Student housing'}],
        'Rotterdam': [{'name': 'SSH Rotterdam', 'url': 'https://www.sshxl.nl',
                      'description': 'Student housing Rotterdam', 'specialization': 'Student housing'}]
    }
    
    added_count = 0
    for city in cities:
        for portal in portals:
            db.add(RealEstateAgency(name=portal['name_template'].format(city), city=city, country_code='NL',
                                   website_url=portal['url'], description=portal['description'],
                                   specialization=portal['specialization'], is_verified=True, is_active=True))
            added_count += 1
            print(f"✅ Added: {portal['name_template'].format(city)}")
    
    for city, accommodations in student_accommodation.items():
        for acc in accommodations:
            db.add(RealEstateAgency(name=acc['name'], city=city, country_code='NL',
                                   website_url=acc['url'], description=acc['description'],
                                   specialization=acc['specialization'], is_verified=True, is_active=True))
            added_count += 1
            print(f"✅ Added: {acc['name']}")
    
    db.commit()
    print(f"\n✅ Successfully added {added_count} housing agencies for Netherlands")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
