#!/usr/bin/env python3
"""
Generate translations for all institution types across all supported languages
"""
import json
import os
from pathlib import Path
import psycopg2

# Database connection
DB_CONFIG = {
    'host': 'localhost',
    'port': 5434,  # External port from docker-compose
    'database': 'codex_db',
    'user': 'user',
    'password': 'password'
}

# Supported languages
LANGUAGES = {
    'uk': 'Ukrainian',
    'ru': 'Russian',
    'en': 'English',
    'de': 'German',
    'fr': 'French',
    'es': 'Spanish',
    'it': 'Italian',
    'cs': 'Czech',
    'sk': 'Slovak',
    'pl': 'Polish',
    'pt': 'Portuguese'
}

# Institution types - mapping JSON keys to database type values
INSTITUTION_TYPES = {
    'languageSchools': 'language_school',
    'vocationalSchools': 'vocational_school',
    'conservatories': 'conservatory',
    'foundationPrograms': 'foundation_program'
}

def get_institutions_from_db():
    """Query database for all institutions"""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    institutions = {}
    
    for json_key, type_value in INSTITUTION_TYPES.items():
        # Query universities table filtered by type
        cursor.execute(
            "SELECT id, name, description FROM universities WHERE type = %s ORDER BY id",
            (type_value,)
        )
        results = cursor.fetchall()
        institutions[json_key] = [
            {
                'id': row[0],
                'name': row[1],
                'description': row[2] or f"A prestigious {type_value.replace('_', ' ')} institution"
            }
            for row in results
        ]
        print(f"Found {len(results)} {json_key}")
    
    cursor.close()
    conn.close()
    
    return institutions

def generate_translations(institutions):
    """Generate translation structure for all languages"""
    translations = {}
    
    for lang_code in LANGUAGES.keys():
        translations[lang_code] = {}
        
        for inst_type, inst_list in institutions.items():
            translations[lang_code][inst_type] = {}
            
            for inst in inst_list:
                inst_id = str(inst['id'])
                translations[lang_code][inst_type][inst_id] = {
                    'name': inst['name'],  # Keep original name (usually proper noun)
                    'description': inst['description']  # Keep English description for now
                }
    
    return translations

def update_common_json_files(translations):
    """Update all common.json files with institution translations"""
    frontend_locales = Path('frontend/locales')
    
    for lang_code, trans_data in translations.items():
        lang_dir = frontend_locales / lang_code
        common_file = lang_dir / 'common.json'
        
        if not common_file.exists():
            print(f"⚠️  Skipping {lang_code} - file not found: {common_file}")
            continue
        
        # Load existing translations
        with open(common_file, 'r', encoding='utf-8') as f:
            existing = json.load(f)
        
        # Add institution translations
        for inst_type, inst_trans in trans_data.items():
            existing[inst_type] = inst_trans
        
        # Save updated translations
        with open(common_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=4)
        
        print(f"Updated {lang_code}/common.json with {sum(len(v) for v in trans_data.values())} institutions")

def main():
    print("Generating institution translations...")
    print("=" * 60)
    
    # Step 1: Get institutions from database
    print("\nQuerying database...")
    institutions = get_institutions_from_db()
    
    total_institutions = sum(len(v) for v in institutions.values())
    print(f"\nTotal institutions found: {total_institutions}")
    
    # Step 2: Generate translations
    print("\nGenerating translations for all languages...")
    translations = generate_translations(institutions)
    
    # Step 3: Update common.json files
    print("\nUpdating common.json files...")
    update_common_json_files(translations)
    
    print("\n" + "=" * 60)
    print(f"Successfully generated translations for:")
    print(f"   - {len(LANGUAGES)} languages")
    print(f"   - {len(INSTITUTION_TYPES)} institution types")
    print(f"   - {total_institutions} total institutions")
    print("\nDone! Reload your frontend to see the changes.")

if __name__ == '__main__':
    main()
