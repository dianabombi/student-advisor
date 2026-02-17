#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Spanish real estate agencies and university accommodation
Based on successful UK/France implementation
"""

import sys
sys.path.append('/app')

from main import SessionLocal, RealEstateAgency

db = SessionLocal()

try:
    # Spanish cities (major university cities)
    cities = [
        'Madrid',
        'Barcelona',
        'Valencia',
        'Sevilla',
        'Zaragoza',
        'Málaga',
        'Murcia',
        'Palma',
        'Bilbao',
        'Alicante',
        'Granada',
        'Salamanca',
        'Santiago de Compostela',
        'Pamplona',
        'San Sebastián'
    ]
    
    # Top Spanish real estate portals (for all cities)
    portals = [
        {
            'name_template': 'Idealista - {}',
            'url': 'https://www.idealista.com',
            'description': 'Portal inmobiliario líder en España',
            'specialization': 'Alquiler y venta'
        },
        {
            'name_template': 'Fotocasa - {}',
            'url': 'https://www.fotocasa.es',
            'description': 'Portal de alquiler y compra de pisos',
            'specialization': 'Alquiler de pisos'
        },
        {
            'name_template': 'Pisos.com - {}',
            'url': 'https://www.pisos.com',
            'description': 'Inmobiliaria online para alquiler y venta',
            'specialization': 'Alquiler y venta'
        }
    ]
    
    # Student-specific accommodation
    student_accommodation = {
        'Madrid': [
            {
                'name': 'Uniplaces - Madrid',
                'url': 'https://www.uniplaces.com',
                'description': 'Plataforma de alojamiento estudiantil verificado',
                'specialization': 'Alojamiento estudiantil'
            }
        ],
        'Barcelona': [
            {
                'name': 'Uniplaces - Barcelona',
                'url': 'https://www.uniplaces.com',
                'description': 'Plataforma de alojamiento estudiantil verificado',
                'specialization': 'Alojamiento estudiantil'
            }
        ],
        'Salamanca': [
            {
                'name': 'Colegios Mayores Salamanca',
                'url': 'https://www.usal.es',
                'description': 'Residencias universitarias en Salamanca',
                'specialization': 'Residencias universitarias'
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
                country_code='ES',
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
                country_code='ES',
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
    print(f"\n✅ Successfully added {added_count} housing agencies for Spain")
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
