
# Fixed script to use GENERIC URLs where deep links fail
import sys
import unicodedata

# Add the project root to the python path
sys.path.append('/app')

from main import SessionLocal, JobAgency, University

def normalize_city_for_url(city):
    """Normalize city name for URLs"""
    # Handle German umlauts: München -> muenchen
    normalized = city.lower()
    replacements = {
        'ä': 'ae',
        'ö': 'oe',
        'ü': 'ue',
        'ß': 'ss'
    }
    for char, replacement in replacements.items():
        normalized = normalized.replace(char, replacement)
    
    # Remove other accents
    normalized = unicodedata.normalize('NFKD', normalized).encode('ASCII', 'ignore').decode('utf-8')
    return normalized

def add_austrian_job_agencies():
    """Add Austrian agencies for all cities in DB"""
    db = SessionLocal()
    
    try:
        # Get cities dynamically
        cities = db.query(University.city).filter(University.country == 'AT').distinct().all()
        unique_cities = sorted(list(set([city[0] for city in cities if city[0]])))
        
        print(f"🔍 Found {len(unique_cities)} cities in Austria")
        
        for city in unique_cities:
            url_city = normalize_city_for_url(city)
            
            # 1. Karriere.at (Deep link WORKS)
            karriere_url = f"https://www.karriere.at/jobs/{url_city}?keywords=student"
            
            # 2. Unijobs.at (Deep links FAIL 404 -> Use Homepage)
            unijobs_url = "https://www.unijobs.at"
            
            # 3. Hogastjob (Deep links FAIL 404 -> Use Homepage)
            hogast_url = "https://www.hogastjob.com"
            
            agencies = [
                {
                    'name': f'Karriere.at - {city}',
                    'city': city,
                    'country_code': 'AT',
                    'website_url': karriere_url,
                    'description': f'Leading job portal in {city}',
                    'specialization': 'student_jobs',
                },
                {
                    'name': f'Unijobs.at - {city}',
                    'city': city,
                    'country_code': 'AT',
                    'website_url': unijobs_url,
                    'description': f'University jobs in {city}',
                    'specialization': 'student_jobs',
                },
                {
                    'name': f'Hogastjob - {city}',
                    'city': city,
                    'country_code': 'AT',
                    'website_url': hogast_url,
                    'description': f'Tourism & Part-time jobs in {city}',
                    'specialization': 'student_jobs',
                }
            ]
            
            for data in agencies:
                # Update existing or create new
                existing = db.query(JobAgency).filter(
                    JobAgency.name == data['name'],
                    JobAgency.city == data['city']
                ).first()
                
                if existing:
                    print(f"🔄 Updating: {data['name']} URL")
                    existing.website_url = data['website_url']
                    existing.is_active = True
                else:
                    agency = JobAgency(**data)
                    agency.is_active = True
                    db.add(agency)
                    print(f"✅ Added: {data['name']}")
        
        db.commit()
        print("\n✅ Successfully updated Austrian job agencies with working URLs!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_austrian_job_agencies()
