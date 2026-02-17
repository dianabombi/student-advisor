"""
Додавання монакських навчальних закладів
ВАЖЛИВО: Використовуються ТІЛЬКИ перевірені офіційні URL
Монако - найменша франкомовна країна, тому має дуже обмежену кількість закладів
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def main():
    print("Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    
    try:
        cursor = conn.cursor()
        
        # Get Monaco jurisdiction ID
        cursor.execute("SELECT id FROM jurisdictions WHERE code = 'MC'")
        result = cursor.fetchone()
        if not result:
            print("Monaco jurisdiction not found!")
            return
        jurisdiction_id = result[0]
        
        # Monaco institution (very limited due to extremely small size)
        institutions = [
            {
                'name': 'International University of Monaco',
                'name_local': 'Université Internationale de Monaco',
                'type': 'university',
                'city': 'Monaco',
                'website_url': 'https://www.monaco.edu',
                'description': 'Private business university in Monaco, offering programs in business and finance.'
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
                    VALUES (%s, %s, %s, %s, 'MC', %s, %s, %s, true)
                """, (
                    inst['name'], inst['name_local'], inst['type'], inst['city'],
                    inst['website_url'], inst['description'], jurisdiction_id
                ))
                print(f"Added: {inst['name']}")
            else:
                print(f"Already exists: {inst['name']}")
        
        # Show summary
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nMonaco institutions summary:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.execute("""
            SELECT name, website_url 
            FROM universities 
            WHERE jurisdiction_id = %s
            ORDER BY type, name
        """, (jurisdiction_id,))
        
        print("\nAll Monaco institutions:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.close()
        print("\nMonaco institutions added successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
