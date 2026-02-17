-- Migration: Create cases table
-- Date: 2025-12-05
-- Description: Create cases table with UUID, status enum, and proper indexes

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create status enum type
CREATE TYPE case_status AS ENUM (
    'draft',
    'submitted',
    'under_review',
    'hearing_scheduled',
    'resolved',
    'cancelled'
);

-- Create cases table
CREATE TABLE cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status case_status DEFAULT 'draft' NOT NULL,
    assigned_to INTEGER REFERENCES users(id) ON DELETE SET NULL,
    deadline TIMESTAMP,
    claim_amount DECIMAL(15, 2),  -- Сума претензії
    priority VARCHAR(20) DEFAULT 'medium',  -- low, medium, high, urgent
    client_name VARCHAR(255),
    client_email VARCHAR(255),
    client_phone VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Create indexes for fast filtering
CREATE INDEX idx_cases_user_id ON cases(user_id);
CREATE INDEX idx_cases_status ON cases(status);
CREATE INDEX idx_cases_assigned_to ON cases(assigned_to);
CREATE INDEX idx_cases_deadline ON cases(deadline);
CREATE INDEX idx_cases_created_at ON cases(created_at DESC);

-- Create trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION update_cases_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_cases_updated_at
    BEFORE UPDATE ON cases
    FOR EACH ROW
    EXECUTE FUNCTION update_cases_updated_at();

-- Add comments for documentation
COMMENT ON TABLE cases IS 'Legal cases managed in the system';
COMMENT ON COLUMN cases.id IS 'Unique case identifier (UUID)';
COMMENT ON COLUMN cases.user_id IS 'Case owner (client)';
COMMENT ON COLUMN cases.assigned_to IS 'Assigned lawyer';
COMMENT ON COLUMN cases.status IS 'Current case status';
COMMENT ON COLUMN cases.deadline IS 'Case deadline';
COMMENT ON COLUMN cases.claim_amount IS 'Claim amount in EUR';
