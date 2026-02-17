#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get Polish cities with universities
"""

from main import SessionLocal
from models import EducationalInstitution

db = SessionLocal()

cities = db.query(EducationalInstitution.city).filter(
    EducationalInstitution.jurisdiction_code == 'PL'
).distinct().all()

polish_cities = sorted(set([city[0] for city in cities if city[0]]))

print(f'Polish cities with universities: {len(polish_cities)}')
for city in polish_cities:
    print(f'  - {city}')

db.close()
