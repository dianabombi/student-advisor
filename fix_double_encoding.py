import json
import sys

# Fix console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# The file is double-encoded. We need to:
# 1. Read it as UTF-8 (which gives us mojibake strings)
# 2. Encode those strings as latin-1 (to get original bytes)
# 3. Decode as UTF-8 (to get correct Russian text)
# 4. Save with proper UTF-8

print("Fixing double-encoded Russian file...")

with open(r'c:\Users\info\OneDrive\Dokumenty\CODEX\frontend\locales\ru\common.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def fix_double_encoding(obj):
    """Recursively fix double-encoded strings in a dictionary"""
    if isinstance(obj, dict):
        return {k: fix_double_encoding(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [fix_double_encoding(item) for item in obj]
    elif isinstance(obj, str):
        try:
            # Try to fix double encoding
            # The string was UTF-8 bytes interpreted as Windows-1252, then encoded as UTF-8 again
            return obj.encode('latin-1').decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            # If it fails, return as is
            return obj
    else:
        return obj

fixed_data = fix_double_encoding(data)

# Write back with proper UTF-8
with open(r'c:\Users\info\OneDrive\Dokumenty\CODEX\frontend\locales\ru\common.json', 'w', encoding='utf-8', newline='\n') as f:
    json.dump(fixed_data, f, ensure_ascii=False, indent=4)

print("[OK] Fixed!")

# Test
sample = fixed_data['auth']['login']['welcome']
print(f"Sample: {sample}")
print(f"Should be: Добро пожаловать!")
