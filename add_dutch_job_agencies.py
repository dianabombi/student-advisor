import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.orm import sessionmaker, declarative_base

# Define Base
Base = declarative_base()

class JobAgency(Base):
    __tablename__ = "job_agencies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    website_url = Column(String)
    city = Column(String, index=True)
    country_code = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    description = Column(Text, nullable=True)

def add_dutch_agencies():
    # Setup DB connection from env (or default to localhost for dev)
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        # Fallback specifically for this standalone run if env is missing
        print("Warning: DATABASE_URL not found, assuming local docker-compose default")
        DATABASE_URL = "postgresql://user:password@db:5432/codex_db"
    
    # Logic to fix host for local execution is REMOVED for Docker pipe execution
    # if "@db:" in DATABASE_URL:
    #     DATABASE_URL = DATABASE_URL.replace("@db:", "@localhost:")
    # elif "@db/" in DATABASE_URL:
    #     DATABASE_URL = DATABASE_URL.replace("@db/", "@localhost/")

    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    cities = [
        "Amsterdam", "Rotterdam", "Utrecht", "Leiden", "Groningen", 
        "Delft", "The Hague", "Eindhoven", "Maastricht", "Tilburg", 
        "Nijmegen", "Wageningen", "Enschede"
    ]

    # Common agencies for all cities
    base_agencies = [
        {"name": "StudentJob.nl", "url": "https://www.studentjob.nl", "description": "Specialized platform for student jobs and internships."},
        {"name": "Indeed Netherlands", "url": "https://www.indeed.nl", "description": "General job search engine with extensive student listings."},
        {"name": "Randstad", "url": "https://www.randstad.nl", "description": "Major employment agency with student-specific vacancies."},
        {"name": "YoungCapital", "url": "https://www.youngcapital.nl", "description": "Agency focused on students, graduates and young professionals."}
    ]

    count = 0
    try:
        for city in cities:
            for agency in base_agencies:
                exists = db.query(JobAgency).filter(
                    JobAgency.name == agency["name"],
                    JobAgency.city == city,
                    JobAgency.country_code == "NL"
                ).first()

                if not exists:
                    new_agency = JobAgency(
                        name=agency["name"],
                        website_url=agency["url"],
                        city=city,
                        country_code="NL",
                        description=agency["description"]
                    )
                    db.add(new_agency)
                    print(f"Added: {agency['name']} ({city})")
                    count += 1
                else:
                    # Update description if missing
                    if not exists.description:
                        exists.description = agency["description"]
                        print(f"Updated description: {agency['name']} ({city})")
        
        db.commit()
        print(f"Successfully added/updated {count} Dutch agencies!")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_dutch_agencies()
