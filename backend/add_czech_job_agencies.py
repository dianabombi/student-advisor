#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Додати чеські агенції з вакансіями для студентів

Міста: Praha, Brno, Olomouc
Портали: Jobs.cz, Prace.cz, Fajn-brigady.cz, JenPrace.cz
"""

import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency

def add_czech_job_agencies():
    """Додати чеські агенції"""
    db = SessionLocal()
    
    try:
        # Чеські міста
        cities = ['Praha', 'Brno', 'Olomouc']
        
        agencies_data = []
        
        for city in cities:
            # Jobs.cz
            agencies_data.append({
                'name': f'Jobs.cz - {city}',
                'city': city,
                'country_code': 'CZ',
                'website_url': 'https://www.jobs.cz',
                'description': f'Brigády v {city}',
                'specialization': 'student_jobs',
                'is_active': True
            })
            
            # Prace.cz
            agencies_data.append({
                'name': f'Prace.cz - {city}',
                'city': city,
                'country_code': 'CZ',
                'website_url': 'https://www.prace.cz',
                'description': f'Part-time {city}',
                'specialization': 'student_jobs',
                'is_active': True
            })
            
            # Fajn-brigady.cz
            agencies_data.append({
                'name': f'Fajn-brigády - {city}',
                'city': city,
                'country_code': 'CZ',
                'website_url': 'https://www.fajn-brigady.cz',
                'description': f'Brigády {city}',
                'specialization': 'student_jobs',
                'is_active': True
            })
            
            # JenPrace.cz
            agencies_data.append({
                'name': f'JenPráce - {city}',
                'city': city,
                'country_code': 'CZ',
                'website_url': 'https://www.jenprace.cz',
                'description': f'Práce {city}',
                'specialization': 'student_jobs',
                'is_active': True
            })
        
        # Додати в базу даних
        for data in agencies_data:
            # Перевірити, чи вже існує
            existing = db.query(JobAgency).filter(
                JobAgency.name == data['name'],
                JobAgency.city == data['city']
            ).first()
            
            if existing:
                print(f"⚠️ Вже існує: {data['name']}")
                continue
            
            agency = JobAgency(**data)
            db.add(agency)
            print(f"✅ Додано: {data['name']}")
        
        db.commit()
        print(f"\n✅ Успішно додано {len(agencies_data)} чеських агенцій!")
        print(f"Міста: {', '.join(cities)}")
        print(f"Портали: Jobs.cz, Prace.cz, Fajn-brigády.cz, JenPráce.cz")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Помилка: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_czech_job_agencies()
