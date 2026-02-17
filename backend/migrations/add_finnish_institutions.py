"""
Додавання фінських навчальних закладів
ВАЖЛИВО: Використовуються ТІЛЬКИ перевірені офіційні URL
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='FI'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_finnish_universities(conn, jurisdiction_id):
    """Add major Finnish universities with VERIFIED URLs"""
    cursor = conn.cursor()
    
    universities = [
        {
            'name': 'University of Helsinki',
            'name_local': 'Helsingin yliopisto',
            'type': 'university',
            'city': 'Helsinki',
            'country': 'FI',
            'website_url': 'https://www.helsinki.fi',
            'student_count': 31000,
            'ranking_position': 1,
            'description': 'Largest and oldest university in Finland, founded in 1640. Strong in humanities, sciences, law, and medicine.'
        },
        {
            'name': 'Aalto University',
            'name_local': 'Aalto-yliopisto',
            'type': 'university',
            'city': 'Espoo',
            'country': 'FI',
            'website_url': 'https://www.aalto.fi',
            'student_count': 20000,
            'ranking_position': 2,
            'description': 'Leading technical university formed in 2010, specializing in technology, business, and art & design.'
        },
        {
            'name': 'University of Turku',
            'name_local': 'Turun yliopisto',
            'type': 'university',
            'city': 'Turku',
            'country': 'FI',
            'website_url': 'https://www.utu.fi',
            'student_count': 20000,
            'ranking_position': 3,
            'description': 'Second largest university in Finland, offering programs in humanities, sciences, medicine, and law.'
        },
        {
            'name': 'University of Oulu',
            'name_local': 'Oulun yliopisto',
            'type': 'university',
            'city': 'Oulu',
            'country': 'FI',
            'website_url': 'https://www.oulu.fi',
            'student_count': 13000,
            'ranking_position': 4,
            'description': 'Northern Finland\'s leading university, strong in technology, natural sciences, and medicine.'
        },
        {
            'name': 'University of Jyväskylä',
            'name_local': 'Jyväskylän yliopisto',
            'type': 'university',
            'city': 'Jyväskylä',
            'country': 'FI',
            'website_url': 'https://www.jyu.fi',
            'student_count': 15000,
            'ranking_position': 5,
            'description': 'University in central Finland, known for education, sports sciences, and humanities.'
        },
        {
            'name': 'Tampere University',
            'name_local': 'Tampereen yliopisto',
            'type': 'university',
            'city': 'Tampere',
            'country': 'FI',
            'website_url': 'https://www.tuni.fi',
            'student_count': 24000,
            'ranking_position': 6,
            'description': 'Multidisciplinary university formed in 2019, offering programs in technology, health, and society.'
        },
        {
            'name': 'University of Eastern Finland',
            'name_local': 'Itä-Suomen yliopisto',
            'type': 'university',
            'city': 'Joensuu',
            'country': 'FI',
            'website_url': 'https://www.uef.fi',
            'student_count': 15000,
            'ranking_position': 7,
            'description': 'University in eastern Finland, strong in health sciences, natural sciences, and social sciences.'
        }
    ]
    
    for uni in universities:
        cursor.execute(
            "SELECT id FROM universities WHERE name = %s AND jurisdiction_id = %s",
            (uni['name'], jurisdiction_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.execute("""
                INSERT INTO universities 
                (name, name_local, type, city, country, website_url, student_count, 
                 ranking_position, description, jurisdiction_id, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, true)
            """, (
                uni['name'], uni['name_local'], uni['type'], uni['city'], uni['country'],
                uni['website_url'], uni['student_count'], uni['ranking_position'],
                uni['description'], jurisdiction_id
            ))
            print(f"Added: {uni['name']}")
        else:
            print(f"Already exists: {uni['name']}")
    
    cursor.close()

def add_finnish_language_schools(conn, jurisdiction_id):
    """Add Finnish language schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Helsinki Summer University',
            'name_local': 'Helsingin kesäyliopisto',
            'type': 'language_school',
            'city': 'Helsinki',
            'website_url': 'https://www.helsinkisummeruniversity.fi',
            'description': 'Finnish language courses for foreigners in Helsinki, offering intensive and part-time programs.'
        },
        {
            'name': 'University of Helsinki Language Centre',
            'name_local': 'Helsingin yliopiston kielikeskus',
            'type': 'language_school',
            'city': 'Helsinki',
            'website_url': 'https://www.helsinki.fi/en/language-centre',
            'description': 'Finnish language courses at University of Helsinki for international students and staff.'
        }
    ]
    
    for school in schools:
        cursor.execute(
            "SELECT id FROM universities WHERE name = %s AND jurisdiction_id = %s",
            (school['name'], jurisdiction_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.execute("""
                INSERT INTO universities 
                (name, name_local, type, city, country, website_url, description, jurisdiction_id, is_active)
                VALUES (%s, %s, %s, %s, 'FI', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added language school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_finnish_conservatories(conn, jurisdiction_id):
    """Add Finnish conservatories with VERIFIED URLs"""
    cursor = conn.cursor()
    
    conservatories = [
        {
            'name': 'Sibelius Academy',
            'name_local': 'Taideyliopiston Sibelius-Akatemia',
            'type': 'conservatory',
            'city': 'Helsinki',
            'website_url': 'https://www.uniarts.fi/en/units/sibelius-academy',
            'description': 'Finland\'s leading music academy, part of University of the Arts Helsinki.'
        }
    ]
    
    for conservatory in conservatories:
        cursor.execute(
            "SELECT id FROM universities WHERE name = %s AND jurisdiction_id = %s",
            (conservatory['name'], jurisdiction_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.execute("""
                INSERT INTO universities 
                (name, name_local, type, city, country, website_url, description, jurisdiction_id, is_active)
                VALUES (%s, %s, %s, %s, 'FI', %s, %s, %s, true)
            """, (
                conservatory['name'], conservatory['name_local'], conservatory['type'], 
                conservatory['city'], conservatory['website_url'], conservatory['description'], 
                jurisdiction_id
            ))
            print(f"Added conservatory: {conservatory['name']}")
        else:
            print(f"Already exists: {conservatory['name']}")
    
    cursor.close()

def main():
    print("Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    
    try:
        jurisdiction_id = get_jurisdiction_id(conn, 'FI')
        if not jurisdiction_id:
            print("Finnish jurisdiction not found!")
            return
        
        print(f"Found Finnish jurisdiction (ID: {jurisdiction_id})")
        
        print("\nAdding Finnish universities...")
        add_finnish_universities(conn, jurisdiction_id)
        
        print("\nAdding Finnish language schools...")
        add_finnish_language_schools(conn, jurisdiction_id)
        
        print("\nAdding Finnish conservatories...")
        add_finnish_conservatories(conn, jurisdiction_id)
        
        print("\nAll Finnish educational institutions added successfully!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nFinnish institutions summary:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        cursor.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
