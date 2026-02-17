"""
Додавання ватиканських католицьких духовних навчальних закладів
ВАЖЛИВО: Використовуються ТІЛЬКИ перевірені офіційні URL
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
        
        # Get Vatican jurisdiction ID
        cursor.execute("SELECT id FROM jurisdictions WHERE code = 'VA'")
        jurisdiction_id = cursor.fetchone()[0]
        
        # Vatican Catholic universities and seminaries
        vatican_institutions = [
            {
                'name': 'Pontifical Gregorian University',
                'name_local': 'Pontificia Università Gregoriana',
                'type': 'university',
                'city': 'Vatican City',
                'website_url': 'https://www.unigre.it',
                'description': 'Jesuit university specializing in theology, philosophy, and canon law.'
            },
            {
                'name': 'Pontifical Lateran University',
                'name_local': 'Pontificia Università Lateranense',
                'type': 'university',
                'city': 'Vatican City',
                'website_url': 'https://www.pul.va',
                'description': 'Papal university offering programs in theology, philosophy, and canon law.'
            },
            {
                'name': 'Pontifical University of Saint Thomas Aquinas',
                'name_local': 'Pontificia Università San Tommaso d\'Aquino',
                'type': 'university',
                'city': 'Vatican City',
                'website_url': 'https://www.pust.it',
                'description': 'Dominican university specializing in Thomistic philosophy and theology.'
            },
            {
                'name': 'Pontifical Biblical Institute',
                'name_local': 'Pontificio Istituto Biblico',
                'type': 'vocational_school',
                'city': 'Vatican City',
                'website_url': 'https://www.biblico.it',
                'description': 'Jesuit institute specializing in biblical studies and ancient Near Eastern languages.'
            },
            {
                'name': 'Pontifical Institute of Sacred Music',
                'name_local': 'Pontificio Istituto di Musica Sacra',
                'type': 'conservatory',
                'city': 'Vatican City',
                'website_url': 'https://www.musicasacra.va',
                'description': 'Institute specializing in sacred music and Gregorian chant.'
            }
        ]
        
        for inst in vatican_institutions:
            cursor.execute(
                "SELECT id FROM universities WHERE name = %s AND jurisdiction_id = %s",
                (inst['name'], jurisdiction_id)
            )
            existing = cursor.fetchone()
            
            if not existing:
                cursor.execute("""
                    INSERT INTO universities 
                    (name, name_local, type, city, country, website_url, description, jurisdiction_id, is_active)
                    VALUES (%s, %s, %s, %s, 'VA', %s, %s, %s, true)
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
        
        print("\nVatican institutions summary:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.execute("""
            SELECT name, website_url 
            FROM universities 
            WHERE jurisdiction_id = %s
            ORDER BY type, name
        """, (jurisdiction_id,))
        
        print("\nAll Vatican institutions:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.close()
        print("\nVatican institutions added successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
