#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Деактивація непрацюючої агенції StudentJob.sk
"""

import sys
sys.path.append('/app')

from main import SessionLocal, JobAgency

def deactivate_studentjob():
    """Деактивувати StudentJob.sk"""
    db = SessionLocal()
    
    try:
        # Знайти всі записи StudentJob
        agencies = db.query(JobAgency).filter(
            JobAgency.name.like('%StudentJob%')
        ).all()
        
        if not agencies:
            print("⚠️ Агенції StudentJob не знайдено")
            return
        
        # Деактивувати
        for agency in agencies:
            agency.is_active = False
            print(f"❌ Деактивовано: {agency.name} - {agency.city}")
        
        db.commit()
        print(f"\n✅ Деактивовано {len(agencies)} записів StudentJob.sk")
        print("Причина: Сайт https://www.studentjob.sk недоступний (ERR_CONNECTION_REFUSED)")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Помилка: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    deactivate_studentjob()
