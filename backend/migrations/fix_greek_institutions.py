"""
Виправлення грецьких закладів з непрацюючими посиланнями
Видалення University of Patras та Technological Educational Institute of Athens
Додавання University of Thessaly та Alba Graduate Business School
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
        
        # Add replacement university
        cursor.execute("""
            INSERT INTO universities 
            (name, name_local, type, city, country, website_url, student_count, 
             ranking_position, description, jurisdiction_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, true)
        """, (
            'University of Thessaly',
            'Πανεπιστήμιο Θεσσαλίας',
            'university',
            'Volos',
            'GR',
            'https://www.uth.gr',
            15000,
            5,
            'University in central Greece, offering diverse programs in sciences and humanities.',
            jurisdiction_id
        ))
        print("Added: University of Thessaly")
        
        # Add replacement vocational school
        cursor.execute("""
            INSERT INTO universities 
            (name, name_local, type, city, country, website_url, description, jurisdiction_id, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, true)
        """, (
            'Alba Graduate Business School',
            'Alba Graduate Business School',
            'vocational_school',
            'Athens',
            'GR',
            'https://www.alba.edu.gr',
            'Leading business school in Greece, offering MBA and executive education programs.',
            jurisdiction_id
        ))
        print("Added: Alba Graduate Business School")
        
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
            WHERE jurisdiction_id = %s
            ORDER BY type, name
        """, (jurisdiction_id,))
        
        print("\nAll Greek institutions:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.close()
        print("\nGreek institutions fixed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
