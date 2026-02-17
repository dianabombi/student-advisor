from main import SessionLocal, JobAgency

db = SessionLocal()

# Check agencies with is_active filter
print("Checking agencies in Košice with is_active=True:")
agencies_active = db.query(JobAgency).filter(
    JobAgency.city == 'Košice',
    JobAgency.is_active == True
).all()

print(f"Found {len(agencies_active)} ACTIVE agencies")

# Check without filter
print("\nChecking agencies in Košice WITHOUT is_active filter:")
agencies_all = db.query(JobAgency).filter(
    JobAgency.city == 'Košice'
).all()

print(f"Found {len(agencies_all)} TOTAL agencies")

if agencies_all:
    print("\nAgency details:")
    for agency in agencies_all:
        print(f"  - {agency.name}")
        print(f"    is_active: {agency.is_active}")
        print(f"    URL: {agency.website_url}")

db.close()
