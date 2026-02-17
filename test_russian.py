import json
import sys
from pathlib import Path

# Fix console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

locales_dir = Path(r'c:\Users\info\OneDrive\Dokumenty\CODEX\frontend\locales')

print("Fixing Russian encoding issue...")

# Read Russian file
ru_file = locales_dir / 'ru' / 'common.json'
with open(ru_file, 'r', encoding='utf-8') as f:
    ru_data = json.load(f)

# Write back with proper UTF-8 (no BOM)
with open(ru_file, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(ru_data, f, ensure_ascii=False, indent=4)

print("[OK] Fixed Russian encoding")

# Now check if the issue is in the browser or file
# Test by printing a sample
sample_text = ru_data['auth']['login']['welcome']
print(f"Sample Russian text: {sample_text}")
print(f"Should be: Добро пожаловать!")

print("\nDone!")
