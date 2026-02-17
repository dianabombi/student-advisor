#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Додати польські агенції з вакансіями для студентів

Міста: Gdańsk, Kraków, Poznań, Warszawa, Wrocław
Портали: Pracuj.pl, OLX.pl
"""

import sys
import unicodedata

# Add the project root to the python path
sys.path.append('/app')


from main import SessionLocal, JobAgency, University

def get_polish_cities_from_db(db):
    """Get all unique cities in Poland from University table"""
    cities = db.query(University.city).filter(University.country == 'PL').distinct().all()
    # Handle tuple result and remove None/Empty
    unique_cities = sorted(list(set([city[0] for city in cities if city[0]])))
    return unique_cities

def normalize_city_for_url(city):
    """Normalize city name for URLs (remove accents, lowercase)"""
    # Normalize unicode characters to closest ASCII
    normalized = unicodedata.normalize('NFKD', city).encode('ASCII', 'ignore').decode('utf-8')
    return normalized.lower()

def add_polish_job_agencies():
    """Додати польські агенції для всіх міст в БД"""
    db = SessionLocal()
    
    try:
        # Отримати міста з БД динамічно
        cities = get_polish_cities_from_db(db)
        print(f"🔍 Знайдено міст у Польщі: {len(cities)}")
        print(f"Список: {', '.join(cities)}")
        
        if not cities:
            print("❌ Не знайдено університетів у Польщі. Додайте спочатку університети.")
            return

        agencies_data = []
        
        for city in cities:
            url_city = normalize_city_for_url(city)
            
            # Pracuj.pl
            # Pattern: https://www.pracuj.pl/praca/[city];wp
            # or https://www.pracuj.pl/praca/[city]
            agencies_data.append({
                'name': f'Pracuj.pl - {city}',
                'city': city,
                'country_code': 'PL',
                'website_url': f'https://www.pracuj.pl/praca/{url_city};wp',
                'description': f'Oferty pracy w {city}',
                'specialization': 'student_jobs',
                'is_active': True
            })
            
            # OLX.pl
            # Pattern: https://www.olx.pl/praca/[city]/
            agencies_data.append({
                'name': f'OLX.pl - {city}',
                'city': city,
                'country_code': 'PL',
                'website_url': f'https://www.olx.pl/praca/{url_city}/',
                'description': f'Praca dorywcza {city}',
                'specialization': 'student_jobs',
                'is_active': True
            })
            
            # Jooble (optional, good aggregator)
            # Pattern: https://pl.jooble.org/praca-student/{city}
            agencies_data.append({
                'name': f'Jooble - {city}',
                'city': city,
                'country_code': 'PL',
                'website_url': f'https://pl.jooble.org/praca-student/{url_city}',
                'description': f'Praca dla studenta w {city}',
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
        print(f"\n✅ Успішно додано {len(agencies_data)} польських агенцій!")
        print(f"Міста: {', '.join(cities)}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Помилка: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_polish_job_agencies()
