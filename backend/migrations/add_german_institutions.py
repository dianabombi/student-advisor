"""
Додавання німецьких навчальних закладів
Університети, мовні школи та інші заклади, які приймають іноземних студентів
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='DE'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_german_universities(conn, jurisdiction_id):
    """Add major German universities that accept international students"""
    cursor = conn.cursor()
    
    universities = [
        {
            'name': 'Ludwig Maximilian University of Munich',
            'name_local': 'Ludwig-Maximilians-Universität München',
            'type': 'university',
            'city': 'München',
            'country': 'DE',
            'website_url': 'https://www.lmu.de',
            'student_count': 52000,
            'ranking_position': 1,
            'description': 'One of Europe\'s leading research universities, offering programs in humanities, natural sciences, law, medicine, and social sciences.'
        },
        {
            'name': 'Technical University of Munich',
            'name_local': 'Technische Universität München',
            'type': 'university',
            'city': 'München',
            'country': 'DE',
            'website_url': 'https://www.tum.de',
            'student_count': 45000,
            'ranking_position': 2,
            'description': 'Top technical university in Germany, specializing in engineering, IT, natural sciences, and medicine.'
        },
        {
            'name': 'Heidelberg University',
            'name_local': 'Ruprecht-Karls-Universität Heidelberg',
            'type': 'university',
            'city': 'Heidelberg',
            'country': 'DE',
            'website_url': 'https://www.uni-heidelberg.de',
            'student_count': 30000,
            'ranking_position': 3,
            'description': 'Germany\'s oldest university, founded in 1386. Strong in medicine, natural sciences, humanities, and law.'
        },
        {
            'name': 'Humboldt University of Berlin',
            'name_local': 'Humboldt-Universität zu Berlin',
            'type': 'university',
            'city': 'Berlin',
            'country': 'DE',
            'website_url': 'https://www.hu-berlin.de',
            'student_count': 35000,
            'ranking_position': 4,
            'description': 'Prestigious university in Berlin, offering programs in humanities, social sciences, natural sciences, and medicine.'
        },
        {
            'name': 'Free University of Berlin',
            'name_local': 'Freie Universität Berlin',
            'type': 'university',
            'city': 'Berlin',
            'country': 'DE',
            'website_url': 'https://www.fu-berlin.de',
            'student_count': 33000,
            'ranking_position': 5,
            'description': 'Leading research university in Berlin, strong in humanities, social sciences, and natural sciences.'
        },
        {
            'name': 'RWTH Aachen University',
            'name_local': 'Rheinisch-Westfälische Technische Hochschule Aachen',
            'type': 'university',
            'city': 'Aachen',
            'country': 'DE',
            'website_url': 'https://www.rwth-aachen.de',
            'student_count': 47000,
            'ranking_position': 6,
            'description': 'Largest technical university in Germany, specializing in engineering, IT, and natural sciences.'
        },
        {
            'name': 'University of Freiburg',
            'name_local': 'Albert-Ludwigs-Universität Freiburg',
            'type': 'university',
            'city': 'Freiburg',
            'country': 'DE',
            'website_url': 'https://www.uni-freiburg.de',
            'student_count': 25000,
            'ranking_position': 7,
            'description': 'Historic university offering programs in humanities, natural sciences, medicine, and law.'
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

def add_german_language_schools(conn, jurisdiction_id):
    """Add German language schools for foreigners"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Goethe-Institut Munich',
            'name_local': 'Goethe-Institut München',
            'type': 'language_school',
            'city': 'München',
            'website_url': 'https://www.goethe.de/ins/de/de/sta/mue.html',
            'description': 'World-renowned German language and culture institute offering courses for all levels.'
        },
        {
            'name': 'DID Deutsch-Institut Berlin',
            'name_local': 'DID Deutsch-Institut Berlin',
            'type': 'language_school',
            'city': 'Berlin',
            'website_url': 'https://www.did.de',
            'description': 'Premium German language school in Berlin with intensive courses and exam preparation.'
        },
        {
            'name': 'Tandem Munich',
            'name_local': 'Tandem München',
            'type': 'language_school',
            'city': 'München',
            'website_url': 'https://www.tandem-muenchen.de',
            'description': 'International language school offering German courses and cultural activities in Munich.'
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
                VALUES (%s, %s, %s, %s, 'DE', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added language school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_german_vocational_schools(conn, jurisdiction_id):
    """Add German vocational schools (Berufsschulen)"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'IHK Munich Business School',
            'name_local': 'IHK Akademie München',
            'type': 'vocational_school',
            'city': 'München',
            'website_url': 'https://www.ihk-akademie-muenchen.de',
            'description': 'Vocational training institute offering business and professional courses.'
        },
        {
            'name': 'Berlin School of Economics',
            'name_local': 'Berliner Wirtschaftsschule',
            'type': 'vocational_school',
            'city': 'Berlin',
            'website_url': 'https://www.bwakademie.de',
            'description': 'Vocational school specializing in business, economics, and management training.'
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
                VALUES (%s, %s, %s, %s, 'DE', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added vocational school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_german_conservatories(conn, jurisdiction_id):
    """Add German conservatories and music universities"""
    cursor = conn.cursor()
    
    conservatories = [
        {
            'name': 'University of Music and Performing Arts Munich',
            'name_local': 'Hochschule für Musik und Theater München',
            'type': 'conservatory',
            'city': 'München',
            'website_url': 'https://www.hmtm.de',
            'description': 'Leading music university in Munich, offering programs in classical music, jazz, and performing arts.'
        },
        {
            'name': 'Berlin University of the Arts',
            'name_local': 'Universität der Künste Berlin',
            'type': 'conservatory',
            'city': 'Berlin',
            'website_url': 'https://www.udk-berlin.de',
            'description': 'Largest art university in Europe, specializing in music, fine arts, design, and performing arts.'
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
                VALUES (%s, %s, %s, %s, 'DE', %s, %s, %s, true)
            """, (
                conservatory['name'], conservatory['name_local'], conservatory['type'], 
                conservatory['city'], conservatory['website_url'], conservatory['description'], 
                jurisdiction_id
            ))
            print(f"Added conservatory: {conservatory['name']}")
        else:
            print(f"Already exists: {conservatory['name']}")
    
    cursor.close()

def add_german_foundation_programs(conn, jurisdiction_id):
    """Add foundation/preparatory programs (Studienkolleg)"""
    cursor = conn.cursor()
    
    programs = [
        {
            'name': 'Studienkolleg Munich',
            'name_local': 'Studienkolleg München',
            'type': 'foundation_program',
            'city': 'München',
            'website_url': 'https://www.studienkolleg.lmu.de',
            'description': 'Preparatory course for international students planning to study at German universities.'
        },
        {
            'name': 'Studienkolleg Berlin',
            'name_local': 'Studienkolleg Berlin',
            'type': 'foundation_program',
            'city': 'Berlin',
            'website_url': 'https://www.studienkolleg-berlin.de',
            'description': 'Foundation year program preparing international students for studies at German universities.'
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
                VALUES (%s, %s, %s, %s, 'DE', %s, %s, %s, true)
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
        # Get German jurisdiction ID
        jurisdiction_id = get_jurisdiction_id(conn, 'DE')
        if not jurisdiction_id:
            print("German jurisdiction not found!")
            return
        
        print(f"Found German jurisdiction (ID: {jurisdiction_id})")
        
        # Add all German institutions
        print("\nAdding German universities...")
        add_german_universities(conn, jurisdiction_id)
        
        print("\nAdding German language schools...")
        add_german_language_schools(conn, jurisdiction_id)
        
        print("\nAdding German vocational schools...")
        add_german_vocational_schools(conn, jurisdiction_id)
        
        print("\nAdding German conservatories...")
        add_german_conservatories(conn, jurisdiction_id)
        
        print("\nAdding foundation programs...")
        add_german_foundation_programs(conn, jurisdiction_id)
        
        print("\nAll German educational institutions added successfully!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nGerman institutions summary:")
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
