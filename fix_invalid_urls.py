#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix invalid URLs for institutions
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://student_user:student_pass@localhost:5433/student_platform')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def fix_urls():
    """Fix invalid URLs for institutions"""
    db = SessionLocal()
    
    try:
        # Fix SPŠE - change from spse.sk (for sale) to zochova.sk
        db.execute(text("""
            UPDATE universities 
            SET website_url = 'https://www.zochova.sk'
            WHERE name_local = 'Stredná priemyselná škola elektrotechnická'
        """))
        print("[OK] Fixed SPSE URL: spse.sk -> zochova.sk")
        
        # Fix Hotelová akadémia - change from hotelka.eu (SSL error) to edupage.org
        db.execute(text("""
            UPDATE universities 
            SET website_url = 'https://hamikoviniho.edupage.org'
            WHERE name_local = 'Hotelová akadémia Bratislava'
        """))
        print("[OK] Fixed Hotelova akademia URL: hotelka.eu -> hamikoviniho.edupage.org")
        
        db.commit()
        print("\n[SUCCESS] URLs fixed successfully!")
        
        # Verify changes
        result = db.execute(text("""
            SELECT id, name_local, website_url 
            FROM universities 
            WHERE name_local IN ('Stredná priemyselná škola elektrotechnická', 'Hotelová akadémia Bratislava')
        """))
        
        print("\nVerification:")
        for row in result:
            print(f"  ID {row[0]}: {row[1]}")
            print(f"    URL: {row[2]}")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    fix_urls()
