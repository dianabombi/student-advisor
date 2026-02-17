"""
Quick script to create YOUR admin account.
Edit the credentials below and run once.
"""

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# ============================================
# 🔐 YOUR ADMIN CREDENTIALS - EDIT THESE!
# ============================================
ADMIN_EMAIL = "valo-sro@centrum.sk"
ADMIN_NAME = "Eduard Pavlyshche"
ADMIN_PASSWORD = "1111111111"
# ============================================

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://codexuser:codexpass@localhost:5432/codexdb')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def main():
    print("=" * 50)
    print(f"Creating Super Admin: {ADMIN_EMAIL}")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        # Check if exists
        result = db.execute(
            text("SELECT id, role FROM users WHERE email = :email"),
            {"email": ADMIN_EMAIL}
        ).fetchone()
        
        if result:
            if result.role == 'admin':
                print(f"✅ {ADMIN_EMAIL} is already an admin!")
            else:
                db.execute(
                    text("UPDATE users SET role = 'admin' WHERE email = :email"),
                    {"email": ADMIN_EMAIL}
                )
                db.commit()
                print(f"✅ Upgraded {ADMIN_EMAIL} to ADMIN!")
        else:
            # Create new admin
            hashed = pwd_context.hash(ADMIN_PASSWORD)
            db.execute(
                text("""
                    INSERT INTO users (
                        name, email, hashed_password, role, is_active,
                        subscription_status, created_at,
                        consent_ai_tool, consent_no_advice, consent_no_attorney,
                        consent_timestamp, consent_terms_version
                    ) VALUES (
                        :name, :email, :password, 'admin', true,
                        'active', :created_at,
                        true, true, true,
                        :created_at, '1.0'
                    )
                """),
                {
                    "name": ADMIN_NAME,
                    "email": ADMIN_EMAIL,
                    "password": hashed,
                    "created_at": datetime.utcnow()
                }
            )
            db.commit()
            print(f"✅ Super Admin created!")
        
        print("\n🎉 Login at: http://localhost:3000/login")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Password: {ADMIN_PASSWORD}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
