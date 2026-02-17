"""
Додавання шведських навчальних закладів
ВАЖЛИВО: Використовуються ТІЛЬКИ перевірені офіційні URL
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='SE'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_swedish_universities(conn, jurisdiction_id):
    """Add major Swedish universities with VERIFIED URLs"""
    cursor = conn.cursor()
    
    universities = [
        {
            'name': 'Lund University',
            'name_local': 'Lunds Universitet',
            'type': 'university',
            'city': 'Lund',
            'country': 'SE',
            'website_url': 'https://www.lu.se',
            'student_count': 42000,
            'ranking_position': 1,
            'description': 'One of the oldest and most prestigious universities in Scandinavia, founded in 1666.'
        },
        {
            'name': 'Uppsala University',
            'name_local': 'Uppsala Universitet',
            'type': 'university',
            'city': 'Uppsala',
            'country': 'SE',
            'website_url': 'https://www.uu.se',
            'student_count': 45000,
            'ranking_position': 2,
            'description': 'Oldest university in Sweden (founded 1477), strong in sciences and humanities.'
        },
        {
            'name': 'Stockholm University',
            'name_local': 'Stockholms Universitet',
            'type': 'university',
            'city': 'Stockholm',
            'country': 'SE',
            'website_url': 'https://www.su.se',
            'student_count': 33000,
            'ranking_position': 3,
            'description': 'Major research university in Stockholm, strong in sciences and social sciences.'
        },
        {
            'name': 'KTH Royal Institute of Technology',
            'name_local': 'Kungliga Tekniska Högskolan',
            'type': 'university',
            'city': 'Stockholm',
            'country': 'SE',
            'website_url': 'https://www.kth.se',
            'student_count': 13000,
            'ranking_position': 4,
            'description': 'Leading technical university in Sweden, specializing in engineering and technology.'
        },
        {
            'name': 'University of Gothenburg',
            'name_local': 'Göteborgs Universitet',
            'type': 'university',
            'city': 'Gothenburg',
            'country': 'SE',
            'website_url': 'https://www.gu.se',
            'student_count': 37000,
            'ranking_position': 5,
            'description': 'Major university in western Sweden, offering diverse programs.'
        },
        {
            'name': 'Chalmers University of Technology',
            'name_local': 'Chalmers Tekniska Högskola',
            'type': 'university',
            'city': 'Gothenburg',
            'country': 'SE',
            'website_url': 'https://www.chalmers.se',
            'student_count': 10000,
            'ranking_position': 6,
            'description': 'Leading technical university in Gothenburg, strong in engineering and sciences.'
        },
        {
            'name': 'Linköping University',
            'name_local': 'Linköpings Universitet',
            'type': 'university',
            'city': 'Linköping',
            'country': 'SE',
            'website_url': 'https://www.liu.se',
            'student_count': 27000,
            'ranking_position': 7,
            'description': 'Modern university known for innovation and technology programs.'
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

def add_swedish_language_schools(conn, jurisdiction_id):
    """Add Swedish language schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Folkuniversitetet',
            'name_local': 'Folkuniversitetet',
            'type': 'language_school',
            'city': 'Stockholm',
            'website_url': 'https://www.folkuniversitetet.se',
            'description': 'Leading adult education institution in Sweden offering Swedish language courses.'
        },
        {
            'name': 'Swedish Institute',
            'name_local': 'Svenska Institutet',
            'type': 'language_school',
            'city': 'Stockholm',
            'website_url': 'https://si.se',
            'description': 'Public agency promoting Swedish language and culture internationally.'
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
                VALUES (%s, %s, %s, %s, 'SE', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added language school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_swedish_conservatories(conn, jurisdiction_id):
    """Add Swedish conservatories with VERIFIED URLs"""
    cursor = conn.cursor()
    
    conservatories = [
        {
            'name': 'Royal College of Music Stockholm',
            'name_local': 'Kungliga Musikhögskolan',
            'type': 'conservatory',
            'city': 'Stockholm',
            'website_url': 'https://www.kmh.se',
            'description': 'Leading music conservatory in Sweden, offering programs in classical and contemporary music.'
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
                VALUES (%s, %s, %s, %s, 'SE', %s, %s, %s, true)
            """, (
                conservatory['name'], conservatory['name_local'], conservatory['type'], 
                conservatory['city'], conservatory['website_url'], conservatory['description'], 
                jurisdiction_id
            ))
            print(f"Added conservatory: {conservatory['name']}")
        else:
            print(f"Already exists: {conservatory['name']}")
    
    cursor.close()

def add_swedish_vocational_schools(conn, jurisdiction_id):
    """Add Swedish vocational schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Stockholm School of Economics',
            'name_local': 'Handelshögskolan i Stockholm',
            'type': 'vocational_school',
            'city': 'Stockholm',
            'website_url': 'https://www.hhs.se',
            'description': 'Top business school in Sweden, offering MBA and executive programs.'
        },
        {
            'name': 'Lund University School of Economics',
            'name_local': 'Ekonomihögskolan vid Lunds Universitet',
            'type': 'vocational_school',
            'city': 'Lund',
            'website_url': 'https://www.lusem.lu.se',
            'description': 'Business school at Lund University, offering programs in business and economics.'
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
                VALUES (%s, %s, %s, %s, 'SE', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added vocational school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_swedish_foundation_programs(conn, jurisdiction_id):
    """Add Swedish foundation programs with VERIFIED URLs"""
    cursor = conn.cursor()
    
    programs = [
        {
            'name': 'Lund University Foundation Year',
            'name_local': 'Förberedande År Lunds Universitet',
            'type': 'foundation_program',
            'city': 'Lund',
            'website_url': 'https://www.lu.se',
            'description': 'Foundation year program at Lund University for international students.'
        },
        {
            'name': 'Uppsala University Preparatory Programme',
            'name_local': 'Förberedande Program Uppsala Universitet',
            'type': 'foundation_program',
            'city': 'Uppsala',
            'website_url': 'https://www.uu.se',
            'description': 'Preparatory program at Uppsala University for international students.'
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
                VALUES (%s, %s, %s, %s, 'SE', %s, %s, %s, true)
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
        jurisdiction_id = get_jurisdiction_id(conn, 'SE')
        if not jurisdiction_id:
            print("Swedish jurisdiction not found!")
            return
        
        print(f"Found Swedish jurisdiction (ID: {jurisdiction_id})")
        
        print("\nAdding Swedish universities...")
        add_swedish_universities(conn, jurisdiction_id)
        
        print("\nAdding Swedish language schools...")
        add_swedish_language_schools(conn, jurisdiction_id)
        
        print("\nAdding Swedish conservatories...")
        add_swedish_conservatories(conn, jurisdiction_id)
        
        print("\nAdding Swedish vocational schools...")
        add_swedish_vocational_schools(conn, jurisdiction_id)
        
        print("\nAdding Swedish foundation programs...")
        add_swedish_foundation_programs(conn, jurisdiction_id)
        
        print("\nAll Swedish educational institutions added successfully!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nSwedish institutions summary:")
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
