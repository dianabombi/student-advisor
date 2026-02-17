#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Housing Agency Generator
Generates migration scripts and adds housing agencies for any country
"""

import sys
sys.path.append('/app')

from main import SessionLocal, University, Jurisdiction, RealEstateAgency

# Country-specific portals configuration
COUNTRY_PORTALS = {
    'IE': {  # Ireland
        'portals': [
            {'name': 'Daft.ie', 'url': 'https://www.daft.ie', 'desc': 'Ireland\'s largest property website', 'spec': 'Rental and sales'},
            {'name': 'Rent.ie', 'url': 'https://www.rent.ie', 'desc': 'Irish rental property portal', 'spec': 'Rental'},
            {'name': 'MyHome.ie', 'url': 'https://www.myhome.ie', 'desc': 'Property search in Ireland', 'spec': 'Rental and sales'}
        ],
        'student': {'Dublin': [{'name': 'Uniplaces - Dublin', 'url': 'https://www.uniplaces.com', 'desc': 'Student accommodation', 'spec': 'Student housing'}]}
    },
    'PT': {  # Portugal
        'portals': [
            {'name': 'Idealista', 'url': 'https://www.idealista.pt', 'desc': 'Portal imobiliário líder em Portugal', 'spec': 'Arrendamento e venda'},
            {'name': 'Imovirtual', 'url': 'https://www.imovirtual.com', 'desc': 'Anúncios imobiliários', 'spec': 'Arrendamento'},
            {'name': 'Casa Sapo', 'url': 'https://casa.sapo.pt', 'desc': 'Portal imobiliário português', 'spec': 'Arrendamento e venda'}
        ],
        'student': {'Lisbon': [{'name': 'Uniplaces - Lisboa', 'url': 'https://www.uniplaces.com', 'desc': 'Alojamento estudantil', 'spec': 'Student housing'}]}
    },
    'GR': {  # Greece
        'portals': [
            {'name': 'Spitogatos', 'url': 'https://www.spitogatos.gr', 'desc': 'Largest Greek property portal', 'spec': 'Rental and sales'},
            {'name': 'XE.gr', 'url': 'https://www.xe.gr', 'desc': 'Greek real estate listings', 'spec': 'Rental'},
            {'name': 'Tospitimou', 'url': 'https://www.tospitimou.gr', 'desc': 'Property search in Greece', 'spec': 'Rental and sales'}
        ],
        'student': {}
    },
    'SE': {  # Sweden
        'portals': [
            {'name': 'Blocket Bostad', 'url': 'https://www.blocket.se/bostad', 'desc': 'Sveriges största bostadssajt', 'spec': 'Uthyrning'},
            {'name': 'Hemnet', 'url': 'https://www.hemnet.se', 'desc': 'Bostadsportal i Sverige', 'spec': 'Försäljning och uthyrning'},
            {'name': 'Qasa', 'url': 'https://www.qasa.se', 'desc': 'Hyresportal', 'spec': 'Uthyrning'}
        ],
        'student': {'Stockholm': [{'name': 'SSSB Stockholm', 'url': 'https://www.sssb.se', 'desc': 'Student housing Stockholm', 'spec': 'Student housing'}]}
    },
    'NO': {  # Norway
        'portals': [
            {'name': 'Finn.no', 'url': 'https://www.finn.no/realestate', 'desc': 'Norges største boligportal', 'spec': 'Utleie og salg'},
            {'name': 'Hybel.no', 'url': 'https://www.hybel.no', 'desc': 'Utleieportal', 'spec': 'Utleie'},
            {'name': 'Boligportal.no', 'url': 'https://www.boligportal.no', 'desc': 'Boligannonser', 'spec': 'Utleie'}
        ],
        'student': {'Oslo': [{'name': 'SiO Bolig', 'url': 'https://www.sio.no', 'desc': 'Student housing Oslo', 'spec': 'Student housing'}]}
    },
    'DK': {  # Denmark
        'portals': [
            {'name': 'Boligportal', 'url': 'https://www.boligportal.dk', 'desc': 'Danmarks største boligportal', 'spec': 'Udlejning'},
            {'name': 'Boligsiden', 'url': 'https://www.boligsiden.dk', 'desc': 'Boligannoncer', 'spec': 'Udlejning og salg'},
            {'name': 'FindBolig', 'url': 'https://www.findbolig.nu', 'desc': 'Boligsøgning', 'spec': 'Udlejning'}
        ],
        'student': {'Copenhagen': [{'name': 'KKIK Copenhagen', 'url': 'https://www.kkik.dk', 'desc': 'Student housing', 'spec': 'Student housing'}]}
    },
    'FI': {  # Finland
        'portals': [
            {'name': 'Oikotie Asunnot', 'url': 'https://asunnot.oikotie.fi', 'desc': 'Suomen suurin asuntopalvelu', 'spec': 'Vuokraus ja myynti'},
            {'name': 'Vuokraovi', 'url': 'https://www.vuokraovi.com', 'desc': 'Vuokra-asuntopalvelu', 'spec': 'Vuokraus'},
            {'name': 'Etuovi', 'url': 'https://www.etuovi.com', 'desc': 'Asuntoilmoitukset', 'spec': 'Vuokraus ja myynti'}
        ],
        'student': {'Helsinki': [{'name': 'HOAS Helsinki', 'url': 'https://www.hoas.fi', 'desc': 'Student housing', 'spec': 'Student housing'}]}
    },
    'HR': {  # Croatia
        'portals': [
            {'name': 'Njuškalo', 'url': 'https://www.njuskalo.hr', 'desc': 'Najveći portal za nekretnine', 'spec': 'Najam i prodaja'},
            {'name': 'Index Oglasi', 'url': 'https://www.index.hr/oglasi/nekretnine', 'desc': 'Nekretnine u Hrvatskoj', 'spec': 'Najam'},
            {'name': 'Crozilla', 'url': 'https://www.crozilla.com', 'desc': 'Portal za nekretnine', 'spec': 'Najam i prodaja'}
        ],
        'student': {}
    },
    'HU': {  # Hungary
        'portals': [
            {'name': 'Ingatlan.com', 'url': 'https://www.ingatlan.com', 'desc': 'Magyarország legnagyobb ingatlanportálja', 'spec': 'Kiadó és eladó'},
            {'name': 'Alberlet', 'url': 'https://www.alberlet.hu', 'desc': 'Albérlet kereső', 'spec': 'Kiadó'},
            {'name': 'Jofogas', 'url': 'https://www.jofogas.hu/ingatlan', 'desc': 'Ingatlan hirdetések', 'spec': 'Kiadó és eladó'}
        ],
        'student': {}
    },
    'SI': {  # Slovenia
        'portals': [
            {'name': 'Nepremicnine.net', 'url': 'https://www.nepremicnine.net', 'desc': 'Največji portal za nepremičnine', 'spec': 'Najem in prodaja'},
            {'name': 'Bolha', 'url': 'https://www.bolha.com', 'desc': 'Nepremičninski oglasi', 'spec': 'Najem'},
            {'name': 'Domofond', 'url': 'https://www.domofond.si', 'desc': 'Nepremičnine v Sloveniji', 'spec': 'Najem in prodaja'}
        ],
        'student': {}
    },
    'LU': {  # Luxembourg
        'portals': [
            {'name': 'Athome', 'url': 'https://www.athome.lu', 'desc': 'Premier portail immobilier au Luxembourg', 'spec': 'Location et vente'},
            {'name': 'Immotop', 'url': 'https://www.immotop.lu', 'desc': 'Annonces immobilières', 'spec': 'Location'},
            {'name': 'Wortimmo', 'url': 'https://www.wortimmo.lu', 'desc': 'Portail immobilier', 'spec': 'Location et vente'}
        ],
        'student': {}
    }
}

def generate_housing_for_country(country_code):
    """Generate housing agencies for a specific country"""
    db = SessionLocal()
    
    try:
        # Get jurisdiction
        juris = db.query(Jurisdiction).filter(Jurisdiction.code == country_code).first()
        if not juris:
            print(f"❌ Jurisdiction {country_code} not found")
            return
        
        # Get cities with universities
        cities = db.query(University.city).filter(University.jurisdiction_id == juris.id).distinct().all()
        city_list = sorted([c[0] for c in cities if c[0]])
        
        if not city_list:
            print(f"⚠️ No cities with universities found for {country_code}")
            return
        
        print(f"\n🏙️ {country_code}: {len(city_list)} cities - {', '.join(city_list)}")
        
        # Get portals configuration
        if country_code not in COUNTRY_PORTALS:
            print(f"⚠️ No portal configuration for {country_code}")
            return
        
        config = COUNTRY_PORTALS[country_code]
        portals = config['portals']
        student_acc = config.get('student', {})
        
        added_count = 0
        
        # Add portals for each city
        for city in city_list:
            for portal in portals:
                agency = RealEstateAgency(
                    name=f"{portal['name']} - {city}",
                    city=city,
                    country_code=country_code,
                    website_url=portal['url'],
                    description=portal['desc'],
                    specialization=portal['spec'],
                    is_verified=True,
                    is_active=True
                )
                db.add(agency)
                added_count += 1
        
        # Add student accommodation
        for city, accommodations in student_acc.items():
            if city in city_list:
                for acc in accommodations:
                    agency = RealEstateAgency(
                        name=acc['name'],
                        city=city,
                        country_code=country_code,
                        website_url=acc['url'],
                        description=acc['desc'],
                        specialization=acc['spec'],
                        is_verified=True,
                        is_active=True
                    )
                    db.add(agency)
                    added_count += 1
        
        db.commit()
        print(f"✅ Added {added_count} agencies for {country_code}")
        
    except Exception as e:
        print(f"❌ Error for {country_code}: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    # Countries to process
    countries = ['IE', 'PT', 'GR', 'SE', 'NO', 'DK', 'FI', 'HR', 'HU', 'SI', 'LU']
    
    print("🚀 Starting automated housing agency generation...")
    print(f"📋 Processing {len(countries)} countries\n")
    
    for country in countries:
        generate_housing_for_country(country)
    
    print("\n✅ All done!")
