
from main import SessionLocal, University
from sqlalchemy import func

def get_stats():
    db = SessionLocal()
    try:
        results = db.query(University.country, func.count(University.id))\
                    .group_by(University.country)\
                    .order_by(func.count(University.id).desc())\
                    .all()
        
        print("\n📊 Universities by Country:")
        print("-" * 30)
        for country, count in results:
            print(f"{country}: {count}")
            
    finally:
        db.close()

if __name__ == "__main__":
    get_stats()
