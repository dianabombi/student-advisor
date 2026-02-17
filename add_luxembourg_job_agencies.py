import sys
import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.orm import sessionmaker, declarative_base
# from dotenv import load_dotenv

# Load environment variables
# load_dotenv()

# Define Base
Base = declarative_base()

# Define JobAgency model locally to avoid importing heavy backend.main
class JobAgency(Base):
    __tablename__ = 'job_agencies'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    website_url = Column(String)
    city = Column(String)
    country_code = Column(String)
    description = Column(Text)
    specialization = Column(String)
    is_active = Column(Boolean, default=True)

def add_luxembourg_agencies():
    # Setup DB connection
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        print("Error: DATABASE_URL not found in .env")
        return

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    agencies = [
        # LUXEMBOURG CITY
        {
            "name": "Jobs.lu",
            "url": "https://www.jobs.lu",
            "city": "Luxembourg",
            "country_code": "LU",
            "description": "Leading job board in Luxembourg with English listings",
            "specialization": "General, Student jobs, Internships"
        },
        {
            "name": "Moovijob.com",
            "url": "https://www.moovijob.com",
            "city": "Luxembourg",
            "country_code": "LU",
            "description": "Major recruitment site in Luxembourg, organizes job fairs",
            "specialization": "General, Student jobs, Seasonal work"
        },
        {
            "name": "Jugendinfo.lu",
            "url": "https://www.jugendinfo.lu",
            "city": "Luxembourg",
            "country_code": "LU",
            "description": "Information and jobs specifically for young people",
            "specialization": "Student jobs, Summer jobs, Internships"
        },
        {
            "name": "Indeed Luxembourg",
            "url": "https://lu.indeed.com",
            "city": "Luxembourg",
            "country_code": "LU",
            "description": "Global job search engine - Luxembourg branch",
            "specialization": "General, Student jobs"
        },
        
        # ESCH-SUR-ALZETTE (Main University Campus)
        {
            "name": "Jobs.lu",
            "url": "https://www.jobs.lu",
            "city": "Esch-sur-Alzette",
            "country_code": "LU",
            "description": "Leading job board in Luxembourg",
            "specialization": "General, Student jobs"
        },
        {
            "name": "Moovijob.com",
            "url": "https://www.moovijob.com",
            "city": "Esch-sur-Alzette",
            "country_code": "LU",
            "description": "Major recruitment site in Luxembourg",
            "specialization": "General, Student jobs"
        },
        {
            "name": "Jugendinfo.lu",
            "url": "https://www.jugendinfo.lu",
            "city": "Esch-sur-Alzette",
            "country_code": "LU",
            "description": "Information and jobs specifically for young people",
            "specialization": "Student jobs"
        },
        
        # DIFFERDANGE (LUNEX University)
        {
            "name": "Jobs.lu",
            "url": "https://www.jobs.lu",
            "city": "Differdange",
            "country_code": "LU",
            "description": "Leading job board in Luxembourg",
            "specialization": "General, Student jobs"
        },
        {
            "name": "Moovijob.com",
            "url": "https://www.moovijob.com",
            "city": "Differdange",
            "country_code": "LU",
            "description": "Major recruitment site in Luxembourg",
            "specialization": "General, Student jobs"
        }
    ]
    
    print(f"Adding {len(agencies)} Luxembourg agencies...")
    
    count = 0
    try:
        for agency_data in agencies:
            # Check if exists
            exists = db.query(JobAgency).filter(
                JobAgency.name == agency_data["name"],
                JobAgency.city == agency_data["city"],
                JobAgency.country_code == agency_data["country_code"]
            ).first()
            
            if not exists:
                new_agency = JobAgency(
                    name=agency_data["name"],
                    website_url=agency_data["url"],
                    city=agency_data["city"],
                    country_code=agency_data["country_code"],
                    description=agency_data["description"],
                    specialization=agency_data["specialization"],
                    is_active=True
                )
                db.add(new_agency)
                count += 1
                print(f"Added: {agency_data['name']} ({agency_data['city']})")
            else:
                print(f"Skipped (exists): {agency_data['name']} ({agency_data['city']})")
                
        db.commit()
        print(f"✅ Successfully added {count} new Luxembourg agencies!")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_luxembourg_agencies()
