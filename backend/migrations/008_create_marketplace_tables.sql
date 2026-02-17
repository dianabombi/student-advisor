-- Migration: Create Marketplace Tables
-- Version: 008
-- Date: 2024-12-23
-- Description: Adds marketplace functionality for lawyer services, orders, reviews, and transactions

-- ============================================
-- 1. CREATE LAWYERS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS lawyers (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Lawyer profile
    full_name VARCHAR(255) NOT NULL,
    title VARCHAR(100),  -- JUDr., Mgr., etc.
    license_number VARCHAR(100) UNIQUE NOT NULL,
    bar_association VARCHAR(255),
    
    -- Professional details
    specializations JSONB DEFAULT '[]',  -- ["civil_law", "criminal_law", etc.]
    languages JSONB DEFAULT '[]',  -- ["sk", "en", "de"]
    experience_years INTEGER,
    education TEXT,
    certifications TEXT,
    
    -- Contact and location
    office_address TEXT,
    city VARCHAR(100),
    country VARCHAR(2) DEFAULT 'SK',
    phone VARCHAR(50),
    website VARCHAR(500),
    
    -- Pricing
    hourly_rate DECIMAL(10, 2),
    consultation_fee DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'EUR',
    
    -- Profile content
    bio TEXT,
    profile_image_url VARCHAR(500),
    
    -- Status and verification
    is_verified BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    verification_date TIMESTAMP,
    verification_documents JSONB,
    
    -- Statistics
    total_cases INTEGER DEFAULT 0,
    success_rate DECIMAL(5, 2),
    average_rating DECIMAL(3, 2),
    total_reviews INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for lawyers
CREATE INDEX IF NOT EXISTS idx_lawyers_user_id ON lawyers(user_id);
CREATE INDEX IF NOT EXISTS idx_lawyers_license_number ON lawyers(license_number);
CREATE INDEX IF NOT EXISTS idx_lawyers_city ON lawyers(city);
CREATE INDEX IF NOT EXISTS idx_lawyers_country ON lawyers(country);
CREATE INDEX IF NOT EXISTS idx_lawyers_is_verified ON lawyers(is_verified);
CREATE INDEX IF NOT EXISTS idx_lawyers_is_active ON lawyers(is_active);
CREATE INDEX IF NOT EXISTS idx_lawyers_specializations ON lawyers USING GIN(specializations);
CREATE INDEX IF NOT EXISTS idx_lawyers_languages ON lawyers USING GIN(languages);
CREATE INDEX IF NOT EXISTS idx_lawyers_average_rating ON lawyers(average_rating DESC);

COMMENT ON TABLE lawyers IS 'Lawyer profiles in the marketplace';
COMMENT ON COLUMN lawyers.specializations IS 'JSON array of legal specializations';
COMMENT ON COLUMN lawyers.languages IS 'JSON array of supported languages';


-- ============================================
-- 2. CREATE LEGAL_CASES TABLE (Marketplace Cases)
-- ============================================

CREATE TABLE IF NOT EXISTS legal_cases (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lawyer_id INTEGER REFERENCES lawyers(id) ON DELETE SET NULL,
    
    -- Case details
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    case_type VARCHAR(100) NOT NULL,  -- divorce, contract, criminal, etc.
    category_id INTEGER,
    
    -- Case specifics
    jurisdiction VARCHAR(2) DEFAULT 'SK',
    urgency VARCHAR(50) DEFAULT 'normal',  -- low, normal, high, urgent
    budget_min DECIMAL(10, 2),
    budget_max DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'EUR',
    
    -- Status
    status VARCHAR(50) DEFAULT 'open',  -- open, assigned, in_progress, completed, cancelled
    visibility VARCHAR(50) DEFAULT 'public',  -- public, private
    
    -- Metadata
    required_specializations JSONB DEFAULT '[]',
    preferred_languages JSONB DEFAULT '[]',
    attachments JSONB DEFAULT '[]',
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    assigned_at TIMESTAMP,
    completed_at TIMESTAMP,
    deadline TIMESTAMP
);

-- Indexes for legal_cases
CREATE INDEX IF NOT EXISTS idx_legal_cases_user_id ON legal_cases(user_id);
CREATE INDEX IF NOT EXISTS idx_legal_cases_lawyer_id ON legal_cases(lawyer_id);
CREATE INDEX IF NOT EXISTS idx_legal_cases_status ON legal_cases(status);
CREATE INDEX IF NOT EXISTS idx_legal_cases_case_type ON legal_cases(case_type);
CREATE INDEX IF NOT EXISTS idx_legal_cases_jurisdiction ON legal_cases(jurisdiction);
CREATE INDEX IF NOT EXISTS idx_legal_cases_urgency ON legal_cases(urgency);
CREATE INDEX IF NOT EXISTS idx_legal_cases_created_at ON legal_cases(created_at DESC);

-- Add check constraint for status
ALTER TABLE legal_cases ADD CONSTRAINT IF NOT EXISTS chk_legal_cases_status 
    CHECK (status IN ('open', 'assigned', 'in_progress', 'completed', 'cancelled'));

-- Add check constraint for urgency
ALTER TABLE legal_cases ADD CONSTRAINT IF NOT EXISTS chk_legal_cases_urgency 
    CHECK (urgency IN ('low', 'normal', 'high', 'urgent'));

COMMENT ON TABLE legal_cases IS 'Legal cases posted by users seeking lawyer services';


-- ============================================
-- 3. CREATE ORDERS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(100) UNIQUE NOT NULL,
    
    -- Parties
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lawyer_id INTEGER NOT NULL REFERENCES lawyers(id) ON DELETE CASCADE,
    case_id INTEGER REFERENCES legal_cases(id) ON DELETE SET NULL,
    
    -- Order details
    service_type VARCHAR(100) NOT NULL,  -- consultation, case_handling, document_review, etc.
    description TEXT,
    
    -- Pricing
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'EUR',
    payment_status VARCHAR(50) DEFAULT 'pending',  -- pending, paid, refunded, cancelled
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending',  -- pending, accepted, in_progress, completed, cancelled
    
    -- Metadata
    terms_agreed BOOLEAN DEFAULT false,
    terms_agreed_at TIMESTAMP,
    contract_url VARCHAR(500),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accepted_at TIMESTAMP,
    completed_at TIMESTAMP,
    cancelled_at TIMESTAMP
);

