#!/usr/bin/env python3
import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency

db = SessionLocal()

# Test the exact query from _get_agencies_context
city = "Bendern"
country_code = "LI"

agencies = db.query(JobAgency).filter(
    JobAgency.city.ilike(city),
    JobAgency.country_code == country_code,
    JobAgency.is_active == True
).all()

print(f"Query: city.ilike('{city}'), country_code=='{country_code}'")
print(f"Found {len(agencies)} agencies:")
for a in agencies:
    print(f"  - {a.name} (city: '{a.city}', country: '{a.country_code}')")

db.close()
