"""Check and fix admin user role"""
import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/student_platform')
engine = create_engine(DATABASE_URL)

print("\nChecking admin users in database...\n")

with engine.connect() as conn:
    # Check all users with admin-like emails
    result = conn.execute(text("""
        SELECT id, name, email, role, is_active 
        FROM users 
        WHERE email LIKE '%admin%' OR role = 'admin'
        ORDER BY id
    """)).fetchall()
    
    if result:
        print("Found users:")
        for row in result:
            print(f"  ID: {row[0]}, Name: {row[1]}, Email: {row[2]}, Role: {row[3]}, Active: {row[4]}")
        
        # Ask which user to make admin
        print("\n" + "="*60)
        user_id = input("Enter user ID to set as admin (or press Enter to skip): ").strip()
        
        if user_id:
            conn.execute(
                text("UPDATE users SET role = 'admin', is_active = true WHERE id = :id"),
                {'id': int(user_id)}
            )
            conn.commit()
            print(f"\n[OK] User ID {user_id} is now admin!")
            
            # Show updated info
            updated = conn.execute(
                text("SELECT id, name, email, role FROM users WHERE id = :id"),
                {'id': int(user_id)}
            ).fetchone()
            print(f"\nUpdated user:")
            print(f"  ID: {updated[0]}")
            print(f"  Name: {updated[1]}")
            print(f"  Email: {updated[2]}")
            print(f"  Role: {updated[3]}")
            print(f"\nLogin with: {updated[2]}")
            print(f"Use your current password")
            print(f"Go to: http://localhost:3000/auth/login")
    else:
        print("[ERROR] No admin users found in database!")
        print("\nPlease create a regular user first, then run this script to promote them to admin.")
