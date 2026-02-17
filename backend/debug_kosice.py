from main import SessionLocal, JobAgency
from sqlalchemy import text

db = SessionLocal()

# Check agencies in Košice
print("Checking agencies in Košice...")
agencies = db.query(JobAgency).filter(JobAgency.city == 'Košice').all()

print(f"\nFound {len(agencies)} agencies in Košice:")
for agency in agencies:
    print(f"  - {agency.name}: {agency.website_url}")

# Check all cities
print("\n" + "="*60)
print("All cities in database:")
result = db.execute(text("SELECT DISTINCT city FROM job_agencies ORDER BY city"))
for row in result:
    count = db.query(JobAgency).filter(JobAgency.city == row.city).count()
    print(f"  {row.city}: {count} agencies")

db.close()
