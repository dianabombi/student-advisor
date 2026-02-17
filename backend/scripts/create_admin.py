"""Create admin user with ALL required fields"""
import os
from sqlalchemy import create_engine, text
import bcrypt
from datetime import datetime

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

EMAIL = "admin@student.com"
PASSWORD = "Admin123!"
NAME = "Admin User"

hashed = bcrypt.hashpw(PASSWORD.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')

with engine.connect() as conn:
    # Insert with ALL consent fields
    conn.execute(text("""
        INSERT INTO users (
            name, email, hashed_password, role, is_active, created_at,
            consent_ai_tool, consent_no_advice, consent_no_attorney,
            consent_timestamp, consent_terms_version, consent_upl_version
        )
        VALUES (
            :name, :email, :pwd, 'admin', true, NOW(),
            true, true, true,
            NOW(), '1.0', '1.0'
        )
    """), {'name': NAME, 'email': EMAIL, 'pwd': hashed})
    conn.commit()
    print(f"✅ Created admin: {EMAIL}")
    
    # Verify
    result = conn.execute(text("SELECT id, email, role FROM users WHERE role = 'admin'")).fetchall()
    print(f"\nAll admins: {result}")
    print(f"\n📧 Email: {EMAIL}")
    print(f"🔐 Password: {PASSWORD}")
