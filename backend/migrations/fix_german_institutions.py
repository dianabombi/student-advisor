"""
Додавання німецьких закладів з перевіреними посиланнями
Заміна закладів, які не мають робочих URL
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='DE'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_institutions(conn, jurisdiction_id):
    """Add German institutions with verified URLs"""
    cursor = conn.cursor()
    
    institutions = [
        # Vocational Schools
        {
            'name': 'DAA German Employees Academy',
            'name_local': 'Deutsche Angestellten-Akademie',
            'type': 'vocational_school',
            'city': 'Hamburg',
            'website_url': 'https://www.daa.de',
            'description': 'Leading vocational training provider in Germany offering courses in business, IT, and healthcare.'
        },
        {
            'name': 'BFW Vocational Training Center',
            'name_local': 'Berufsförderungswerk',
            'type': 'vocational_school',
            'city': 'Berlin',
            'website_url': 'https://www.bfw.de',
            'description': 'Vocational rehabilitation and training center offering professional courses and certifications.'
        },
        # Foundation Programs
        {
            'name': 'Heidelberg Studienkolleg',
            'name_local': 'Studienkolleg Heidelberg',
            'type': 'foundation_program',
            'city': 'Heidelberg',
            'website_url': 'https://www.uni-heidelberg.de',
            'description': 'Preparatory course at Heidelberg University for international students planning to study in Germany.'
        },
        {
            'name': 'Frankfurt International Preparatory School',
            'name_local': 'Studienkolleg Frankfurt',
            'type': 'foundation_program',
            'city': 'Frankfurt',
            'website_url': 'https://www.uni-frankfurt.de',
            'description': 'Foundation year program preparing international students for German university admission.'
        }
    ]
    
    for inst in institutions:
        cursor.execute(
            "SELECT id FROM universities WHERE name = %s AND jurisdiction_id = %s",
            (inst['name'], jurisdiction_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.execute("""
                INSERT INTO universities 
                (name, name_local, type, city, country, website_url, description, jurisdiction_id, is_active)
                VALUES (%s, %s, %s, %s, 'DE', %s, %s, %s, true)
            """, (
                inst['name'], inst['name_local'], inst['type'], inst['city'],
                inst['website_url'], inst['description'], jurisdiction_id
            ))
            print(f"Added: {inst['name']}")
        else:
            print(f"Already exists: {inst['name']}")
    
    cursor.close()

def main():
    print("Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    
    try:
        jurisdiction_id = get_jurisdiction_id(conn, 'DE')
        if not jurisdiction_id:
            print("German jurisdiction not found!")
            return
        
        print(f"Found German jurisdiction (ID: {jurisdiction_id})")
        print("\nAdding German institutions with verified URLs...")
        add_institutions(conn, jurisdiction_id)
        
        print("\nAll institutions added successfully!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nGerman institutions summary:")
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
