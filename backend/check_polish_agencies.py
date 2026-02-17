#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check Polish agencies in database
"""

from main import SessionLocal
from sqlalchemy import text

db = SessionLocal()

# Check if agencies exist
result = db.execute(text("SELECT name, city, country_code FROM real_estate_agencies WHERE city = 'Warszawa' LIMIT 10"))

print("Polish agencies in database:")
for row in result:
    print(f"  {row[0]} | {row[1]} | {row[2]}")

# Count total
count = db.execute(text("SELECT COUNT(*) FROM real_estate_agencies WHERE country_code = 'PL'"))
total = count.fetchone()[0]
print(f"\nTotal Polish agencies: {total}")

db.close()
