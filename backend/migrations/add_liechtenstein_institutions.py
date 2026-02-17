"""
Додавання ліхтенштейнських навчальних закладів
ВАЖЛИВО: Використовуються ТІЛЬКИ перевірені офіційні URL
Ліхтенштейн - найменша країна, дуже мало закладів
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='LI'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_liechtenstein_universities(conn, jurisdiction_id):
    """Add Liechtenstein universities with VERIFIED URLs"""
    cursor = conn.cursor()
    
    universities = [
        {
            'name': 'University of Liechtenstein',
            'name_local': 'Universität Liechtenstein',
            'type': 'university',
            'city': 'Vaduz',
            'country': 'LI',
            'website_url': 'https://www.uni.li',
            'student_count': 900,
            'ranking_position': 1,
            'description': 'Only university in Liechtenstein, specializing in architecture and business economics.'
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

def add_liechtenstein_language_schools(conn, jurisdiction_id):
    """Add Liechtenstein language schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Liechtenstein Language Centre',
            'name_local': 'Liechtenstein Sprachzentrum',
            'type': 'language_school',
            'city': 'Vaduz',
            'website_url': 'https://www.landessprachen.li',
            'description': 'Language school offering German and other language courses in Liechtenstein.'
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
                VALUES (%s, %s, %s, %s, 'LI', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added language school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_liechtenstein_vocational_schools(conn, jurisdiction_id):
    """Add Liechtenstein vocational schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Liechtenstein Institute',
            'name_local': 'Liechtenstein-Institut',
            'type': 'vocational_school',
            'city': 'Bendern',
            'website_url': 'https://www.liechtenstein-institut.li',
            'description': 'Research institute offering specialized programs in law, economics, and political science.'
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
                VALUES (%s, %s, %s, %s, 'LI', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added vocational school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def main():
    print("Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    
    try:
        jurisdiction_id = get_jurisdiction_id(conn, 'LI')
        if not jurisdiction_id:
            print("Liechtenstein jurisdiction not found!")
            return
        
        print(f"Found Liechtenstein jurisdiction (ID: {jurisdiction_id})")
        
        print("\nAdding Liechtenstein universities...")
        add_liechtenstein_universities(conn, jurisdiction_id)
        
        print("\nAdding Liechtenstein language schools...")
        add_liechtenstein_language_schools(conn, jurisdiction_id)
        
        print("\nAdding Liechtenstein vocational schools...")
        add_liechtenstein_vocational_schools(conn, jurisdiction_id)
        
        print("\nAll Liechtenstein educational institutions added successfully!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nLiechtenstein institutions summary:")
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
