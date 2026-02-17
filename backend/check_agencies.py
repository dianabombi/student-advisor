from main import SessionLocal
from sqlalchemy import text

db = SessionLocal()

# Check if job_agencies table exists and has data
result = db.execute(text("SELECT COUNT(*) as count FROM job_agencies"))
count = result.fetchone()[0]
print(f"Total job agencies in database: {count}")

if count > 0:
    # Show sample
    result = db.execute(text("SELECT name, city, website_url FROM job_agencies LIMIT 10"))
    print("\nSample agencies:")
    for row in result:
        print(f"  {row.city:20} | {row.name:30} | {row.website_url}")
else:
    print("\nNO JOB AGENCIES FOUND IN DATABASE!")
    print("You need to run: python backend/migrations/add_job_agencies.py")

db.close()
