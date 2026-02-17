#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Czech Republic Housing Agencies
Adds verified real estate portals and university dormitories for Czech cities
"""

import sys
sys.path.append('/app')

from main import SessionLocal, RealEstateAgency

def add_czech_agencies():
    """Add Czech housing agencies to database"""
    db = SessionLocal()
    
    try:
        print("🇨🇿 Adding Czech Republic Housing Agencies...")
        
        # Czech cities with universities
        cities = [
            'Praha',
            'Brno', 
            'Ostrava',
            'Olomouc',
            'Plzeň',
            'Liberec',
            'Hradec Králové',
            'České Budějovice',
            'Pardubice'
        ]
        
        # Major Czech real estate portals
        portals = [
            {
                'name': 'Sreality.cz',
                'url': 'https://www.sreality.cz',
                'description': 'Největší český realitní portál',
                'specialization': 'Pronájem a prodej'
            },
            {
                'name': 'Bezrealitky.cz',
                'url': 'https://www.bezrealitky.cz',
                'description': 'Přímé pronájmy bez realitních kanceláří',
                'specialization': 'Pronájem bez provize'
            },
            {
                'name': 'Reality.iDNES.cz',
                'url': 'https://reality.idnes.cz',
                'description': 'Realitní sekce iDNES',
                'specialization': 'Pronájem a prodej'
            },
            {
                'name': 'UlovDomov.cz',
                'url': 'https://www.ulovdomov.cz',
                'description': 'Agregátor realitních nabídek',
                'specialization': 'Pronájem a prodej'
            }
        ]
        
        agencies_added = 0
        
        # Add portals for each city
        for city in cities:
            for portal in portals:
                agency = RealEstateAgency(
                    name=f"{portal['name']} - {city}",
                    website_url=portal['url'],
                    city=city,
                    country_code='CZ',
                    description=portal['description'],
                    specialization=portal['specialization'],
                    is_verified=True,
                    is_active=True
                )
                db.add(agency)
                agencies_added += 1
                print(f"  ✅ Added: {agency.name}")
        
        # University dormitories
        dormitories = [
            {
                'name': 'Univerzita Karlova - Koleje',
                'url': 'https://www.cuni.cz',
                'city': 'Praha',
                'description': 'Studentské koleje Univerzity Karlovy'
            },
            {
                'name': 'ČVUT - Studentské koleje',
                'url': 'https://www.cvut.cz',
                'city': 'Praha',
                'description': 'Koleje ČVUT v Praze'
            },
            {
                'name': 'Masarykova univerzita - Koleje',
                'url': 'https://www.muni.cz',
                'city': 'Brno',
                'description': 'Studentské koleje Masarykovy univerzity'
            },
            {
                'name': 'VUT - Studentské koleje',
                'url': 'https://www.vutbr.cz',
                'city': 'Brno',
                'description': 'Koleje VUT v Brně'
            },
            {
                'name': 'Ostravská univerzita - Koleje',
                'url': 'https://www.osu.cz',
                'city': 'Ostrava',
                'description': 'Studentské koleje Ostravské univerzity'
            },
            {
                'name': 'VŠB-TUO - Koleje',
                'url': 'https://www.vsb.cz',
                'city': 'Ostrava',
                'description': 'Koleje VŠB-TU Ostrava'
            },
            {
                'name': 'Univerzita Palackého - Koleje',
                'url': 'https://www.upol.cz',
                'city': 'Olomouc',
                'description': 'Studentské koleje UP Olomouc'
            },
            {
                'name': 'Západočeská univerzita - Koleje',
                'url': 'https://www.zcu.cz',
                'city': 'Plzeň',
                'description': 'Studentské koleje ZČU Plzeň'
            },
            {
                'name': 'TU Liberec - Koleje',
                'url': 'https://www.tul.cz',
                'city': 'Liberec',
                'description': 'Studentské koleje TU Liberec'
            },
            {
                'name': 'Univerzita Hradec Králové - Koleje',
                'url': 'https://www.uhk.cz',
                'city': 'Hradec Králové',
                'description': 'Studentské koleje UHK'
            },
            {
                'name': 'Jihočeská univerzita - Koleje',
                'url': 'https://www.jcu.cz',
                'city': 'České Budějovice',
                'description': 'Studentské koleje JU'
            },
            {
                'name': 'Univerzita Pardubice - Koleje',
                'url': 'https://www.upce.cz',
                'city': 'Pardubice',
                'description': 'Studentské koleje UPa'
            }
        ]
        
        for dorm in dormitories:
            agency = RealEstateAgency(
                name=dorm['name'],
                website_url=dorm['url'],
                city=dorm['city'],
                country_code='CZ',
                description=dorm['description'],
                specialization='Studentské ubytování',
                is_verified=True,
                is_active=True
            )
            db.add(agency)
            agencies_added += 1
            print(f"  ✅ Added: {agency.name}")
        
        db.commit()
        print(f"\n✅ Successfully added {agencies_added} Czech housing agencies!")
        print(f"   - {len(cities)} cities covered")
        print(f"   - {len(portals)} portals × {len(cities)} cities = {len(portals) * len(cities)} portal entries")
        print(f"   - {len(dormitories)} university dormitories")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    add_czech_agencies()
