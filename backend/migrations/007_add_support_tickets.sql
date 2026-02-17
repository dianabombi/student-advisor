-- Migration: Add support tickets table for AI Help Desk
-- Date: 2025-12-14

CREATE TABLE IF NOT EXISTS support_tickets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    issue_description TEXT NOT NULL,
    ai_response TEXT,
    logs_analyzed INTEGER DEFAULT 0,
    errors_found INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'ai_resolved',
    needs_human BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

CREATE INDEX idx_support_user_id ON support_tickets(user_id);
CREATE INDEX idx_support_status ON support_tickets(status);
CREATE INDEX idx_support_created ON support_tickets(created_at DESC);

-- Add comments
COMMENT ON TABLE support_tickets IS 'AI Help Desk support tickets';
COMMENT ON COLUMN support_tickets.status IS 'ai_resolved, escalated, closed';
COMMENT ON COLUMN support_tickets.needs_human IS 'True if AI detected complex issue requiring human operator';
