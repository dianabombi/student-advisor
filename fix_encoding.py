import json
import os
import sys
from pathlib import Path

# Fix console encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Path to locales directory
locales_dir = Path(r'c:\Users\info\OneDrive\Dokumenty\CODEX\frontend\locales')

# Languages to fix
languages = ['cs', 'pl', 'en', 'de', 'uk', 'ru', 'fr', 'es', 'it', 'sk']

print("Fixing UTF-8 encoding in translation files...")

for lang in languages:
    file_path = locales_dir / lang / 'common.json'
    
    if not file_path.exists():
        print(f"[SKIP] {lang}/common.json not found")
        continue
    
    try:
        # Try reading with different encodings
        content = None
        original_encoding = None
        
        # Try UTF-8 with BOM first
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                content = f.read()
                original_encoding = 'utf-8-sig'
        except UnicodeDecodeError:
            # Try UTF-8 without BOM
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    original_encoding = 'utf-8'
            except UnicodeDecodeError:
                # Try Windows-1252 (common issue)
                try:
                    with open(file_path, 'r', encoding='windows-1252') as f:
                        content = f.read()
                        original_encoding = 'windows-1252'
                except UnicodeDecodeError:
                    # Try ISO-8859-1
                    with open(file_path, 'r', encoding='iso-8859-1') as f:
                        content = f.read()
                        original_encoding = 'iso-8859-1'
        
        # Parse JSON to validate
        data = json.loads(content)
        
        # Write back with proper UTF-8 encoding (no BOM)
        with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"[OK] Fixed {lang}/common.json (was {original_encoding})")
        
    except Exception as e:
        print(f"[ERROR] {lang}/common.json: {str(e)}")

print("\n[DONE] Encoding fix complete!")
