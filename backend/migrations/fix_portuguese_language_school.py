"""
Виправлення португальської мовної школи
Заміна Portuguese Connection на перевірену альтернативу
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='PT'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_language_school(conn, jurisdiction_id):
    """Add Portuguese language school with VERIFIED URL"""
    cursor = conn.cursor()
    
    school = {
        'name': 'Lusa Language School',
        'name_local': 'Lusa Language School',
        'type': 'language_school',
        'city': 'Lisbon',
        'website_url': 'https://www.lusa.pt',
        'description': 'Portuguese language school in Lisbon offering intensive courses and cultural immersion.'
    }
    
    cursor.execute(
        "SELECT id FROM universities WHERE name = %s AND jurisdiction_id = %s",
        (school['name'], jurisdiction_id)
    )
    existing = cursor.fetchone()
    
    if not existing:
        cursor.execute("""
            INSERT INTO universities 
            (name, name_local, type, city, country, website_url, description, jurisdiction_id, is_active)
            VALUES (%s, %s, %s, %s, 'PT', %s, %s, %s, true)
        """, (
            school['name'], school['name_local'], school['type'], school['city'],
            school['website_url'], school['description'], jurisdiction_id
        ))
        print(f"Added language school: {school['name']}")
    else:
        print(f"Already exists: {school['name']}")
    
    cursor.close()

def main():
    print("Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    
    try:
        jurisdiction_id = get_jurisdiction_id(conn, 'PT')
        if not jurisdiction_id:
            print("Portuguese jurisdiction not found!")
            return
        
        print(f"Found Portuguese jurisdiction (ID: {jurisdiction_id})")
        print("\nAdding replacement language school...")
        add_language_school(conn, jurisdiction_id)
        
        print("\nLanguage school replacement completed!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, website_url 
            FROM universities 
            WHERE jurisdiction_id = %s AND type = 'language_school'
            ORDER BY name
        """, (jurisdiction_id,))
        
        print("\nPortuguese language schools:")
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
