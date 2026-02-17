#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Polish housing agencies - Batch 1, Country 3/3
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def add_polish_housing_agencies():
    """Add housing agencies for Poland"""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Polish cities with universities
    cities = ['Warszawa', 'Kraków', 'Poznań', 'Wrocław', 'Gdańsk']
    
    # Top 3 Polish housing portals
    portals = [
        {
            'name': 'Otodom.pl',
            'url': 'https://www.otodom.pl',
            'description': 'Największy portal nieruchomości w Polsce',
            'description_en': 'Largest real estate portal in Poland',
            'specialization': 'Wynajem i sprzedaż'
        },
        {
            'name': 'OLX.pl',
            'url': 'https://www.olx.pl',
            'description': 'Popularne ogłoszenia nieruchomości',
            'description_en': 'Popular real estate classifieds',
            'specialization': 'Wynajem i sprzedaż'
        },
        {
            'name': 'Gratka.pl',
            'url': 'https://www.gratka.pl',
            'description': 'Zaufany portal nieruchomości',
            'description_en': 'Trusted real estate portal',
            'specialization': 'Wynajem i sprzedaż'
        }
    ]
    
    added_count = 0
    
    # Add portals for each city
    for city in cities:
        for portal in portals:
            agency_name = f"{portal['name']} - {city}"
            
            # Check if exists
            cursor.execute(
                "SELECT id FROM real_estate_agencies WHERE name = %s AND city = %s AND country_code = 'PL'",
                (agency_name, city)
            )
            
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO real_estate_agencies 
                    (name, city, country_code, website_url, description, specialization)
                    VALUES (%s, %s, 'PL', %s, %s, %s)
                """, (
                    agency_name,
                    city,
                    portal['url'],
                    portal['description_en'],
                    portal['specialization']
                ))
                added_count += 1
                print(f"✅ Added: {agency_name}")
            else:
                print(f"⏭️  Exists: {agency_name}")
    
    # Add university dormitories
    dormitories = [
        {
            'name': 'University of Warsaw - Dormitories',
            'name_local': 'Uniwersytet Warszawski - Akademiki',
            'city': 'Warszawa',
            'url': 'https://www.uw.edu.pl',
            'description': 'Student dormitories at University of Warsaw',
            'specialization': 'Student housing'
        },
        {
            'name': 'Jagiellonian University - Dormitories',
            'name_local': 'Uniwersytet Jagielloński - Akademiki',
            'city': 'Kraków',
            'url': 'https://www.uj.edu.pl',
            'description': 'Student dormitories at Jagiellonian University',
            'specialization': 'Student housing'
        },
        {
            'name': 'Adam Mickiewicz University - Dormitories',
            'name_local': 'UAM - Akademiki',
            'city': 'Poznań',
            'url': 'https://www.amu.edu.pl',
            'description': 'Student dormitories at Adam Mickiewicz University',
            'specialization': 'Student housing'
        },
        {
            'name': 'University of Wrocław - Dormitories',
            'name_local': 'Uniwersytet Wrocławski - Akademiki',
            'city': 'Wrocław',
            'url': 'https://www.uni.wroc.pl',
            'description': 'Student dormitories at University of Wrocław',
            'specialization': 'Student housing'
        },
        {
            'name': 'Gdańsk University of Technology - Dormitories',
            'name_local': 'Politechnika Gdańska - Akademiki',
            'city': 'Gdańsk',
            'url': 'https://www.pg.edu.pl',
            'description': 'Student dormitories at Gdańsk University of Technology',
            'specialization': 'Student housing'
        }
    ]
    
    for dorm in dormitories:
        cursor.execute(
            "SELECT id FROM real_estate_agencies WHERE name = %s AND city = %s AND country_code = 'PL'",
            (dorm['name'], dorm['city'])
        )
        
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO real_estate_agencies 
                (name, city, country_code, website_url, description, specialization)
                VALUES (%s, %s, 'PL', %s, %s, %s)
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
        "SELECT COUNT(*) FROM real_estate_agencies WHERE country_code = 'PL'"
    )
    total = cursor.fetchone()[0]
    
    print(f"\n📊 Summary:")
    print(f"   Added in this run: {added_count}")
    print(f"   Total Polish agencies: {total}")
    print(f"   Cities: {len(cities)}")
    print(f"   Portals: {len(portals)}")
    print(f"   Dormitories: {len(dormitories)}")
    
    cursor.close()
    conn.close()
    
    print("\n✅ Poland housing agencies added successfully!")

if __name__ == "__main__":
    add_polish_housing_agencies()
