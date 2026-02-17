#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug why Polish agencies not found
"""

from main import SessionLocal, RealEstateAgency

db = SessionLocal()

print("=" * 70)
print("DEBUGGING POLISH AGENCIES")
print("=" * 70)

# Check what's in database
print("\n1. Direct SQL query:")
from sqlalchemy import text
result = db.execute(text("SELECT name, city, country_code FROM real_estate_agencies WHERE city = 'Warszawa' LIMIT 5"))
for row in result:
    print(f"   {row[0]} | {row[1]} | {row[2]}")

# Check with ORM - exact match
print("\n2. ORM exact match (city == 'Warszawa'):")
agencies = db.query(RealEstateAgency).filter(
    RealEstateAgency.city == 'Warszawa',
    RealEstateAgency.country_code == 'PL'
).all()
print(f"   Found: {len(agencies)}")

# Check with ORM - ilike (case-insensitive)
print("\n3. ORM ilike match (city.ilike('Warszawa')):")
agencies = db.query(RealEstateAgency).filter(
    RealEstateAgency.city.ilike('Warszawa'),
    RealEstateAgency.country_code == 'PL'
).all()
print(f"   Found: {len(agencies)}")

# Check with ORM - ilike + is_active
print("\n4. ORM ilike + is_active:")
agencies = db.query(RealEstateAgency).filter(
    RealEstateAgency.city.ilike('Warszawa'),
    RealEstateAgency.country_code == 'PL',
    RealEstateAgency.is_active == True
).all()
print(f"   Found: {len(agencies)}")
for agency in agencies:
    print(f"   - {agency.name} | is_active={agency.is_active}")

db.close()
