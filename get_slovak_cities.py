#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Отримати список всіх міст з навчальними закладами в Словаччині
"""

import sys
sys.path.append('/app')

from main import SessionLocal, University, Jurisdiction

def get_slovak_cities():
    """Отримати всі міста з університетами в Словаччині"""
    db = SessionLocal()
    
    try:
        # Знайти юрисдикцію Словаччини
        sk_jurisdiction = db.query(Jurisdiction).filter(Jurisdiction.code == 'SK').first()
        
        if not sk_jurisdiction:
            print("❌ Юрисдикція SK не знайдена")
            return
        
        # Отримати всі університети в Словаччині
        universities = db.query(University).filter(
            University.jurisdiction_id == sk_jurisdiction.id
        ).all()
        
        # Зібрати унікальні міста
        cities = set()
        for uni in universities:
            if uni.city:
                cities.add(uni.city)
        
        print(f"Всього міст з навчальними закладами в Словаччині: {len(cities)}")
        print("\nСписок міст:")
        for city in sorted(cities):
            print(f"  - {city}")
        
        return sorted(cities)
        
    finally:
        db.close()

if __name__ == "__main__":
    get_slovak_cities()
