"""
Додавання угорських професійних шкіл
ВАЖЛИВО: Використовуються ТІЛЬКИ перевірені офіційні URL
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='HU'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_vocational_schools(conn, jurisdiction_id):
    """Add Hungarian vocational schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Budapest Business School',
            'name_local': 'Budapesti Gazdasági Egyetem',
            'type': 'vocational_school',
            'city': 'Budapest',
            'website_url': 'https://www.uni-bge.hu',
            'description': 'Leading business and economics vocational university in Hungary.'
        },
        {
            'name': 'Óbuda University',
            'name_local': 'Óbudai Egyetem',
            'type': 'vocational_school',
            'city': 'Budapest',
            'website_url': 'https://www.uni-obuda.hu',
            'description': 'Technical vocational university offering programs in engineering, IT, and applied sciences.'
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
                VALUES (%s, %s, %s, %s, 'HU', %s, %s, %s, true)
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
        jurisdiction_id = get_jurisdiction_id(conn, 'HU')
        if not jurisdiction_id:
            print("Hungarian jurisdiction not found!")
            return
        
        print(f"Found Hungarian jurisdiction (ID: {jurisdiction_id})")
        print("\nAdding Hungarian vocational schools...")
        add_vocational_schools(conn, jurisdiction_id)
        
        print("\nVocational schools added successfully!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nHungarian institutions summary:")
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
