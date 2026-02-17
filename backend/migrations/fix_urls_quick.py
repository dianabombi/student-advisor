#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick script to fix job agency URLs
Run from backend directory: python -c "from migrations.fix_urls_quick import fix_urls; fix_urls()"
"""

def fix_urls():
    """Fix all job agency URLs to use main domains only"""
    import sys
    import os
    
    # Add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from main import SessionLocal, JobAgency
    
    db = SessionLocal()
    
    try:
        # Get all job agencies
        agencies = db.query(JobAgency).all()
        
        print(f"Found {len(agencies)} job agencies")
        
        updated = 0
        for agency in agencies:
            old_url = agency.website_url
            
            # Fix URLs to main domains only
            if 'profesia.sk' in old_url:
                agency.website_url = 'https://www.profesia.sk'
            elif 'studentjob.sk' in old_url:
                agency.website_url = 'https://www.studentjob.sk'
            elif 'brigada.sk' in old_url:
                agency.website_url = 'https://www.brigada.sk'
            elif 'kariera.sk' in old_url or 'kariera.zoznam.sk' in old_url:
                agency.website_url = 'https://www.kariera.sk'
            elif 'indeed' in old_url:
                agency.website_url = 'https://sk.indeed.com'
            elif 'manpower.sk' in old_url:
                agency.website_url = 'https://www.manpower.sk'
            elif 'grafton.sk' in old_url:
                agency.website_url = 'https://www.grafton.sk'
            
            if old_url != agency.website_url:
                print(f"✅ Updated: {agency.name}")
                print(f"   Old: {old_url}")
                print(f"   New: {agency.website_url}")
                updated += 1
        
        db.commit()
        print(f"\n✅ Successfully updated {updated} job agency URLs!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    fix_urls()
