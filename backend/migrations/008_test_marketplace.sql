-- ============================================
-- MARKETPLACE TABLES VERIFICATION SCRIPT
-- PostgreSQL Version
-- ============================================

\echo '=========================================='
\echo 'TEST 1: Checking all tables exist'
\echo '=========================================='

SELECT 
    table_name,
    table_type
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN (
    'lawyers',
    'legal_cases', 
    'orders',
    'reviews',
    'transactions',
    'messages',
    'lawyer_availability',
    'notifications',
    'lawyer_activity_log',
    'case_categories'
)
ORDER BY table_name;

-- Expected result: 10 tables listed

\echo ''
\echo '=========================================='
\echo 'TEST 2: Checking indexes on lawyers table'
\echo '=========================================='

SELECT 
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'lawyers'
  AND schemaname = 'public'
ORDER BY indexname;

-- Expected: Multiple indexes including idx_lawyers_average_rating, idx_lawyers_specializations, etc.

\echo ''
\echo '=========================================='
\echo 'TEST 3: Checking all indexes count'
\echo '=========================================='

SELECT 
    tablename,
    COUNT(*) as index_count
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename IN (
    'lawyers',
    'legal_cases', 
    'orders',
    'reviews',
    'transactions',
    'messages',
    'lawyer_availability',
    'notifications',
    'lawyer_activity_log',
    'case_categories'
)
GROUP BY tablename
ORDER BY tablename;

\echo ''
\echo '=========================================='
\echo 'TEST 4: Checking constraints'
\echo '=========================================='

SELECT 
    conname as constraint_name,
    conrelid::regclass as table_name,
    contype as constraint_type,
    pg_get_constraintdef(oid) as constraint_definition
FROM pg_constraint
WHERE conrelid::regclass::text IN (
    'lawyers',
    'legal_cases', 
    'orders',
    'reviews',
    'transactions'
)
AND contype = 'c'  -- Check constraints
ORDER BY table_name, constraint_name;

\echo ''
\echo '=========================================='
\echo 'TEST 5: Checking triggers'
\echo '=========================================='

SELECT 
    trigger_name,
    event_object_table as table_name,
    action_timing,
    event_manipulation,
    action_statement
FROM information_schema.triggers
WHERE event_object_schema = 'public'
  AND event_object_table IN (
    'lawyers',
    'legal_cases', 
    'orders',
    'reviews',
    'lawyer_availability',
    'case_categories'
)
ORDER BY table_name, trigger_name;

\echo ''
\echo '=========================================='
\echo 'TEST 6: Checking views'
\echo '=========================================='

SELECT 
    table_name as view_name,
    view_definition
FROM information_schema.views
WHERE table_schema = 'public'
  AND table_name IN ('marketplace_orders', 'active_lawyers');

\echo ''
\echo '=========================================='
\echo 'TEST 7: Checking case categories seed data'
\echo '=========================================='

SELECT 
    id,
    name_key,
    icon,
    color,
    sort_order,
    is_active
FROM case_categories
ORDER BY sort_order;

-- Expected: 10 categories

\echo ''
\echo '=========================================='
\echo 'TEST 8: Creating test lawyer'
\echo '=========================================='

-- First, check if we have a user with id=1
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM users WHERE id = 1) THEN
        RAISE NOTICE 'Creating test user with id=1';
        INSERT INTO users (id, name, email, hashed_password, role, is_active, is_verified)
        VALUES (1, 'Test User', 'test@codex.local', 'hashed_password', 'user', true, true)
        ON CONFLICT (id) DO NOTHING;
    END IF;
END $$;

-- Insert test lawyer
INSERT INTO lawyers (
    user_id, 
    full_name, 
    title, 
    license_number, 
    bar_association,
    specializations, 
    languages,
    experience_years,
    bio,
    average_rating,
    hourly_rate,
    consultation_fee,
    is_verified,
    is_active
) VALUES (
    1,
    'JUDr. Test Lawyer',
    'JUDr.',
    'SK-TEST-001',
    'Slovak Bar Association',
    '["civil_law", "consumer_protection"]'::jsonb,
    '["sk", "en"]'::jsonb,
    5,
    'Test bio for testing purposes',
    4.8,
    150.00,
    49.00,
    true,
    true
)
ON CONFLICT (license_number) DO UPDATE
SET full_name = EXCLUDED.full_name;

-- Verify insert
SELECT 
    id,
    full_name,
    title,
    license_number,
    specializations,
    languages,
    average_rating,
    is_verified
FROM lawyers 
WHERE license_number = 'SK-TEST-001';

\echo ''
\echo '=========================================='
\echo 'TEST 9: Creating test legal case'
\echo '=========================================='

-- Insert test legal case
INSERT INTO legal_cases (
    user_id,
    case_type,
    title,
    description,
    status,
    jurisdiction,
    urgency,
    required_specializations,
    preferred_languages
) VALUES (
    1,
    'civil_law',
    'Test Civil Law Case',
    'Testing case creation for marketplace',
    'open',
    'SK',
    'normal',
    '["civil_law"]'::jsonb,
    '["sk"]'::jsonb
)
RETURNING id, title, status, created_at;

-- Check latest case
SELECT 
    id,
    title,
    case_type,
    status,
    jurisdiction,
    created_at
FROM legal_cases 
ORDER BY id DESC 
LIMIT 1;

\echo ''
\echo '=========================================='
\echo 'TEST 10: Creating test order'
\echo '=========================================='

-- Get lawyer_id for test
DO $$
DECLARE
    v_lawyer_id INTEGER;
    v_case_id INTEGER;
