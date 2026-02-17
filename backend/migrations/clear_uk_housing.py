#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clear UK housing agencies before re-running migration"""

import sys
sys.path.append('/app')

from main import SessionLocal, RealEstateAgency

db = SessionLocal()

try:
    # Delete all UK agencies
    deleted = db.query(RealEstateAgency).filter(
        RealEstateAgency.country_code == 'GB'
    ).delete()
    
    db.commit()
    print(f"✅ Deleted {deleted} UK housing agencies")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
