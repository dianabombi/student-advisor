# Database Migrations

## Overview

This directory contains SQL migration scripts for the CODEX database schema.

## Migration Files

### 001_add_auth_tables.sql

**Date:** 2024-12-04  
**Description:** Adds authentication and authorization tables

**Changes:**

1. **Extended `users` table:**
   - Added `role` column (user, admin, partner_lawyer)
   - Added `is_active` and `is_verified` status fields
   - Added profile fields (phone, organization, bio, avatar_url)
   - Added verification and password reset token fields
   - Added `updated_at` timestamp
   - Created indexes for performance
   - Added constraints for data integrity

2. **Created `sessions` table:**
   - Stores user sessions for NextAuth
   - Supports refresh tokens
   - Tracks IP address and user agent
   - Automatic cleanup of expired sessions

3. **Created `cases` table:**
   - Legal cases/matters for users
   - Supports draft data in JSON format
   - Status tracking (draft, active, closed, archived)
   - Reference numbers and court information

4. **Added triggers:**
   - Automatic `updated_at` timestamp updates
   - For users, sessions, and cases tables

## Running Migrations

### Using Docker

```bash
# Copy migration file to container
docker cp migrations/001_add_auth_tables.sql codex-db:/tmp/

# Execute migration
docker exec -it codex-db psql -U postgres -d codex_db -f /tmp/001_add_auth_tables.sql
```

### Using psql Directly

```bash
psql -U postgres -d codex_db -f migrations/001_add_auth_tables.sql
```

### From Python (Alembic)

```bash
# Generate Alembic migration from models
alembic revision --autogenerate -m "Add auth tables"

# Apply migration
alembic upgrade head
```

## Verification

After running migration, verify tables:

```sql
-- Check users table structure
\d users

-- Check new tables
\d sessions
\d cases

-- Verify data
SELECT role, COUNT(*) FROM users GROUP BY role;
SELECT COUNT(*) FROM sessions;
SELECT COUNT(*) FROM cases;
```

## Rollback

To rollback this migration:

```sql
-- Remove triggers
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
DROP TRIGGER IF EXISTS update_sessions_updated_at ON sessions;
DROP TRIGGER IF EXISTS update_cases_updated_at ON cases;

-- Drop tables
DROP TABLE IF EXISTS cases CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;

-- Remove columns from users (be careful!)
ALTER TABLE users DROP COLUMN IF EXISTS role;
ALTER TABLE users DROP COLUMN IF EXISTS is_active;
ALTER TABLE users DROP COLUMN IF EXISTS is_verified;
-- ... etc
```

**⚠️ Warning:** Rollback will delete all session and case data!

## Migration Checklist

Before running migration:
- [ ] Backup database
- [ ] Test on development/staging first
- [ ] Review migration script
- [ ] Check for conflicts

After running migration:
- [ ] Verify table structure
- [ ] Check indexes created
- [ ] Test constraints
- [ ] Update application code
- [ ] Test user registration/login
- [ ] Monitor for errors

## Notes

- Default admin user is created (email: `admin@codex.local`, password: `admin123`)
- **Change admin password in production!**
- All existing users will have role='user' by default
- Sessions table supports refresh tokens for long-lived sessions
- Cases table uses JSONB for flexible draft data storage

---

**Last Updated:** 2024-12-04  
**Schema Version:** 001
