"""
Виправлення Alba Graduate Business School
Додавання Athens Information Technology як заміну
"""

import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")

def main():
    print("Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    
    try:
        cursor = conn.cursor()
        
        # Get Greek jurisdiction ID
        cursor.execute("SELECT id FROM jurisdictions WHERE code = 'GR'")
        jurisdiction_id = cursor.fetchone()[0]
        
        # Add replacement vocational school
        cursor.execute("""
            INSERT INTO universities 
            (name, name_local, type, city, country, website_url, description, jurisdiction_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, true)
        """, (
            'Athens Information Technology',
            'Athens Information Technology',
            'vocational_school',
            'Athens',
            'GR',
            'https://www.ait.gr',
            'Private technology institute offering programs in computer science and IT.',
            jurisdiction_id
        ))
        print("Added: Athens Information Technology")
        
        # Show summary
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = %s 
            GROUP BY type 
            ORDER BY type
        """, (jurisdiction_id,))
        
        print("\nGreek institutions after fix:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.execute("""
            SELECT name, website_url 
            FROM universities 
            WHERE jurisdiction_id = %s AND type = 'vocational_school'
            ORDER BY name
        """, (jurisdiction_id,))
        
        print("\nGreek vocational schools:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.close()
        print("\nGreek vocational school fixed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
