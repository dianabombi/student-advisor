#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import sys

# Database connection via docker network
conn = psycopg2.connect(
    host="db",
    port=5432,
    database="codex_db",
    user="user",
    password="password"
)

# Set UTF-8 encoding
conn.set_client_encoding('UTF8')
cur = conn.cursor()

# Delete existing
cur.execute("DELETE FROM universities WHERE id IN (1,2,3,4,5);")

# Insert with proper UTF-8
universities = [
    (1, "Comenius University in Bratislava", "Univerzita Komenského v Bratislave", "university", "Bratislava", "SK",
     "Najstaršia a najväčšia univerzita na Slovensku, založená v roku 1919.", "https://uniba.sk", 20000, 1, 1, True),
    
    (2, "Slovak University of Technology in Bratislava", "Slovenská technická univerzita v Bratislave", "university", "Bratislava", "SK",
     "Popredná technická univerzita zameraná na inžinierstvo a technológie.", "https://stuba.sk", 15000, 2, 1, True),
    
    (3, "University of Economics in Bratislava", "Ekonomická univerzita v Bratislave", "university", "Bratislava", "SK",
     "Špecializovaná univerzita pre ekonomiku, obchod a manažment.", "https://euba.sk", 8000, 3, 1, True),
    
    (4, "Pavol Jozef Šafárik University in Košice", "Univerzita Pavla Jozefa Šafárika v Košiciach", "university", "Košice", "SK",
     "Významná univerzita vo východnom Slovensku s dlhou tradíciou.", "https://upjs.sk", 7000, 4, 1, True),
    
    (5, "Matej Bel University in Banská Bystrica", "Univerzita Mateja Bela v Banskej Bystrici", "university", "Banská Bystrica", "SK",
     "Moderná univerzita v strednom Slovensku s širokým spektrom programov.", "https://umb.sk", 9000, 5, 1, True)
]

for univ in universities:
    cur.execute("""
        INSERT INTO universities (
            id, name, name_local, type, city, country, description, 
            website_url, student_count, ranking_position, jurisdiction_id, is_active
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, univ)

conn.commit()
cur.close()
conn.close()

print("SUCCESS: Universities inserted with UTF-8 encoding")
