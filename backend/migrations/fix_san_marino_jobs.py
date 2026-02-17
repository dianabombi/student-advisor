#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix San Marino job agencies - remove closed InfoJobs.it and add working portals
"""

import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency

db = SessionLocal()

try:
    # Delete InfoJobs.it (closed platform)
    infojobs = db.query(JobAgency).filter(
        JobAgency.name.like('InfoJobs%'),
        JobAgency.country_code == 'SM'
    ).all()
    
    for agency in infojobs:
        print(f"❌ Deleting closed portal: {agency.name}")
        db.delete(agency)
    
    # Add working San Marino job portals
    new_agencies = [
        {
            'name': 'LinkedIn - San Marino',
            'city': 'San Marino',
            'country_code': 'SM',
            'website_url': 'https://www.linkedin.com',
            'description': 'Piattaforma professionale più utilizzata a San Marino',
            'specialization': 'Lavori per studenti',
            'is_active': True
        },
        {
            'name': 'Bakeca.it - San Marino',
            'city': 'San Marino',
            'country_code': 'SM',
            'website_url': 'https://www.bakeca.it',
            'description': 'Portale di lavoro italiano (usato a San Marino)',
            'specialization': 'Lavori per studenti',
            'is_active': True
        },
        {
            'name': 'Indeed.it - San Marino',
            'city': 'San Marino',
            'country_code': 'SM',
            'website_url': 'https://it.indeed.com',
            'description': 'Portale di lavoro internazionale',
            'specialization': 'Lavori per studenti',
            'is_active': True
        }
    ]
    
    for data in new_agencies:
        agency = JobAgency(**data)
        db.add(agency)
        print(f"✅ Added: {data['name']}")
    
    db.commit()
    print(f"\n✅ Successfully updated San Marino job agencies")
    print(f"   Deleted: {len(infojobs)} closed portals")
    print(f"   Added: {len(new_agencies)} working portals")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
