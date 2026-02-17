-- Migration: Fix Constraints and Triggers for Marketplace Tables
-- Version: 008b
-- Date: 2024-12-23
-- Description: Fixes constraint syntax and creates missing trigger functions

-- ============================================
-- 1. CREATE MISSING TRIGGER FUNCTION
-- ============================================

-- This function should already exist from migration 001, but we'll create it if missing
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- ============================================
-- 2. FIX CONSTRAINTS (PostgreSQL doesn't support IF NOT EXISTS for constraints)
-- ============================================

-- Drop and recreate constraints for legal_cases
DO $$
BEGIN
    -- Try to drop if exists, ignore error if doesn't exist
    ALTER TABLE legal_cases DROP CONSTRAINT IF EXISTS chk_legal_cases_status;
    ALTER TABLE legal_cases DROP CONSTRAINT IF EXISTS chk_legal_cases_urgency;
EXCEPTION
    WHEN undefined_object THEN NULL;
END $$;

ALTER TABLE legal_cases ADD CONSTRAINT chk_legal_cases_status 
    CHECK (status IN ('open', 'assigned', 'in_progress', 'completed', 'cancelled'));

ALTER TABLE legal_cases ADD CONSTRAINT chk_legal_cases_urgency 
    CHECK (urgency IN ('low', 'normal', 'high', 'urgent'));


-- Drop and recreate constraints for orders
DO $$
BEGIN
    ALTER TABLE orders DROP CONSTRAINT IF EXISTS chk_orders_status;
    ALTER TABLE orders DROP CONSTRAINT IF EXISTS chk_orders_payment_status;
EXCEPTION
    WHEN undefined_object THEN NULL;
END $$;

ALTER TABLE orders ADD CONSTRAINT chk_orders_status 
    CHECK (status IN ('pending', 'accepted', 'in_progress', 'completed', 'cancelled'));

ALTER TABLE orders ADD CONSTRAINT chk_orders_payment_status 
    CHECK (payment_status IN ('pending', 'paid', 'refunded', 'cancelled'));


-- Drop and recreate constraints for transactions
DO $$
BEGIN
    ALTER TABLE transactions DROP CONSTRAINT IF EXISTS chk_transactions_status;
EXCEPTION
    WHEN undefined_object THEN NULL;
END $$;

ALTER TABLE transactions ADD CONSTRAINT chk_transactions_status 
    CHECK (status IN ('pending', 'completed', 'failed', 'refunded'));


-- ============================================
-- 3. CREATE TRIGGERS FOR UPDATED_AT
-- ============================================

-- Trigger for lawyers table
DROP TRIGGER IF EXISTS update_lawyers_updated_at ON lawyers;
CREATE TRIGGER update_lawyers_updated_at
    BEFORE UPDATE ON lawyers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for legal_cases table
DROP TRIGGER IF EXISTS update_legal_cases_updated_at ON legal_cases;
CREATE TRIGGER update_legal_cases_updated_at
    BEFORE UPDATE ON legal_cases
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for orders table
DROP TRIGGER IF EXISTS update_orders_updated_at ON orders;
CREATE TRIGGER update_orders_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for reviews table
DROP TRIGGER IF EXISTS update_reviews_updated_at ON reviews;
CREATE TRIGGER update_reviews_updated_at
    BEFORE UPDATE ON reviews
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for lawyer_availability table
DROP TRIGGER IF EXISTS update_lawyer_availability_updated_at ON lawyer_availability;
CREATE TRIGGER update_lawyer_availability_updated_at
    BEFORE UPDATE ON lawyer_availability
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for case_categories table
DROP TRIGGER IF EXISTS update_case_categories_updated_at ON case_categories;
CREATE TRIGGER update_case_categories_updated_at
    BEFORE UPDATE ON case_categories
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


-- ============================================
-- VERIFICATION
-- ============================================

-- Verify all constraints
SELECT 
    conname as constraint_name,
    conrelid::regclass as table_name,
    pg_get_constraintdef(oid) as constraint_definition
FROM pg_constraint
WHERE conrelid IN (
    'legal_cases'::regclass,
    'orders'::regclass,
    'transactions'::regclass
)
AND contype = 'c'  -- Check constraints
ORDER BY table_name, constraint_name;

-- Verify all triggers
SELECT 
    trigger_name,
    event_object_table,
    action_statement
FROM information_schema.triggers
WHERE event_object_schema = 'public'
AND event_object_table IN (
    'lawyers', 'legal_cases', 'orders', 'reviews',
    'lawyer_availability', 'case_categories'
)
ORDER BY event_object_table, trigger_name;
