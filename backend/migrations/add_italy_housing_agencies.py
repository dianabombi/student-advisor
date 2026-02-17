#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Italian real estate agencies and university accommodation
Based on successful UK/France/Spain implementation
"""

import sys
sys.path.append('/app')

from main import SessionLocal, RealEstateAgency

db = SessionLocal()

try:
    # Italian cities (major university cities)
    cities = [
        'Rome',
        'Milan',
        'Naples',
        'Turin',
        'Florence',
        'Bologna',
        'Padua',
        'Pisa',
        'Venice',
        'Verona',
        'Genoa',
        'Palermo',
        'Bari',
        'Catania',
        'Perugia',
        'Siena'
    ]
    
    # Top Italian real estate portals (for all cities)
    portals = [
        {
            'name_template': 'Immobiliare.it - {}',
            'url': 'https://www.immobiliare.it',
            'description': 'Il portale immobiliare leader in Italia',
            'specialization': 'Affitto e vendita'
        },
        {
            'name_template': 'Casa.it - {}',
            'url': 'https://www.casa.it',
            'description': 'Portale per affitto e vendita immobili',
            'specialization': 'Affitto case'
        },
        {
            'name_template': 'Idealista Italia - {}',
            'url': 'https://www.idealista.it',
            'description': 'Annunci immobiliari per affitto e vendita',
            'specialization': 'Affitto e vendita'
        }
    ]
    
    # Student-specific accommodation
    student_accommodation = {
        'Rome': [
            {
                'name': 'Uniplaces - Roma',
                'url': 'https://www.uniplaces.com',
                'description': 'Piattaforma di alloggi per studenti verificati',
                'specialization': 'Alloggi studenti'
            }
        ],
        'Milan': [
            {
                'name': 'Uniplaces - Milano',
                'url': 'https://www.uniplaces.com',
                'description': 'Piattaforma di alloggi per studenti verificati',
                'specialization': 'Alloggi studenti'
            }
        ],
        'Bologna': [
            {
                'name': 'ER.GO - Bologna',
                'url': 'https://www.er-go.it',
                'description': 'Residenze universitarie a Bologna',
                'specialization': 'Residenze universitarie'
            }
        ]
    }
    
    added_count = 0
    
    # Add real estate portals for each city
    for city in cities:
        for portal in portals:
            agency = RealEstateAgency(
                name=portal['name_template'].format(city),
                city=city,
                country_code='IT',
                website_url=portal['url'],
                description=portal['description'],
                specialization=portal['specialization'],
                is_verified=True,
                is_active=True
            )
            db.add(agency)
            added_count += 1
            print(f"✅ Added: {agency.name}")
    
    # Add student accommodation
    for city, accommodations in student_accommodation.items():
        for accommodation in accommodations:
            agency = RealEstateAgency(
                name=accommodation['name'],
                city=city,
                country_code='IT',
                website_url=accommodation['url'],
                description=accommodation['description'],
                specialization=accommodation['specialization'],
                is_verified=True,
                is_active=True
            )
            db.add(agency)
            added_count += 1
            print(f"✅ Added: {agency.name}")
    
    db.commit()
    print(f"\n✅ Successfully added {added_count} housing agencies for Italy")
    print(f"   Cities: {len(cities)}")
    print(f"   Portals per city: {len(portals)}")
    print(f"   Student accommodation: {sum(len(acc) for acc in student_accommodation.values())}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
