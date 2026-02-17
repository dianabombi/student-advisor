"""
Виправлення ліхтенштейнської мовної школи
Видалення Liechtenstein Language Centre (непрацююче посилання)
Ліхтенштейн - дуже мала країна, залишаємо тільки університет та інститут
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
        
        # Показати поточний стан
        cursor.execute("""
            SELECT type, COUNT(*) as count 
            FROM universities 
            WHERE jurisdiction_id = 18
            GROUP BY type 
            ORDER BY type
        """)
        
        print("\nLiechtenstein institutions after fix:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.execute("""
            SELECT name, website_url 
            FROM universities 
            WHERE jurisdiction_id = 18
            ORDER BY type, name
        """)
        
        print("\nAll Liechtenstein institutions:")
        for row in cursor.fetchall():
            print(f"   {row[0]}: {row[1]}")
        
        cursor.close()
        print("\nLanguage school removed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
