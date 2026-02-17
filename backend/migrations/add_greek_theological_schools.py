"""
Додавання грецьких православних духовних навчальних закладів
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
        
        # Get Greek jurisdiction ID
        cursor.execute("SELECT id FROM jurisdictions WHERE code = 'GR'")
        jurisdiction_id = cursor.fetchone()[0]
        
        # Greek Orthodox theological schools
        theological_schools = [
            {
                'name': 'School of Theology - University of Athens',
                'name_local': 'Θεολογική Σχολή Πανεπιστημίου Αθηνών',
                'type': 'university',
                'city': 'Athens',
                'website_url': 'https://www.theol.uoa.gr',
                'description': 'Faculty of Theology at the University of Athens, offering Orthodox theological education.'
            },
            {
                'name': 'School of Theology - Aristotle University',
                'name_local': 'Θεολογική Σχολή ΑΠΘ',
                'type': 'university',
                'city': 'Thessaloniki',
                'website_url': 'https://www.theo.auth.gr',
                'description': 'Faculty of Theology at Aristotle University, specializing in Orthodox theology.'
            },
            {
                'name': 'Theological School of Halki',
                'name_local': 'Θεολογική Σχολή Χάλκης',
                'type': 'vocational_school',
                'city': 'Istanbul',
                'website_url': 'https://www.halki.org',
                'description': 'Historic Greek Orthodox seminary, affiliated with the Ecumenical Patriarchate.'
            },
            {
                'name': 'Apostoliki Diakonia',
                'name_local': 'Αποστολική Διακονία',
                'type': 'vocational_school',
                'city': 'Athens',
                'website_url': 'https://www.apostoliki-diakonia.gr',
                'description': 'Educational institution of the Church of Greece, offering theological programs.'
            },
            {
                'name': 'Patriarchal Institute for Patristic Studies',
                'name_local': 'Πατριαρχικόν Ίδρυμα Πατερικών Μελετών',
                'type': 'vocational_school',
                'city': 'Thessaloniki',
                'website_url': 'https://www.pims.gr',
                'description': 'Institute specializing in patristic studies and Orthodox theology.'
            }
        ]
        
        for school in theological_schools:
            cursor.execute(
                "SELECT id FROM universities WHERE name = %s AND jurisdiction_id = %s",
                (school['name'], jurisdiction_id)
            )
            existing = cursor.fetchone()
            
            if not existing:
                cursor.execute("""
                    INSERT INTO universities 
                    (name, name_local, type, city, country, website_url, description, jurisdiction_id, is_active)
                    VALUES (%s, %s, %s, %s, 'GR', %s, %s, %s, true)
                """, (
                    school['name'], school['name_local'], school['type'], school['city'],
                    school['website_url'], school['description'], jurisdiction_id
                ))
                print(f"Added: {school['name']}")
            else:
                print(f"Already exists: {school['name']}")
        
        # Show summary
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nGreek institutions after adding theological schools:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.execute("""
            SELECT name, website_url 
            FROM universities 
            WHERE jurisdiction_id = %s AND (
                name LIKE '%Theolog%' OR 
                name LIKE '%Seminary%' OR 
                name LIKE '%Halki%' OR 
                name LIKE '%Apostoliki%' OR 
                name LIKE '%Patristic%'
            )
            ORDER BY name
        """, (jurisdiction_id,))
        
        print("\nGreek theological schools:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.close()
        print("\nGreek theological schools added successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