-- Indexes for orders
CREATE INDEX IF NOT EXISTS idx_orders_order_number ON orders(order_number);
CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_lawyer_id ON orders(lawyer_id);
CREATE INDEX IF NOT EXISTS idx_orders_case_id ON orders(case_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_payment_status ON orders(payment_status);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at DESC);

-- Add check constraints
ALTER TABLE orders ADD CONSTRAINT IF NOT EXISTS chk_orders_status 
    CHECK (status IN ('pending', 'accepted', 'in_progress', 'completed', 'cancelled'));

ALTER TABLE orders ADD CONSTRAINT IF NOT EXISTS chk_orders_payment_status 
    CHECK (payment_status IN ('pending', 'paid', 'refunded', 'cancelled'));

COMMENT ON TABLE orders IS 'Service orders between users and lawyers';


-- ============================================
-- 4. CREATE REVIEWS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    
    -- Parties
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lawyer_id INTEGER NOT NULL REFERENCES lawyers(id) ON DELETE CASCADE,
    order_id INTEGER REFERENCES orders(id) ON DELETE SET NULL,
    
    -- Review content
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title VARCHAR(255),
    comment TEXT,
    
    -- Review aspects (optional detailed ratings)
    professionalism_rating INTEGER CHECK (professionalism_rating >= 1 AND professionalism_rating <= 5),
    communication_rating INTEGER CHECK (communication_rating >= 1 AND communication_rating <= 5),
    expertise_rating INTEGER CHECK (expertise_rating >= 1 AND expertise_rating <= 5),
    value_rating INTEGER CHECK (value_rating >= 1 AND value_rating <= 5),
    
    -- Status
    is_verified BOOLEAN DEFAULT false,
    is_visible BOOLEAN DEFAULT true,
    
    -- Response from lawyer
    lawyer_response TEXT,
    lawyer_response_at TIMESTAMP,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for reviews
