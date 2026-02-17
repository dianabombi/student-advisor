"""
Додавання хорватських навчальних закладів
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
        
        # Get Croatia jurisdiction ID
        cursor.execute("SELECT id FROM jurisdictions WHERE code = 'HR'")
        result = cursor.fetchone()
        if not result:
            print("Croatia jurisdiction not found!")
            return
        jurisdiction_id = result[0]
        
        # Croatian institutions
        institutions = [
            # Universities
            {
                'name': 'University of Zagreb',
                'name_local': 'Sveučilište u Zagrebu',
                'type': 'university',
                'city': 'Zagreb',
                'website_url': 'https://www.unizg.hr',
                'description': 'Largest and oldest university in Croatia, founded in 1669.'
            },
            {
                'name': 'University of Split',
                'name_local': 'Sveučilište u Splitu',
                'type': 'university',
                'city': 'Split',
                'website_url': 'https://www.unist.hr',
                'description': 'Major university in Dalmatia region.'
            },
            {
                'name': 'University of Rijeka',
                'name_local': 'Sveučilište u Rijeci',
                'type': 'university',
                'city': 'Rijeka',
                'website_url': 'https://www.uniri.hr',
                'description': 'University in the coastal city of Rijeka.'
            },
            {
                'name': 'University of Osijek',
                'name_local': 'Sveučilište Josipa Jurja Strossmayera u Osijeku',
                'type': 'university',
                'city': 'Osijek',
                'website_url': 'https://www.unios.hr',
                'description': 'University in eastern Croatia.'
            },
            # Language Schools
            {
                'name': 'Croatian Language School',
                'name_local': 'Škola hrvatskog jezika',
                'type': 'language_school',
                'city': 'Zagreb',
                'website_url': 'https://www.croaticum.ffzg.unizg.hr',
                'description': 'Centre for Croatian as a foreign language at University of Zagreb.'
            },
            {
                'name': 'Croaticum',
                'name_local': 'Croaticum - Centar za hrvatski kao drugi i strani jezik',
                'type': 'language_school',
                'city': 'Zagreb',
                'website_url': 'https://www.croaticum.hr',
                'description': 'Centre for Croatian as a second and foreign language.'
            },
            # Conservatory
            {
                'name': 'Zagreb Academy of Music',
                'name_local': 'Muzička akademija u Zagrebu',
                'type': 'conservatory',
                'city': 'Zagreb',
                'website_url': 'https://www.muza.unizg.hr',
                'description': 'Music academy offering programs in classical music.'
            },
            # Vocational Schools
            {
                'name': 'RIT Croatia',
                'name_local': 'RIT Croatia',
                'type': 'vocational_school',
                'city': 'Zagreb',
                'website_url': 'https://www.croatia.rit.edu',
                'description': 'American university campus in Croatia offering professional programs.'
            },
            {
                'name': 'Zagreb School of Economics and Management',
                'name_local': 'Zagrebačka škola ekonomije i managementa',
                'type': 'vocational_school',
                'city': 'Zagreb',
                'website_url': 'https://www.zsem.hr',
                'description': 'Private business school offering professional programs.'
            },
            # Foundation Programs
            {
                'name': 'University of Zagreb Preparatory Course',
                'name_local': 'Pripremni tečaj Sveučilišta u Zagrebu',
                'type': 'foundation_program',
                'city': 'Zagreb',
                'website_url': 'https://www.unizg.hr',
                'description': 'Preparatory program for international students.'
            },
            {
                'name': 'University of Split Foundation Year',
                'name_local': 'Pripremna godina Sveučilišta u Splitu',
                'type': 'foundation_program',
                'city': 'Split',
                'website_url': 'https://www.unist.hr',
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
                    VALUES (%s, %s, %s, %s, 'HR', %s, %s, %s, true)
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
        
        print("\nCroatia institutions summary:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.close()
        print("\nCroatia institutions added successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
