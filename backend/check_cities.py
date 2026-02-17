#!/usr/bin/env python3
import sys
sys.path.append('/app')
from main import SessionLocal, University, Jurisdiction

db = SessionLocal()
for code in ['BE', 'CH', 'NL']:
    juris = db.query(Jurisdiction).filter(Jurisdiction.code == code).first()
    if juris:
        cities = db.query(University.city).filter(University.jurisdiction_id == juris.id).distinct().all()
        print(f'{code}: {sorted([c[0] for c in cities if c[0]])}')
db.close()
