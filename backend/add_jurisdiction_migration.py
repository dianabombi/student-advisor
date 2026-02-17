import sys
sys.path.append('/app')

from backend.database import engine
from sqlalchemy import text

print("Starting migration: Add jurisdiction to universities")

try:
    with engine.connect() as conn:
        # Add jurisdiction column
        print("Adding jurisdiction column...")
        conn.execute(text("""
            ALTER TABLE universities 
            ADD COLUMN IF NOT EXISTS jurisdiction VARCHAR(10) DEFAULT 'SK';
        """))
        
        # Update all existing universities to 'SK' jurisdiction
        print("Setting all existing universities to SK jurisdiction...")
        result = conn.execute(text("""
            UPDATE universities 
            SET jurisdiction = 'SK' 
            WHERE jurisdiction IS NULL OR jurisdiction = '';
        """))
        
        conn.commit()
        print(f"✅ Migration completed! Updated {result.rowcount} universities")
        
except Exception as e:
    print(f"❌ Migration failed: {e}")
    sys.exit(1)
