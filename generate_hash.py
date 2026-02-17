import sys
sys.path.append('/app')

from api.auth import get_password_hash, verify_password

# Create hash for admin123
password = "admin123"
hashed = get_password_hash(password)

print(f"Password: {password}")
print(f"Hash: {hashed}")
print(f"Hash length: {len(hashed)}")

# Verify it works
if verify_password(password, hashed):
    print("✅ Verification successful!")
else:
    print("❌ Verification failed!")

# Print SQL update command
print("\n--- SQL UPDATE COMMAND ---")
print(f"UPDATE users SET hashed_password = '{hashed}' WHERE role = 'admin';")
