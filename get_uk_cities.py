
import sys
# Add the project root to the python path
sys.path.append('/app')

from main import SessionLocal, University

def get_uk_cities():
    db = SessionLocal()
    try:
        # Get all distinct cities for UK (GB)
        # Check both GB and UK just in case, but stats said GB
        cities = db.query(University.city).filter(University.country.in_(['GB', 'UK'])).distinct().all()
        unique_cities = sorted(list(set([city[0] for city in cities if city[0]])))
        
        print(f"Found {len(unique_cities)} cities in UK/GB:")
        for city in unique_cities:
            print(f"- {city}")
            
        return unique_cities
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        db.close()

if __name__ == "__main__":
    get_uk_cities()
