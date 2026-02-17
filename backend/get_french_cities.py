
import sys
# Add the project root to the python path
sys.path.append('/app')

from main import SessionLocal, University

def get_french_cities():
    db = SessionLocal()
    try:
        # Get all distinct cities for France (FR)
        cities = db.query(University.city).filter(University.country == 'FR').distinct().all()
        unique_cities = sorted(list(set([city[0] for city in cities if city[0]])))
        
        print(f"Found {len(unique_cities)} cities in France:")
        for city in unique_cities:
            print(f"- {city}")
            
        return unique_cities
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        db.close()

if __name__ == "__main__":
    get_french_cities()
