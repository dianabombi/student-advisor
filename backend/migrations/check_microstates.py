#!/usr/bin/env python3
import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency, University, Jurisdiction

db = SessionLocal()

# Check Liechtenstein
j = db.query(Jurisdiction).filter(Jurisdiction.code == 'LI').first()
print(f'Liechtenstein jurisdiction: {j.code if j else "NOT FOUND"}')

if j:
    agencies = db.query(JobAgency).filter(JobAgency.country_code == 'LI').count()
    print(f'Job agencies: {agencies}')
    
    cities = db.query(University.city).filter(University.jurisdiction_id == j.id).distinct().all()
    print(f'Cities with universities: {[c[0] for c in cities]}')
else:
    print('Liechtenstein jurisdiction not found in database')

# Check other micro-states
for code in ['VA', 'SM', 'MC', 'AD']:
    j = db.query(Jurisdiction).filter(Jurisdiction.code == code).first()
    if j:
        agencies = db.query(JobAgency).filter(JobAgency.country_code == code).count()
        print(f'{code}: {agencies} agencies')

db.close()
