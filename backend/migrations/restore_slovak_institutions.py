"""
Відновлення даних словацьких навчальних закладів
Додає/оновлює університети, мовні школи, професійні школи та інші заклади
"""

import psycopg2
import os

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='SK'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def update_universities(conn, jurisdiction_id):
    """Update existing universities and add missing ones"""
    cursor = conn.cursor()
    
    universities = [
        {
            'name': 'Comenius University in Bratislava',
            'name_local': 'Univerzita Komenského v Bratislave',
            'type': 'university',
            'city': 'Bratislava',
            'country': 'SK',
            'website_url': 'https://uniba.sk',
            'student_count': 20000,
            'ranking_position': 1,
            'description': 'The oldest and largest university in Slovakia, founded in 1919. Offers programs in medicine, law, natural sciences, and humanities.'
        },
        {
            'name': 'Slovak University of Technology in Bratislava',
            'name_local': 'Slovenská technická univerzita v Bratislave',
            'type': 'university',
            'city': 'Bratislava',
            'country': 'SK',
            'website_url': 'https://www.stuba.sk',
            'student_count': 15000,
            'ranking_position': 2,
            'description': 'Leading technical university in Slovakia, specializing in engineering, architecture, and technology.'
        },
        {
            'name': 'University of Economics in Bratislava',
            'name_local': 'Ekonomická univerzita v Bratislave',
            'type': 'university',
            'city': 'Bratislava',
            'country': 'SK',
            'website_url': 'https://euba.sk',
            'student_count': 8000,
            'ranking_position': 3,
            'description': 'Premier economics and business university in Slovakia, offering programs in economics, business administration, and international relations.'
        },
        {
            'name': 'Pavol Jozef Šafárik University in Košice',
            'name_local': 'Univerzita Pavla Jozefa Šafárika v Košiciach',
            'type': 'university',
            'city': 'Košice',
            'country': 'SK',
            'website_url': 'https://www.upjs.sk',
            'student_count': 7000,
            'ranking_position': 4,
            'description': 'Major university in eastern Slovakia, strong in natural sciences, medicine, and public administration.'
        },
        {
            'name': 'Technical University of Košice',
            'name_local': 'Technická univerzita v Košiciach',
            'type': 'university',
            'city': 'Košice',
            'country': 'SK',
            'website_url': 'https://www.tuke.sk',
            'student_count': 10000,
            'ranking_position': 5,
            'description': 'Technical university focused on engineering, informatics, and technology in eastern Slovakia.'
        }
    ]
    
    for uni in universities:
        # Check if university exists
        cursor.execute(
            "SELECT id FROM universities WHERE name = %s",
            (uni['name'],)
        )
        existing = cursor.fetchone()
        
        if existing:
            # Update existing
            cursor.execute("""
                UPDATE universities 
                SET name_local = %s, type = %s, city = %s, country = %s, 
                    website_url = %s, student_count = %s, ranking_position = %s,
                    description = %s, jurisdiction_id = %s, is_active = true
                WHERE name = %s
            """, (
                uni['name_local'], uni['type'], uni['city'], uni['country'],
                uni['website_url'], uni['student_count'], uni['ranking_position'],
                uni['description'], jurisdiction_id, uni['name']
            ))
            print(f"✅ Updated: {uni['name']}")
        else:
            # Insert new
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
    
    cursor.close()

def add_language_schools(conn, jurisdiction_id):
    """Add language schools"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'State Language School Bratislava',
            'name_local': 'Štátna jazyková škola Bratislava',
            'type': 'language_school',
            'city': 'Bratislava',
            'website_url': 'https://1sjs.sk',
            'description': 'State-run language school offering courses in English, German, French, Spanish, and other languages.'
        },
        {
            'name': 'VEVE Language School',
            'name_local': 'Jazyková škola VEVE',
            'type': 'language_school',
            'city': 'Bratislava',
            'website_url': 'https://veve.sk',
            'description': 'Private language school specializing in Slovak language courses for foreigners.'
        },
        {
            'name': 'International House Bratislava',
            'name_local': 'International House Bratislava',
            'type': 'language_school',
            'city': 'Bratislava',
            'website_url': 'https://ihbratislava.sk',
            'description': 'International language school offering English and Slovak courses with certified teachers.'
        }
    ]
    
    for school in schools:
        cursor.execute(
            "SELECT id FROM universities WHERE name = %s",
            (school['name'],)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.execute("""
                INSERT INTO universities 
                (name, name_local, type, city, country, website_url, description, jurisdiction_id, is_active)
                VALUES (%s, %s, %s, %s, 'SK', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"✅ Added language school: {school['name']}")
    
    cursor.close()

