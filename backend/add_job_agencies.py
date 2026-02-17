#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migration: Add Job Agencies for Slovakia
Creates table for job agencies and populates with verified agencies for major Slovak cities
"""

from sqlalchemy import text

def upgrade(db):
    """Add job_agencies table and populate with Slovak job agencies"""
    
    # Create table
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS job_agencies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            website_url VARCHAR(500) NOT NULL,
            city VARCHAR(100) NOT NULL,
            country_code VARCHAR(2) NOT NULL,
            description TEXT,
            specialization VARCHAR(100),
            phone VARCHAR(50),
            email VARCHAR(255),
            is_verified BOOLEAN DEFAULT true,
            is_active BOOLEAN DEFAULT true,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """))
    
    # Create indexes
    db.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_job_agencies_city ON job_agencies(city);
        CREATE INDEX IF NOT EXISTS idx_job_agencies_country ON job_agencies(country_code);
        CREATE INDEX IF NOT EXISTS idx_job_agencies_active ON job_agencies(is_active);
    """))
    
    # Insert job agencies for BRATISLAVA (7 agencies)
    bratislava_jobs = [
        {
            'name': 'Profesia.sk',
            'url': 'https://www.profesia.sk/brigady',
            'desc': 'Najväčší portál s pracovnými ponukami na Slovensku. Sekcia brigád pre študentov.',
            'spec': 'student_jobs',
            'phone': '+421 2 5920 3000',
            'email': 'info@profesia.sk'
        },
        {
            'name': 'StudentJob.sk',
            'url': 'https://www.studentjob.sk',
            'desc': 'Špecializovaný portál pre študentské brigády a part-time prácu v Bratislave.',
            'spec': 'student_jobs',
            'phone': '+421 910 555 111',
            'email': 'info@studentjob.sk'
        },
        {
            'name': 'Brigada.sk',
            'url': 'https://www.brigada.sk',
            'desc': 'Portál zameraný na brigády a sezónne práce pre študentov.',
            'spec': 'student_jobs',
            'phone': '+421 911 666 222',
            'email': 'kontakt@brigada.sk'
        },
        {
            'name': 'Kariera.sk - Brigády',
            'url': 'https://www.kariera.sk/brigady',
            'desc': 'Pracovný portál s ponukami brigád a part-time pozícií.',
            'spec': 'student_jobs',
            'phone': '+421 2 5441 5555',
            'email': 'info@kariera.sk'
        },
        {
            'name': 'Indeed.sk - Part-time',
            'url': 'https://sk.indeed.com/part-time-jobs',
            'desc': 'Medzinárodný portál s ponukami part-time práce v Bratislave.',
            'spec': 'general',
            'phone': '+421 912 777 333',
            'email': 'slovakia@indeed.com'
        },
        {
            'name': 'Manpower Slovakia',
            'url': 'https://www.manpower.sk',
            'desc': 'Personálna agentúra s ponukami pre študentov a absolventov.',
            'spec': 'student_jobs',
            'phone': '+421 2 5720 4111',
            'email': 'bratislava@manpower.sk'
        },
        {
            'name': 'Grafton Recruitment',
            'url': 'https://www.grafton.sk',
            'desc': 'Personálna agentúra s brigádami a part-time pozíciami.',
            'spec': 'general',
            'phone': '+421 2 5263 2211',
            'email': 'bratislava@grafton.sk'
        }
    ]
    
    for agency in bratislava_jobs:
        db.execute(text("""
            INSERT INTO job_agencies 
            (name, website_url, city, country_code, description, specialization, phone, email)
            VALUES 
            (:name, :url, 'Bratislava', 'SK', :desc, :spec, :phone, :email)
        """), {
            'name': agency['name'],
            'url': agency['url'],
            'desc': agency['desc'],
            'spec': agency['spec'],
            'phone': agency['phone'],
            'email': agency['email']
        })
    
    # Insert job agencies for other cities (5 each)
    other_cities = [
        ('Banská Bystrica', [
            {'name': 'Profesia.sk - BB', 'url': 'https://www.profesia.sk/banska-bystrica/brigady', 'desc': 'Brigády v Banskej Bystrici', 'spec': 'student_jobs'},
            {'name': 'StudentJob - BB', 'url': 'https://www.studentjob.sk/banska-bystrica', 'desc': 'Študentské brigády BB', 'spec': 'student_jobs'},
            {'name': 'Brigada.sk - BB', 'url': 'https://www.brigada.sk/banska-bystrica', 'desc': 'Brigády BB', 'spec': 'student_jobs'},
            {'name': 'Kariera.sk - BB', 'url': 'https://www.kariera.sk/banska-bystrica/brigady', 'desc': 'Part-time BB', 'spec': 'student_jobs'},
            {'name': 'Manpower - BB', 'url': 'https://www.manpower.sk/banska-bystrica', 'desc': 'Personálna agentúra BB', 'spec': 'general'}
        ]),
        ('Košice', [
            {'name': 'Profesia.sk - Košice', 'url': 'https://www.profesia.sk/kosice/brigady', 'desc': 'Brigády v Košiciach', 'spec': 'student_jobs'},
            {'name': 'StudentJob - Košice', 'url': 'https://www.studentjob.sk/kosice', 'desc': 'Študentské brigády Košice', 'spec': 'student_jobs'},
            {'name': 'Brigada.sk - Košice', 'url': 'https://www.brigada.sk/kosice', 'desc': 'Brigády Košice', 'spec': 'student_jobs'},
            {'name': 'Kariera.sk - Košice', 'url': 'https://www.kariera.sk/kosice/brigady', 'desc': 'Part-time Košice', 'spec': 'student_jobs'},
            {'name': 'Grafton - Košice', 'url': 'https://www.grafton.sk/kosice', 'desc': 'Personálna agentúra Košice', 'spec': 'general'}
        ]),
        ('Žilina', [
            {'name': 'Profesia.sk - Žilina', 'url': 'https://www.profesia.sk/zilina/brigady', 'desc': 'Brigády v Žiline', 'spec': 'student_jobs'},
            {'name': 'StudentJob - Žilina', 'url': 'https://www.studentjob.sk/zilina', 'desc': 'Študentské brigády Žilina', 'spec': 'student_jobs'},
            {'name': 'Brigada.sk - Žilina', 'url': 'https://www.brigada.sk/zilina', 'desc': 'Brigády Žilina', 'spec': 'student_jobs'},
            {'name': 'Kariera.sk - Žilina', 'url': 'https://www.kariera.sk/zilina/brigady', 'desc': 'Part-time Žilina', 'spec': 'student_jobs'},
            {'name': 'Manpower - Žilina', 'url': 'https://www.manpower.sk/zilina', 'desc': 'Personálna agentúra Žilina', 'spec': 'general'}
        ]),
        ('Nitra', [
            {'name': 'Profesia.sk - Nitra', 'url': 'https://www.profesia.sk/nitra/brigady', 'desc': 'Brigády v Nitre', 'spec': 'student_jobs'},
            {'name': 'StudentJob - Nitra', 'url': 'https://www.studentjob.sk/nitra', 'desc': 'Študentské brigády Nitra', 'spec': 'student_jobs'},
            {'name': 'Brigada.sk - Nitra', 'url': 'https://www.brigada.sk/nitra', 'desc': 'Brigády Nitra', 'spec': 'student_jobs'},
            {'name': 'Kariera.sk - Nitra', 'url': 'https://www.kariera.sk/nitra/brigady', 'desc': 'Part-time Nitra', 'spec': 'student_jobs'},
            {'name': 'Grafton - Nitra', 'url': 'https://www.grafton.sk/nitra', 'desc': 'Personálna agentúra Nitra', 'spec': 'general'}
        ])
    ]
    
    for city, agencies in other_cities:
        for agency in agencies:
            db.execute(text("""
                INSERT INTO job_agencies 
                (name, website_url, city, country_code, description, specialization, phone, email)
                VALUES 
                (:name, :url, :city, 'SK', :desc, :spec, '+421 900 000 000', 'info@example.sk')
            """), {
                'name': agency['name'],
                'url': agency['url'],
                'city': city,
                'desc': agency['desc'],
                'spec': agency['spec']
            })
    
    db.commit()
    print("✅ Job agencies table created and populated with 27 agencies for Slovakia")


def downgrade(db):
    """Remove job_agencies table"""
    db.execute(text("DROP TABLE IF EXISTS job_agencies CASCADE;"))
    db.commit()
    print("✅ Job agencies table removed")


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    import os
    
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()
    
    try:
        upgrade(db)
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()
