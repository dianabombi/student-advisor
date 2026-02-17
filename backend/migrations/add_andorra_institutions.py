"""
Додавання андоррських навчальних закладів
ВАЖЛИВО: Використовуються ТІЛЬКИ перевірені офіційні URL
Андорра - маленька країна в Піренеях, тому має обмежену кількість закладів
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
        
        # Get Andorra jurisdiction ID
        cursor.execute("SELECT id FROM jurisdictions WHERE code = 'AD'")
        result = cursor.fetchone()
        if not result:
            print("Andorra jurisdiction not found!")
            return
        jurisdiction_id = result[0]
        
        # Andorran institution (very limited due to small size)
        institutions = [
            {
                'name': 'University of Andorra',
                'name_local': 'Universitat d\'Andorra',
                'type': 'university',
                'city': 'Sant Julià de Lòria',
                'website_url': 'https://www.uda.ad',
                'description': 'The only university in Andorra, offering programs in various fields.'
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
                    VALUES (%s, %s, %s, %s, 'AD', %s, %s, %s, true)
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
        
        print("\nAndorra institutions summary:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.execute("""
            SELECT name, website_url 
            FROM universities 
            WHERE jurisdiction_id = %s
            ORDER BY type, name
        """, (jurisdiction_id,))
        
        print("\nAll Andorra institutions:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.close()
        print("\nAndorra institutions added successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
