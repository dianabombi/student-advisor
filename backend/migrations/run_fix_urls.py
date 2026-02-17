#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run SQL migration to fix job agency URLs
Student Advisor Platform
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from main import SessionLocal
    from sqlalchemy import text
    
    print("Connecting to database...")
    db = SessionLocal()
    
    print("\n" + "="*60)
    print("FIXING JOB AGENCY URLs - Removing subpages")
    print("="*60 + "\n")
    
    # 1. Update Profesia.sk URLs
    result = db.execute(text("""
        UPDATE job_agencies 
        SET website_url = 'https://www.profesia.sk'
        WHERE website_url LIKE '%profesia.sk%'
        AND website_url != 'https://www.profesia.sk'
    """))
    print(f"[1/7] Profesia.sk: Updated {result.rowcount} URLs")
    
    # 2. Update StudentJob URLs
    result = db.execute(text("""
        UPDATE job_agencies 
        SET website_url = 'https://www.studentjob.sk'
        WHERE website_url LIKE '%studentjob.sk%'
        AND website_url != 'https://www.studentjob.sk'
    """))
    print(f"[2/7] StudentJob: Updated {result.rowcount} URLs")
    
    # 3. Update Brigada.sk URLs
    result = db.execute(text("""
        UPDATE job_agencies 
        SET website_url = 'https://www.brigada.sk'
        WHERE website_url LIKE '%brigada.sk%'
        AND website_url != 'https://www.brigada.sk'
    """))
    print(f"[3/7] Brigada.sk: Updated {result.rowcount} URLs")
    
    # 4. Update Kariera.sk URLs
    result = db.execute(text("""
        UPDATE job_agencies 
        SET website_url = 'https://www.kariera.sk'
        WHERE (website_url LIKE '%kariera.sk%' OR website_url LIKE '%kariera.zoznam.sk%')
        AND website_url != 'https://www.kariera.sk'
    """))
    print(f"[4/7] Kariera.sk: Updated {result.rowcount} URLs")
    
    # 5. Update Indeed URLs
    result = db.execute(text("""
        UPDATE job_agencies 
        SET website_url = 'https://sk.indeed.com'
        WHERE (website_url LIKE '%indeed.com%' OR website_url LIKE '%indeed.sk%')
        AND website_url != 'https://sk.indeed.com'
    """))
    print(f"[5/7] Indeed: Updated {result.rowcount} URLs")
    
    # 6. Update Manpower URLs
    result = db.execute(text("""
        UPDATE job_agencies 
        SET website_url = 'https://www.manpower.sk'
        WHERE website_url LIKE '%manpower.sk%'
        AND website_url != 'https://www.manpower.sk'
    """))
    print(f"[6/7] Manpower: Updated {result.rowcount} URLs")
    
    # 7. Update Grafton URLs
    result = db.execute(text("""
        UPDATE job_agencies 
        SET website_url = 'https://www.grafton.sk'
        WHERE website_url LIKE '%grafton.sk%'
        AND website_url != 'https://www.grafton.sk'
    """))
    print(f"[7/7] Grafton: Updated {result.rowcount} URLs")
    
    # Commit changes
    db.commit()
    
    print("\n" + "="*60)
    print("SUCCESS! All job agency URLs have been fixed")
    print("="*60)
    
    # Verify changes
    print("\nVerifying changes...")
    result = db.execute(text("""
        SELECT name, city, website_url 
        FROM job_agencies 
        ORDER BY city, name
        LIMIT 10
    """))
    
    print("\nSample of updated agencies:")
    for row in result:
        print(f"  {row.city:20} | {row.name:30} | {row.website_url}")
    
    print("\nAll URLs now use main domains only (no subpages)")
    print("Backend restart required to apply changes")
    
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
