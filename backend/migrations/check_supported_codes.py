#!/usr/bin/env python3
# Check if all countries in database are in supported_codes

db_countries = ['AD', 'AT', 'BE', 'CH', 'CZ', 'DE', 'DK', 'ES', 'FI', 'FR', 'GB', 'GR', 'HR', 'HU', 'IE', 'IT', 'LI', 'LU', 'MC', 'NL', 'NO', 'PL', 'PT', 'SE', 'SI', 'SK', 'SM', 'VA']

supported_codes = [
    'SK', 'CZ', 'PL', 'DE', 'AT', 'CH', 'GB', 'IE', 'FR', 
    'BE', 'NL', 'IT', 'ES', 'PT', 'DK', 'SE', 'NO', 'FI', 
    'GR', 'HU', 'SI', 'HR', 'LU',
    'LI', 'VA', 'SM', 'MC', 'AD'
]

print("Countries in DB but NOT in supported_codes:")
missing = [c for c in db_countries if c not in supported_codes]
if missing:
    for c in missing:
        print(f"  ❌ {c}")
else:
    print("  ✅ All countries are supported!")

print("\nCountries in supported_codes but NOT in DB:")
extra = [c for c in supported_codes if c not in db_countries]
if extra:
    for c in extra:
        print(f"  ⚠️ {c}")
else:
    print("  ✅ No extra countries!")

print(f"\nTotal countries in DB: {len(db_countries)}")
print(f"Total supported codes: {len(supported_codes)}")
