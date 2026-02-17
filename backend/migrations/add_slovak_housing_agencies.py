#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Slovak real estate agencies and university dormitories
"""

import sys
sys.path.append('/app')

from main import SessionLocal, RealEstateAgency

db = SessionLocal()

try:
    # Slovak cities (same as Jobs AI)
    cities = [
        'Bratislava', 'Košice', 'Prešov', 'Žilina', 'Nitra',
        'Banská Bystrica', 'Trnava', 'Martin', 'Trenčín'
    ]
    
    # Real estate portals (for all cities)
    portals = [
        {
            'name_template': 'Nehnuteľnosti.sk - {}',
            'url': 'https://www.nehnutelnosti.sk',
            'description': 'Najväčší slovenský portál nehnuteľností',
            'specialization': 'Prenájom a predaj'
        },
        {
            'name_template': 'Reality.sk - {}',
            'url': 'https://www.reality.sk',
            'description': 'Portál pre nehnuteľnosti na predaj, prenájom a aukcie',
            'specialization': 'Prenájom a predaj'
        },
        {
            'name_template': 'Topreality.sk - {}',
            'url': 'https://www.topreality.sk',
            'description': 'Realitný portál skupiny Nehnuteľnosti.sk',
            'specialization': 'Prenájom a predaj'
        },
        {
            'name_template': 'Bezrealitky.sk - {}',
            'url': 'https://www.bezrealitky.sk',
            'description': 'Predaj a prenájom bez provízie',
            'specialization': 'Prenájom a predaj bez provízie'
        }
    ]
    
    # University dormitories (specific to cities)
    dormitories = {
        'Bratislava': [
            {
                'name': 'Univerzita Komenského - Študentské domovy',
                'url': 'https://www.uniba.sk',
                'description': 'Študentské ubytovanie Univerzity Komenského',
                'specialization': 'Študentské ubytovanie'
            },
            {
                'name': 'STU - Študentské domovy',
                'url': 'https://www.stuba.sk',
                'description': 'Študentské ubytovanie Slovenskej technickej univerzity',
                'specialization': 'Študentské ubytovanie'
            }
        ],
        'Košice': [
            {
                'name': 'UPJŠ - Študentské domovy',
                'url': 'https://www.upjs.sk',
                'description': 'Študentské ubytovanie Univerzity Pavla Jozefa Šafárika',
                'specialization': 'Študentské ubytovanie'
            },
            {
                'name': 'TUKE - Študentské domovy',
                'url': 'https://www.tuke.sk',
                'description': 'Študentské ubytovanie Technickej univerzity v Košiciach',
                'specialization': 'Študentské ubytovanie'
            }
        ],
        'Žilina': [
            {
                'name': 'UNIZA - Študentské domovy',
                'url': 'https://www.uniza.sk',
                'description': 'Študentské ubytovanie Žilinskej univerzity',
                'specialization': 'Študentské ubytovanie'
            }
        ],
        'Nitra': [
            {
                'name': 'UKF - Študentské domovy',
                'url': 'https://www.ukf.sk',
                'description': 'Študentské ubytovanie Univerzity Konštantína Filozofa',
                'specialization': 'Študentské ubytovanie'
            }
        ],
        'Banská Bystrica': [
            {
                'name': 'UMB - Študentské domovy',
                'url': 'https://www.umb.sk',
                'description': 'Študentské ubytovanie Univerzity Mateja Bela',
                'specialization': 'Študentské ubytovanie'
            }
        ],
        'Trnava': [
            {
                'name': 'UCM - Študentské domovy',
                'url': 'https://www.ucm.sk',
                'description': 'Študentské ubytovanie Univerzity sv. Cyrila a Metoda',
                'specialization': 'Študentské ubytovanie'
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
                country_code='SK',
                website_url=portal['url'],
                description=portal['description'],
                specialization=portal['specialization'],
                is_verified=True,
                is_active=True
            )
            db.add(agency)
            added_count += 1
            print(f"✅ Added: {agency.name}")
    
    # Add university dormitories
    for city, dorms in dormitories.items():
        for dorm in dorms:
            agency = RealEstateAgency(
                name=dorm['name'],
                city=city,
                country_code='SK',
                website_url=dorm['url'],
                description=dorm['description'],
                specialization=dorm['specialization'],
                is_verified=True,
                is_active=True
            )
            db.add(agency)
            added_count += 1
            print(f"✅ Added: {agency.name}")
    
    db.commit()
    print(f"\n✅ Successfully added {added_count} housing agencies for Slovakia")
    print(f"   Cities: {len(cities)}")
    print(f"   Portals per city: {len(portals)}")
    print(f"   University dormitories: {sum(len(dorms) for dorms in dormitories.values())}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
