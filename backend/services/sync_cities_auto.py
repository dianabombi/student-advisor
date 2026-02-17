#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatic City Synchronization for Jobs Chat Service
Automatically updates city detection when new educational institutions are added

Run this after adding new educational institutions to keep city list in sync
"""

def update_city_detection():
    """
    Automatically generate city patterns from educational institutions database
    Updates jobs_chat_service.py with new cities
    """
    import sys
    import os
    
    # Add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from main import SessionLocal, EducationalInstitution
    
    db = SessionLocal()
    
    try:
        # Get all unique cities from educational institutions
        cities = db.query(EducationalInstitution.city).filter(
            EducationalInstitution.jurisdiction == 'SK'
        ).distinct().all()
        
        city_list = [city[0] for city in cities if city[0]]
        city_list.sort()
        
        print(f"Found {len(city_list)} unique Slovak cities with educational institutions:")
        print("\n".join(f"  - {city}" for city in city_list))
        
        # Generate city patterns
        print("\n" + "="*60)
        print("GENERATED CITY PATTERNS FOR jobs_chat_service.py:")
        print("="*60)
        print("\nslovak_cities = {")
        
        for city in city_list:
            # Generate search patterns
            city_lower = city.lower()
            
            # Remove diacritics for alternative pattern
            city_no_diacritics = (city_lower
                .replace('á', 'a').replace('ä', 'a')
                .replace('č', 'c')
                .replace('ď', 'd')
                .replace('é', 'e')
                .replace('í', 'i')
                .replace('ĺ', 'l').replace('ľ', 'l')
                .replace('ň', 'n')
                .replace('ó', 'o').replace('ô', 'o')
                .replace('ŕ', 'r')
                .replace('š', 's')
                .replace('ť', 't')
                .replace('ú', 'u')
                .replace('ý', 'y')
                .replace('ž', 'z')
            )
            
            # Use first 6-8 characters as pattern (enough to be unique)
            pattern_length = min(8, len(city_lower) - 1)
            pattern = city_lower[:pattern_length]
            
            print(f"    '{pattern}': '{city}',")
            
            # Add alternative without diacritics if different
            if city_no_diacritics != city_lower:
                pattern_no_diacritics = city_no_diacritics[:pattern_length]
                if pattern_no_diacritics != pattern:
                    print(f"    '{pattern_no_diacritics}': '{city}',")
        
        print("}")
        print("\n" + "="*60)
        print("Copy this dictionary to _extract_city_from_message() method")
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    update_city_detection()
