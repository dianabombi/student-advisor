"""
Додавання словенських навчальних закладів
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
        
        # Get Slovenia jurisdiction ID
        cursor.execute("SELECT id FROM jurisdictions WHERE code = 'SI'")
        result = cursor.fetchone()
        if not result:
            print("Slovenia jurisdiction not found!")
            return
        jurisdiction_id = result[0]
        
        # Slovenian institutions
        institutions = [
            # Universities
            {
                'name': 'University of Ljubljana',
                'name_local': 'Univerza v Ljubljani',
                'type': 'university',
                'city': 'Ljubljana',
                'website_url': 'https://www.uni-lj.si',
                'description': 'Largest and oldest university in Slovenia, founded in 1919.'
            },
            {
                'name': 'University of Maribor',
                'name_local': 'Univerza v Mariboru',
                'type': 'university',
                'city': 'Maribor',
                'website_url': 'https://www.um.si',
                'description': 'Second largest university in Slovenia.'
            },
            {
                'name': 'University of Primorska',
                'name_local': 'Univerza na Primorskem',
                'type': 'university',
                'city': 'Koper',
                'website_url': 'https://www.upr.si',
                'description': 'University in coastal Slovenia.'
            },
            {
                'name': 'University of Nova Gorica',
                'name_local': 'Univerza v Novi Gorici',
                'type': 'university',
                'city': 'Nova Gorica',
                'website_url': 'https://www.ung.si',
                'description': 'Private research university in western Slovenia.'
            },
            # Language Schools
            {
                'name': 'Ljubljana Language School',
                'name_local': 'Jezikovna šola Ljubljana',
                'type': 'language_school',
                'city': 'Ljubljana',
                'website_url': 'https://www.jezikovna-sola.si',
                'description': 'Language school offering Slovenian and other language courses.'
            },
            {
                'name': 'Slovenian Language Centre',
                'name_local': 'Center za slovenščino kot drugi jezik',
                'type': 'language_school',
                'city': 'Ljubljana',
                'website_url': 'https://www.centerslo.si',
                'description': 'Centre for Slovenian as a second language.'
            },
            # Conservatory
            {
                'name': 'Academy of Music Ljubljana',
                'name_local': 'Akademija za glasbo',
                'type': 'conservatory',
                'city': 'Ljubljana',
                'website_url': 'https://www.ag.uni-lj.si',
                'description': 'Music academy offering programs in classical music.'
            },
            # Vocational Schools
            {
                'name': 'DOBA Business School',
                'name_local': 'DOBA Fakulteta',
                'type': 'vocational_school',
                'city': 'Maribor',
                'website_url': 'https://www.doba.si',
                'description': 'Business school offering professional programs.'
            },
            {
                'name': 'GEA College',
                'name_local': 'GEA College',
                'type': 'vocational_school',
                'city': 'Ljubljana',
                'website_url': 'https://www.gea-college.si',
                'description': 'College offering professional programs in business and tourism.'
            },
            # Foundation Programs
            {
                'name': 'University of Ljubljana Preparatory Course',
                'name_local': 'Pripravni tečaj Univerze v Ljubljani',
                'type': 'foundation_program',
                'city': 'Ljubljana',
                'website_url': 'https://www.uni-lj.si',
                'description': 'Preparatory program for international students.'
            },
            {
                'name': 'University of Maribor Foundation Year',
                'name_local': 'Pripravno leto Univerze v Mariboru',
                'type': 'foundation_program',
                'city': 'Maribor',
                'website_url': 'https://www.um.si',
                'description': 'Foundation year program for international students.'
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
                    VALUES (%s, %s, %s, %s, 'SI', %s, %s, %s, true)
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
        
        print("\nSlovenia institutions summary:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.close()
        print("\nSlovenia institutions added successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
