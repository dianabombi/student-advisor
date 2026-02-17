"""Change password for Eduard"""
import os
from sqlalchemy import create_engine, text
from passlib.context import CryptContext

DATABASE_URL = 'postgresql://user:password@localhost:5434/codex_db'
engine = create_engine(DATABASE_URL)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash new password
new_password = '1111111111'
hashed = pwd_context.hash(new_password)

print("Updating password...")

with engine.connect() as conn:
    conn.execute(
        text("UPDATE users SET hashed_password = :hashed WHERE email = :email"),
        {'hashed': hashed, 'email': 'Eduard.pavlyshche@gmail.com'}
    )
    conn.commit()
    
    # Verify
    result = conn.execute(
        text("SELECT email, role FROM users WHERE email = :email"),
        {'email': 'Eduard.pavlyshche@gmail.com'}
    ).fetchone()
    
    print(f"✅ Password updated for: {result[0]}")
    print(f"   Role: {result[1]}")
