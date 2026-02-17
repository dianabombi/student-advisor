"""
Додавання австрійських професійних шкіл (Berufsschulen)
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

def add_austrian_vocational_schools(conn, jurisdiction_id):
    """Add Austrian vocational schools (Berufsschulen)"""
    cursor = conn.cursor()
    
    schools = [
        {
            'name': 'Vienna Business School',
            'name_local': 'Vienna Business School',
            'type': 'vocational_school',
            'city': 'Wien',
            'website_url': 'https://www.vbs.ac.at',
            'description': 'Leading business school in Vienna offering vocational education in business, tourism, and IT.'
        },
        {
            'name': 'WIFI Vienna',
            'name_local': 'WIFI Wien',
            'type': 'vocational_school',
            'city': 'Wien',
            'website_url': 'https://www.wifiwien.at',
            'description': 'Vocational training institute offering courses in various professional fields for adults and career changers.'
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
            print(f"Added vocational school: {school['name']}")
        else:
            print(f"Already exists: {school['name']}")
    
    cursor.close()

def main():
    print("Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    
    try:
        jurisdiction_id = get_jurisdiction_id(conn, 'AT')
        if not jurisdiction_id:
            print("Austrian jurisdiction not found!")
            return
        
        print(f"Found Austrian jurisdiction (ID: {jurisdiction_id})")
        print("\nAdding Austrian vocational schools...")
        add_austrian_vocational_schools(conn, jurisdiction_id)
        
        print("\nAustrian vocational schools added successfully!")
        
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
