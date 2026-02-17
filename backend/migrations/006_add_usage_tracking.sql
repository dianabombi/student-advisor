-- Add usage tracking columns to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS monthly_request_limit INTEGER DEFAULT 500;
ALTER TABLE users ADD COLUMN IF NOT EXISTS requests_used_this_month INTEGER DEFAULT 0;

-- Create usage history table for detailed tracking
CREATE TABLE IF NOT EXISTS usage_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    request_type VARCHAR(50) NOT NULL,  -- 'chat', 'document_upload', etc.
    tokens_used INTEGER,
    cost_estimate DECIMAL(10, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_usage_user_date ON usage_history(user_id, created_at);

-- Create subscription plans table
CREATE TABLE IF NOT EXISTS subscription_plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,  -- 'basic', 'professional', 'enterprise'
    price_monthly DECIMAL(10, 2),
    price_6months DECIMAL(10, 2),
    price_yearly DECIMAL(10, 2),
    request_limit INTEGER,
    features JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert subscription plans with correct pricing
INSERT INTO subscription_plans (name, price_monthly, price_6months, price_yearly, request_limit, features)
VALUES 
    ('basic', 30.00, 150.00, 270.00, 500, '{"support": "email", "documents": 100}'),
    ('professional', 70.00, 360.00, 660.00, 1500, '{"support": "priority", "documents": 500}'),
    ('enterprise', 150.00, 780.00, 1440.00, 3500, '{"support": "24/7", "documents": "unlimited"}')
ON CONFLICT (name) DO UPDATE SET
    price_monthly = EXCLUDED.price_monthly,
    price_6months = EXCLUDED.price_6months,
    price_yearly = EXCLUDED.price_yearly,
    request_limit = EXCLUDED.request_limit,
    features = EXCLUDED.features;
