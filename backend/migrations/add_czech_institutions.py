"""
Додавання чеських навчальних закладів
Університети, мовні школи та інші заклади, які приймають іноземних студентів
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='CZ'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_czech_universities(conn, jurisdiction_id):
    """Add major Czech universities that accept international students"""
    cursor = conn.cursor()
    
    universities = [
        {
            'name': 'Charles University',
            'name_local': 'Univerzita Karlova',
            'type': 'university',
            'city': 'Praha',
            'country': 'CZ',
            'website_url': 'https://cuni.cz',
            'student_count': 50000,
            'ranking_position': 1,
            'description': 'Oldest and largest university in Czech Republic, founded in 1348. Offers programs in medicine, law, natural sciences, humanities, and social sciences. Many programs available in English.'
        },
        {
            'name': 'Czech Technical University in Prague',
            'name_local': 'České vysoké učení technické v Praze',
            'type': 'university',
            'city': 'Praha',
            'country': 'CZ',
            'website_url': 'https://www.cvut.cz',
            'student_count': 18000,
            'ranking_position': 2,
            'description': 'Leading technical university offering programs in engineering, architecture, and technology. Many English-taught programs for international students.'
        },
        {
            'name': 'Masaryk University',
            'name_local': 'Masarykova univerzita',
            'type': 'university',
            'city': 'Brno',
            'country': 'CZ',
            'website_url': 'https://www.muni.cz',
            'student_count': 35000,
            'ranking_position': 3,
            'description': 'Second largest university in Czech Republic. Strong in medicine, natural sciences, law, and social sciences. Offers many English programs.'
        },
        {
            'name': 'Brno University of Technology',
            'name_local': 'Vysoké učení technické v Brně',
            'type': 'university',
            'city': 'Brno',
            'country': 'CZ',
            'website_url': 'https://www.vutbr.cz',
            'student_count': 20000,
            'ranking_position': 4,
            'description': 'Major technical university in Brno, specializing in engineering, IT, architecture, and technology.'
        },
        {
            'name': 'University of Economics, Prague',
            'name_local': 'Vysoká škola ekonomická v Praze',
            'type': 'university',
            'city': 'Praha',
            'country': 'CZ',
            'website_url': 'https://www.vse.cz',
            'student_count': 15000,
            'ranking_position': 5,
            'description': 'Leading economics and business university. Offers programs in economics, business administration, international relations, and informatics.'
        },
        {
            'name': 'Palacký University Olomouc',
            'name_local': 'Univerzita Palackého v Olomouci',
            'type': 'university',
            'city': 'Olomouc',
            'country': 'CZ',
            'website_url': 'https://www.upol.cz',
            'student_count': 22000,
            'ranking_position': 6,
            'description': 'Historic university offering programs in medicine, natural sciences, humanities, and education. Popular among international students.'
        },
        {
            'name': 'Czech University of Life Sciences Prague',
            'name_local': 'Česká zemědělská univerzita v Praze',
            'type': 'university',
            'city': 'Praha',
            'country': 'CZ',
            'website_url': 'https://www.czu.cz',
            'student_count': 16000,
            'ranking_position': 7,
            'description': 'Specializes in agriculture, forestry, environmental sciences, and engineering. Offers many English programs.'
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
            print(f"✅ Added: {uni['name']}")
        else:
            print(f"⏭️  Already exists: {uni['name']}")
    
    cursor.close()

def add_czech_language_schools(conn, jurisdiction_id):
    """Add Czech language schools for foreigners"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Prague Language Institute',
            'name_local': 'Pražský jazykový institut',
            'type': 'language_school',
            'city': 'Praha',
            'website_url': 'https://www.pli.cz',
            'description': 'Language school specializing in Czech language courses for foreigners, including preparatory courses for university admission.'
        },
        {
            'name': 'Institute of Language and Preparatory Studies, Charles University',
            'name_local': 'Ústav jazykové a odborné přípravy UK',
            'type': 'language_school',
            'city': 'Praha',
            'website_url': 'https://www.ujop.cuni.cz',
            'description': 'Official preparatory institute of Charles University offering Czech language courses and university preparation programs.'
        },
        {
            'name': 'Language School Akcent',
            'name_local': 'Jazyková škola Akcent',
            'type': 'language_school',
            'city': 'Praha',
            'website_url': 'https://www.akcent.cz',
            'description': 'Popular language school offering Czech courses for foreigners at all levels.'
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
                VALUES (%s, %s, %s, %s, 'CZ', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"✅ Added language school: {school['name']}")
        else:
            print(f"⏭️  Already exists: {school['name']}")
    
    cursor.close()

def add_czech_foundation_programs(conn, jurisdiction_id):
    """Add foundation/preparatory programs"""
    cursor = conn.cursor()
    
    programs = [
        {
            'name': 'Charles University Foundation Year',
            'name_local': 'Přípravný kurz UK',
            'type': 'foundation_program',
            'city': 'Praha',
            'website_url': 'https://www.ujop.cuni.cz',
            'description': 'One-year preparatory program for international students planning to study at Czech universities.'
        },
        {
            'name': 'Czech Technical University Preparatory Course',
            'name_local': 'Přípravný kurz ČVUT',
            'type': 'foundation_program',
            'city': 'Praha',
            'website_url': 'https://www.cvut.cz',
            'description': 'Preparatory course for international students focusing on Czech language and technical subjects.'
        },
        {
            'name': 'GoStudy Czech Republic',
            'name_local': 'GoStudy Česká republika',
            'type': 'foundation_program',
            'city': 'Praha',
            'website_url': 'https://www.gostudy.cz',
            'description': 'Comprehensive foundation program preparing international students for Czech universities with Czech language training.'
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
                VALUES (%s, %s, %s, %s, 'CZ', %s, %s, %s, true)
            """, (
                prog['name'], prog['name_local'], prog['type'], prog['city'],
                prog['website_url'], prog['description'], jurisdiction_id
            ))
            print(f"✅ Added foundation program: {prog['name']}")
        else:
            print(f"⏭️  Already exists: {prog['name']}")
    
    cursor.close()

def main():
    print("🔄 Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    
    try:
        # Get Czech jurisdiction ID
        jurisdiction_id = get_jurisdiction_id(conn, 'CZ')
        if not jurisdiction_id:
            print("❌ Czech jurisdiction not found!")
            return
        
        print(f"✅ Found Czech jurisdiction (ID: {jurisdiction_id})")
        
        # Add all Czech institutions
        print("\n📚 Adding Czech universities...")
        add_czech_universities(conn, jurisdiction_id)
        
        print("\n🗣️ Adding Czech language schools...")
        add_czech_language_schools(conn, jurisdiction_id)
        
        print("\n🎓 Adding foundation programs...")
        add_czech_foundation_programs(conn, jurisdiction_id)
        
        print("\n✅ All Czech educational institutions added successfully!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\n📊 Summary:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        cursor.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
