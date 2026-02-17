#!/usr/bin/env python3
import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency

db = SessionLocal()
total = db.query(JobAgency).count()
countries = db.query(JobAgency.country_code).distinct().all()

print(f'Total agencies: {total}')
print(f'Countries: {len(countries)}')

for c in sorted([x[0] for x in countries]):
    count = db.query(JobAgency).filter(JobAgency.country_code == c).count()
    print(f'  {c}: {count}')

db.close()
