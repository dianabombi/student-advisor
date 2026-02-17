#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add UK real estate agencies and university accommodation
"""

import sys
sys.path.append('/app')

from main import SessionLocal, RealEstateAgency

db = SessionLocal()

try:
    # UK cities (major university cities)
    cities = [
        'London', 'Edinburgh', 'Manchester', 'Birmingham', 'Glasgow',
        'Bristol', 'Leeds', 'Liverpool', 'Oxford', 'Cambridge',
        'Newcastle', 'Sheffield', 'Nottingham', 'Southampton', 'Cardiff',
        'Belfast', 'Aberdeen', 'Leicester', 'Coventry', 'York'
    ]
    
    # Real estate portals (for all cities)
    portals = [
        {
            'name_template': 'Rightmove - {}',
            'url': 'https://www.rightmove.co.uk',
            'description': "UK's largest property portal with millions of listings",
            'specialization': 'Rentals and sales'
        },
        {
            'name_template': 'Zoopla - {}',
            'url': 'https://www.zoopla.co.uk',
            'description': 'Leading UK property website with comprehensive search',
            'specialization': 'Long-term rentals'
        },
        {
            'name_template': 'SpareRoom - {}',
            'url': 'https://www.spareroom.co.uk',
            'description': "UK's number one flatshare site for students and professionals",
            'specialization': 'Flatshares and rooms'
        }
    ]
    
    # Student-specific accommodation (specific to cities)
    student_accommodation = {
        'London': [
            {
                'name': 'Student.com - London',
                'url': 'https://www.student.com',
                'description': 'Global student housing marketplace',
                'specialization': 'Student accommodation'
            },
            {
                'name': 'Uniplaces - London',
                'url': 'https://www.uniplaces.com',
                'description': 'Verified student accommodation platform',
                'specialization': 'Student housing'
            },
            {
                'name': 'Accommodation for Students',
                'url': 'https://www.accommodationforstudents.com',
                'description': 'Specialist student accommodation website',
                'specialization': 'Student housing'
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
                country_code='GB',
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
                country_code='GB',
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
    print(f"\n✅ Successfully added {added_count} housing agencies for United Kingdom")
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
