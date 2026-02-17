#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct database fix for job agency URLs
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://codex_user:your_password@localhost/codex_db")

print("Connecting to database...")

try:
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    print("Connected to database")
    
    # Update URLs directly with SQL
    updates = [
        ("Profesia.sk", "profesia.sk", "https://www.profesia.sk"),
        ("StudentJob", "studentjob.sk", "https://www.studentjob.sk"),
        ("Brigada.sk", "brigada.sk", "https://www.brigada.sk"),
        ("Kariera.sk", "kariera", "https://www.kariera.sk"),
        ("Indeed", "indeed", "https://sk.indeed.com"),
        ("Manpower", "manpower.sk", "https://www.manpower.sk"),
        ("Grafton", "grafton.sk", "https://www.grafton.sk"),
    ]
    
    total_updated = 0
    
    for name, pattern, new_url in updates:
        result = db.execute(text(f"""
            UPDATE job_agencies 
            SET website_url = :new_url
            WHERE website_url LIKE :pattern
            AND website_url != :new_url
        """), {"new_url": new_url, "pattern": f"%{pattern}%"})
        
        count = result.rowcount
        if count > 0:
            print(f"[OK] Updated {count} {name} URLs to {new_url}")
            total_updated += count
    
    db.commit()
    print(f"\n[SUCCESS] Updated {total_updated} job agency URLs!")
    print("All URLs now use main domains only (no subpages)")
    
except Exception as e:
    print(f"[ERROR] {e}")
    print("\nMake sure:")
    print("1. Database is running")
    print("2. DATABASE_URL environment variable is set")
    print("3. Or update DATABASE_URL in this script")
finally:
    try:
        db.close()
    except:
        pass
