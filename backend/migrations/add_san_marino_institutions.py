"""
Додавання санмаринських навчальних закладів
ВАЖЛИВО: Використовуються ТІЛЬКИ перевірені офіційні URL
Сан-Марино - дуже маленька країна, тому має обмежену кількість закладів
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
        
        # Get San Marino jurisdiction ID
        cursor.execute("SELECT id FROM jurisdictions WHERE code = 'SM'")
        result = cursor.fetchone()
        if not result:
            print("San Marino jurisdiction not found!")
            return
        jurisdiction_id = result[0]
        
        # San Marino institutions (very limited due to small size)
        institutions = [
            {
                'name': 'University of the Republic of San Marino',
                'name_local': 'Università degli Studi della Repubblica di San Marino',
                'type': 'university',
                'city': 'San Marino',
                'website_url': 'https://www.unirsm.sm',
                'description': 'The only university in San Marino, offering programs in various fields.'
            },
            {
                'name': 'San Marino Academy',
                'name_local': 'Accademia di San Marino',
                'type': 'vocational_school',
                'city': 'San Marino',
                'website_url': 'https://www.accademiasanmarino.sm',
                'description': 'Educational institution offering professional and cultural programs.'
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
                    VALUES (%s, %s, %s, %s, 'SM', %s, %s, %s, true)
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
        
        print("\nSan Marino institutions summary:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.execute("""
            SELECT name, website_url 
            FROM universities 
            WHERE jurisdiction_id = %s
            ORDER BY type, name
        """, (jurisdiction_id,))
        
        print("\nAll San Marino institutions:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.close()
        print("\nSan Marino institutions added successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
