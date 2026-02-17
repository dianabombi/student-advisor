"""Check what backend returns for Eduard's user"""
import requests

# First, check database
print("="*60)
print("DATABASE CHECK:")
print("="*60)

import os
from sqlalchemy import create_engine, text

DATABASE_URL = 'postgresql://user:password@localhost:5434/codex_db'
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(
        text("SELECT id, name, email, role, is_active FROM users WHERE email = 'Eduard.pavlyshche@gmail.com'")
    ).fetchone()
    
    if result:
        print(f"User found in database:")
        print(f"  ID: {result[0]}")
        print(f"  Name: {result[1]}")
        print(f"  Email: {result[2]}")
        print(f"  Role: {result[3]}")  # <-- This should be 'admin'
        print(f"  Active: {result[4]}")
    else:
        print("User NOT found in database!")

print("\n" + "="*60)
print("BACKEND API CHECK:")
print("="*60)
print("\nTo test login API, you need to:")
print("1. Go to http://localhost:3000/auth/login")
print("2. Open DevTools (F12 or Ctrl+Shift+I)")
print("3. Go to Network tab")
print("4. Login with Eduard.pavlyshche@gmail.com")
print("5. Find the 'login' request")
print("6. Click on it and check the Response")
print("7. Look for 'user' -> 'role' field")
print("\nIt should show: role: 'admin'")
print("If it shows role: 'user' or something else, that's the problem!")
