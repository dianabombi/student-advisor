#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import psycopg2
import sys

# Ensure UTF-8 encoding
sys.stdout.reconfigure(encoding='utf-8')

# Database connection
conn = psycopg2.connect(
    host="localhost",
    port=5433,
    database="codex_db",
    user="user",
    password="password",
    client_encoding='UTF8'
)
conn.set_client_encoding('UTF8')

cur = conn.cursor()

# Delete existing universities
print("Deleting existing universities...")
cur.execute("DELETE FROM universities WHERE id IN (1,2,3,4,5);")

# Insert universities with correct UTF-8 encoding
universities = [
    (1, "Comenius University in Bratislava", "Univerzita Komenského v Bratislave", "university", "Bratislava", "SK",
     "Najstaršia a najväčšia univerzita na Slovensku, založená v roku 1919.", "https://uniba.sk", 20000, 1, 1),
    
    (2, "Slovak University of Technology in Bratislava", "Slovenská technická univerzita v Bratislave", "university", "Bratislava", "SK",
     "Popredná technická univerzita zameraná na inžinierstvo a technológie.", "https://stuba.sk", 15000, 2, 1),
    
    (3, "University of Economics in Bratislava", "Ekonomická univerzita v Bratislave", "university", "Bratislava", "SK",
     "Špecializovaná univerzita pre ekonomiku, obchod a manažment.", "https://euba.sk", 8000, 3, 1),
    
    (4, "Pavol Jozef Šafárik University in Košice", "Univerzita Pavla Jozefa Šafárika v Košiciach", "university", "Košice", "SK",
     "Významná univerzita vo východnom Slovensku s dlhou tradíciou.", "https://upjs.sk", 7000, 4, 1),
    
    (5, "Matej Bel University in Banská Bystrica", "Univerzita Mateja Bela v Banskej Bystrici", "university", "Banská Bystrica", "SK",
     "Moderná univerzita v strednom Slovensku s širokým spektrom programov.", "https://umb.sk", 9000, 5, 1)
]

print("Inserting universities with UTF-8 encoding...")
for univ in universities:
    cur.execute("""
        INSERT INTO universities (
            id, name, name_local, type, city, country, description, 
            website_url, student_count, ranking_position, jurisdiction_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, univ)
    print(f"✓ Inserted: {univ[2]}")

conn.commit()
cur.close()
conn.close()

print("\n✅ All universities updated with correct UTF-8 encoding!")
