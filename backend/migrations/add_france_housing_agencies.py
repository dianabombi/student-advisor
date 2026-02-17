#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add French real estate agencies and university accommodation
Based on successful UK implementation
"""

import sys
sys.path.append('/app')

from main import SessionLocal, RealEstateAgency

db = SessionLocal()

try:
    # French cities (major university cities)
    # Based on cities already in housing_chat_service.py
    cities = [
        'Paris',
        'Lyon',
        'Marseille',
        'Toulouse',
        'Nice',
        'Nantes',
        'Strasbourg',
        'Montpellier',
        'Bordeaux',
        'Lille',
        'Rennes',
        'Grenoble',
        'Aix-en-Provence',
        'Cergy',
        'Jouy-en-Josas',
        'Palaiseau'
    ]
    
    # Top French real estate portals (for all cities)
    portals = [
        {
            'name_template': 'SeLoger - {}',
            'url': 'https://www.seloger.com',
            'description': 'Premier site immobilier français pour la location et la vente',
            'specialization': 'Location et vente'
        },
        {
            'name_template': 'Leboncoin Immobilier - {}',
            'url': 'https://www.leboncoin.fr',
            'description': 'Site de petites annonces immobilières entre particuliers',
            'specialization': 'Location entre particuliers'
        },
        {
            'name_template': 'PAP - {}',
            'url': 'https://www.pap.fr',
            'description': 'De Particulier À Particulier - location sans frais d\'agence',
            'specialization': 'Location sans commission'
        }
    ]
    
    # Student-specific accommodation (specific to cities)
    student_accommodation = {
        'Paris': [
            {
                'name': 'Studapart - Paris',
                'url': 'https://www.studapart.com',
                'description': 'Plateforme de logement étudiant certifié',
                'specialization': 'Logement étudiant'
            },
            {
                'name': 'CROUS Paris',
                'url': 'https://www.crous-paris.fr',
                'description': 'Résidences universitaires CROUS à Paris',
                'specialization': 'Résidences universitaires'
            }
        ],
        'Lyon': [
            {
                'name': 'CROUS Lyon',
                'url': 'https://www.crous-lyon.fr',
                'description': 'Résidences universitaires CROUS à Lyon',
                'specialization': 'Résidences universitaires'
            }
        ],
        'Toulouse': [
            {
                'name': 'CROUS Toulouse',
                'url': 'https://www.crous-toulouse.fr',
                'description': 'Résidences universitaires CROUS à Toulouse',
                'specialization': 'Résidences universitaires'
            }
        ],
        'Marseille': [
            {
                'name': 'CROUS Aix-Marseille',
                'url': 'https://www.crous-aix-marseille.fr',
                'description': 'Résidences universitaires CROUS à Marseille',
                'specialization': 'Résidences universitaires'
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
                country_code='FR',
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
                country_code='FR',
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
    print(f"\n✅ Successfully added {added_count} housing agencies for France")
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
