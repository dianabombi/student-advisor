-- Migration: Add jurisdictions support to lawyers table
-- Date: 2025-12-24
-- Purpose: Add multi-jurisdiction support for marketplace lawyers

-- Add jurisdictions column to lawyers table
ALTER TABLE lawyers 
ADD COLUMN IF NOT EXISTS jurisdictions JSONB DEFAULT '["SK"]'::jsonb;

-- Create index for jurisdiction filtering (GIN index for JSONB)
CREATE INDEX IF NOT EXISTS idx_lawyers_jurisdictions 
ON lawyers USING GIN (jurisdictions);

-- Update existing lawyers to have SK jurisdiction by default
UPDATE lawyers 
SET jurisdictions = '["SK"]'::jsonb 
WHERE jurisdictions IS NULL OR jurisdictions = '[]'::jsonb;

-- Add comment for documentation
COMMENT ON COLUMN lawyers.jurisdictions IS 'Array of jurisdiction codes where lawyer is licensed (e.g., ["SK", "CZ", "PL"])';

-- Verify migration
SELECT 
    id,
    full_name,
    license_number,
    jurisdictions,
    is_verified
FROM lawyers
LIMIT 5;
