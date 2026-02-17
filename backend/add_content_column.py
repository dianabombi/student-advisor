from main import engine
from sqlalchemy import text

print("Adding content column to documents table...")

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE documents ADD COLUMN IF NOT EXISTS content TEXT"))
    conn.commit()

print("✅ Column added successfully!")
