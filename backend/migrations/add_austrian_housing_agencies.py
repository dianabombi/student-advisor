#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Austrian housing agencies - Batch 2, Country 2/3

Top 3 Austrian housing portals:
1. Willhaben.at - Largest classifieds
2. ImmobilienScout24.at - Leading property portal
3. Immowelt.at - Major marketplace

Cities: Wien, Graz, Innsbruck, Salzburg, Linz
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def add_austrian_housing_agencies():
    """Add housing agencies for Austria"""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Top 5 Austrian university cities
    cities = ['Wien', 'Graz', 'Innsbruck', 'Salzburg', 'Linz']
    
    # Top 3 Austrian housing portals
    portals = [
        {
            'name': 'Willhaben.at',
            'url': 'https://www.willhaben.at',
            'description': 'Austria\'s largest classified website for rentals',
            'specialization': 'Apartments and houses'
        },
        {
            'name': 'ImmobilienScout24.at',
            'url': 'https://www.immobilienscout24.at',
            'description': 'Leading online property portal in Austria',
            'specialization': 'Long-term rentals'
        },
        {
            'name': 'Immowelt.at',
            'url': 'https://www.immowelt.at',
            'description': 'Major real estate marketplace in Austria',
            'specialization': 'Rent and purchase'
        }
    ]
    
    added_count = 0
    
    # Add portals for each city
    for city in cities:
        for portal in portals:
            agency_name = f"{portal['name']} - {city}"
            
            # Check if exists
            cursor.execute(
                "SELECT id FROM real_estate_agencies WHERE name = %s AND city = %s AND country_code = 'AT'",
                (agency_name, city)
            )
            
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO real_estate_agencies 
                    (name, city, country_code, website_url, description, specialization, is_active)
                    VALUES (%s, %s, 'AT', %s, %s, %s, TRUE)
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
    
    # Add student housing organizations (ÖH - Austrian Students' Union housing)
    student_housing = [
        {
            'name': 'ÖH Wien - Student Housing',
            'city': 'Wien',
            'url': 'https://www.oeh.ac.at',
            'description': 'Student housing assistance in Vienna',
            'specialization': 'Student housing'
        },
        {
            'name': 'ÖH Graz - Student Housing',
            'city': 'Graz',
            'url': 'https://www.oehunigraz.at',
            'description': 'Student housing assistance in Graz',
            'specialization': 'Student housing'
        },
        {
            'name': 'ÖH Innsbruck - Student Housing',
            'city': 'Innsbruck',
            'url': 'https://www.oeh.cc',
            'description': 'Student housing assistance in Innsbruck',
            'specialization': 'Student housing'
        },
        {
            'name': 'ÖH Salzburg - Student Housing',
            'city': 'Salzburg',
            'url': 'https://www.oeh-salzburg.at',
            'description': 'Student housing assistance in Salzburg',
            'specialization': 'Student housing'
        },
        {
            'name': 'ÖH Linz - Student Housing',
            'city': 'Linz',
            'url': 'https://www.oeh.jku.at',
            'description': 'Student housing assistance in Linz',
            'specialization': 'Student housing'
        }
    ]
    
    for housing in student_housing:
        cursor.execute(
            "SELECT id FROM real_estate_agencies WHERE name = %s AND city = %s AND country_code = 'AT'",
            (housing['name'], housing['city'])
        )
        
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO real_estate_agencies 
                (name, city, country_code, website_url, description, specialization, is_active)
                VALUES (%s, %s, 'AT', %s, %s, %s, TRUE)
            """, (
                housing['name'],
                housing['city'],
                housing['url'],
                housing['description'],
                housing['specialization']
            ))
            added_count += 1
            print(f"✅ Added student housing: {housing['name']}")
        else:
            print(f"⏭️  Exists: {housing['name']}")
    
    # Summary
    cursor.execute(
        "SELECT COUNT(*) FROM real_estate_agencies WHERE country_code = 'AT'"
    )
    total = cursor.fetchone()[0]
    
    print(f"\n📊 Summary:")
    print(f"   Added in this run: {added_count}")
    print(f"   Total Austrian agencies: {total}")
    print(f"   Cities: {len(cities)}")
    print(f"   Portals: {len(portals)}")
    print(f"   Student housing: {len(student_housing)}")
    
    cursor.close()
    conn.close()
    
    print("\n✅ Austria housing agencies added successfully!")

if __name__ == "__main__":
    add_austrian_housing_agencies()
