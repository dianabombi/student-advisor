import json
import sys
from pathlib import Path

# Fix console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

locales_dir = Path(r'c:\Users\info\OneDrive\Dokumenty\CODEX\frontend\locales')

# Languages with separate marketplace files
langs_to_integrate = {
    'ru': 'marketplace_ru.json',
    'cs': 'marketplace_cs.json',
    'pl': 'marketplace_pl.json'
}

print("Integrating marketplace translations...")

for lang, marketplace_file in langs_to_integrate.items():
    marketplace_path = locales_dir / marketplace_file
    common_path = locales_dir / lang / 'common.json'
    
    if not marketplace_path.exists():
        print(f"[SKIP] {marketplace_file} not found")
        continue
    
    # Read marketplace translations
    with open(marketplace_path, 'r', encoding='utf-8') as f:
        marketplace_data = json.load(f)
    
    # Read or create common.json
    if common_path.exists():
        with open(common_path, 'r', encoding='utf-8') as f:
            common_data = json.load(f)
    else:
        common_data = {}
    
    # Merge marketplace section
    if 'marketplace' in marketplace_data:
        common_data['marketplace'] = marketplace_data['marketplace']
        print(f"[OK] Integrated marketplace translations for {lang}")
    
    # Write back
    with open(common_path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(common_data, f, ensure_ascii=False, indent=4)

print("\n[DONE] Integration complete!")
