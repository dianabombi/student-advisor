from main import SessionLocal
from sqlalchemy import text

db = SessionLocal()

# Update all job agencies to set is_active = True
result = db.execute(text("""
    UPDATE job_agencies 
    SET is_active = TRUE
    WHERE is_active IS NULL OR is_active = FALSE
"""))

print(f"Updated {result.rowcount} job agencies to is_active=TRUE")

db.commit()
db.close()

print("SUCCESS: All job agencies are now active!")
