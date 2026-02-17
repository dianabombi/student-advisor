"""
Деактивація непрацюючої агенції StudentJob.sk

Причина: Сайт https://www.studentjob.sk недоступний (ERR_CONNECTION_REFUSED)
Дата: 2026-01-17
"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime


def upgrade():
    """Деактивувати StudentJob.sk для всіх міст"""
    
    # Деактивуємо всі записи StudentJob
    op.execute("""
        UPDATE job_agencies 
        SET is_active = FALSE,
            updated_at = NOW()
        WHERE name LIKE '%StudentJob%'
    """)
    
    print("✅ Деактивовано агенцію StudentJob.sk (сайт недоступний)")


def downgrade():
    """Відновити StudentJob.sk"""
    
    # Відновлюємо записи StudentJob
    op.execute("""
        UPDATE job_agencies 
        SET is_active = TRUE,
            updated_at = NOW()
        WHERE name LIKE '%StudentJob%'
    """)
    
    print("✅ Відновлено агенцію StudentJob.sk")
