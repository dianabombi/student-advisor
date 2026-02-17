"""
Додавання італійських навчальних закладів
ВАЖЛИВО: Використовуються ТІЛЬКИ перевірені офіційні URL
ВКЛЮЧАЄ: Католицькі духовні навчальні заклади
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='IT'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_italian_universities(conn, jurisdiction_id):
    """Add major Italian universities with VERIFIED URLs"""
    cursor = conn.cursor()
    
    universities = [
        {
            'name': 'Sapienza University of Rome',
            'name_local': 'Sapienza Università di Roma',
            'type': 'university',
            'city': 'Rome',
            'country': 'IT',
            'website_url': 'https://www.uniroma1.it',
            'student_count': 112000,
            'ranking_position': 1,
            'description': 'Largest university in Europe, one of the oldest in the world, strong in all disciplines.'
        },
        {
            'name': 'University of Bologna',
            'name_local': 'Università di Bologna',
            'type': 'university',
            'city': 'Bologna',
            'country': 'IT',
            'website_url': 'https://www.unibo.it',
            'student_count': 85000,
            'ranking_position': 2,
            'description': 'Oldest university in the world (founded 1088), leading in humanities and sciences.'
        },
        {
            'name': 'University of Milan',
            'name_local': 'Università degli Studi di Milano',
            'type': 'university',
            'city': 'Milan',
            'country': 'IT',
            'website_url': 'https://www.unimi.it',
            'student_count': 64000,
            'ranking_position': 3,
            'description': 'Major research university in Milan, strong in sciences, medicine, and humanities.'
        },
        {
            'name': 'Polytechnic University of Milan',
            'name_local': 'Politecnico di Milano',
            'type': 'university',
            'city': 'Milan',
            'country': 'IT',
            'website_url': 'https://www.polimi.it',
            'student_count': 47000,
            'ranking_position': 4,
            'description': 'Leading technical university in Italy, specializing in engineering, architecture, and design.'
        },
        {
            'name': 'University of Padua',
            'name_local': 'Università degli Studi di Padova',
            'type': 'university',
            'city': 'Padua',
            'country': 'IT',
            'website_url': 'https://www.unipd.it',
            'student_count': 62000,
            'ranking_position': 5,
            'description': 'One of the oldest universities in the world (founded 1222), strong in sciences and medicine.'
        },
        {
            'name': 'University of Florence',
            'name_local': 'Università degli Studi di Firenze',
            'type': 'university',
            'city': 'Florence',
            'country': 'IT',
            'website_url': 'https://www.unifi.it',
            'student_count': 51000,
            'ranking_position': 6,
            'description': 'Major university in Tuscany, offering programs in humanities, sciences, and engineering.'
        },
        {
            'name': 'University of Pisa',
            'name_local': 'Università di Pisa',
            'type': 'university',
            'city': 'Pisa',
            'country': 'IT',
            'website_url': 'https://www.unipi.it',
            'student_count': 50000,
            'ranking_position': 7,
            'description': 'Historic university founded in 1343, strong in sciences, engineering, and humanities.'
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

def add_catholic_institutions(conn, jurisdiction_id):
    """Add Catholic theological institutions with VERIFIED URLs"""
    cursor = conn.cursor()
    
    institutions = [
        {
            'name': 'Pontifical Gregorian University',
            'name_local': 'Pontificia Università Gregoriana',
            'type': 'university',
            'city': 'Rome',
            'country': 'IT',
            'website_url': 'https://www.unigre.it',
            'student_count': 3000,
            'ranking_position': 8,
            'description': 'Pontifical university in Rome, specializing in theology, philosophy, and canon law.'
        },
        {
            'name': 'Pontifical Lateran University',
            'name_local': 'Pontificia Università Lateranense',
            'type': 'university',
            'city': 'Rome',
            'country': 'IT',
            'website_url': 'https://www.pul.va',
            'student_count': 1500,
            'ranking_position': 9,
            'description': 'Pontifical university specializing in theology, philosophy, and canon law.'
        }
    ]
    
    for inst in institutions:
        cursor.execute(
            "SELECT id FROM universities WHERE name = %s AND jurisdiction_id = %s",
            (inst['name'], jurisdiction_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.execute("""
                INSERT INTO universities 
                (name, name_local, type, city, country, website_url, student_count, 
                 ranking_position, description, jurisdiction_id, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, true)
            """, (
                inst['name'], inst['name_local'], inst['type'], inst['city'], inst['country'],
                inst['website_url'], inst['student_count'], inst['ranking_position'],
                inst['description'], jurisdiction_id
            ))
            print(f"Added Catholic institution: {inst['name']}")
        else:
            print(f"Already exists: {inst['name']}")
    
    cursor.close()

def add_italian_language_schools(conn, jurisdiction_id):
    """Add Italian language schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Dante Alighieri Society Rome',
            'name_local': 'Società Dante Alighieri Roma',
            'type': 'language_school',
            'city': 'Rome',
            'website_url': 'https://www.ladante.it',
            'description': 'Leading Italian language and culture school in Rome.'
        },
        {
            'name': 'Scuola Leonardo da Vinci',
            'name_local': 'Scuola Leonardo da Vinci',
            'type': 'language_school',
            'city': 'Florence',
            'website_url': 'https://www.scuolaleonardo.com',
            'description': 'Italian language school with locations in Florence, Milan, Rome, and Siena.'
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
                VALUES (%s, %s, %s, %s, 'IT', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added language school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_italian_conservatories(conn, jurisdiction_id):
    """Add Italian conservatories with VERIFIED URLs"""
    cursor = conn.cursor()
    
    conservatories = [
        {
            'name': 'Santa Cecilia Conservatory',
            'name_local': 'Conservatorio di Santa Cecilia',
            'type': 'conservatory',
            'city': 'Rome',
            'website_url': 'https://www.conservatoriosantacecilia.it',
            'description': 'Leading music conservatory in Rome, one of the oldest in Italy.'
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
                VALUES (%s, %s, %s, %s, 'IT', %s, %s, %s, true)
            """, (
                conservatory['name'], conservatory['name_local'], conservatory['type'], 
                conservatory['city'], conservatory['website_url'], conservatory['description'], 
                jurisdiction_id
            ))
            print(f"Added conservatory: {conservatory['name']}")
        else:
            print(f"Already exists: {conservatory['name']}")
    
    cursor.close()

def add_italian_vocational_schools(conn, jurisdiction_id):
    """Add Italian vocational schools with VERIFIED URLs"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'SDA Bocconi School of Management',
            'name_local': 'SDA Bocconi School of Management',
            'type': 'vocational_school',
            'city': 'Milan',
            'website_url': 'https://www.sdabocconi.it',
            'description': 'Top business school in Italy, offering MBA and executive programs.'
        },
        {
            'name': 'MIP Politecnico di Milano',
            'name_local': 'MIP Politecnico di Milano',
            'type': 'vocational_school',
            'city': 'Milan',
            'website_url': 'https://www.mip.polimi.it',
            'description': 'Business school at Politecnico di Milano, specializing in engineering management.'
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
                VALUES (%s, %s, %s, %s, 'IT', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"Added vocational school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def add_italian_foundation_programs(conn, jurisdiction_id):
    """Add Italian foundation programs with VERIFIED URLs"""
    cursor = conn.cursor()
    
    programs = [
        {
            'name': 'Sapienza Foundation Programme',
            'name_local': 'Programma Preparatorio Sapienza',
            'type': 'foundation_program',
            'city': 'Rome',
            'website_url': 'https://www.uniroma1.it',
            'description': 'Foundation year program at Sapienza University for international students.'
        },
        {
            'name': 'Bologna Preparatory Year',
            'name_local': 'Anno Preparatorio Bologna',
            'type': 'foundation_program',
            'city': 'Bologna',
            'website_url': 'https://www.unibo.it',
            'description': 'Preparatory program at University of Bologna for international students.'
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
                VALUES (%s, %s, %s, %s, 'IT', %s, %s, %s, true)
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
        jurisdiction_id = get_jurisdiction_id(conn, 'IT')
        if not jurisdiction_id:
            print("Italian jurisdiction not found!")
            return
        
        print(f"Found Italian jurisdiction (ID: {jurisdiction_id})")
        
        print("\nAdding Italian universities...")
        add_italian_universities(conn, jurisdiction_id)
        
        print("\nAdding Catholic theological institutions...")
        add_catholic_institutions(conn, jurisdiction_id)
        
        print("\nAdding Italian language schools...")
        add_italian_language_schools(conn, jurisdiction_id)
        
        print("\nAdding Italian conservatories...")
        add_italian_conservatories(conn, jurisdiction_id)
        
        print("\nAdding Italian vocational schools...")
        add_italian_vocational_schools(conn, jurisdiction_id)
        
        print("\nAdding Italian foundation programs...")
        add_italian_foundation_programs(conn, jurisdiction_id)
        
        print("\nAll Italian educational institutions added successfully!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nItalian institutions summary:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        # Show Catholic institutions
        cursor.execute("""
            SELECT name, website_url 
            FROM universities 
            WHERE jurisdiction_id = %s 
            AND (name LIKE '%Pontifical%' OR name LIKE '%Pontificia%')
            ORDER BY name
        """, (jurisdiction_id,))
        
        print("\nCatholic theological institutions:")
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
