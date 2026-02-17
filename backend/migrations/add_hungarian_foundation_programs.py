"""
Додавання угорських підготовчих програм
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

def add_foundation_programs(conn, jurisdiction_id):
    """Add Hungarian foundation/preparatory programs with VERIFIED URLs"""
    cursor = conn.cursor()
    
    programs = [
        {
            'name': 'University of Debrecen Preparatory Program',
            'name_local': 'Debreceni Egyetem Előkészítő Program',
            'type': 'foundation_program',
            'city': 'Debrecen',
            'website_url': 'https://www.edu.unideb.hu',
            'description': 'Foundation year program at University of Debrecen preparing international students for Hungarian university studies.'
        },
        {
            'name': 'Budapest Preparatory Course',
            'name_local': 'Budapesti Előkészítő Tanfolyam',
            'type': 'foundation_program',
            'city': 'Budapest',
            'website_url': 'https://www.elte.hu',
            'description': 'Preparatory program at ELTE University for international students planning to study in Hungary.'
        }
    ]
    
    for prog in programs:
        cursor.execute(
            "SELECT id FROM universities WHERE name = %s AND jurisdiction_id = %s",
            (prog['name'], jurisdiction_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.execute("""
                INSERT INTO universities 
                (name, name_local, type, city, country, website_url, description, jurisdiction_id, is_active)
                VALUES (%s, %s, %s, %s, 'HU', %s, %s, %s, true)
            """, (
                prog['name'], prog['name_local'], prog['type'], prog['city'],
                prog['website_url'], prog['description'], jurisdiction_id
            ))
            print(f"Added foundation program: {prog['name']}")
        else:
            print(f"Already exists: {prog['name']}")
    
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
        print("\nAdding Hungarian foundation programs...")
        add_foundation_programs(conn, jurisdiction_id)
        
        print("\nFoundation programs added successfully!")
        
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
