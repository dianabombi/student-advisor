import json
import codecs

# Read the Russian file with explicit UTF-8
with codecs.open(r'c:\Users\info\OneDrive\Dokumenty\CODEX\frontend\locales\ru\common.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Write it back with UTF-8 without BOM, ensuring proper encoding
with codecs.open(r'c:\Users\info\OneDrive\Dokumenty\CODEX\frontend\locales\ru\common.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Fixed Russian encoding")

# Test by reading a sample
sample = data['auth']['login']['welcome']
print(f"Sample text: {sample}")
print(f"Bytes: {sample.encode('utf-8')}")
