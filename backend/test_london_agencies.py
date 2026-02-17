#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test if London agencies exist in database"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Test case-insensitive search for London
print("Testing London agencies...")
cursor.execute("""
    SELECT city, name, website_url 
    FROM real_estate_agencies 
    WHERE country_code = 'GB' AND city ILIKE %s
    LIMIT 10
""", ('london',))

results = cursor.fetchall()
print(f"\nFound {len(results)} agencies for London:")
for city, name, url in results:
    print(f"  - {city}: {name} ({url})")

# Test exact match
print("\n\nTesting exact match 'London'...")
cursor.execute("""
    SELECT city, name 
    FROM real_estate_agencies 
    WHERE country_code = 'GB' AND city = %s
    LIMIT 5
""", ('London',))

exact_results = cursor.fetchall()
print(f"Found {len(exact_results)} agencies with exact 'London':")
for city, name in exact_results:
    print(f"  - {city}: {name}")

cursor.close()
conn.close()
