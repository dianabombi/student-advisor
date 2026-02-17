"""
Додавання фінських професійних шкіл (vocational schools)
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

def add_vocational_schools(conn, jurisdiction_id):
    """Add Finnish vocational schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Omnia Vocational College',
            'name_local': 'Ammattiopisto Omnia',
            'type': 'vocational_school',
            'city': 'Espoo',
            'website_url': 'https://www.omnia.fi/en',
            'description': 'Large vocational college in Helsinki region offering programs in business, technology, and social services.'
        },
        {
            'name': 'Stadin ammattiopisto',
            'name_local': 'Stadin ammattiopisto',
            'type': 'vocational_school',
            'city': 'Helsinki',
            'website_url': 'https://www.hel.fi/stadin-ammattiopisto/en',
            'description': 'Helsinki vocational college offering diverse vocational education and training programs.'
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
            print(f"Added vocational school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
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
        print("\nAdding Finnish vocational schools...")
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
