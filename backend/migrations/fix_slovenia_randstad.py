#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Slovenia job agencies - replace non-existent Randstad.si with working portals
"""

import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency

db = SessionLocal()

try:
    # Delete Randstad.si agencies (doesn't exist)
    randstad_si = db.query(JobAgency).filter(
        JobAgency.country_code == 'SI',
        JobAgency.website_url.like('%randstad.si%')
    ).all()
    
    cities_to_update = []
    for agency in randstad_si:
        print(f"❌ Deleting: {agency.name} - {agency.city}")
        cities_to_update.append(agency.city)
        db.delete(agency)
    
    # Add working Slovenian job portals for each city
    cities = list(set(cities_to_update))  # Unique cities
    
    new_agencies = []
    for city in cities:
        new_agencies.extend([
            {
                'name': f'MojeDelo.com - {city}',
                'city': city,
                'country_code': 'SI',
                'website_url': 'https://www.mojedelo.com',
                'description': 'Največji slovenski portal za iskanje zaposlitve',
                'specialization': 'Študentsko delo',
                'is_active': True
            },
            {
                'name': f'e-Študentski Servis - {city}',
                'city': city,
                'country_code': 'SI',
                'website_url': 'https://www.studentski-servis.com',
                'description': 'Največji posrednik za študentsko delo v Sloveniji',
                'specialization': 'Študentsko delo',
                'is_active': True
            },
            {
                'name': f'Indeed.si - {city}',
                'city': city,
                'country_code': 'SI',
                'website_url': 'https://si.indeed.com',
                'description': 'Mednarodni portal za iskanje zaposlitve',
                'specialization': 'Študentsko delo',
                'is_active': True
            }
        ])
    
    for data in new_agencies:
        agency = JobAgency(**data)
        db.add(agency)
        print(f"✅ Added: {data['name']}")
    
    db.commit()
    print(f"\n✅ Successfully updated Slovenia job agencies")
    print(f"   Deleted: {len(randstad_si)} Randstad.si portals")
    print(f"   Added: {len(new_agencies)} working portals")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
