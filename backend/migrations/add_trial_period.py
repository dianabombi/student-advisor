"""
Database migration to add trial period support

This migration adds trial period tracking fields to the users table
and trial flag to the subscriptions table.
"""

from sqlalchemy import create_engine, text
import os
from datetime import datetime, timedelta

def upgrade():
    """Add trial period fields to database"""
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/codex_db")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        print("Starting migration: add_trial_period")
        
        # Add new columns to users table
        print("Adding trial period columns to users table...")
        conn.execute(text('''
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS trial_start_date TIMESTAMP,
            ADD COLUMN IF NOT EXISTS trial_end_date TIMESTAMP,
            ADD COLUMN IF NOT EXISTS trial_used BOOLEAN DEFAULT FALSE,
            ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(20) DEFAULT 'trial'
        '''))
        
        # Add is_trial column to subscriptions table
        print("Adding is_trial column to subscriptions table...")
        conn.execute(text('''
            ALTER TABLE subscriptions 
            ADD COLUMN IF NOT EXISTS is_trial BOOLEAN DEFAULT FALSE
        '''))
        
        # Update existing users to have trial period
        print("Initializing trial period for existing users...")
        conn.execute(text('''
            UPDATE users 
            SET trial_start_date = created_at,
                trial_end_date = created_at + INTERVAL '7 days',
                trial_used = TRUE,
                subscription_status = CASE 
                    WHEN created_at + INTERVAL '7 days' > NOW() THEN 'trial'
                    ELSE 'expired'
                END
            WHERE trial_start_date IS NULL
        '''))
        
        # Create trial subscriptions for existing users who don't have active subscriptions
        print("Creating trial subscriptions for existing users...")
        conn.execute(text('''
            INSERT INTO subscriptions (user_id, plan_type, amount, status, start_date, end_date, is_trial, created_at, updated_at)
            SELECT 
                u.id,
                'trial',
                0,
                CASE 
                    WHEN u.trial_end_date > NOW() THEN 'active'
                    ELSE 'expired'
                END,
                u.trial_start_date,
                u.trial_end_date,
                TRUE,
                u.created_at,
                NOW()
            FROM users u
            WHERE NOT EXISTS (
                SELECT 1 FROM subscriptions s 
                WHERE s.user_id = u.id AND s.is_trial = TRUE
            )
        '''))
        
        conn.commit()
        print("Migration completed successfully!")

def downgrade():
    """Remove trial period fields from database"""
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/codex_db")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        print("Starting rollback: add_trial_period")
        
        # Remove columns from users table
        print("Removing trial period columns from users table...")
        conn.execute(text('''
            ALTER TABLE users 
            DROP COLUMN IF EXISTS trial_start_date,
            DROP COLUMN IF EXISTS trial_end_date,
            DROP COLUMN IF EXISTS trial_used,
            DROP COLUMN IF EXISTS subscription_status
        '''))
        
        # Remove is_trial column from subscriptions table
        print("Removing is_trial column from subscriptions table...")
        conn.execute(text('''
            ALTER TABLE subscriptions 
            DROP COLUMN IF EXISTS is_trial
        '''))
        
        # Delete trial subscriptions
        print("Removing trial subscriptions...")
        conn.execute(text('''
            DELETE FROM subscriptions WHERE plan_type = 'trial'
        '''))
        
        conn.commit()
        print("Rollback completed successfully!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "downgrade":
        downgrade()
    else:
        upgrade()
