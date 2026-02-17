"""
Додавання ірландських навчальних закладів
ВАЖЛИВО: Використовуються ТІЛЬКИ перевірені офіційні URL
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='IE'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_irish_universities(conn, jurisdiction_id):
    """Add major Irish universities with VERIFIED URLs"""
    cursor = conn.cursor()
    
    universities = [
        {
            'name': 'Trinity College Dublin',
            'name_local': 'Trinity College Dublin',
            'type': 'university',
            'city': 'Dublin',
            'country': 'IE',
            'website_url': 'https://www.tcd.ie',
            'student_count': 18000,
            'ranking_position': 1,
            'description': 'Oldest university in Ireland, founded in 1592, strong in humanities and sciences.'
        },
        {
            'name': 'University College Dublin',
            'name_local': 'University College Dublin',
            'type': 'university',
            'city': 'Dublin',
            'country': 'IE',
            'website_url': 'https://www.ucd.ie',
            'student_count': 33000,
            'ranking_position': 2,
            'description': 'Largest university in Ireland, offering diverse programs across all fields.'
        },
        {
            'name': 'National University of Ireland Galway',
            'name_local': 'Ollscoil na hÉireann Gaillimh',
            'type': 'university',
            'city': 'Galway',
            'country': 'IE',
            'website_url': 'https://www.universityofgalway.ie',
            'student_count': 19000,
            'ranking_position': 3,
            'description': 'Major university in western Ireland, strong in Irish language and culture.'
        },
        {
            'name': 'University College Cork',
            'name_local': 'Coláiste na hOllscoile Corcaigh',
            'type': 'university',
            'city': 'Cork',
            'country': 'IE',
            'website_url': 'https://www.ucc.ie',
            'student_count': 22000,
            'ranking_position': 4,
            'description': 'Major university in southern Ireland, offering comprehensive programs.'
        },
        {
            'name': 'Dublin City University',
            'name_local': 'Ollscoil Chathair Bhaile Átha Cliath',
            'type': 'university',
            'city': 'Dublin',
            'country': 'IE',
            'website_url': 'https://www.dcu.ie',
            'student_count': 17000,
            'ranking_position': 5,
            'description': 'Modern university in Dublin, strong in business and technology.'
        },
        {
            'name': 'University of Limerick',
            'name_local': 'Ollscoil Luimnigh',
            'type': 'university',
            'city': 'Limerick',
            'country': 'IE',
            'website_url': 'https://www.ul.ie',
            'student_count': 16000,
            'ranking_position': 6,
            'description': 'University in mid-western Ireland, known for cooperative education.'
        },
        {
            'name': 'Maynooth University',
            'name_local': 'Ollscoil Mhá Nuad',
            'type': 'university',
            'city': 'Maynooth',
            'country': 'IE',
            'website_url': 'https://www.maynoothuniversity.ie',
            'student_count': 13000,
            'ranking_position': 7,
            'description': 'University near Dublin, strong in humanities and social sciences.'
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

def add_irish_language_schools(conn, jurisdiction_id):
    """Add Irish language schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Emerald Cultural Institute',
            'name_local': 'Emerald Cultural Institute',
            'type': 'language_school',
            'city': 'Dublin',
            'website_url': 'https://www.eci.ie',
            'description': 'Language school offering English courses in Dublin.'
        },
        {
            'name': 'Atlas Language School',
            'name_local': 'Atlas Language School',
            'type': 'language_school',
            'city': 'Dublin',
            'website_url': 'https://www.atlaslanguageschool.com',
            'description': 'International language school offering English courses in Dublin.'
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
                VALUES (%s, %s, %s, %s, 'IE', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added language school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_irish_conservatories(conn, jurisdiction_id):
    """Add Irish conservatories with VERIFIED URLs"""
    cursor = conn.cursor()
    
    conservatories = [
        {
            'name': 'Royal Irish Academy of Music',
            'name_local': 'Royal Irish Academy of Music',
            'type': 'conservatory',
            'city': 'Dublin',
            'website_url': 'https://www.riam.ie',
            'description': 'Leading music conservatory in Ireland, offering programs in classical and contemporary music.'
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
                VALUES (%s, %s, %s, %s, 'IE', %s, %s, %s, true)
            """, (
                conservatory['name'], conservatory['name_local'], conservatory['type'], 
                conservatory['city'], conservatory['website_url'], conservatory['description'], 
                jurisdiction_id
            ))
            print(f"Added conservatory: {conservatory['name']}")
        else:
            print(f"Already exists: {conservatory['name']}")
    
    cursor.close()

def add_irish_vocational_schools(conn, jurisdiction_id):
    """Add Irish vocational schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Technological University Dublin',
            'name_local': 'Ollscoil Teicneolaíochta Bhaile Átha Cliath',
            'type': 'vocational_school',
            'city': 'Dublin',
            'website_url': 'https://www.tudublin.ie',
            'description': 'Technological university offering professional programs in engineering and business.'
        },
        {
            'name': 'Griffith College Dublin',
            'name_local': 'Griffith College Dublin',
            'type': 'vocational_school',
            'city': 'Dublin',
            'website_url': 'https://www.griffith.ie',
            'description': 'Private college offering programs in business, law, and media.'
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
                VALUES (%s, %s, %s, %s, 'IE', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added vocational school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_irish_foundation_programs(conn, jurisdiction_id):
    """Add Irish foundation programs with VERIFIED URLs"""
    cursor = conn.cursor()
    
    programs = [
        {
            'name': 'Trinity College Dublin Foundation Year',
            'name_local': 'Trinity College Dublin Foundation Year',
            'type': 'foundation_program',
            'city': 'Dublin',
            'website_url': 'https://www.tcd.ie',
            'description': 'Foundation year program at Trinity College Dublin for international students.'
        },
        {
            'name': 'UCD International Foundation Programme',
            'name_local': 'UCD International Foundation Programme',
            'type': 'foundation_program',
            'city': 'Dublin',
            'website_url': 'https://www.ucd.ie',
            'description': 'Foundation program at University College Dublin for international students.'
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
                VALUES (%s, %s, %s, %s, 'IE', %s, %s, %s, true)
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
        jurisdiction_id = get_jurisdiction_id(conn, 'IE')
        if not jurisdiction_id:
            print("Irish jurisdiction not found!")
            return
        
        print(f"Found Irish jurisdiction (ID: {jurisdiction_id})")
        
        print("\nAdding Irish universities...")
        add_irish_universities(conn, jurisdiction_id)
        
        print("\nAdding Irish language schools...")
        add_irish_language_schools(conn, jurisdiction_id)
        
        print("\nAdding Irish conservatories...")
        add_irish_conservatories(conn, jurisdiction_id)
        
        print("\nAdding Irish vocational schools...")
        add_irish_vocational_schools(conn, jurisdiction_id)
        
        print("\nAdding Irish foundation programs...")
        add_irish_foundation_programs(conn, jurisdiction_id)
        
        print("\nAll Irish educational institutions added successfully!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nIrish institutions summary:")
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
