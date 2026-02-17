#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Jobs AI Setup for Remaining Countries

This script automatically adds job agencies for all remaining countries.
It handles:
1. Database migration (job agencies)
2. City detection updates (multilingual)
3. Country mapping
4. Portal instructions

Countries: DK, NO, FI, GR, HU, SI, HR
"""

import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency, University, Jurisdiction

# Country configurations
COUNTRIES = {
    'DK': {
        'name': 'Denmark',
        'portals': [
            {'name': 'Jobindex.dk', 'url': 'https://www.jobindex.dk', 'desc': 'Danmarks største jobportal'},
            {'name': 'Randstad.dk', 'url': 'https://www.randstad.dk', 'desc': 'Rekrutterings- og vikarbureau'},
            {'name': 'Manpower.dk', 'url': 'https://www.manpower.dk', 'desc': 'Vikarbureau og rekruttering'}
        ]
    },
    'NO': {
        'name': 'Norway',
        'portals': [
            {'name': 'Finn.no', 'url': 'https://www.finn.no/job', 'desc': 'Norges største jobbportal'},
            {'name': 'Randstad.no', 'url': 'https://www.randstad.no', 'desc': 'Rekrutterings- og bemanningsbyrå'},
            {'name': 'Manpower.no', 'url': 'https://www.manpower.no', 'desc': 'Bemanningsselskap'}
        ]
    },
    'FI': {
        'name': 'Finland',
        'portals': [
            {'name': 'Mol.fi', 'url': 'https://www.mol.fi', 'desc': 'Työ- ja elinkeinoministeriö'},
            {'name': 'Randstad.fi', 'url': 'https://www.randstad.fi', 'desc': 'Henkilöstöpalveluyritys'},
            {'name': 'Manpower.fi', 'url': 'https://www.manpower.fi', 'desc': 'Henkilöstöpalvelut'}
        ]
    },
    'GR': {
        'name': 'Greece',
        'portals': [
            {'name': 'Kariera.gr', 'url': 'https://www.kariera.gr', 'desc': 'Αναζήτηση εργασίας στην Ελλάδα'},
            {'name': 'Randstad.gr', 'url': 'https://www.randstad.gr', 'desc': 'Υπηρεσίες προσωπικού'},
            {'name': 'Manpower.gr', 'url': 'https://www.manpower.gr', 'desc': 'Υπηρεσίες απασχόλησης'}
        ]
    },
    'HU': {
        'name': 'Hungary',
        'portals': [
            {'name': 'Profession.hu', 'url': 'https://www.profession.hu', 'desc': 'Álláskeresés Magyarországon'},
            {'name': 'Randstad.hu', 'url': 'https://www.randstad.hu', 'desc': 'Munkaerő-kölcsönzés'},
            {'name': 'Manpower.hu', 'url': 'https://www.manpower.hu', 'desc': 'Munkaerő-közvetítés'}
        ]
    },
    'SI': {
        'name': 'Slovenia',
        'portals': [
            {'name': 'MojeDelo.com', 'url': 'https://www.mojedelo.com', 'desc': 'Iskanje zaposlitve v Sloveniji'},
            {'name': 'Randstad.si', 'url': 'https://www.randstad.si', 'desc': 'Kadrovske storitve'},
            {'name': 'Manpower.si', 'url': 'https://www.manpower.si', 'desc': 'Zaposlovanje'}
        ]
    },
    'HR': {
        'name': 'Croatia',
        'portals': [
            {'name': 'MojPosao.net', 'url': 'https://www.mojposao.net', 'desc': 'Traženje posla u Hrvatskoj'},
            {'name': 'Randstad.hr', 'url': 'https://www.randstad.hr', 'desc': 'Usluge zapošljavanja'},
            {'name': 'Manpower.hr', 'url': 'https://www.manpower.hr', 'desc': 'Agencija za zapošljavanje'}
        ]
    }
}

def get_cities_for_country(db, country_code):
    """Get cities with universities for a country"""
    jurisdiction = db.query(Jurisdiction).filter(Jurisdiction.code == country_code).first()
    if not jurisdiction:
        return []
    
    cities = db.query(University.city).filter(
        University.jurisdiction_id == jurisdiction.id
    ).distinct().all()
    
    return sorted([c[0] for c in cities if c[0]])

def add_agencies_for_country(db, country_code, config):
    """Add job agencies for a specific country"""
    cities = get_cities_for_country(db, country_code)
    
    if not cities:
        print(f"⚠️  No cities found for {country_code}, skipping...")
        return 0
    
    # Delete existing agencies
    existing = db.query(JobAgency).filter(JobAgency.country_code == country_code).count()
    if existing > 0:
        print(f"  Deleting {existing} existing {country_code} agencies...")
        db.query(JobAgency).filter(JobAgency.country_code == country_code).delete()
        db.commit()
    
    # Add new agencies
    count = 0
    for city in cities:
        for portal in config['portals']:
            agency = JobAgency(
                name=f"{portal['name']} - {city}",
                city=city,
                country_code=country_code,
                website_url=portal['url'],
                description=portal['desc'],
                specialization='student_jobs',
                is_active=True
            )
            db.add(agency)
            count += 1
    
    db.commit()
    print(f"✅ {country_code}: Added {count} agencies ({len(config['portals'])} portals × {len(cities)} cities)")
    print(f"   Cities: {', '.join(cities)}")
    return count

def main():
    """Main execution"""
    db = SessionLocal()
    total = 0
    
    try:
        print("🚀 Starting automated Jobs AI setup for remaining countries...\n")
        
        for country_code, config in COUNTRIES.items():
            print(f"📍 Processing {config['name']} ({country_code})...")
            count = add_agencies_for_country(db, country_code, config)
            total += count
            print()
        
        print(f"🎉 COMPLETED! Total agencies added: {total}")
        print(f"Countries processed: {', '.join(COUNTRIES.keys())}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
