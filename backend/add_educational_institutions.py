#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add educational institutions (language schools, vocational schools, conservatories, foundation programs)
to the database
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5433/codex_db')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Import models
from main import University

def add_educational_institutions():
    """Add language schools, vocational schools, conservatories, and foundation programs"""
    
    institutions = [
        # === LANGUAGE SCHOOLS ===
        {
            'name': 'State Language School Bratislava',
            'name_local': 'Štátna jazyková škola Bratislava',
            'description': 'The largest and oldest state language school in Bratislava, offering Slovak language courses for foreigners',
            'website_url': 'https://1sjs.sk',
            'contact_email': 'info@1sjs.sk',
            'contact_phone': '+421 2 5443 2437',
            'address': 'Palisády 38, 811 06 Bratislava',
            'city': 'Bratislava',
            'country': 'SK',
            'student_count': 500,
            'founded_year': 1954,
            'institution_type': 'language_school',
            'programs_count': 10
        },
        {
            'name': 'VEVE Language School',
            'name_local': 'Jazyková škola VEVE',
            'description': 'Private language school offering Slovak language courses for foreigners with flexible schedules',
            'website_url': 'https://veve.sk',
            'contact_email': 'info@veve.sk',
            'address': 'Bratislava',
            'city': 'Bratislava',
            'country': 'SK',
            'student_count': 200,
            'institution_type': 'language_school',
            'programs_count': 5
        },
        {
            'name': 'International House Bratislava',
            'name_local': 'International House Bratislava',
            'description': 'International language school offering Slovak language courses from beginner to advanced levels',
            'website_url': 'https://ihbratislava.sk',
            'contact_email': 'info@ihbratislava.sk',
            'address': 'Bratislava',
            'city': 'Bratislava',
            'country': 'SK',
            'student_count': 300,
            'institution_type': 'language_school',
            'programs_count': 8
        },
        
        # === VOCATIONAL SCHOOLS ===
        {
            'name': 'Business Academy Bratislava',
            'name_local': 'Obchodná akadémia, Nevädzová 3, Bratislava',
            'description': 'One of the most active vocational schools in Slovakia specializing in economics and business',
            'website_url': 'https://oanba.edupage.org',
            'contact_email': 'oanba@oanba.sk',
            'address': 'Nevädzová 3, Bratislava',
            'city': 'Bratislava',
            'country': 'SK',
            'student_count': 600,
            'founded_year': 1950,
            'institution_type': 'vocational_school',
            'programs_count': 4
        },
        {
            'name': 'Hotel Academy Bratislava',
            'name_local': 'Hotelová akadémia, Mikovíniho 1, Bratislava',
            'description': 'State hotel academy providing education in hospitality and gastronomy services',
            'website_url': 'https://www.hotelka.eu',
            'contact_email': 'info@hotelka.eu',
            'address': 'Mikovíniho 1, 841 03 Bratislava',
            'city': 'Bratislava',
            'country': 'SK',
            'student_count': 400,
            'founded_year': 1954,
            'institution_type': 'vocational_school',
            'programs_count': 3
        },
        {
            'name': 'Secondary Industrial School of Electrical Engineering',
            'name_local': 'Stredná priemyselná škola elektrotechnická',
            'description': 'Technical vocational school specializing in electrical engineering and electronics',
            'website_url': 'https://spse.sk',
            'address': 'Bratislava',
            'city': 'Bratislava',
            'country': 'SK',
            'student_count': 500,
            'institution_type': 'vocational_school',
            'programs_count': 5
        },
        
        # === CONSERVATORIES ===
        {
            'name': 'Conservatory Bratislava',
            'name_local': 'Konzervatórium Bratislava',
            'description': 'Secondary art school providing education in singing, musical instruments, and musical-dramatic art',
            'website_url': 'https://konzervatorium.sk',
            'contact_email': 'info@konzervatorium.sk',
            'address': 'Tolstého 11, 811 06 Bratislava',
            'city': 'Bratislava',
            'country': 'SK',
            'student_count': 300,
            'founded_year': 1919,
            'institution_type': 'conservatory',
            'programs_count': 6
        },
        {
            'name': 'Dance Conservatory Bratislava',
            'name_local': 'Tanečné konzervatórium Bratislava',
            'description': 'Specialized conservatory for dance education and choreography',
            'website_url': 'https://tkba.sk',
            'address': 'Bratislava',
            'city': 'Bratislava',
            'country': 'SK',
            'student_count': 150,
            'institution_type': 'conservatory',
            'programs_count': 3
        },
        
        # === FOUNDATION PROGRAMS ===
        {
            'name': 'STU Foundation Program for Foreigners',
            'name_local': 'Prípravný kurz slovenčiny STU',
            'description': 'Intensive Slovak language foundation program preparing foreigners for university studies in Slovakia',
            'website_url': 'https://www.stuba.sk',
            'contact_email': 'icv@stuba.sk',
            'address': 'Vazovova 5, 812 43 Bratislava',
            'city': 'Bratislava',
            'country': 'SK',
            'student_count': 100,
            'institution_type': 'foundation_program',
            'programs_count': 2
        },
        {
            'name': 'EUBA Foundation Program',
            'name_local': 'Prípravný kurz slovenčiny EUBA',
            'description': 'One-year Slovak language foundation program for international students planning to study at Slovak universities',
            'website_url': 'https://www.euba.sk',
            'contact_email': 'foundation@euba.sk',
            'address': 'Bratislava',
            'city': 'Bratislava',
            'country': 'SK',
            'student_count': 80,
            'institution_type': 'foundation_program',
            'programs_count': 1
        },
        {
            'name': 'GoStudy Slovakia Foundation Program',
            'name_local': 'GoStudy Prípravný program',
            'description': 'Comprehensive foundation program including Slovak language (B2 level) and general subjects preparation',
            'website_url': 'https://gostudy.eu',
            'contact_email': 'info@gostudy.eu',
            'address': 'Bratislava',
            'city': 'Bratislava',
            'country': 'SK',
            'student_count': 120,
            'institution_type': 'foundation_program',
            'programs_count': 4
        },
    ]
    
    # Get SK jurisdiction
    from main import Jurisdiction
    sk_jurisdiction = session.query(Jurisdiction).filter_by(code='SK').first()
    if not sk_jurisdiction:
        print("ERROR: SK jurisdiction not found. Please create it first.")
        return
    
    added_count = 0
    for inst_data in institutions:
        # Check if institution already exists
        existing = session.query(University).filter_by(
            name=inst_data['name']
        ).first()
        
        if existing:
            print(f"SKIP: {inst_data['name']} already exists")
            continue
        
        # Create new institution
        institution = University(
            name=inst_data['name'],
            name_local=inst_data['name_local'],
            description=inst_data['description'],
            website_url=inst_data['website_url'],
            contact_email=inst_data.get('contact_email'),
            contact_phone=inst_data.get('contact_phone'),
            address=inst_data.get('address'),
            city=inst_data['city'],
            country=inst_data['country'],
            jurisdiction_id=sk_jurisdiction.id,
            student_count=inst_data.get('student_count', 0),
            founded_year=inst_data.get('founded_year'),
            type=inst_data.get('institution_type', 'other'),
            is_active=True,
            created_at=datetime.utcnow()
        )
        
        session.add(institution)
        added_count += 1
        print(f"ADDED: {inst_data['name_local']}")
    
    session.commit()
    print(f"\n✅ Successfully added {added_count} educational institutions")
    print(f"Total institutions in database: {session.query(University).count()}")

if __name__ == '__main__':
    try:
        add_educational_institutions()
    except Exception as e:
        print(f"ERROR: {e}")
        session.rollback()
    finally:
        session.close()
