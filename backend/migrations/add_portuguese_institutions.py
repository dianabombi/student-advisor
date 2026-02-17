"""
Додавання португальських навчальних закладів
ВАЖЛИВО: Використовуються ТІЛЬКИ перевірені офіційні URL
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='PT'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_portuguese_universities(conn, jurisdiction_id):
    """Add major Portuguese universities with VERIFIED URLs"""
    cursor = conn.cursor()
    
    universities = [
        {
            'name': 'University of Lisbon',
            'name_local': 'Universidade de Lisboa',
            'type': 'university',
            'city': 'Lisbon',
            'country': 'PT',
            'website_url': 'https://www.ulisboa.pt',
            'student_count': 50000,
            'ranking_position': 1,
            'description': 'Largest university in Portugal, offering programs in all major fields.'
        },
        {
            'name': 'University of Porto',
            'name_local': 'Universidade do Porto',
            'type': 'university',
            'city': 'Porto',
            'country': 'PT',
            'website_url': 'https://www.up.pt',
            'student_count': 32000,
            'ranking_position': 2,
            'description': 'Leading university in northern Portugal, strong in sciences and engineering.'
        },
        {
            'name': 'University of Coimbra',
            'name_local': 'Universidade de Coimbra',
            'type': 'university',
            'city': 'Coimbra',
            'country': 'PT',
            'website_url': 'https://www.uc.pt',
            'student_count': 25000,
            'ranking_position': 3,
            'description': 'One of the oldest universities in the world (founded 1290), UNESCO World Heritage site.'
        },
        {
            'name': 'NOVA University Lisbon',
            'name_local': 'Universidade NOVA de Lisboa',
            'type': 'university',
            'city': 'Lisbon',
            'country': 'PT',
            'website_url': 'https://www.unl.pt',
            'student_count': 20000,
            'ranking_position': 4,
            'description': 'Modern research university in Lisbon, strong in sciences and social sciences.'
        },
        {
            'name': 'University of Minho',
            'name_local': 'Universidade do Minho',
            'type': 'university',
            'city': 'Braga',
            'country': 'PT',
            'website_url': 'https://www.uminho.pt',
            'student_count': 19000,
            'ranking_position': 5,
            'description': 'Public university in northern Portugal, known for engineering and sciences.'
        },
        {
            'name': 'University of Aveiro',
            'name_local': 'Universidade de Aveiro',
            'type': 'university',
            'city': 'Aveiro',
            'country': 'PT',
            'website_url': 'https://www.ua.pt',
            'student_count': 15000,
            'ranking_position': 6,
            'description': 'Young dynamic university, strong in technology and innovation.'
        },
        {
            'name': 'Catholic University of Portugal',
            'name_local': 'Universidade Católica Portuguesa',
            'type': 'university',
            'city': 'Lisbon',
            'country': 'PT',
            'website_url': 'https://www.ucp.pt',
            'student_count': 13000,
            'ranking_position': 7,
            'description': 'Private Catholic university with campuses across Portugal, strong in business and law.'
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

def add_portuguese_language_schools(conn, jurisdiction_id):
    """Add Portuguese language schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'CIAL Centro de Línguas',
            'name_local': 'CIAL Centro de Línguas',
            'type': 'language_school',
            'city': 'Lisbon',
            'website_url': 'https://www.cial.pt',
            'description': 'Leading Portuguese language school in Lisbon offering intensive courses.'
        },
        {
            'name': 'Portuguese Connection',
            'name_local': 'Portuguese Connection',
            'type': 'language_school',
            'city': 'Porto',
            'website_url': 'https://www.portugueseconnection.com',
            'description': 'Portuguese language school in Porto offering immersive language programs.'
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
                VALUES (%s, %s, %s, %s, 'PT', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added language school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_portuguese_conservatories(conn, jurisdiction_id):
    """Add Portuguese conservatories with VERIFIED URLs"""
    cursor = conn.cursor()
    
    conservatories = [
        {
            'name': 'National Conservatory of Lisbon',
            'name_local': 'Conservatório Nacional de Lisboa',
            'type': 'conservatory',
            'city': 'Lisbon',
            'website_url': 'https://www.emcn.edu.pt',
            'description': 'Leading music conservatory in Portugal, offering programs in classical music.'
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
                VALUES (%s, %s, %s, %s, 'PT', %s, %s, %s, true)
            """, (
                conservatory['name'], conservatory['name_local'], conservatory['type'], 
                conservatory['city'], conservatory['website_url'], conservatory['description'], 
                jurisdiction_id
            ))
            print(f"Added conservatory: {conservatory['name']}")
        else:
            print(f"Already exists: {conservatory['name']}")
    
    cursor.close()

def add_portuguese_vocational_schools(conn, jurisdiction_id):
    """Add Portuguese vocational schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'NOVA School of Business and Economics',
            'name_local': 'NOVA School of Business and Economics',
            'type': 'vocational_school',
            'city': 'Lisbon',
            'website_url': 'https://www.novasbe.unl.pt',
            'description': 'Top business school in Portugal, offering MBA and executive programs.'
        },
        {
            'name': 'Porto Business School',
            'name_local': 'Porto Business School',
            'type': 'vocational_school',
            'city': 'Porto',
            'website_url': 'https://www.pbs.up.pt',
            'description': 'Business school at University of Porto, offering programs in business and management.'
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
                VALUES (%s, %s, %s, %s, 'PT', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added vocational school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_portuguese_foundation_programs(conn, jurisdiction_id):
    """Add Portuguese foundation programs with VERIFIED URLs"""
    cursor = conn.cursor()
    
    programs = [
        {
            'name': 'University of Lisbon Foundation Year',
            'name_local': 'Ano Preparatório Universidade de Lisboa',
            'type': 'foundation_program',
            'city': 'Lisbon',
            'website_url': 'https://www.ulisboa.pt',
            'description': 'Foundation year program at University of Lisbon for international students.'
        },
        {
            'name': 'University of Porto Preparatory Programme',
            'name_local': 'Programa Preparatório Universidade do Porto',
            'type': 'foundation_program',
            'city': 'Porto',
            'website_url': 'https://www.up.pt',
            'description': 'Preparatory program at University of Porto for international students.'
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
                VALUES (%s, %s, %s, %s, 'PT', %s, %s, %s, true)
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
        jurisdiction_id = get_jurisdiction_id(conn, 'PT')
        if not jurisdiction_id:
            print("Portuguese jurisdiction not found!")
            return
        
        print(f"Found Portuguese jurisdiction (ID: {jurisdiction_id})")
        
        print("\nAdding Portuguese universities...")
        add_portuguese_universities(conn, jurisdiction_id)
        
        print("\nAdding Portuguese language schools...")
        add_portuguese_language_schools(conn, jurisdiction_id)
        
        print("\nAdding Portuguese conservatories...")
        add_portuguese_conservatories(conn, jurisdiction_id)
        
        print("\nAdding Portuguese vocational schools...")
        add_portuguese_vocational_schools(conn, jurisdiction_id)
        
        print("\nAdding Portuguese foundation programs...")
        add_portuguese_foundation_programs(conn, jurisdiction_id)
        
        print("\nAll Portuguese educational institutions added successfully!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nPortuguese institutions summary:")
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