CREATE INDEX IF NOT EXISTS idx_reviews_user_id ON reviews(user_id);
CREATE INDEX IF NOT EXISTS idx_reviews_lawyer_id ON reviews(lawyer_id);
CREATE INDEX IF NOT EXISTS idx_reviews_order_id ON reviews(order_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
CREATE INDEX IF NOT EXISTS idx_reviews_is_visible ON reviews(is_visible);
CREATE INDEX IF NOT EXISTS idx_reviews_created_at ON reviews(created_at DESC);

COMMENT ON TABLE reviews IS 'User reviews and ratings for lawyers';


-- ============================================
-- 5. CREATE TRANSACTIONS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(255) UNIQUE NOT NULL,
    
    -- Parties
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lawyer_id INTEGER REFERENCES lawyers(id) ON DELETE SET NULL,
    order_id INTEGER REFERENCES orders(id) ON DELETE SET NULL,
    
    -- Transaction details
    type VARCHAR(50) NOT NULL,  -- payment, refund, payout, fee
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'EUR',
    
    -- Payment gateway
    payment_method VARCHAR(50),  -- card, bank_transfer, paypal, etc.
    payment_gateway VARCHAR(50),  -- stripe, paypal, etc.
    gateway_transaction_id VARCHAR(255),
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending',  -- pending, completed, failed, refunded
    
    -- Metadata
    description TEXT,
    metadata JSONB,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    failed_at TIMESTAMP
);

-- Indexes for transactions
CREATE INDEX IF NOT EXISTS idx_transactions_transaction_id ON transactions(transaction_id);
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_lawyer_id ON transactions(lawyer_id);
CREATE INDEX IF NOT EXISTS idx_transactions_order_id ON transactions(order_id);
CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status);
CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type);
CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at DESC);

-- Add check constraint for status
ALTER TABLE transactions ADD CONSTRAINT IF NOT EXISTS chk_transactions_status 
    CHECK (status IN ('pending', 'completed', 'failed', 'refunded'));

COMMENT ON TABLE transactions IS 'Financial transactions for marketplace orders';


-- ============================================
-- 6. CREATE MESSAGES TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    
    -- Parties
    sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    recipient_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    
    -- Message content
    subject VARCHAR(500),
    body TEXT NOT NULL,
    attachments JSONB DEFAULT '[]',
    
    -- Status
    is_read BOOLEAN DEFAULT false,
    read_at TIMESTAMP,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for messages
CREATE INDEX IF NOT EXISTS idx_messages_sender_id ON messages(sender_id);
CREATE INDEX IF NOT EXISTS idx_messages_recipient_id ON messages(recipient_id);
CREATE INDEX IF NOT EXISTS idx_messages_order_id ON messages(order_id);
CREATE INDEX IF NOT EXISTS idx_messages_is_read ON messages(is_read);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at DESC);

COMMENT ON TABLE messages IS 'Messages between users and lawyers';


-- ============================================
-- 7. CREATE LAWYER_AVAILABILITY TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS lawyer_availability (
    id SERIAL PRIMARY KEY,
    lawyer_id INTEGER NOT NULL REFERENCES lawyers(id) ON DELETE CASCADE,
    
    -- Availability
    day_of_week INTEGER NOT NULL CHECK (day_of_week >= 0 AND day_of_week <= 6),  -- 0=Sunday, 6=Saturday
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for lawyer_availability
CREATE INDEX IF NOT EXISTS idx_lawyer_availability_lawyer_id ON lawyer_availability(lawyer_id);
CREATE INDEX IF NOT EXISTS idx_lawyer_availability_day_of_week ON lawyer_availability(day_of_week);
CREATE INDEX IF NOT EXISTS idx_lawyer_availability_is_active ON lawyer_availability(is_active);

COMMENT ON TABLE lawyer_availability IS 'Lawyer availability schedule';


-- ============================================
-- 8. CREATE NOTIFICATIONS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Notification content
    type VARCHAR(100) NOT NULL,  -- new_order, message, review, payment, etc.
    title VARCHAR(255) NOT NULL,
    message TEXT,
    
    -- Related entities
    related_entity_type VARCHAR(50),  -- order, message, review, etc.
    related_entity_id INTEGER,
    
    -- Status
    is_read BOOLEAN DEFAULT false,
    read_at TIMESTAMP,
    
    -- Action
    action_url VARCHAR(500),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for notifications
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_type ON notifications(type);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at DESC);

