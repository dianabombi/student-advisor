"""
Script to populate database with sample Slovak universities and programs
Run this after migration to add initial data
"""

import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import University, Program, Jurisdiction, Base

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5434/codex_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def populate_universities():
    """Add 5 Slovak universities with programs"""
    db = SessionLocal()
    
    try:
        # Get Slovakia jurisdiction
        sk_jurisdiction = db.query(Jurisdiction).filter_by(code='SK').first()
        if not sk_jurisdiction:
            print("❌ Slovakia jurisdiction not found! Please add it first.")
            return
        
        print("🎓 Adding Slovak universities...")
        
        # 1. Comenius University
        comenius = University(
            jurisdiction_id=sk_jurisdiction.id,
            name="Comenius University in Bratislava",
            name_local="Univerzita Komenského v Bratislave",
            type="university",
            website_url="https://uniba.sk",
            city="Bratislava",
            country="SK",
            description="The oldest and largest university in Slovakia, founded in 1919. Offers programs in medicine, law, natural sciences, and humanities.",
            student_count=20000,
            ranking_position=1
        )
        db.add(comenius)
        db.flush()
        
        # Add programs for Comenius
        comenius_programs = [
            Program(
                university_id=comenius.id,
                name="Medicine",
                name_local="Všeobecné lekárstvo",
                degree_level="master",
                field_of_study="Medicine",
                language="sk",
                duration_years=6,
                tuition_fee=0,  # Free for EU students
                description="Six-year medical program leading to MD degree",
                admission_requirements={
                    "min_gpa": 3.5,
                    "required_subjects": ["Biology", "Chemistry"],
                    "entrance_exam": True,
                    "language_proficiency": {"sk": "C1"}
                },
                application_deadline=datetime(2026, 4, 30),
                start_date=datetime(2026, 9, 1),
                capacity=200
            ),
            Program(
                university_id=comenius.id,
                name="Computer Science",
                name_local="Informatika",
                degree_level="bachelor",
                field_of_study="Computer Science",
                language="sk",
                duration_years=3,
                tuition_fee=0,
                description="Three-year bachelor program in computer science",
                admission_requirements={
                    "min_gpa": 3.0,
                    "required_subjects": ["Mathematics"],
                    "entrance_exam": True,
                    "language_proficiency": {"sk": "B2"}
                },
                application_deadline=datetime(2026, 6, 30),
                start_date=datetime(2026, 9, 15),
                capacity=150
            )
        ]
        db.add_all(comenius_programs)
        
        # 2. Slovak University of Technology
        stuba = University(
            jurisdiction_id=sk_jurisdiction.id,
            name="Slovak University of Technology in Bratislava",
            name_local="Slovenská technická univerzita v Bratislave",
            type="university",
            website_url="https://www.stuba.sk",
            city="Bratislava",
            country="SK",
            description="Leading technical university specializing in engineering, architecture, and technology.",
            student_count=15000,
            ranking_position=2
        )
        db.add(stuba)
        db.flush()
        
        stuba_programs = [
            Program(
                university_id=stuba.id,
                name="Civil Engineering",
                name_local="Stavebné inžinierstvo",
                degree_level="bachelor",
                field_of_study="Engineering",
                language="sk",
                duration_years=3,
                tuition_fee=0,
                description="Bachelor program in civil engineering",
                admission_requirements={
                    "min_gpa": 2.8,
                    "required_subjects": ["Mathematics", "Physics"],
                    "entrance_exam": True
                },
                application_deadline=datetime(2026, 6, 15),
                start_date=datetime(2026, 9, 15)
            )
        ]
        db.add_all(stuba_programs)
        
        # 3. University of Economics
        euba = University(
            jurisdiction_id=sk_jurisdiction.id,
            name="University of Economics in Bratislava",
            name_local="Ekonomická univerzita v Bratislave",
            type="university",
            website_url="https://euba.sk",
            city="Bratislava",
            country="SK",
            description="Premier economics and business university in Slovakia.",
            student_count=8000,
            ranking_position=3
        )
        db.add(euba)
        db.flush()
        
        euba_programs = [
            Program(
                university_id=euba.id,
                name="Business Administration",
                name_local="Podnikové hospodárstvo",
                degree_level="bachelor",
                field_of_study="Business",
                language="sk",
                duration_years=3,
                tuition_fee=0,
                description="Bachelor program in business administration",
                admission_requirements={
                    "min_gpa": 2.5,
                    "entrance_exam": True
                },
                application_deadline=datetime(2026, 6, 30),
                start_date=datetime(2026, 9, 15)
            )
        ]
        db.add_all(euba_programs)
        
        # 4. Pavol Jozef Šafárik University
        upjs = University(
            jurisdiction_id=sk_jurisdiction.id,
            name="Pavol Jozef Šafárik University in Košice",
            name_local="Univerzita Pavla Jozefa Šafárika v Košiciach",
            type="university",
            website_url="https://www.upjs.sk",
            city="Košice",
            country="SK",
            description="Major university in eastern Slovakia, strong in natural sciences and medicine.",
            student_count=7000,
            ranking_position=4
        )
        db.add(upjs)
        db.flush()
        
        # 5. Technical University of Košice
        tuke = University(
            jurisdiction_id=sk_jurisdiction.id,
            name="Technical University of Košice",
            name_local="Technická univerzita v Košiciach",
            type="university",
            website_url="https://www.tuke.sk",
            city="Košice",
            country="SK",
            description="Technical university focused on engineering, informatics, and technology.",
            student_count=12000,
            ranking_position=5
        )
        db.add(tuke)
        
        db.commit()
        print("✅ Successfully added 5 Slovak universities with programs!")
        print(f"   - {comenius.name}")
        print(f"   - {stuba.name}")
        print(f"   - {euba.name}")
        print(f"   - {upjs.name}")
        print(f"   - {tuke.name}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Populating database with Slovak universities...")
    populate_universities()
    print("✅ Done!")
