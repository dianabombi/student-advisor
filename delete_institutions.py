#!/usr/bin/env python3
import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Delete Hotelova akademia (ID 10) and SPSE (ID 11)
    conn.execute(text("DELETE FROM universities WHERE id IN (10, 11)"))
    conn.commit()
    print("Deleted 2 institutions:")
    print("  - ID 10: Hotelova akademia")
    print("  - ID 11: SPSE")
    
    # Verify
    result = conn.execute(text("SELECT COUNT(*) FROM universities"))
    count = result.fetchone()[0]
    print(f"\nTotal institutions remaining: {count}")
