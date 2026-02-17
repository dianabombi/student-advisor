-- Migration: Create case_documents table
-- Date: 2025-12-05
-- Description: Link uploaded files (MinIO) with cases

CREATE TABLE case_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id UUID NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
    file_name VARCHAR(500) NOT NULL,
    file_key VARCHAR(1000) NOT NULL,  -- MinIO path/key
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    uploaded_by INTEGER REFERENCES users(id)
);

-- Create indexes
CREATE INDEX idx_case_documents_case_id ON case_documents(case_id);
CREATE INDEX idx_case_documents_uploaded_at ON case_documents(uploaded_at DESC);

-- Add comments
COMMENT ON TABLE case_documents IS 'Links uploaded files (MinIO) with cases';
COMMENT ON COLUMN case_documents.file_key IS 'MinIO object key/path';
