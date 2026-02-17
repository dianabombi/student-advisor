-- Migration 002: Case Management Module
-- Adds deadlines, assignments, comments, documents, and audit logging

-- ============================================
-- 1. EXTEND CASES TABLE
-- ============================================

ALTER TABLE cases ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent'));
ALTER TABLE cases ADD COLUMN IF NOT EXISTS deadline TIMESTAMP;
ALTER TABLE cases ADD COLUMN IF NOT EXISTS assigned_lawyer_id INTEGER REFERENCES users(id);
ALTER TABLE cases ADD COLUMN IF NOT EXISTS client_name VARCHAR(255);
ALTER TABLE cases ADD COLUMN IF NOT EXISTS client_email VARCHAR(255);
ALTER TABLE cases ADD COLUMN IF NOT EXISTS client_phone VARCHAR(50);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_cases_priority ON cases(priority);
CREATE INDEX IF NOT EXISTS idx_cases_deadline ON cases(deadline);
CREATE INDEX IF NOT EXISTS idx_cases_assigned_lawyer ON cases(assigned_lawyer_id);

-- ============================================
-- 2. CASE ASSIGNMENTS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS case_assignments (
    id SERIAL PRIMARY KEY,
    case_id INTEGER NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    lawyer_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_by INTEGER REFERENCES users(id),
    role VARCHAR(20) DEFAULT 'assistant' CHECK (role IN ('primary', 'assistant')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Prevent duplicate assignments
    UNIQUE(case_id, lawyer_id)
);

CREATE INDEX IF NOT EXISTS idx_assignments_case ON case_assignments(case_id);
CREATE INDEX IF NOT EXISTS idx_assignments_lawyer ON case_assignments(lawyer_id);
CREATE INDEX IF NOT EXISTS idx_assignments_role ON case_assignments(role);

COMMENT ON TABLE case_assignments IS 'Tracks lawyer assignments to cases';
COMMENT ON COLUMN case_assignments.role IS 'primary = main lawyer, assistant = supporting lawyer';

-- ============================================
-- 3. CASE COMMENTS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS case_comments (
    id SERIAL PRIMARY KEY,
    case_id INTEGER NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    comment TEXT NOT NULL,
    is_internal BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited BOOLEAN DEFAULT false
);

CREATE INDEX IF NOT EXISTS idx_comments_case ON case_comments(case_id);
CREATE INDEX IF NOT EXISTS idx_comments_user ON case_comments(user_id);
CREATE INDEX IF NOT EXISTS idx_comments_created ON case_comments(created_at DESC);

COMMENT ON TABLE case_comments IS 'Comments and notes on cases';
COMMENT ON COLUMN case_comments.is_internal IS 'Internal notes (not visible to client)';

-- Trigger to update updated_at
CREATE OR REPLACE FUNCTION update_comment_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    NEW.edited = true;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_comment_timestamp
    BEFORE UPDATE ON case_comments
    FOR EACH ROW
    EXECUTE FUNCTION update_comment_timestamp();

-- ============================================
-- 4. CASE DOCUMENTS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS case_documents (
    id SERIAL PRIMARY KEY,
    case_id INTEGER NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    attached_by INTEGER NOT NULL REFERENCES users(id),
    attached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    
    -- Prevent duplicate attachments
    UNIQUE(case_id, document_id)
);

CREATE INDEX IF NOT EXISTS idx_case_docs_case ON case_documents(case_id);
CREATE INDEX IF NOT EXISTS idx_case_docs_document ON case_documents(document_id);

COMMENT ON TABLE case_documents IS 'Links documents to cases';

-- ============================================
-- 5. CASE DEADLINES TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS case_deadlines (
    id SERIAL PRIMARY KEY,
    case_id INTEGER NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    deadline TIMESTAMP NOT NULL,
    reminder_24h_sent BOOLEAN DEFAULT false,
    reminder_1h_sent BOOLEAN DEFAULT false,
    completed BOOLEAN DEFAULT false,
    completed_at TIMESTAMP,
    created_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_deadlines_case ON case_deadlines(case_id);
CREATE INDEX IF NOT EXISTS idx_deadlines_deadline ON case_deadlines(deadline);
CREATE INDEX IF NOT EXISTS idx_deadlines_completed ON case_deadlines(completed);
CREATE INDEX IF NOT EXISTS idx_deadlines_reminders ON case_deadlines(reminder_24h_sent, reminder_1h_sent) WHERE NOT completed;

COMMENT ON TABLE case_deadlines IS 'Deadlines and reminders for cases';
COMMENT ON COLUMN case_deadlines.reminder_24h_sent IS 'Whether 24-hour reminder was sent';
COMMENT ON COLUMN case_deadlines.reminder_1h_sent IS 'Whether 1-hour reminder was sent';

-- ============================================
-- 6. CASE AUDIT LOG TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS case_audit_log (
    id SERIAL PRIMARY KEY,
    case_id INTEGER NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(50) NOT NULL,
    changes JSONB,
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_case ON case_audit_log(case_id);
CREATE INDEX IF NOT EXISTS idx_audit_user ON case_audit_log(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON case_audit_log(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_action ON case_audit_log(action);

COMMENT ON TABLE case_audit_log IS 'Audit trail for all case changes';
COMMENT ON COLUMN case_audit_log.action IS 'created, updated, assigned, commented, etc.';
COMMENT ON COLUMN case_audit_log.changes IS 'JSON of what changed';

-- ============================================
-- 7. NOTIFICATIONS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    link VARCHAR(500),
    read BOOLEAN DEFAULT false,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Metadata
    related_case_id INTEGER REFERENCES cases(id) ON DELETE CASCADE,
    related_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_read ON notifications(read);
CREATE INDEX IF NOT EXISTS idx_notifications_created ON notifications(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_notifications_type ON notifications(type);

COMMENT ON TABLE notifications IS 'In-app notifications for users';
COMMENT ON COLUMN notifications.type IS 'deadline_reminder, assignment, comment, status_change, etc.';

-- ============================================
-- 8. SEED DATA (OPTIONAL)
-- ============================================

-- Example: Update existing cases with default priority
UPDATE cases SET priority = 'medium' WHERE priority IS NULL;

-- ============================================
-- ROLLBACK INSTRUCTIONS
-- ============================================

/*
To rollback this migration:

DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS case_audit_log CASCADE;
DROP TABLE IF EXISTS case_deadlines CASCADE;
DROP TABLE IF EXISTS case_documents CASCADE;
DROP TABLE IF EXISTS case_comments CASCADE;
DROP TRIGGER IF EXISTS trigger_update_comment_timestamp ON case_comments;
DROP FUNCTION IF EXISTS update_comment_timestamp();
DROP TABLE IF EXISTS case_assignments CASCADE;

ALTER TABLE cases DROP COLUMN IF EXISTS priority;
ALTER TABLE cases DROP COLUMN IF EXISTS deadline;
ALTER TABLE cases DROP COLUMN IF EXISTS assigned_lawyer_id;
ALTER TABLE cases DROP COLUMN IF EXISTS client_name;
ALTER TABLE cases DROP COLUMN IF EXISTS client_email;
ALTER TABLE cases DROP COLUMN IF EXISTS client_phone;
*/

-- ============================================
-- VERIFICATION QUERIES
-- ============================================

/*
-- Check tables created
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'case_%' 
ORDER BY table_name;

-- Check cases table columns
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'cases'
ORDER BY ordinal_position;

-- Check indexes
SELECT tablename, indexname 
FROM pg_indexes 
WHERE tablename LIKE 'case_%' 
ORDER BY tablename, indexname;
*/
