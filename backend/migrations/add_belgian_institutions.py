"""
Додавання бельгійських навчальних закладів
ВАЖЛИВО: Використовуються ТІЛЬКИ перевірені офіційні URL
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='BE'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_belgian_universities(conn, jurisdiction_id):
    """Add major Belgian universities with VERIFIED URLs"""
    cursor = conn.cursor()
    
    universities = [
        {
            'name': 'KU Leuven',
            'name_local': 'Katholieke Universiteit Leuven',
            'type': 'university',
            'city': 'Leuven',
            'country': 'BE',
            'website_url': 'https://www.kuleuven.be',
            'student_count': 58000,
            'ranking_position': 1,
            'description': 'Oldest and largest university in Belgium, consistently ranked among Europe\'s best.'
        },
        {
            'name': 'Ghent University',
            'name_local': 'Universiteit Gent',
            'type': 'university',
            'city': 'Ghent',
            'country': 'BE',
            'website_url': 'https://www.ugent.be',
            'student_count': 44000,
            'ranking_position': 2,
            'description': 'Major research university in Flanders, strong in sciences and engineering.'
        },
        {
            'name': 'Université Catholique de Louvain',
            'name_local': 'Université Catholique de Louvain',
            'type': 'university',
            'city': 'Louvain-la-Neuve',
            'country': 'BE',
            'website_url': 'https://www.uclouvain.be',
            'student_count': 31000,
            'ranking_position': 3,
            'description': 'Leading French-speaking university in Belgium, strong in humanities and sciences.'
        },
        {
            'name': 'Vrije Universiteit Brussel',
            'name_local': 'Vrije Universiteit Brussel',
            'type': 'university',
            'city': 'Brussels',
            'country': 'BE',
            'website_url': 'https://www.vub.be',
            'student_count': 17000,
            'ranking_position': 4,
            'description': 'Free university in Brussels, known for research and innovation.'
        },
        {
            'name': 'University of Antwerp',
            'name_local': 'Universiteit Antwerpen',
            'type': 'university',
            'city': 'Antwerp',
            'country': 'BE',
            'website_url': 'https://www.uantwerpen.be',
            'student_count': 20000,
            'ranking_position': 5,
            'description': 'Young dynamic university in Antwerp, strong in sciences and social sciences.'
        },
        {
            'name': 'Université Libre de Bruxelles',
            'name_local': 'Université Libre de Bruxelles',
            'type': 'university',
            'city': 'Brussels',
            'country': 'BE',
            'website_url': 'https://www.ulb.be',
            'student_count': 33000,
            'ranking_position': 6,
            'description': 'Major French-speaking university in Brussels, strong in humanities and sciences.'
        },
        {
            'name': 'University of Liège',
            'name_local': 'Université de Liège',
            'type': 'university',
            'city': 'Liège',
            'country': 'BE',
            'website_url': 'https://www.uliege.be',
            'student_count': 23000,
            'ranking_position': 7,
            'description': 'Public university in Wallonia, offering programs in sciences, engineering, and humanities.'
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

def add_belgian_language_schools(conn, jurisdiction_id):
    """Add Belgian language schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'CLL Language Centres',
            'name_local': 'CLL Centres de Langues',
            'type': 'language_school',
            'city': 'Brussels',
            'website_url': 'https://www.cll.be',
            'description': 'Leading language school in Belgium offering French, Dutch, and English courses.'
        },
        {
            'name': 'Brussels Language Studies',
            'name_local': 'Brussels Language Studies',
            'type': 'language_school',
            'city': 'Brussels',
            'website_url': 'https://www.bls-languageschools.com',
            'description': 'International language school in Brussels offering courses in multiple languages.'
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
                VALUES (%s, %s, %s, %s, 'BE', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added language school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_belgian_conservatories(conn, jurisdiction_id):
    """Add Belgian conservatories with VERIFIED URLs"""
    cursor = conn.cursor()
    
    conservatories = [
        {
            'name': 'Royal Conservatory of Brussels',
            'name_local': 'Conservatoire Royal de Bruxelles',
            'type': 'conservatory',
            'city': 'Brussels',
            'website_url': 'https://www.conservatoire.be',
            'description': 'Leading music conservatory in Belgium, offering programs in classical music and jazz.'
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
                VALUES (%s, %s, %s, %s, 'BE', %s, %s, %s, true)
            """, (
                conservatory['name'], conservatory['name_local'], conservatory['type'], 
                conservatory['city'], conservatory['website_url'], conservatory['description'], 
                jurisdiction_id
            ))
            print(f"Added conservatory: {conservatory['name']}")
        else:
            print(f"Already exists: {conservatory['name']}")
    
    cursor.close()

def add_belgian_vocational_schools(conn, jurisdiction_id):
    """Add Belgian vocational schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Solvay Brussels School',
            'name_local': 'Solvay Brussels School',
            'type': 'vocational_school',
            'city': 'Brussels',
            'website_url': 'https://www.solvay.edu',
            'description': 'Top business school at ULB, offering MBA and executive programs.'
        },
        {
            'name': 'Vlerick Business School',
            'name_local': 'Vlerick Business School',
            'type': 'vocational_school',
            'city': 'Ghent',
            'website_url': 'https://www.vlerick.com',
            'description': 'Leading European business school with campuses in Belgium and abroad.'
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
                VALUES (%s, %s, %s, %s, 'BE', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added vocational school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_belgian_foundation_programs(conn, jurisdiction_id):
    """Add Belgian foundation programs with VERIFIED URLs"""
    cursor = conn.cursor()
    
    programs = [
        {
            'name': 'KU Leuven Foundation Programme',
            'name_local': 'KU Leuven Voorbereidingsprogramma',
            'type': 'foundation_program',
            'city': 'Leuven',
            'website_url': 'https://www.kuleuven.be',
            'description': 'Foundation year program at KU Leuven for international students.'
        },
        {
            'name': 'UCLouvain Preparatory Year',
            'name_local': 'UCLouvain Année Préparatoire',
            'type': 'foundation_program',
            'city': 'Louvain-la-Neuve',
            'website_url': 'https://www.uclouvain.be',
            'description': 'Preparatory program at UCLouvain for international students.'
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
                VALUES (%s, %s, %s, %s, 'BE', %s, %s, %s, true)
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
        jurisdiction_id = get_jurisdiction_id(conn, 'BE')
        if not jurisdiction_id:
            print("Belgian jurisdiction not found!")
            return
        
        print(f"Found Belgian jurisdiction (ID: {jurisdiction_id})")
        
        print("\nAdding Belgian universities...")
        add_belgian_universities(conn, jurisdiction_id)
        
        print("\nAdding Belgian language schools...")
        add_belgian_language_schools(conn, jurisdiction_id)
        
        print("\nAdding Belgian conservatories...")
        add_belgian_conservatories(conn, jurisdiction_id)
        
        print("\nAdding Belgian vocational schools...")
        add_belgian_vocational_schools(conn, jurisdiction_id)
        
        print("\nAdding Belgian foundation programs...")
        add_belgian_foundation_programs(conn, jurisdiction_id)
        
        print("\nAll Belgian educational institutions added successfully!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nBelgian institutions summary:")
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
