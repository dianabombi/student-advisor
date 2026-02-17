#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add Job Agencies for Micro-States

These small countries often use neighboring countries' job portals or have very limited local options.
For Liechtenstein: Swiss and Austrian portals are commonly used
For Vatican, San Marino, Monaco, Andorra: Limited to no student job market
"""

import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency, University, Jurisdiction

MICRO_STATES = {
    'LI': {
        'name': 'Liechtenstein',
        'portals': [
            {'name': 'Jobs.li', 'url': 'https://www.jobs.li', 'desc': 'Liechtenstein job portal'},
            {'name': 'Jobchannel.li', 'url': 'https://www.jobchannel.li', 'desc': 'Jobs in Liechtenstein'},
            {'name': 'Indeed.ch', 'url': 'https://www.indeed.ch', 'desc': 'Swiss job portal (used in Liechtenstein)'}
        ]
    },
    'VA': {
        'name': 'Vatican City',
        'portals': [
            {'name': 'Vatican.va', 'url': 'https://www.vatican.va', 'desc': 'Official Vatican website'},
        ],
        'note': 'Very limited student job market'
    },
    'SM': {
        'name': 'San Marino',
        'portals': [
            {'name': 'InfoJobs.it', 'url': 'https://www.infojobs.it', 'desc': 'Italian job portal (used in San Marino)'},
        ],
        'note': 'Uses Italian job portals'
    },
    'MC': {
        'name': 'Monaco',
        'portals': [
            {'name': 'Monaco.mc', 'url': 'https://www.service-emploi-monaco.mc', 'desc': 'Monaco employment service'},
            {'name': 'Indeed.fr', 'url': 'https://www.indeed.fr', 'desc': 'French job portal (used in Monaco)'}
        ]
    },
    'AD': {
        'name': 'Andorra',
        'portals': [
            {'name': 'Andorra.ad', 'url': 'https://www.govern.ad/treball', 'desc': 'Andorran government employment'},
            {'name': 'InfoJobs.es', 'url': 'https://www.infojobs.net', 'desc': 'Spanish job portal (used in Andorra)'}
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
    
    city_list = [c[0] for c in cities if c[0]]
    
    # If no cities with universities, use capital city
    if not city_list:
        capitals = {
            'LI': ['Vaduz'],
            'VA': ['Vatican City'],
            'SM': ['San Marino'],
            'MC': ['Monaco'],
            'AD': ['Andorra la Vella']
        }
        city_list = capitals.get(country_code, [])
    
    return city_list

def add_agencies_for_microstate(db, country_code, config):
    """Add job agencies for a micro-state"""
    cities = get_cities_for_country(db, country_code)
    
    if not cities:
        print(f"⚠️  No cities found for {country_code}, using capital...")
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
    note = config.get('note', '')
    print(f"✅ {country_code}: Added {count} agencies ({len(config['portals'])} portals × {len(cities)} cities) {note}")
    print(f"   Cities: {', '.join(cities)}")
    return count

def main():
    """Main execution"""
    db = SessionLocal()
    total = 0
    
    try:
        print("🚀 Adding Jobs AI for micro-states...\n")
        
        for country_code, config in MICRO_STATES.items():
            print(f"📍 Processing {config['name']} ({country_code})...")
            count = add_agencies_for_microstate(db, country_code, config)
            total += count
            print()
        
        print(f"🎉 COMPLETED! Total agencies added: {total}")
        print(f"Micro-states processed: {', '.join(MICRO_STATES.keys())}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
