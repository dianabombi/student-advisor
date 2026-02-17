#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Dutch housing agencies - Batch 2, Country 3/3

Top 3 Dutch housing portals:
1. Funda.nl - Largest housing portal
2. Pararius.nl - Popular for rentals
3. Kamernet.nl - Best for students/rooms

Cities: Amsterdam, Utrecht, Rotterdam, Leiden, Groningen
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def add_dutch_housing_agencies():
    """Add housing agencies for Netherlands"""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Top 5 Dutch university cities
    cities = ['Amsterdam', 'Utrecht', 'Rotterdam', 'Leiden', 'Groningen']
    
    # Top 3 Dutch housing portals
    portals = [
        {
            'name': 'Funda.nl',
            'url': 'https://www.funda.nl',
            'description': 'Largest housing portal in the Netherlands',
            'specialization': 'Rent and purchase'
        },
        {
            'name': 'Pararius.nl',
            'url': 'https://www.pararius.nl',
            'description': 'Popular rental platform in the Netherlands',
            'specialization': 'Long-term rentals'
        },
        {
            'name': 'Kamernet.nl',
            'url': 'https://www.kamernet.nl',
            'description': 'Leading platform for student housing and rooms',
            'specialization': 'Student housing'
        }
    ]
    
    added_count = 0
    
    # Add portals for each city
    for city in cities:
        for portal in portals:
            agency_name = f"{portal['name']} - {city}"
            
            # Check if exists
            cursor.execute(
                "SELECT id FROM real_estate_agencies WHERE name = %s AND city = %s AND country_code = 'NL'",
                (agency_name, city)
            )
            
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO real_estate_agencies 
                    (name, city, country_code, website_url, description, specialization, is_active)
                    VALUES (%s, %s, 'NL', %s, %s, %s, TRUE)
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
    
    # Add student housing organizations
    student_housing = [
        {
            'name': 'DUWO - Student Housing Amsterdam',
            'city': 'Amsterdam',
            'url': 'https://www.duwo.nl',
            'description': 'Student housing provider in Amsterdam',
            'specialization': 'Student housing'
        },
        {
            'name': 'SSH - Student Housing Utrecht',
            'city': 'Utrecht',
            'url': 'https://www.sshxl.nl',
            'description': 'Student housing provider in Utrecht',
            'specialization': 'Student housing'
        },
        {
            'name': 'ROOM - Student Housing Rotterdam',
            'city': 'Rotterdam',
            'url': 'https://www.room.nl',
            'description': 'Student housing provider in Rotterdam',
            'specialization': 'Student housing'
        },
        {
            'name': 'DUWO - Student Housing Leiden',
            'city': 'Leiden',
            'url': 'https://www.duwo.nl',
            'description': 'Student housing provider in Leiden',
            'specialization': 'Student housing'
        },
        {
            'name': 'SSH - Student Housing Groningen',
            'city': 'Groningen',
            'url': 'https://www.sshgroningen.nl',
            'description': 'Student housing provider in Groningen',
            'specialization': 'Student housing'
        }
    ]
    
    for housing in student_housing:
        cursor.execute(
            "SELECT id FROM real_estate_agencies WHERE name = %s AND city = %s AND country_code = 'NL'",
            (housing['name'], housing['city'])
        )
        
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO real_estate_agencies 
                (name, city, country_code, website_url, description, specialization, is_active)
                VALUES (%s, %s, 'NL', %s, %s, %s, TRUE)
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
        "SELECT COUNT(*) FROM real_estate_agencies WHERE country_code = 'NL'"
    )
    total = cursor.fetchone()[0]
    
    print(f"\n📊 Summary:")
    print(f"   Added in this run: {added_count}")
    print(f"   Total Dutch agencies: {total}")
    print(f"   Cities: {len(cities)}")
    print(f"   Portals: {len(portals)}")
    print(f"   Student housing: {len(student_housing)}")
    
    cursor.close()
    conn.close()
    
    print("\n✅ Netherlands housing agencies added successfully!")

if __name__ == "__main__":
    add_dutch_housing_agencies()
