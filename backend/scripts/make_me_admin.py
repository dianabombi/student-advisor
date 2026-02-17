"""Make Eduard.pavlyshche@gmail.com admin"""
import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/student_platform')
engine = create_engine(DATABASE_URL)

MY_EMAIL = "Eduard.pavlyshche@gmail.com"

print(f"\nMaking {MY_EMAIL} admin...\n")

with engine.connect() as conn:
    # Check if user exists
    user = conn.execute(
        text("SELECT id, name, email, role FROM users WHERE email = :email"),
        {'email': MY_EMAIL}
    ).fetchone()
    
    if not user:
        print(f"[ERROR] User with email {MY_EMAIL} not found!")
        print("Please register first at http://localhost:3000/auth/register")
    else:
        print(f"Found user:")
        print(f"  ID: {user[0]}")
        print(f"  Name: {user[1]}")
        print(f"  Email: {user[2]}")
        print(f"  Current Role: {user[3]}")
        
        # Update role to admin
        conn.execute(
            text("UPDATE users SET role = 'admin', is_active = true WHERE email = :email"),
            {'email': MY_EMAIL}
        )
        conn.commit()
        
        # Verify update
        updated = conn.execute(
            text("SELECT id, name, email, role FROM users WHERE email = :email"),
            {'email': MY_EMAIL}
        ).fetchone()
        
        print(f"\n[OK] User updated to admin!")
        print(f"  ID: {updated[0]}")
        print(f"  Name: {updated[1]}")
        print(f"  Email: {updated[2]}")
        print(f"  New Role: {updated[3]}")
        print(f"\n" + "="*60)
        print("NEXT STEPS:")
        print("1. Logout from platform (if logged in)")
        print("2. Go to: http://localhost:3000/auth/login")
        print(f"3. Login with: {MY_EMAIL}")
        print("4. You will be redirected to /admin/dashboard")
        print("="*60 + "\n")