def add_vocational_schools(conn, jurisdiction_id):
    """Add vocational schools"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Business Academy Bratislava',
            'name_local': 'Obchodná akadémia, Nevädzová 3, Bratislava',
            'type': 'vocational_school',
            'city': 'Bratislava',
            'website_url': 'https://oanba.edupage.org',
            'description': 'Vocational school specializing in business, economics, and administration.'
        }
    ]
    
    for school in schools:
        cursor.execute(
            "SELECT id FROM universities WHERE name = %s",
            (school['name'],)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.execute("""
                INSERT INTO universities 
                (name, name_local, type, city, country, website_url, description, jurisdiction_id, is_active)
                VALUES (%s, %s, %s, %s, 'SK', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"✅ Added vocational school: {school['name']}")
    
    cursor.close()

def add_other_institutions(conn, jurisdiction_id):
    """Add conservatories and foundation programs"""
    cursor = conn.cursor()
    
    institutions = [
        {
            'name': 'Conservatory Bratislava',
            'name_local': 'Konzervatórium Bratislava',
            'type': 'conservatory',
            'city': 'Bratislava',
            'website_url': 'https://konzervatorium.sk',
            'description': 'Music and arts conservatory offering professional training in music, dance, and drama.'
        },
        {
            'name': 'STU Foundation Program for Foreigners',
            'name_local': 'Prípravný kurz slovenčiny STU',
            'type': 'foundation_program',
            'city': 'Bratislava',
            'website_url': 'https://www.stuba.sk',
            'description': 'Slovak language preparatory course for international students planning to study at STU.'
        },
        {
            'name': 'EUBA Foundation Program',
            'name_local': 'Prípravný kurz slovenčiny EUBA',
            'type': 'foundation_program',
            'city': 'Bratislava',
            'website_url': 'https://www.euba.sk',
            'description': 'Slovak language and academic preparation program for international students.'
        },
        {
            'name': 'GoStudy Slovakia Foundation Program',
            'name_local': 'GoStudy Prípravný program',
            'type': 'foundation_program',
            'city': 'Bratislava',
            'website_url': 'https://gostudy.eu',
            'description': 'Comprehensive foundation program preparing international students for Slovak universities.'
        }
    ]
    
    for inst in institutions:
        cursor.execute(
            "SELECT id FROM universities WHERE name = %s",
            (inst['name'],)
        )
        existing = cursor.fetchone()
        
        if not existing:
            cursor.execute("""
                INSERT INTO universities 
                (name, name_local, type, city, country, website_url, description, jurisdiction_id, is_active)
                VALUES (%s, %s, %s, %s, 'SK', %s, %s, %s, true)
            """, (
                inst['name'], inst['name_local'], inst['type'], inst['city'],
                inst['website_url'], inst['description'], jurisdiction_id
            ))
            print(f"✅ Added {inst['type']}: {inst['name']}")
    
    cursor.close()

def main():
    print("🔄 Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    
    try:
        # Get Slovak jurisdiction ID
        jurisdiction_id = get_jurisdiction_id(conn, 'SK')
        if not jurisdiction_id:
            print("❌ Slovak jurisdiction not found!")
            return
        
        print(f"✅ Found Slovak jurisdiction (ID: {jurisdiction_id})")
        
        # Update/add all institutions
        print("\n📚 Updating universities...")
        update_universities(conn, jurisdiction_id)
        
        print("\n🗣️ Adding language schools...")
        add_language_schools(conn, jurisdiction_id)
        
        print("\n🏫 Adding vocational schools...")
        add_vocational_schools(conn, jurisdiction_id)
        
        print("\n🎭 Adding other institutions...")
        add_other_institutions(conn, jurisdiction_id)
        
        print("\n✅ All Slovak educational institutions restored successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
