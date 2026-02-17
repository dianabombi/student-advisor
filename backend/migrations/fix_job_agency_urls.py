#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Job Agency URLs - Remove subpages, use only main domains
"""

from sqlalchemy import text

def upgrade(db):
    """Fix job agency URLs to use only main domains"""
    
    # Update all Profesia URLs to main domain
    db.execute(text("""
        UPDATE job_agencies 
        SET website_url = 'https://www.profesia.sk'
        WHERE website_url LIKE '%profesia.sk%'
    """))
    
    # Update all StudentJob URLs to main domain
    db.execute(text("""
        UPDATE job_agencies 
        SET website_url = 'https://www.studentjob.sk'
        WHERE website_url LIKE '%studentjob.sk%'
    """))
    
    # Update all Brigada URLs to main domain
    db.execute(text("""
        UPDATE job_agencies 
        SET website_url = 'https://www.brigada.sk'
        WHERE website_url LIKE '%brigada.sk%'
    """))
    
    # Update all Kariera URLs to main domain
    db.execute(text("""
        UPDATE job_agencies 
        SET website_url = 'https://www.kariera.sk'
        WHERE website_url LIKE '%kariera.sk%'
    """))
    
    # Update all Indeed URLs to main domain
    db.execute(text("""
        UPDATE job_agencies 
        SET website_url = 'https://sk.indeed.com'
        WHERE website_url LIKE '%indeed.com%' OR website_url LIKE '%indeed.sk%'
    """))
    
    # Update all Manpower URLs to main domain
    db.execute(text("""
        UPDATE job_agencies 
        SET website_url = 'https://www.manpower.sk'
        WHERE website_url LIKE '%manpower.sk%'
    """))
    
    # Update all Grafton URLs to main domain
    db.execute(text("""
        UPDATE job_agencies 
        SET website_url = 'https://www.grafton.sk'
        WHERE website_url LIKE '%grafton.sk%'
    """))
    
    db.commit()
    print("✅ Job agency URLs fixed - all using main domains only")


def downgrade(db):
    """Revert URL changes"""
    print("⚠️  Downgrade not implemented - URLs remain as main domains")


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    import os
    
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        upgrade(db)
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()
