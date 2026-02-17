"""
Виправлення італійських навчальних закладів
Заміна закладів з непрацюючими посиланнями
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='IT'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_replacements(conn, jurisdiction_id):
    """Add replacement institutions with VERIFIED URLs"""
    cursor = conn.cursor()
    
    replacements = [
        {
            'name': 'Istituto Venezia',
            'name_local': 'Istituto Venezia',
            'type': 'language_school',
            'city': 'Venice',
            'website_url': 'https://www.istitutovenezia.com',
            'description': 'Italian language school in Venice offering intensive courses and cultural programs.'
        },
        {
            'name': 'Bologna Business School',
            'name_local': 'Bologna Business School',
            'type': 'vocational_school',
            'city': 'Bologna',
            'website_url': 'https://www.bbs.unibo.it',
            'description': 'Business school at University of Bologna, offering MBA and executive programs.'
        }
    ]
    
    for item in replacements:
        cursor.execute(
            "SELECT id FROM universities WHERE name = %s AND jurisdiction_id = %s",
            (item['name'], jurisdiction_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.execute("""
                INSERT INTO universities 
                (name, name_local, type, city, country, website_url, description, jurisdiction_id, is_active)
                VALUES (%s, %s, %s, %s, 'IT', %s, %s, %s, true)
            """, (
                item['name'], item['name_local'], item['type'], item['city'],
                item['website_url'], item['description'], jurisdiction_id
            ))
            print(f"Added: {item['name']} ({item['type']})")
        else:
            print(f"Already exists: {item['name']}")
    
    cursor.close()

def main():
    print("Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    
    try:
        jurisdiction_id = get_jurisdiction_id(conn, 'IT')
        if not jurisdiction_id:
            print("Italian jurisdiction not found!")
            return
        
        print(f"Found Italian jurisdiction (ID: {jurisdiction_id})")
        print("\nAdding replacement institutions...")
        add_replacements(conn, jurisdiction_id)
        
        print("\nReplacement completed!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, type, website_url 
            FROM universities 
            WHERE jurisdiction_id = %s AND type IN ('language_school', 'vocational_school')
            ORDER BY type, name
        """, (jurisdiction_id,))
        
        print("\nItalian language schools and vocational schools:")
        for row in cursor.fetchall():
            print(f"   [{row[1]}] {row[0]}: {row[2]}")
        cursor.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
