"""
Add jurisdiction field to universities table
"""

from sqlalchemy import text
from backend.database import engine

def upgrade():
    with engine.connect() as conn:
        # Add jurisdiction column
        conn.execute(text("""
            ALTER TABLE universities 
            ADD COLUMN IF NOT EXISTS jurisdiction VARCHAR(10) DEFAULT 'sk';
        """))
        
        # Update all existing universities to 'sk' jurisdiction
        conn.execute(text("""
            UPDATE universities 
            SET jurisdiction = 'sk' 
            WHERE jurisdiction IS NULL;
        """))
        
        conn.commit()
        print("✅ Added jurisdiction field to universities table")

def downgrade():
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE universities DROP COLUMN IF EXISTS jurisdiction;"))
        conn.commit()
        print("✅ Removed jurisdiction field from universities table")

if __name__ == "__main__":
    print("Running migration: Add jurisdiction to universities")
    upgrade()
    print("Migration completed successfully!")
