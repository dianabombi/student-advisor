"""
Додавання чеських професійних шкіл та консерваторій
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def get_jurisdiction_id(conn, code='CZ'):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM jurisdictions WHERE code = %s", (code,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_czech_vocational_schools(conn, jurisdiction_id):
    """Add Czech vocational schools (Střední odborné školy)"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Business Academy Prague',
            'name_local': 'Obchodní akademie, Praha 1, Resslova 8',
            'type': 'vocational_school',
            'city': 'Praha',
            'website_url': 'https://oa-resslova.cz',
            'description': 'Prestigious vocational school specializing in business, economics, and administration. Offers programs in Czech and English.'
        },
        {
            'name': 'Secondary Technical School of Electrical Engineering Prague',
            'name_local': 'Střední průmyslová škola elektrotechnická, Praha',
            'type': 'vocational_school',
            'city': 'Praha',
            'website_url': 'https://www.spse.cz',
            'description': 'Technical vocational school focusing on electrical engineering, electronics, and IT.'
        },
        {
            'name': 'Hotel School Prague',
            'name_local': 'Hotelová škola, Praha',
            'type': 'vocational_school',
            'city': 'Praha',
            'website_url': 'https://www.hotelka.cz',
            'description': 'Vocational school specializing in hotel management, tourism, and gastronomy.'
        },
        {
            'name': 'Business Academy Brno',
            'name_local': 'Obchodní akademie, Brno, Kotlářská 9',
            'type': 'vocational_school',
            'city': 'Brno',
            'website_url': 'https://www.oa-brno.cz',
            'description': 'Vocational school offering programs in business, economics, and foreign languages.'
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
            print(f"✅ Added vocational school: {school['name']}")
        else:
            print(f"⏭️  Already exists: {school['name']}")
    
    cursor.close()

def add_czech_conservatories(conn, jurisdiction_id):
    """Add Czech conservatories (Konzervatoře)"""
    cursor = conn.cursor()
    
    conservatories = [
        {
            'name': 'Prague Conservatory',
            'name_local': 'Pražská konzervatoř',
            'type': 'conservatory',
            'city': 'Praha',
            'website_url': 'https://www.prgcons.cz',
            'description': 'Prestigious music conservatory offering programs in classical music, jazz, and musical theatre. Founded in 1808.'
        },
        {
            'name': 'Jaroslav Ježek Conservatory',
            'name_local': 'Konzervatoř Jaroslava Ježka',
            'type': 'conservatory',
            'city': 'Praha',
            'website_url': 'https://www.kjj.cz',
            'description': 'Modern conservatory specializing in jazz, popular music, and musical production.'
        },
        {
            'name': 'Brno Conservatory',
            'name_local': 'Konzervatoř Brno',
            'type': 'conservatory',
            'city': 'Brno',
            'website_url': 'https://www.konzervatorbmo.cz',
            'description': 'Music and dance conservatory offering programs in classical music, dance, and drama.'
        },
        {
            'name': 'Duncan Centre Conservatory',
            'name_local': 'Konzervatoř Duncan Centre',
            'type': 'conservatory',
            'city': 'Praha',
            'website_url': 'https://www.duncancentre.cz',
            'description': 'Private conservatory specializing in contemporary dance, ballet, and choreography.'
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
                VALUES (%s, %s, %s, %s, 'CZ', %s, %s, %s, true)
            """, (
                conservatory['name'], conservatory['name_local'], conservatory['type'], 
                conservatory['city'], conservatory['website_url'], conservatory['description'], 
                jurisdiction_id
            ))
            print(f"✅ Added conservatory: {conservatory['name']}")
        else:
            print(f"⏭️  Already exists: {conservatory['name']}")
    
    cursor.close()

def main():
    print("🔄 Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    
    try:
        jurisdiction_id = get_jurisdiction_id(conn, 'CZ')
        if not jurisdiction_id:
            print("❌ Czech jurisdiction not found!")
            return
        
        print(f"✅ Found Czech jurisdiction (ID: {jurisdiction_id})")
        
        print("\n🏫 Adding Czech vocational schools...")
        add_czech_vocational_schools(conn, jurisdiction_id)
        
        print("\n🎨 Adding Czech conservatories...")
        add_czech_conservatories(conn, jurisdiction_id)
        
        print("\n✅ All Czech vocational schools and conservatories added!")
        
        # Show summary
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\n📊 Czech institutions summary:")
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