BEGIN
    -- Get test lawyer id
    SELECT id INTO v_lawyer_id FROM lawyers WHERE license_number = 'SK-TEST-001' LIMIT 1;
    
    -- Get latest case id
    SELECT id INTO v_case_id FROM legal_cases ORDER BY id DESC LIMIT 1;
    
    IF v_lawyer_id IS NOT NULL AND v_case_id IS NOT NULL THEN
        -- Insert test order
        INSERT INTO orders (
            order_number,
            user_id,
            lawyer_id,
            case_id,
            service_type,
            description,
            amount,
            currency,
            status,
            payment_status
        ) VALUES (
            'ORD-TEST-' || TO_CHAR(NOW(), 'YYYYMMDD') || '-001',
            1,
            v_lawyer_id,
            v_case_id,
            'consultation',
            'Test consultation order',
            49.00,
            'EUR',
            'pending',
            'pending'
        )
        ON CONFLICT (order_number) DO NOTHING;
        
        RAISE NOTICE 'Test order created successfully';
    ELSE
        RAISE NOTICE 'Cannot create order: lawyer_id=%, case_id=%', v_lawyer_id, v_case_id;
    END IF;
END $$;

-- Verify order
SELECT 
    order_number,
    service_type,
    amount,
    currency,
    status,
    payment_status,
    created_at
FROM orders 
ORDER BY id DESC 
LIMIT 1;

\echo ''
\echo '=========================================='
\echo 'TEST 11: Testing marketplace_orders view'
\echo '=========================================='

SELECT 
    order_number,
    service_type,
    amount,
    status,
    user_name,
    lawyer_name,
    lawyer_title,
    case_title
FROM marketplace_orders
LIMIT 5;

\echo ''
\echo '=========================================='
\echo 'TEST 12: Testing active_lawyers view'
\echo '=========================================='

SELECT 
    full_name,
    title,
    license_number,
    average_rating,
    total_reviews,
    total_orders,
    completed_orders,
    is_verified
FROM active_lawyers
LIMIT 5;

\echo ''
\echo '=========================================='
\echo 'TEST 13: Creating test review'
\echo '=========================================='

DO $$
DECLARE
    v_lawyer_id INTEGER;
    v_order_id INTEGER;
BEGIN
    -- Get test lawyer and order ids
    SELECT id INTO v_lawyer_id FROM lawyers WHERE license_number = 'SK-TEST-001' LIMIT 1;
    SELECT id INTO v_order_id FROM orders ORDER BY id DESC LIMIT 1;
    
    IF v_lawyer_id IS NOT NULL THEN
        -- Insert test review
        INSERT INTO reviews (
            user_id,
            lawyer_id,
            order_id,
            rating,
            title,
            comment,
            professionalism_rating,
            communication_rating,
            expertise_rating,
            value_rating,
            is_verified,
            is_visible
        ) VALUES (
            1,
            v_lawyer_id,
            v_order_id,
            5,
            'Excellent Service',
            'Very professional and helpful lawyer. Highly recommended!',
            5,
            5,
            5,
            5,
            true,
            true
        );
        
        RAISE NOTICE 'Test review created successfully';
    END IF;
END $$;

-- Verify review and check if lawyer stats were updated by trigger
SELECT 
    r.rating,
    r.title,
    r.comment,
    l.average_rating as lawyer_avg_rating,
    l.total_reviews as lawyer_total_reviews
FROM reviews r
JOIN lawyers l ON r.lawyer_id = l.id
WHERE l.license_number = 'SK-TEST-001'
ORDER BY r.id DESC
LIMIT 1;

\echo ''
\echo '=========================================='
\echo 'TEST 14: Testing trigger - updated_at'
\echo '=========================================='

-- Update lawyer and check if updated_at changes
UPDATE lawyers 
SET bio = 'Updated bio for testing trigger'
WHERE license_number = 'SK-TEST-001';

SELECT 
    full_name,
    bio,
    created_at,
    updated_at,
    (updated_at > created_at) as trigger_worked
FROM lawyers
WHERE license_number = 'SK-TEST-001';

\echo ''
\echo '=========================================='
\echo 'TEST 15: Performance check - Query speed'
\echo '=========================================='

-- Test query performance
EXPLAIN ANALYZE
SELECT 
    l.full_name,
    l.average_rating,
    COUNT(o.id) as order_count
FROM lawyers l
LEFT JOIN orders o ON l.id = o.lawyer_id
WHERE l.is_active = true
  AND l.is_verified = true
GROUP BY l.id, l.full_name, l.average_rating
ORDER BY l.average_rating DESC
LIMIT 10;

\echo ''
\echo '=========================================='
\echo 'FINAL SUMMARY'
\echo '=========================================='

SELECT 
    'lawyers' as table_name,
    COUNT(*) as record_count
FROM lawyers
UNION ALL
SELECT 'legal_cases', COUNT(*) FROM legal_cases
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews
UNION ALL
SELECT 'transactions', COUNT(*) FROM transactions
UNION ALL
SELECT 'messages', COUNT(*) FROM messages
UNION ALL
SELECT 'lawyer_availability', COUNT(*) FROM lawyer_availability
UNION ALL
SELECT 'notifications', COUNT(*) FROM notifications
UNION ALL
SELECT 'lawyer_activity_log', COUNT(*) FROM lawyer_activity_log
UNION ALL
SELECT 'case_categories', COUNT(*) FROM case_categories
ORDER BY table_name;

\echo ''
\echo '=========================================='
\echo 'ALL TESTS COMPLETED!'
\echo '=========================================='
