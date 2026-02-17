-- Migration 011: Add marketplace payment and escrow tables
-- Created: 2024-12-24
-- Purpose: Support marketplace payments with escrow mechanism

-- ============================================
-- TRANSACTIONS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    transaction_number VARCHAR(50) UNIQUE NOT NULL,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    type VARCHAR(20) NOT NULL CHECK (type IN ('payment', 'payout', 'refund', 'platform_fee')),
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'EUR',
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'completed', 'failed', 'reversed')),
    payment_method VARCHAR(50),
    payment_id VARCHAR(255),  -- Stripe payment intent ID
    description TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_transactions_order ON transactions(order_id);
CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status);
CREATE INDEX IF NOT EXISTS idx_transactions_payment_id ON transactions(payment_id);

-- ============================================
-- ESCROW TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS escrow (
    id SERIAL PRIMARY KEY,
    order_id INTEGER UNIQUE REFERENCES orders(id) ON DELETE CASCADE,
    total_amount DECIMAL(10, 2) NOT NULL,
    platform_fee DECIMAL(10, 2) NOT NULL,
    lawyer_payout DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'held' CHECK (status IN ('held', 'frozen', 'released', 'refunded')),
    held_at TIMESTAMP DEFAULT NOW(),
    released_at TIMESTAMP,
    auto_release_at TIMESTAMP,  -- Auto-release after 72 hours
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_escrow_order ON escrow(order_id);
CREATE INDEX IF NOT EXISTS idx_escrow_status ON escrow(status);
CREATE INDEX IF NOT EXISTS idx_escrow_auto_release ON escrow(auto_release_at) WHERE status = 'held';

-- ============================================
-- LAWYER WALLETS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS lawyer_wallets (
    id SERIAL PRIMARY KEY,
    lawyer_id INTEGER UNIQUE REFERENCES lawyers(id) ON DELETE CASCADE,
    total_earnings DECIMAL(10, 2) DEFAULT 0,
    available_balance DECIMAL(10, 2) DEFAULT 0,
    pending_balance DECIMAL(10, 2) DEFAULT 0,
    total_withdrawn DECIMAL(10, 2) DEFAULT 0,
    currency VARCHAR(3) DEFAULT 'EUR',
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_lawyer_wallets_lawyer ON lawyer_wallets(lawyer_id);

-- ============================================
-- WITHDRAWALS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS withdrawals (
    id SERIAL PRIMARY KEY,
    withdrawal_number VARCHAR(50) UNIQUE NOT NULL,
    lawyer_id INTEGER REFERENCES lawyers(id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL,
    bank_account VARCHAR(255) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'processing', 'completed', 'rejected')),
    note TEXT,
    admin_note TEXT,
    approved_by INTEGER REFERENCES users(id),
    requested_at TIMESTAMP DEFAULT NOW(),
    approved_at TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_withdrawals_lawyer ON withdrawals(lawyer_id);
CREATE INDEX IF NOT EXISTS idx_withdrawals_status ON withdrawals(status);

-- ============================================
-- DISPUTES TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS disputes (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    raised_by VARCHAR(10) CHECK (raised_by IN ('client', 'lawyer')),
    client_id INTEGER REFERENCES users(id),
    lawyer_id INTEGER REFERENCES lawyers(id),
    reason VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    requested_refund_amount DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'investigating', 'resolved', 'closed')),
    resolution TEXT,
    refund_amount DECIMAL(10, 2),
    resolved_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_disputes_order ON disputes(order_id);
CREATE INDEX IF NOT EXISTS idx_disputes_status ON disputes(status);
CREATE INDEX IF NOT EXISTS idx_disputes_client ON disputes(client_id);
CREATE INDEX IF NOT EXISTS idx_disputes_lawyer ON disputes(lawyer_id);

-- ============================================
-- TRIGGERS
-- ============================================

-- Update lawyer_wallets.updated_at on update
CREATE OR REPLACE FUNCTION update_lawyer_wallets_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_lawyer_wallets_updated_at
    BEFORE UPDATE ON lawyer_wallets
    FOR EACH ROW
    EXECUTE FUNCTION update_lawyer_wallets_updated_at();

-- ============================================
-- COMMENTS
-- ============================================

COMMENT ON TABLE transactions IS 'All payment transactions (payments, payouts, refunds)';
COMMENT ON TABLE escrow IS 'Escrow holdings for marketplace orders';
COMMENT ON TABLE lawyer_wallets IS 'Lawyer earnings and balances';
COMMENT ON TABLE withdrawals IS 'Lawyer withdrawal requests';
COMMENT ON TABLE disputes IS 'Order disputes between clients and lawyers';

COMMENT ON COLUMN escrow.auto_release_at IS 'Automatic release timestamp (72 hours after delivery)';
COMMENT ON COLUMN escrow.platform_fee IS 'CODEX platform fee (20% of total)';
COMMENT ON COLUMN escrow.lawyer_payout IS 'Lawyer payout amount (80% of total)';
