#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add German housing agencies - Batch 2, Country 1/3

Top 3 German housing portals:
1. ImmobilienScout24.de - Market leader
2. Immowelt.de - 2nd largest
3. WG-Gesucht.de - Best for students/shared housing

Cities: Berlin, München, Hamburg, Köln, Frankfurt
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def add_german_housing_agencies():
    """Add housing agencies for Germany"""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Top 5 German university cities
    cities = ['Berlin', 'München', 'Hamburg', 'Köln', 'Frankfurt']
    
    # Top 3 German housing portals
    portals = [
        {
            'name': 'ImmobilienScout24.de',
            'url': 'https://www.immobilienscout24.de',
            'description': 'Germany\'s largest professional real estate platform',
            'specialization': 'Long-term rentals'
        },
        {
            'name': 'Immowelt.de',
            'url': 'https://www.immowelt.de',
            'description': 'Second-largest real estate marketplace in Germany',
            'specialization': 'Apartments and houses'
        },
        {
            'name': 'WG-Gesucht.de',
            'url': 'https://www.wg-gesucht.de',
            'description': 'Leading platform for shared apartments and student housing',
            'specialization': 'Shared housing (WG)'
        }
    ]
    
    added_count = 0
    
    # Add portals for each city
    for city in cities:
        for portal in portals:
            agency_name = f"{portal['name']} - {city}"
            
            # Check if exists
            cursor.execute(
                "SELECT id FROM real_estate_agencies WHERE name = %s AND city = %s AND country_code = 'DE'",
                (agency_name, city)
            )
            
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO real_estate_agencies 
                    (name, city, country_code, website_url, description, specialization, is_active)
                    VALUES (%s, %s, 'DE', %s, %s, %s, TRUE)
                """, (
                    agency_name,
                    city,
                    portal['url'],
                    portal['description'],
                    portal['specialization']
                ))
                added_count += 1
                print(f"✅ Added: {agency_name}")
            else:
                print(f"⏭️  Exists: {agency_name}")
    
    # Add university dormitories for major cities
    dormitories = [
        {
            'name': 'Studentenwerk Berlin - Dormitories',
            'city': 'Berlin',
            'url': 'https://www.stw.berlin',
            'description': 'Student dormitories in Berlin',
            'specialization': 'Student housing'
        },
        {
            'name': 'Studentenwerk München - Dormitories',
            'city': 'München',
            'url': 'https://www.studentenwerk-muenchen.de',
            'description': 'Student dormitories in Munich',
            'specialization': 'Student housing'
        },
        {
            'name': 'Studierendenwerk Hamburg - Dormitories',
            'city': 'Hamburg',
            'url': 'https://www.studierendenwerk-hamburg.de',
            'description': 'Student dormitories in Hamburg',
            'specialization': 'Student housing'
        },
        {
            'name': 'Kölner Studierendenwerk - Dormitories',
            'city': 'Köln',
            'url': 'https://www.kstw.de',
            'description': 'Student dormitories in Cologne',
            'specialization': 'Student housing'
        },
        {
            'name': 'Studentenwerk Frankfurt - Dormitories',
            'city': 'Frankfurt',
            'url': 'https://www.studentenwerkfrankfurt.de',
            'description': 'Student dormitories in Frankfurt',
            'specialization': 'Student housing'
        }
    ]
    
    for dorm in dormitories:
        cursor.execute(
            "SELECT id FROM real_estate_agencies WHERE name = %s AND city = %s AND country_code = 'DE'",
            (dorm['name'], dorm['city'])
        )
        
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO real_estate_agencies 
                (name, city, country_code, website_url, description, specialization, is_active)
                VALUES (%s, %s, 'DE', %s, %s, %s, TRUE)
            """, (
                dorm['name'],
                dorm['city'],
                dorm['url'],
                dorm['description'],
                dorm['specialization']
            ))
            added_count += 1
            print(f"✅ Added dormitory: {dorm['name']}")
        else:
            print(f"⏭️  Exists: {dorm['name']}")
    
    # Summary
    cursor.execute(
        "SELECT COUNT(*) FROM real_estate_agencies WHERE country_code = 'DE'"
    )
    total = cursor.fetchone()[0]
    
    print(f"\n📊 Summary:")
    print(f"   Added in this run: {added_count}")
    print(f"   Total German agencies: {total}")
    print(f"   Cities: {len(cities)}")
    print(f"   Portals: {len(portals)}")
    print(f"   Dormitories: {len(dormitories)}")
    
    cursor.close()
    conn.close()
    
    print("\n✅ Germany housing agencies added successfully!")

if __name__ == "__main__":
    add_german_housing_agencies()
