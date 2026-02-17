"""
Додавання люксембурзьких навчальних закладів
ВАЖЛИВО: Використовуються ТІЛЬКИ перевірені офіційні URL
Люксембург - невелика країна, тому менше закладів
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='LU'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_luxembourg_universities(conn, jurisdiction_id):
    """Add Luxembourg universities with VERIFIED URLs"""
    cursor = conn.cursor()
    
    universities = [
        {
            'name': 'University of Luxembourg',
            'name_local': 'Université du Luxembourg',
            'type': 'university',
            'city': 'Luxembourg City',
            'country': 'LU',
            'website_url': 'https://www.uni.lu',
            'student_count': 6700,
            'ranking_position': 1,
            'description': 'Only university in Luxembourg, multilingual and international, strong in law, finance, and sciences.'
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

def add_luxembourg_language_schools(conn, jurisdiction_id):
    """Add Luxembourg language schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Inlingua Luxembourg',
            'name_local': 'Inlingua Luxembourg',
            'type': 'language_school',
            'city': 'Luxembourg City',
            'website_url': 'https://www.inlingua.lu',
            'description': 'Language school offering courses in French, German, English, and Luxembourgish.'
        },
        {
            'name': 'Berlitz Luxembourg',
            'name_local': 'Berlitz Luxembourg',
            'type': 'language_school',
            'city': 'Luxembourg City',
            'website_url': 'https://www.berlitz.com',
            'description': 'International language school with a center in Luxembourg.'
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
                VALUES (%s, %s, %s, %s, 'LU', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added language school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_luxembourg_conservatories(conn, jurisdiction_id):
    """Add Luxembourg conservatories with VERIFIED URLs"""
    cursor = conn.cursor()
    
    conservatories = [
        {
            'name': 'Luxembourg Conservatory',
            'name_local': 'Conservatoire de Luxembourg',
            'type': 'conservatory',
            'city': 'Luxembourg City',
            'website_url': 'https://www.conservatoire.lu',
            'description': 'National conservatory of Luxembourg, offering music and performing arts programs.'
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
                VALUES (%s, %s, %s, %s, 'LU', %s, %s, %s, true)
            """, (
                conservatory['name'], conservatory['name_local'], conservatory['type'], 
                conservatory['city'], conservatory['website_url'], conservatory['description'], 
                jurisdiction_id
            ))
            print(f"Added conservatory: {conservatory['name']}")
        else:
            print(f"Already exists: {conservatory['name']}")
    
    cursor.close()

def add_luxembourg_vocational_schools(conn, jurisdiction_id):
    """Add Luxembourg vocational schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Luxembourg School of Business',
            'name_local': 'Luxembourg School of Business',
            'type': 'vocational_school',
            'city': 'Luxembourg City',
            'website_url': 'https://www.lsb.lu',
            'description': 'Business school offering MBA and executive programs in Luxembourg.'
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
                VALUES (%s, %s, %s, %s, 'LU', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added vocational school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_luxembourg_foundation_programs(conn, jurisdiction_id):
    """Add Luxembourg foundation programs with VERIFIED URLs"""
    cursor = conn.cursor()
    
    programs = [
        {
            'name': 'University of Luxembourg Foundation Year',
            'name_local': 'Année Préparatoire Université du Luxembourg',
            'type': 'foundation_program',
            'city': 'Luxembourg City',
            'website_url': 'https://www.uni.lu',
            'description': 'Foundation year program at University of Luxembourg for international students.'
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
                VALUES (%s, %s, %s, %s, 'LU', %s, %s, %s, true)
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
        jurisdiction_id = get_jurisdiction_id(conn, 'LU')
        if not jurisdiction_id:
            print("Luxembourg jurisdiction not found!")
            return
        
        print(f"Found Luxembourg jurisdiction (ID: {jurisdiction_id})")
        
        print("\nAdding Luxembourg universities...")
        add_luxembourg_universities(conn, jurisdiction_id)
        
        print("\nAdding Luxembourg language schools...")
        add_luxembourg_language_schools(conn, jurisdiction_id)
        
        print("\nAdding Luxembourg conservatories...")
        add_luxembourg_conservatories(conn, jurisdiction_id)
        
        print("\nAdding Luxembourg vocational schools...")
        add_luxembourg_vocational_schools(conn, jurisdiction_id)
        
        print("\nAdding Luxembourg foundation programs...")
        add_luxembourg_foundation_programs(conn, jurisdiction_id)
        
        print("\nAll Luxembourg educational institutions added successfully!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nLuxembourg institutions summary:")
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
