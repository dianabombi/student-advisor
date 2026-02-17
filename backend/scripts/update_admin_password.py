"""Check and fix admin password hash"""
import os
from sqlalchemy import create_engine, text
import bcrypt

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://codexuser:codexpass@db:5432/codexdb')
engine = create_engine(DATABASE_URL)

# First, check current hash format
with engine.connect() as conn:
    result = conn.execute(text("SELECT hashed_password FROM users WHERE email = 'valo-sro@centrum.sk'")).fetchone()
    current_hash = result[0] if result else None
    print(f"Current hash: {current_hash}")
    print(f"Hash prefix: {current_hash[:10] if current_hash else 'None'}...")

# Create hash using bcrypt library (compatible with passlib)
password = "1111111111"
# Use $2b$ prefix which is compatible with passlib
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12, prefix=b'2b')).decode('utf-8')
print(f"\nNew hash: {hashed}")

# Update
with engine.connect() as conn:
    conn.execute(text("UPDATE users SET hashed_password = :pwd WHERE email = 'valo-sro@centrum.sk'"), {'pwd': hashed})
    conn.commit()
    print("\n✅ Password hash updated!")
    
# Verify
print("\n--- Verification ---")
with engine.connect() as conn:
    result = conn.execute(text("SELECT hashed_password FROM users WHERE email = 'valo-sro@centrum.sk'")).fetchone()
    stored = result[0].encode('utf-8')
    test = bcrypt.checkpw(password.encode('utf-8'), stored)
    print(f"Password verify: {test}")
