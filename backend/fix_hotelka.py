#!/usr/bin/env python3
import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("UPDATE universities SET website_url = 'https://hamikoviniho.edupage.org' WHERE id = 10"))
    conn.commit()
    print("Updated Hotelova akademia URL")
    
    # Verify
    result = conn.execute(text("SELECT id, name_local, website_url FROM universities WHERE id = 10"))
    for row in result:
        print(f"ID {row[0]}: {row[1]}")
        print(f"  URL: {row[2]}")