COMMENT ON TABLE notifications IS 'User notifications for marketplace events';


-- ============================================
-- 9. CREATE LAWYER_ACTIVITY_LOG TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS lawyer_activity_log (
    id SERIAL PRIMARY KEY,
    lawyer_id INTEGER NOT NULL REFERENCES lawyers(id) ON DELETE CASCADE,
    
    -- Activity details
    activity_type VARCHAR(100) NOT NULL,  -- profile_update, case_accepted, order_completed, etc.
    description TEXT,
    metadata JSONB,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for lawyer_activity_log
CREATE INDEX IF NOT EXISTS idx_lawyer_activity_log_lawyer_id ON lawyer_activity_log(lawyer_id);
CREATE INDEX IF NOT EXISTS idx_lawyer_activity_log_activity_type ON lawyer_activity_log(activity_type);
CREATE INDEX IF NOT EXISTS idx_lawyer_activity_log_created_at ON lawyer_activity_log(created_at DESC);

COMMENT ON TABLE lawyer_activity_log IS 'Activity log for lawyer actions';


-- ============================================
-- 10. CREATE CASE_CATEGORIES TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS case_categories (
    id SERIAL PRIMARY KEY,
    
    -- Category details
    name_key VARCHAR(100) UNIQUE NOT NULL,  -- Translation key
    parent_id INTEGER REFERENCES case_categories(id) ON DELETE SET NULL,
    
    -- Display
    icon VARCHAR(100),
    color VARCHAR(50),
    sort_order INTEGER DEFAULT 0,
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for case_categories
CREATE INDEX IF NOT EXISTS idx_case_categories_parent_id ON case_categories(parent_id);
CREATE INDEX IF NOT EXISTS idx_case_categories_is_active ON case_categories(is_active);
CREATE INDEX IF NOT EXISTS idx_case_categories_sort_order ON case_categories(sort_order);

COMMENT ON TABLE case_categories IS 'Categories for legal cases';


-- ============================================
-- 11. CREATE TRIGGERS FOR UPDATED_AT
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
-- 12. CREATE TRIGGER TO UPDATE LAWYER STATISTICS
-- ============================================

CREATE OR REPLACE FUNCTION update_lawyer_statistics()
RETURNS TRIGGER AS $$
BEGIN
    -- Update lawyer statistics when a review is added/updated
    UPDATE lawyers
    SET 
        average_rating = (
            SELECT AVG(rating)::DECIMAL(3,2)
            FROM reviews
            WHERE lawyer_id = NEW.lawyer_id AND is_visible = true
        ),
        total_reviews = (
            SELECT COUNT(*)
            FROM reviews
            WHERE lawyer_id = NEW.lawyer_id AND is_visible = true
        )
    WHERE id = NEW.lawyer_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_lawyer_stats_on_review ON reviews;
CREATE TRIGGER update_lawyer_stats_on_review
    AFTER INSERT OR UPDATE ON reviews
    FOR EACH ROW
    EXECUTE FUNCTION update_lawyer_statistics();


-- ============================================
-- 13. CREATE VIEWS
-- ============================================

-- View for marketplace orders with user and lawyer details
CREATE OR REPLACE VIEW marketplace_orders AS
SELECT 
    o.id,
    o.order_number,
    o.service_type,
    o.amount,
    o.currency,
    o.status,
    o.payment_status,
    o.created_at,
    
    -- User details
    u.name as user_name,
    u.email as user_email,
    
    -- Lawyer details
    l.full_name as lawyer_name,
    l.title as lawyer_title,
    l.license_number as lawyer_license,
    
    -- Case details (if applicable)
    lc.title as case_title,
    lc.case_type
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN lawyers l ON o.lawyer_id = l.id
LEFT JOIN legal_cases lc ON o.case_id = lc.id;

COMMENT ON VIEW marketplace_orders IS 'Comprehensive view of marketplace orders';


-- View for active lawyers with statistics
CREATE OR REPLACE VIEW active_lawyers AS
SELECT 
    l.*,
    u.name as user_name,
    u.email as user_email,
    COUNT(DISTINCT o.id) as total_orders,
    COUNT(DISTINCT CASE WHEN o.status = 'completed' THEN o.id END) as completed_orders
FROM lawyers l
JOIN users u ON l.user_id = u.id
LEFT JOIN orders o ON l.id = o.lawyer_id
WHERE l.is_active = true AND l.is_verified = true
GROUP BY l.id, u.name, u.email;

COMMENT ON VIEW active_lawyers IS 'Active and verified lawyers with statistics';


-- ============================================
-- 14. SEED DATA FOR CASE CATEGORIES
-- ============================================

INSERT INTO case_categories (name_key, icon, color, sort_order) VALUES
('civil_law', 'scale', '#3B82F6', 1),
('criminal_law', 'gavel', '#EF4444', 2),
('family_law', 'users', '#8B5CF6', 3),
('commercial_law', 'briefcase', '#10B981', 4),
('labor_law', 'user-tie', '#F59E0B', 5),
('real_estate_law', 'home', '#06B6D4', 6),
('intellectual_property', 'lightbulb', '#EC4899', 7),
('tax_law', 'calculator', '#6366F1', 8),
('immigration_law', 'globe', '#14B8A6', 9),
('administrative_law', 'building', '#84CC16', 10)
ON CONFLICT (name_key) DO NOTHING;


-- ============================================
-- 15. GRANT PERMISSIONS (if needed)
-- ============================================

-- Uncomment if you need to grant permissions to specific users
-- GRANT SELECT, INSERT, UPDATE, DELETE ON lawyers TO your_app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON legal_cases TO your_app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON orders TO your_app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON reviews TO your_app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON transactions TO your_app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON messages TO your_app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON lawyer_availability TO your_app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON notifications TO your_app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON lawyer_activity_log TO your_app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON case_categories TO your_app_user;


-- ============================================
-- VERIFICATION QUERIES
-- ============================================

-- Verify all tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN (
    'lawyers', 'legal_cases', 'orders', 'reviews', 'transactions', 
    'messages', 'lawyer_availability', 'notifications', 
    'lawyer_activity_log', 'case_categories'
)
ORDER BY table_name;

-- Count tables
SELECT COUNT(*) as marketplace_tables_count
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN (
    'lawyers', 'legal_cases', 'orders', 'reviews', 'transactions', 
    'messages', 'lawyer_availability', 'notifications', 
    'lawyer_activity_log', 'case_categories'
);

-- Verify indexes
SELECT tablename, indexname 
FROM pg_indexes 
WHERE schemaname = 'public' 
AND tablename IN (
    'lawyers', 'legal_cases', 'orders', 'reviews', 'transactions', 
    'messages', 'lawyer_availability', 'notifications', 
    'lawyer_activity_log', 'case_categories'
)
ORDER BY tablename, indexname;

-- Verify triggers
SELECT trigger_name, event_object_table 
FROM information_schema.triggers 
WHERE event_object_schema = 'public'
AND event_object_table IN (
    'lawyers', 'legal_cases', 'orders', 'reviews', 
    'lawyer_availability', 'case_categories'
)
ORDER BY event_object_table, trigger_name;

-- Verify views
SELECT table_name 
FROM information_schema.views 
WHERE table_schema = 'public'
AND table_name IN ('marketplace_orders', 'active_lawyers');

-- Verify case categories
SELECT * FROM case_categories ORDER BY sort_order;
