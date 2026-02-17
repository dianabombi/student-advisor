"""
Додавання австрійських навчальних закладів
Університети, мовні школи та інші заклади, які приймають іноземних студентів
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='AT'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_austrian_universities(conn, jurisdiction_id):
    """Add major Austrian universities that accept international students"""
    cursor = conn.cursor()
    
    universities = [
        {
            'name': 'University of Vienna',
            'name_local': 'Universität Wien',
            'type': 'university',
            'city': 'Wien',
            'country': 'AT',
            'website_url': 'https://www.univie.ac.at',
            'student_count': 90000,
            'ranking_position': 1,
            'description': 'Largest and oldest university in Austria, founded in 1365. Offers programs in humanities, natural sciences, social sciences, law, and theology.'
        },
        {
            'name': 'Vienna University of Technology',
            'name_local': 'Technische Universität Wien',
            'type': 'university',
            'city': 'Wien',
            'country': 'AT',
            'website_url': 'https://www.tuwien.at',
            'student_count': 28000,
            'ranking_position': 2,
            'description': 'Leading technical university in Austria, specializing in engineering, IT, architecture, and natural sciences.'
        },
        {
            'name': 'University of Innsbruck',
            'name_local': 'Universität Innsbruck',
            'type': 'university',
            'city': 'Innsbruck',
            'country': 'AT',
            'website_url': 'https://www.uibk.ac.at',
            'student_count': 28000,
            'ranking_position': 3,
            'description': 'Comprehensive university in the Alps, strong in natural sciences, humanities, and social sciences.'
        },
        {
            'name': 'University of Graz',
            'name_local': 'Universität Graz',
            'type': 'university',
            'city': 'Graz',
            'country': 'AT',
            'website_url': 'https://www.uni-graz.at',
            'student_count': 32000,
            'ranking_position': 4,
            'description': 'Second-largest university in Austria, offering programs in humanities, natural sciences, law, and social sciences.'
        },
        {
            'name': 'Vienna University of Economics and Business',
            'name_local': 'Wirtschaftsuniversität Wien',
            'type': 'university',
            'city': 'Wien',
            'country': 'AT',
            'website_url': 'https://www.wu.ac.at',
            'student_count': 23000,
            'ranking_position': 5,
            'description': 'Largest business university in Europe, specializing in economics, business administration, and law.'
        },
        {
            'name': 'University of Salzburg',
            'name_local': 'Universität Salzburg',
            'type': 'university',
            'city': 'Salzburg',
            'country': 'AT',
            'website_url': 'https://www.plus.ac.at',
            'student_count': 18000,
            'ranking_position': 6,
            'description': 'University in Mozart\'s birthplace, offering programs in humanities, natural sciences, law, and theology.'
        },
        {
            'name': 'Johannes Kepler University Linz',
            'name_local': 'Johannes Kepler Universität Linz',
            'type': 'university',
            'city': 'Linz',
            'country': 'AT',
            'website_url': 'https://www.jku.at',
            'student_count': 20000,
            'ranking_position': 7,
            'description': 'Modern university specializing in law, social sciences, economics, and technical sciences.'
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

def add_austrian_language_schools(conn, jurisdiction_id):
    """Add Austrian language schools for foreigners"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'ActiLingua Academy',
            'name_local': 'ActiLingua Academy',
            'type': 'language_school',
            'city': 'Wien',
            'website_url': 'https://www.actilingua.com',
            'description': 'Premium German language school in Vienna, offering courses for all levels and exam preparation.'
        },
        {
            'name': 'Deutsch-Akademie Vienna',
            'name_local': 'Deutsch-Akademie Wien',
            'type': 'language_school',
            'city': 'Wien',
            'website_url': 'https://www.deutschakademie.com',
            'description': 'German language school with small groups and flexible schedules, located in the heart of Vienna.'
        },
        {
            'name': 'Inlingua Salzburg',
            'name_local': 'Inlingua Salzburg',
            'type': 'language_school',
            'city': 'Salzburg',
            'website_url': 'https://www.inlingua-salzburg.at',
            'description': 'International language school offering German courses in Salzburg for foreigners.'
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
                VALUES (%s, %s, %s, %s, 'AT', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added language school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_austrian_conservatories(conn, jurisdiction_id):
    """Add Austrian conservatories and music universities"""
    cursor = conn.cursor()
    
    conservatories = [
        {
            'name': 'University of Music and Performing Arts Vienna',
            'name_local': 'Universität für Musik und darstellende Kunst Wien',
            'type': 'conservatory',
            'city': 'Wien',
            'website_url': 'https://www.mdw.ac.at',
            'description': 'One of the world\'s leading music universities, offering programs in classical music, jazz, and performing arts.'
        },
        {
            'name': 'Mozarteum University Salzburg',
            'name_local': 'Universität Mozarteum Salzburg',
            'type': 'conservatory',
            'city': 'Salzburg',
            'website_url': 'https://www.moz.ac.at',
            'description': 'Prestigious music university in Mozart\'s birthplace, specializing in classical music, composition, and music education.'
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
                VALUES (%s, %s, %s, %s, 'AT', %s, %s, %s, true)
            """, (
                conservatory['name'], conservatory['name_local'], conservatory['type'], 
                conservatory['city'], conservatory['website_url'], conservatory['description'], 
                jurisdiction_id
            ))
            print(f"Added conservatory: {conservatory['name']}")
        else:
            print(f"Already exists: {conservatory['name']}")
    
    cursor.close()

def add_austrian_foundation_programs(conn, jurisdiction_id):
    """Add foundation/preparatory programs"""
    cursor = conn.cursor()
    
    programs = [
        {
            'name': 'University of Vienna Preparatory Course',
            'name_local': 'Vorstudienlehrgang der Wiener Universitäten',
            'type': 'foundation_program',
            'city': 'Wien',
            'website_url': 'https://www.vorstudienlehrgang.at',
            'description': 'One-year preparatory program for international students planning to study at Austrian universities.'
        },
        {
            'name': 'Graz University Foundation Year',
            'name_local': 'Vorstudienlehrgang Graz',
            'type': 'foundation_program',
            'city': 'Graz',
            'website_url': 'https://www.uni-graz.at',
            'description': 'Foundation year program preparing international students for studies at Austrian universities.'
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
                VALUES (%s, %s, %s, %s, 'AT', %s, %s, %s, true)
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
        # Get Austrian jurisdiction ID
        jurisdiction_id = get_jurisdiction_id(conn, 'AT')
        if not jurisdiction_id:
            print("Austrian jurisdiction not found!")
            return
        
        print(f"Found Austrian jurisdiction (ID: {jurisdiction_id})")
        
        # Add all Austrian institutions
        print("\nAdding Austrian universities...")
        add_austrian_universities(conn, jurisdiction_id)
        
        print("\nAdding Austrian language schools...")
        add_austrian_language_schools(conn, jurisdiction_id)
        
        print("\nAdding Austrian conservatories...")
        add_austrian_conservatories(conn, jurisdiction_id)
        
        print("\nAdding foundation programs...")
        add_austrian_foundation_programs(conn, jurisdiction_id)
        
        print("\nAll Austrian educational institutions added successfully!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nAustrian institutions summary:")
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
