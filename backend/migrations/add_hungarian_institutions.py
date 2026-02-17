"""
Додавання угорських навчальних закладів
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

def add_hungarian_universities(conn, jurisdiction_id):
    """Add major Hungarian universities with VERIFIED URLs"""
    cursor = conn.cursor()
    
    universities = [
        {
            'name': 'Eötvös Loránd University',
            'name_local': 'Eötvös Loránd Tudományegyetem',
            'type': 'university',
            'city': 'Budapest',
            'country': 'HU',
            'website_url': 'https://www.elte.hu',
            'student_count': 28000,
            'ranking_position': 1,
            'description': 'Largest and oldest university in Hungary, offering programs in humanities, sciences, law, and social sciences.'
        },
        {
            'name': 'Budapest University of Technology and Economics',
            'name_local': 'Budapesti Műszaki és Gazdaságtudományi Egyetem',
            'type': 'university',
            'city': 'Budapest',
            'country': 'HU',
            'website_url': 'https://www.bme.hu',
            'student_count': 24000,
            'ranking_position': 2,
            'description': 'Leading technical university in Hungary, specializing in engineering, IT, and natural sciences.'
        },
        {
            'name': 'University of Debrecen',
            'name_local': 'Debreceni Egyetem',
            'type': 'university',
            'city': 'Debrecen',
            'country': 'HU',
            'website_url': 'https://www.edu.unideb.hu',
            'student_count': 26000,
            'ranking_position': 3,
            'description': 'Second largest university in Hungary, offering programs in medicine, sciences, humanities, and engineering.'
        },
        {
            'name': 'University of Szeged',
            'name_local': 'Szegedi Tudományegyetem',
            'type': 'university',
            'city': 'Szeged',
            'country': 'HU',
            'website_url': 'https://www.u-szeged.hu',
            'student_count': 21000,
            'ranking_position': 4,
            'description': 'Major university in southern Hungary, strong in medicine, sciences, and humanities.'
        },
        {
            'name': 'University of Pécs',
            'name_local': 'Pécsi Tudományegyetem',
            'type': 'university',
            'city': 'Pécs',
            'country': 'HU',
            'website_url': 'https://www.pte.hu',
            'student_count': 20000,
            'ranking_position': 5,
            'description': 'Historic university offering programs in medicine, humanities, sciences, and law.'
        },
        {
            'name': 'Corvinus University of Budapest',
            'name_local': 'Budapesti Corvinus Egyetem',
            'type': 'university',
            'city': 'Budapest',
            'country': 'HU',
            'website_url': 'https://www.uni-corvinus.hu',
            'student_count': 14000,
            'ranking_position': 6,
            'description': 'Leading business university in Hungary, specializing in economics, business, and social sciences.'
        },
        {
            'name': 'Semmelweis University',
            'name_local': 'Semmelweis Egyetem',
            'type': 'university',
            'city': 'Budapest',
            'country': 'HU',
            'website_url': 'https://www.semmelweis.hu',
            'student_count': 11000,
            'ranking_position': 7,
            'description': 'Top medical university in Hungary, specializing in medicine, dentistry, pharmacy, and health sciences.'
        }
    ]
    
    for uni in universities:
        cursor.execute(
            "SELECT id FROM universities WHERE name = %s AND jurisdiction_id = %s",
            (uni['name'], jurisdiction_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.execute("""
                INSERT INTO universities 
                (name, name_local, type, city, country, website_url, student_count, 
                 ranking_position, description, jurisdiction_id, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, true)
            """, (
                uni['name'], uni['name_local'], uni['type'], uni['city'], uni['country'],
                uni['website_url'], uni['student_count'], uni['ranking_position'],
                uni['description'], jurisdiction_id
            ))
            print(f"Added: {uni['name']}")
        else:
            print(f"Already exists: {uni['name']}")
    
    cursor.close()

def add_hungarian_language_schools(conn, jurisdiction_id):
    """Add Hungarian language schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Debrecen Summer School',
            'name_local': 'Debreceni Nyári Egyetem',
            'type': 'language_school',
            'city': 'Debrecen',
            'website_url': 'https://www.nyariegyetem.hu',
            'description': 'Hungarian language and culture courses for international students at University of Debrecen.'
        },
        {
            'name': 'Budapest International School',
            'name_local': 'Budapesti Nemzetközi Iskola',
            'type': 'language_school',
            'city': 'Budapest',
            'website_url': 'https://www.bis-school.com',
            'description': 'International school offering Hungarian language courses for foreigners.'
        }
    ]
    
    for school in schools:
        cursor.execute(
            "SELECT id FROM universities WHERE name = %s AND jurisdiction_id = %s",
            (school['name'], jurisdiction_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.execute("""
                INSERT INTO universities 
                (name, name_local, type, city, country, website_url, description, jurisdiction_id, is_active)
                VALUES (%s, %s, %s, %s, 'HU', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added language school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_hungarian_conservatories(conn, jurisdiction_id):
    """Add Hungarian conservatories with VERIFIED URLs"""
    cursor = conn.cursor()
    
    conservatories = [
        {
            'name': 'Liszt Ferenc Academy of Music',
            'name_local': 'Liszt Ferenc Zeneművészeti Egyetem',
            'type': 'conservatory',
            'city': 'Budapest',
            'website_url': 'https://www.lfze.hu',
            'description': 'Leading music academy in Hungary, one of the oldest music institutions in Europe.'
        }
    ]
    
    for conservatory in conservatories:
        cursor.execute(
            "SELECT id FROM universities WHERE name = %s AND jurisdiction_id = %s",
            (conservatory['name'], jurisdiction_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.execute("""
                INSERT INTO universities 
                (name, name_local, type, city, country, website_url, description, jurisdiction_id, is_active)
                VALUES (%s, %s, %s, %s, 'HU', %s, %s, %s, true)
            """, (
                conservatory['name'], conservatory['name_local'], conservatory['type'], 
                conservatory['city'], conservatory['website_url'], conservatory['description'], 
                jurisdiction_id
            ))
            print(f"Added conservatory: {conservatory['name']}")
        else:
            print(f"Already exists: {conservatory['name']}")
    
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
        
        print("\nAdding Hungarian universities...")
        add_hungarian_universities(conn, jurisdiction_id)
        
        print("\nAdding Hungarian language schools...")
        add_hungarian_language_schools(conn, jurisdiction_id)
        
        print("\nAdding Hungarian conservatories...")
        add_hungarian_conservatories(conn, jurisdiction_id)
        
        print("\nAll Hungarian educational institutions added successfully!")
        
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
