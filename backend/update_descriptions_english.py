#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2

# Database connection via docker network
conn = psycopg2.connect(
    host="db",
    port=5432,
    database="codex_db",
    user="user",
    password="password"
)

conn.set_client_encoding('UTF8')
cur = conn.cursor()

# Update descriptions to English
updates = [
    (1, "The oldest and largest university in Slovakia, founded in 1919."),
    (2, "Leading technical university focused on engineering and technology."),
    (3, "Specialized university for economics, business and management."),
    (4, "Prominent university in eastern Slovakia with a long tradition."),
    (5, "Modern university in central Slovakia with a wide range of programs.")
]

for univ_id, description in updates:
    cur.execute("""
        UPDATE universities 
        SET description = %s
        WHERE id = %s
    """, (description, univ_id))

conn.commit()
cur.close()
conn.close()

print("SUCCESS: University descriptions updated to English")
