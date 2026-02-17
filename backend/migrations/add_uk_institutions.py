"""
Додавання британських навчальних закладів
ВАЖЛИВО: Використовуються ТІЛЬКИ перевірені офіційні URL
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='GB'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_uk_universities(conn, jurisdiction_id):
    """Add major UK universities with VERIFIED URLs"""
    cursor = conn.cursor()
    
    universities = [
        {
            'name': 'University of Oxford',
            'name_local': 'University of Oxford',
            'type': 'university',
            'city': 'Oxford',
            'country': 'GB',
            'website_url': 'https://www.ox.ac.uk',
            'student_count': 24000,
            'ranking_position': 1,
            'description': 'Oldest university in the English-speaking world, consistently ranked among the world\'s best.'
        },
        {
            'name': 'University of Cambridge',
            'name_local': 'University of Cambridge',
            'type': 'university',
            'city': 'Cambridge',
            'country': 'GB',
            'website_url': 'https://www.cam.ac.uk',
            'student_count': 24000,
            'ranking_position': 2,
            'description': 'Second-oldest university in the English-speaking world, world-leading in research and teaching.'
        },
        {
            'name': 'Imperial College London',
            'name_local': 'Imperial College London',
            'type': 'university',
            'city': 'London',
            'country': 'GB',
            'website_url': 'https://www.imperial.ac.uk',
            'student_count': 19000,
            'ranking_position': 3,
            'description': 'Leading science, engineering, medicine and business university in London.'
        },
        {
            'name': 'University College London',
            'name_local': 'University College London',
            'type': 'university',
            'city': 'London',
            'country': 'GB',
            'website_url': 'https://www.ucl.ac.uk',
            'student_count': 42000,
            'ranking_position': 4,
            'description': 'London\'s leading multidisciplinary university, with excellence across the arts and sciences.'
        },
        {
            'name': 'University of Edinburgh',
            'name_local': 'University of Edinburgh',
            'type': 'university',
            'city': 'Edinburgh',
            'country': 'GB',
            'website_url': 'https://www.ed.ac.uk',
            'student_count': 35000,
            'ranking_position': 5,
            'description': 'One of Scotland\'s ancient universities, world-leading in research and teaching.'
        },
        {
            'name': 'King\'s College London',
            'name_local': 'King\'s College London',
            'type': 'university',
            'city': 'London',
            'country': 'GB',
            'website_url': 'https://www.kcl.ac.uk',
            'student_count': 33000,
            'ranking_position': 6,
            'description': 'One of England\'s oldest and most prestigious universities, strong in humanities, law, and sciences.'
        },
        {
            'name': 'University of Manchester',
            'name_local': 'University of Manchester',
            'type': 'university',
            'city': 'Manchester',
            'country': 'GB',
            'website_url': 'https://www.manchester.ac.uk',
            'student_count': 40000,
            'ranking_position': 7,
            'description': 'Major research university, birthplace of the computer and splitting of the atom.'
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

def add_uk_language_schools(conn, jurisdiction_id):
    """Add UK language schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'British Council London',
            'name_local': 'British Council London',
            'type': 'language_school',
            'city': 'London',
            'website_url': 'https://www.britishcouncil.org',
            'description': 'World-renowned English language courses from the British Council in London.'
        },
        {
            'name': 'International House London',
            'name_local': 'International House London',
            'type': 'language_school',
            'city': 'London',
            'website_url': 'https://www.ihlondon.com',
            'description': 'Leading English language school in London offering courses for all levels.'
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
                VALUES (%s, %s, %s, %s, 'GB', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added language school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_uk_conservatories(conn, jurisdiction_id):
    """Add UK conservatories with VERIFIED URLs"""
    cursor = conn.cursor()
    
    conservatories = [
        {
            'name': 'Royal College of Music',
            'name_local': 'Royal College of Music',
            'type': 'conservatory',
            'city': 'London',
            'website_url': 'https://www.rcm.ac.uk',
            'description': 'Leading conservatoire in London, training musicians for international careers.'
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
                VALUES (%s, %s, %s, %s, 'GB', %s, %s, %s, true)
            """, (
                conservatory['name'], conservatory['name_local'], conservatory['type'], 
                conservatory['city'], conservatory['website_url'], conservatory['description'], 
                jurisdiction_id
            ))
            print(f"Added conservatory: {conservatory['name']}")
        else:
            print(f"Already exists: {conservatory['name']}")
    
    cursor.close()

def add_uk_vocational_schools(conn, jurisdiction_id):
    """Add UK vocational schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'London Business School',
            'name_local': 'London Business School',
            'type': 'vocational_school',
            'city': 'London',
            'website_url': 'https://www.london.edu',
            'description': 'World-leading business school offering MBA and executive education programs.'
        },
        {
            'name': 'London School of Economics',
            'name_local': 'London School of Economics and Political Science',
            'type': 'vocational_school',
            'city': 'London',
            'website_url': 'https://www.lse.ac.uk',
            'description': 'Specialist university in social sciences, consistently ranked among the world\'s best.'
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
                VALUES (%s, %s, %s, %s, 'GB', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added vocational school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_uk_foundation_programs(conn, jurisdiction_id):
    """Add UK foundation programs with VERIFIED URLs"""
    cursor = conn.cursor()
    
    programs = [
        {
            'name': 'UCL Foundation Programme',
            'name_local': 'UCL Undergraduate Preparatory Certificate',
            'type': 'foundation_program',
            'city': 'London',
            'website_url': 'https://www.ucl.ac.uk',
            'description': 'Foundation year program at UCL for international students.'
        },
        {
            'name': 'King\'s College Foundation Year',
            'name_local': 'King\'s International Foundation Programme',
            'type': 'foundation_program',
            'city': 'London',
            'website_url': 'https://www.kcl.ac.uk',
            'description': 'Preparatory program at King\'s College London for international students.'
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
                VALUES (%s, %s, %s, %s, 'GB', %s, %s, %s, true)
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
        jurisdiction_id = get_jurisdiction_id(conn, 'GB')
        if not jurisdiction_id:
            print("UK jurisdiction not found!")
            return
        
        print(f"Found UK jurisdiction (ID: {jurisdiction_id})")
        
        print("\nAdding UK universities...")
        add_uk_universities(conn, jurisdiction_id)
        
        print("\nAdding UK language schools...")
        add_uk_language_schools(conn, jurisdiction_id)
        
        print("\nAdding UK conservatories...")
        add_uk_conservatories(conn, jurisdiction_id)
        
        print("\nAdding UK vocational schools...")
        add_uk_vocational_schools(conn, jurisdiction_id)
        
        print("\nAdding UK foundation programs...")
        add_uk_foundation_programs(conn, jurisdiction_id)
        
        print("\nAll UK educational institutions added successfully!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nUK institutions summary:")
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
