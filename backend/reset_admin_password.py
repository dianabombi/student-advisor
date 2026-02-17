import sys
sys.path.append('/app')

from passlib.context import CryptContext
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database connection
DATABASE_URL = "postgresql://user:password@db:5432/codex_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def reset_admin_password(email: str, new_password: str):
    """Reset admin password"""
    db = SessionLocal()
    try:
        # Hash the new password
        hashed_password = pwd_context.hash(new_password)
        
        # Update password in database
        query = text("""
            UPDATE users 
            SET hashed_password = :hashed_password 
            WHERE email = :email AND role = 'admin'
        """)
        
        result = db.execute(query, {
            "hashed_password": hashed_password,
            "email": email
        })
        db.commit()
        
        if result.rowcount > 0:
            print(f"✅ Password reset successfully for {email}")
            print(f"New password: {new_password}")
        else:
            print(f"❌ Admin user not found: {email}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Reset password for both admins
    reset_admin_password("valo-sro@centrum.sk", "admin123")
    reset_admin_password("Eduard.pavlyshche@gmail.com", "admin123")
