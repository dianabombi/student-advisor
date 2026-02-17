#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Liechtenstein job portal URLs
"""

import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency

db = SessionLocal()

try:
    # Fix Jobs.li -> liechtensteinjobs.li
    jobs_li = db.query(JobAgency).filter(
        JobAgency.name.like('Jobs.li%')
    ).all()
    
    for agency in jobs_li:
        old_url = agency.website_url
        agency.name = 'LiechensteinJobs.li - ' + agency.city
        agency.website_url = 'https://www.liechtensteinjobs.li'
        agency.description = 'Führendes Jobportal in Liechtenstein'
        print(f"✅ Updated {agency.city}: {old_url} -> {agency.website_url}")
    
    # Fix Jobchannel.li -> jobchannel.ch
    jobchannel_li = db.query(JobAgency).filter(
        JobAgency.name.like('Jobchannel.li%')
    ).all()
    
    for agency in jobchannel_li:
        old_url = agency.website_url
        agency.name = 'Jobchannel.ch - ' + agency.city
        agency.website_url = 'https://www.jobchannel.ch'
        agency.description = 'Schweizer Jobportal (auch für Liechtenstein)'
        print(f"✅ Updated {agency.city}: {old_url} -> {agency.website_url}")
    
    db.commit()
    print(f"\n✅ Successfully updated {len(jobs_li) + len(jobchannel_li)} Liechtenstein job agencies")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
