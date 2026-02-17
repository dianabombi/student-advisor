А Vytvoriť účet
Vytvorte si účet

Field required, Field required, Field required
Meno
Eduard
Priezvisko
Pavlyshche
E-mail
karpaty88888@post.sk
Heslo
•••••
Potvrďte heslo
•••••

Prečítal som a súhlasím s Podmienkami používania a Zásadami ochrany osobných údajov

Vytvoriť účet"""
Додавання польських навчальних закладів
Університети, мовні школи та інші заклади, які приймають іноземних студентів
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='PL'):
    """Get jurisdiction ID by code"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_polish_universities(conn, jurisdiction_id):
    """Add major Polish universities that accept international students"""
    cursor = conn.cursor()
    
    universities = [
        {
            'name': 'University of Warsaw',
            'name_local': 'Uniwersytet Warszawski',
            'type': 'university',
            'city': 'Warszawa',
            'country': 'PL',
            'website_url': 'https://www.uw.edu.pl',
            'student_count': 40000,
            'ranking_position': 1,
            'description': 'Largest and most prestigious university in Poland. Offers programs in humanities, natural sciences, social sciences, and law. Many English-taught programs.'
        },
        {
            'name': 'Jagiellonian University',
            'name_local': 'Uniwersytet Jagielloński',
            'type': 'university',
            'city': 'Kraków',
            'country': 'PL',
            'website_url': 'https://www.uj.edu.pl',
            'student_count': 35000,
            'ranking_position': 2,
            'description': 'Oldest university in Poland, founded in 1364. Strong in medicine, law, humanities, and natural sciences. Very popular among international students.'
        },
        {
            'name': 'Warsaw University of Technology',
            'name_local': 'Politechnika Warszawska',
            'type': 'university',
            'city': 'Warszawa',
            'country': 'PL',
            'website_url': 'https://www.pw.edu.pl',
            'student_count': 30000,
            'ranking_position': 3,
            'description': 'Leading technical university in Poland, specializing in engineering, IT, architecture, and technology.'
        },
        {
            'name': 'Adam Mickiewicz University',
            'name_local': 'Uniwersytet im. Adama Mickiewicza w Poznaniu',
            'type': 'university',
            'city': 'Poznań',
            'country': 'PL',
            'website_url': 'https://www.amu.edu.pl',
            'student_count': 38000,
            'ranking_position': 4,
            'description': 'Major university in western Poland, offering programs in humanities, social sciences, natural sciences, and law.'
        },
        {
            'name': 'AGH University of Science and Technology',
            'name_local': 'Akademia Górniczo-Hutnicza',
            'type': 'university',
            'city': 'Kraków',
            'country': 'PL',
            'website_url': 'https://www.agh.edu.pl',
            'student_count': 25000,
            'ranking_position': 5,
            'description': 'Top technical university specializing in mining, metallurgy, engineering, IT, and applied sciences.'
        },
        {
            'name': 'University of Wrocław',
            'name_local': 'Uniwersytet Wrocławski',
            'type': 'university',
            'city': 'Wrocław',
            'country': 'PL',
            'website_url': 'https://www.uni.wroc.pl',
            'student_count': 26000,
            'ranking_position': 6,
            'description': 'Historic university offering programs in natural sciences, humanities, law, and social sciences.'
        },
        {
            'name': 'Gdańsk University of Technology',
            'name_local': 'Politechnika Gdańska',
            'type': 'university',
            'city': 'Gdańsk',
            'country': 'PL',
            'website_url': 'https://www.pg.edu.pl',
            'student_count': 24000,
            'ranking_position': 7,
            'description': 'Technical university in northern Poland, strong in engineering, IT, and maritime technologies.'
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

def add_polish_language_schools(conn, jurisdiction_id):
    """Add Polish language schools for foreigners"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Polish Language School at University of Warsaw',
            'name_local': 'Szkoła Języka Polskiego UW',
            'type': 'language_school',
            'city': 'Warszawa',
            'website_url': 'https://www.sjp.uw.edu.pl',
            'description': 'Official Polish language school of University of Warsaw, offering courses for foreigners at all levels.'
        },
        {
            'name': 'Jagiellonian University Polish Language School',
            'name_local': 'Szkoła Języka i Kultury Polskiej UJ',
            'type': 'language_school',
            'city': 'Kraków',
            'website_url': 'https://www.sjikp.uj.edu.pl',
            'description': 'Polish language and culture school at Jagiellonian University, popular among international students.'
        },
        {
            'name': 'Glossa Polish Language School',
            'name_local': 'Szkoła Języka Polskiego Glossa',
            'type': 'language_school',
            'city': 'Kraków',
            'website_url': 'https://www.glossa.pl',
            'description': 'Private language school specializing in Polish courses for foreigners, including exam preparation.'
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
                VALUES (%s, %s, %s, %s, 'PL', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"✅ Added language school: {school['name']}")
        else:
            print(f"⏭️  Already exists: {school['name']}")
    
    cursor.close()

def add_polish_vocational_schools(conn, jurisdiction_id):
    """Add Polish vocational schools"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Warsaw School of Economics',
            'name_local': 'Szkoła Główna Handlowa w Warszawie',
            'type': 'vocational_school',
            'city': 'Warszawa',
            'website_url': 'https://www.sgh.waw.pl',
            'description': 'Prestigious business and economics school offering undergraduate and graduate programs.'
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
                VALUES (%s, %s, %s, %s, 'PL', %s, %s, %s, true)
            """, (
                school['name'], school['name_local'], school['type'], school['city'],
                school['website_url'], school['description'], jurisdiction_id
            ))
            print(f"✅ Added vocational school: {school['name']}")
        else:
            print(f"⏭️  Already exists: {school['name']}")
    
    cursor.close()

def add_polish_conservatories(conn, jurisdiction_id):
    """Add Polish conservatories"""
    cursor = conn.cursor()
    
    conservatories = [
        {
            'name': 'Fryderyk Chopin University of Music',
            'name_local': 'Uniwersytet Muzyczny Fryderyka Chopina',
            'type': 'conservatory',
            'city': 'Warszawa',
            'website_url': 'https://www.chopin.edu.pl',
            'description': 'Prestigious music university named after Fryderyk Chopin, offering programs in classical music, jazz, and composition.'
        },
        {
            'name': 'Academy of Music in Kraków',
            'name_local': 'Akademia Muzyczna w Krakowie',
            'type': 'conservatory',
            'city': 'Kraków',
            'website_url': 'https://www.amuz.krakow.pl',
            'description': 'Music academy offering programs in classical music, jazz, composition, and music education.'
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
                VALUES (%s, %s, %s, %s, 'PL', %s, %s, %s, true)
            """, (
                conservatory['name'], conservatory['name_local'], conservatory['type'], 
                conservatory['city'], conservatory['website_url'], conservatory['description'], 
                jurisdiction_id
            ))
            print(f"✅ Added conservatory: {conservatory['name']}")
        else:
            print(f"⏭️  Already exists: {conservatory['name']}")
    
    cursor.close()

def add_polish_foundation_programs(conn, jurisdiction_id):
    """Add foundation/preparatory programs"""
    cursor = conn.cursor()
    
    programs = [
        {
            'name': 'University of Warsaw Preparatory Course',
            'name_local': 'Kurs przygotowawczy UW',
            'type': 'foundation_program',
            'city': 'Warszawa',
            'website_url': 'https://www.uw.edu.pl',
            'description': 'One-year preparatory program for international students planning to study at Polish universities.'
        },
        {
            'name': 'Jagiellonian University Foundation Year',
            'name_local': 'Rok przygotowawczy UJ',
            'type': 'foundation_program',
            'city': 'Kraków',
            'website_url': 'https://www.uj.edu.pl',
            'description': 'Foundation year program preparing international students for studies at Polish universities.'
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
                VALUES (%s, %s, %s, %s, 'PL', %s, %s, %s, true)
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
        # Get Polish jurisdiction ID
        jurisdiction_id = get_jurisdiction_id(conn, 'PL')
        if not jurisdiction_id:
            print("❌ Polish jurisdiction not found!")
            return
        
        print(f"✅ Found Polish jurisdiction (ID: {jurisdiction_id})")
        
        # Add all Polish institutions
        print("\n📚 Adding Polish universities...")
        add_polish_universities(conn, jurisdiction_id)
        
        print("\n🗣️ Adding Polish language schools...")
        add_polish_language_schools(conn, jurisdiction_id)
        
        print("\n🏫 Adding Polish vocational schools...")
        add_polish_vocational_schools(conn, jurisdiction_id)
        
        print("\n🎨 Adding Polish conservatories...")
        add_polish_conservatories(conn, jurisdiction_id)
        
        print("\n🎓 Adding foundation programs...")
        add_polish_foundation_programs(conn, jurisdiction_id)
        
        print("\n✅ All Polish educational institutions added successfully!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\n📊 Polish institutions summary:")
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
