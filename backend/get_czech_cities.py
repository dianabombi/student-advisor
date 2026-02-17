#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Отримати список всіх міст з навчальними закладами в Чехії
"""

import sys
sys.path.append('/app')

from main import SessionLocal, University, Jurisdiction

def get_czech_cities():
    """Отримати всі міста з університетами в Чехії"""
    db = SessionLocal()
    
    try:
        # Знайти юрисдикцію Чехії
        cz_jurisdiction = db.query(Jurisdiction).filter(Jurisdiction.code == 'CZ').first()
        
        if not cz_jurisdiction:
            print("❌ Юрисдикція CZ не знайдена")
            return
        
        # Отримати всі університети в Чехії
        universities = db.query(University).filter(
            University.jurisdiction_id == cz_jurisdiction.id
        ).all()
        
        # Зібрати унікальні міста
        cities = set()
        for uni in universities:
            if uni.city:
                cities.add(uni.city)
        
        print(f"Всього міст з навчальними закладами в Чехії: {len(cities)}")
        print("\nСписок міст:")
        for city in sorted(cities):
            print(f"  - {city}")
        
        return sorted(cities)
        
    finally:
        db.close()

if __name__ == "__main__":
    get_czech_cities()
