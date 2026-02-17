from main import SessionLocal
from sqlalchemy import text

db = SessionLocal()

print("Fixing job agency URLs...")

# 1. Profesia
r1 = db.execute(text("UPDATE job_agencies SET website_url = 'https://www.profesia.sk' WHERE website_url LIKE '%profesia.sk%' AND website_url != 'https://www.profesia.sk'"))
print(f"Profesia: {r1.rowcount} updated")

# 2. StudentJob
r2 = db.execute(text("UPDATE job_agencies SET website_url = 'https://www.studentjob.sk' WHERE website_url LIKE '%studentjob.sk%' AND website_url != 'https://www.studentjob.sk'"))
print(f"StudentJob: {r2.rowcount} updated")

# 3. Brigada
r3 = db.execute(text("UPDATE job_agencies SET website_url = 'https://www.brigada.sk' WHERE website_url LIKE '%brigada.sk%' AND website_url != 'https://www.brigada.sk'"))
print(f"Brigada: {r3.rowcount} updated")

# 4. Kariera
r4 = db.execute(text("UPDATE job_agencies SET website_url = 'https://www.kariera.sk' WHERE (website_url LIKE '%kariera.sk%' OR website_url LIKE '%kariera.zoznam.sk%') AND website_url != 'https://www.kariera.sk'"))
print(f"Kariera: {r4.rowcount} updated")

# 5. Indeed
r5 = db.execute(text("UPDATE job_agencies SET website_url = 'https://sk.indeed.com' WHERE (website_url LIKE '%indeed.com%' OR website_url LIKE '%indeed.sk%') AND website_url != 'https://sk.indeed.com'"))
print(f"Indeed: {r5.rowcount} updated")

# 6. Manpower
r6 = db.execute(text("UPDATE job_agencies SET website_url = 'https://www.manpower.sk' WHERE website_url LIKE '%manpower.sk%' AND website_url != 'https://www.manpower.sk'"))
print(f"Manpower: {r6.rowcount} updated")

# 7. Grafton
r7 = db.execute(text("UPDATE job_agencies SET website_url = 'https://www.grafton.sk' WHERE website_url LIKE '%grafton.sk%' AND website_url != 'https://www.grafton.sk'"))
print(f"Grafton: {r7.rowcount} updated")

db.commit()
print("\nSUCCESS: All URLs fixed!")
db.close()
