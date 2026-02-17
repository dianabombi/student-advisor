#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Belgian real estate agencies and university accommodation
Based on successful UK/France/Spain/Italy implementation
"""

import sys
sys.path.append('/app')

from main import SessionLocal, RealEstateAgency

db = SessionLocal()

try:
    # Belgian cities (from university database)
    cities = ['Brussels', 'Antwerp', 'Ghent', 'Leuven', 'Liège', 'Louvain-la-Neuve']
    
    # Top Belgian real estate portals
    portals = [
        {
            'name_template': 'Immoweb - {}',
            'url': 'https://www.immoweb.be',
            'description': 'Le plus grand site immobilier de Belgique',
            'specialization': 'Location et vente'
        },
        {
            'name_template': 'Zimmo - {}',
            'url': 'https://www.zimmo.be',
            'description': 'Portail immobilier belge pour location et vente',
            'specialization': 'Location'
        },
        {
            'name_template': 'Immoscoop - {}',
            'url': 'https://www.immoscoop.be',
            'description': 'Annonces immobilières en Belgique',
            'specialization': 'Location et vente'
        }
    ]
    
    # Student accommodation
    student_accommodation = {
        'Brussels': [
            {'name': 'Uniplaces - Brussels', 'url': 'https://www.uniplaces.com', 
             'description': 'Verified student accommodation platform', 'specialization': 'Student housing'}
        ],
        'Leuven': [
            {'name': 'KU Leuven Housing', 'url': 'https://www.kuleuven.be/english/studentservices/housing',
             'description': 'KU Leuven student housing service', 'specialization': 'University housing'}
        ]
    }
    
    added_count = 0
    
    for city in cities:
        for portal in portals:
            agency = RealEstateAgency(
                name=portal['name_template'].format(city), city=city, country_code='BE',
                website_url=portal['url'], description=portal['description'],
                specialization=portal['specialization'], is_verified=True, is_active=True
            )
            db.add(agency)
            added_count += 1
            print(f"✅ Added: {agency.name}")
    
    for city, accommodations in student_accommodation.items():
        for accommodation in accommodations:
            agency = RealEstateAgency(
                name=accommodation['name'], city=city, country_code='BE',
                website_url=accommodation['url'], description=accommodation['description'],
                specialization=accommodation['specialization'], is_verified=True, is_active=True
            )
            db.add(agency)
            added_count += 1
            print(f"✅ Added: {agency.name}")
    
    db.commit()
    print(f"\n✅ Successfully added {added_count} housing agencies for Belgium")
    print(f"   Cities: {len(cities)}, Portals: {len(portals)}, Student: {sum(len(acc) for acc in student_accommodation.values())}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
