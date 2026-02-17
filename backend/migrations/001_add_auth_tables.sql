-- Migration: Add Auth Module Tables and Extend User Model
-- Version: 001
-- Date: 2024-12-04
-- Description: Adds role-based access control, sessions, and cases tables

-- ============================================
-- 1. EXTEND USERS TABLE
-- ============================================

-- Add role and status columns
ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'user';
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT true;
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT false;

-- Add profile fields
ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS organization VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS bio TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(500);

-- Add token fields for verification and password reset
ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_token VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_token_expires TIMESTAMP;
ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS reset_token_expires TIMESTAMP;

-- Add updated_at timestamp
ALTER TABLE users ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_is_verified ON users(is_verified);
CREATE INDEX IF NOT EXISTS idx_users_verification_token ON users(verification_token);
CREATE INDEX IF NOT EXISTS idx_users_reset_token ON users(reset_token);

-- Add check constraint for role
ALTER TABLE users ADD CONSTRAINT IF NOT EXISTS chk_users_role 
    CHECK (role IN ('user', 'admin', 'partner_lawyer'));

COMMENT ON COLUMN users.role IS 'User role: user, admin, or partner_lawyer';
COMMENT ON COLUMN users.is_active IS 'Whether user account is active';
COMMENT ON COLUMN users.is_verified IS 'Whether email is verified';


-- ============================================
-- 2. CREATE SESSIONS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires TIMESTAMP NOT NULL,
    
    -- Refresh token support
    refresh_token VARCHAR(255) UNIQUE,
    refresh_token_expires TIMESTAMP,
    
    -- Session metadata
    ip_address VARCHAR(45),  -- IPv6 support
    user_agent TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for sessions
CREATE INDEX IF NOT EXISTS idx_sessions_session_token ON sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expires);
CREATE INDEX IF NOT EXISTS idx_sessions_refresh_token ON sessions(refresh_token);

COMMENT ON TABLE sessions IS 'User sessions for NextAuth and session management';
COMMENT ON COLUMN sessions.session_token IS 'Unique session token';
COMMENT ON COLUMN sessions.refresh_token IS 'Refresh token for extending sessions';


-- ============================================
-- 3. CREATE CASES TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS cases (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Case information
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'draft',
    case_type VARCHAR(100),
    
    -- Draft data (JSON)
    draft_data JSONB,
    
    -- Case metadata
    reference_number VARCHAR(100),
    court VARCHAR(255),
    case_date TIMESTAMP,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP
);

-- Indexes for cases
CREATE INDEX IF NOT EXISTS idx_cases_user_id ON cases(user_id);
CREATE INDEX IF NOT EXISTS idx_cases_status ON cases(status);
CREATE INDEX IF NOT EXISTS idx_cases_case_type ON cases(case_type);
CREATE INDEX IF NOT EXISTS idx_cases_created_at ON cases(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_cases_reference_number ON cases(reference_number);

-- Add check constraint for status
ALTER TABLE cases ADD CONSTRAINT IF NOT EXISTS chk_cases_status 
    CHECK (status IN ('draft', 'active', 'closed', 'archived'));

COMMENT ON TABLE cases IS 'Legal cases/matters managed by users';
COMMENT ON COLUMN cases.status IS 'Case status: draft, active, closed, or archived';
COMMENT ON COLUMN cases.draft_data IS 'JSON data for work-in-progress cases';


-- ============================================
-- 4. CREATE TRIGGERS FOR UPDATED_AT
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for users table
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for sessions table
DROP TRIGGER IF EXISTS update_sessions_updated_at ON sessions;
CREATE TRIGGER update_sessions_updated_at
    BEFORE UPDATE ON sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for cases table
DROP TRIGGER IF EXISTS update_cases_updated_at ON cases;
CREATE TRIGGER update_cases_updated_at
    BEFORE UPDATE ON cases
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================
-- 5. SEED DATA (OPTIONAL)
-- ============================================

-- Update existing users to have default role
UPDATE users SET role = 'user' WHERE role IS NULL;
UPDATE users SET is_active = true WHERE is_active IS NULL;
UPDATE users SET is_verified = false WHERE is_verified IS NULL;

-- Create default admin user (CHANGE PASSWORD IN PRODUCTION!)
-- Password: admin123 (hashed with bcrypt)
INSERT INTO users (name, email, hashed_password, role, is_active, is_verified, created_at)
VALUES (
    'Admin User',
    'admin@codex.local',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5aeE7Ys5CJR6.',
    'admin',
    true,
    true,
    CURRENT_TIMESTAMP
)
ON CONFLICT (email) DO NOTHING;


-- ============================================
-- 6. GRANT PERMISSIONS (if needed)
-- ============================================

-- GRANT SELECT, INSERT, UPDATE, DELETE ON sessions TO your_app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON cases TO your_app_user;
-- GRANT USAGE, SELECT ON SEQUENCE sessions_id_seq TO your_app_user;
-- GRANT USAGE, SELECT ON SEQUENCE cases_id_seq TO your_app_user;


-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Verify users table columns
SELECT column_name, data_type, column_default, is_nullable
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;

-- Verify sessions table exists
SELECT table_name FROM information_schema.tables WHERE table_name = 'sessions';

-- Verify cases table exists
SELECT table_name FROM information_schema.tables WHERE table_name = 'cases';

-- Count users by role
SELECT role, COUNT(*) as count FROM users GROUP BY role;
