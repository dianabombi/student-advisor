"""
Add My Universities tables - Favorites and Notes
"""

from sqlalchemy import text
from backend.database import engine

def upgrade():
    with engine.connect() as conn:
        # Create user_universities table (Favorites)
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS user_universities (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                university_id INTEGER NOT NULL REFERENCES universities(id) ON DELETE CASCADE,
                added_at TIMESTAMP DEFAULT NOW(),
                is_favorite BOOLEAN DEFAULT TRUE,
                UNIQUE(user_id, university_id)
            );
        """))
        
        # Create university_notes table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS university_notes (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                university_id INTEGER NOT NULL REFERENCES universities(id) ON DELETE CASCADE,
                note_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """))
        
        # Create indexes for better performance
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_user_universities_user_id 
            ON user_universities(user_id);
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_university_notes_user_id 
            ON university_notes(user_id);
        """))
        
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_university_notes_university_id 
            ON university_notes(university_id);
        """))
        
        conn.commit()
        print("✅ Created user_universities and university_notes tables")

def downgrade():
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS university_notes CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS user_universities CASCADE;"))
        conn.commit()
        print("✅ Dropped user_universities and university_notes tables")

if __name__ == "__main__":
    print("Running migration: Add My Universities tables")
    upgrade()
    print("Migration completed successfully!")
