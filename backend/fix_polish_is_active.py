#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Polish agencies - set is_active = TRUE
"""

from main import SessionLocal
from sqlalchemy import text

db = SessionLocal()

# Update all Polish agencies to is_active = TRUE
result = db.execute(text("UPDATE real_estate_agencies SET is_active = TRUE WHERE country_code = 'PL'"))
db.commit()

print(f"✅ Updated {result.rowcount} Polish agencies to is_active=TRUE")

# Verify
count = db.execute(text("SELECT COUNT(*) FROM real_estate_agencies WHERE country_code = 'PL' AND is_active = TRUE"))
total = count.fetchone()[0]
print(f"✅ Total active Polish agencies: {total}")

db.close()
