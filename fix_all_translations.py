# -*- coding: utf-8 -*-
"""
Universal Translation Encoding Fixer
This script fixes common UTF-8 encoding issues in translation files
"""

import os
import json

# Paths
locales_path = r'C:\Users\info\OneDrive\Dokumenty\CODEX\frontend\locales'

# Common character fixes for Czech
czech_fixes = {
    'PĹ™ehled': 'Přehled',
    'PĹ™ihlĂˇĹˇenĂ­': 'Přihlášení',
    'VĂ­tejte zpÄ›t!': 'Vítejte zpět!',
    'PĹ™ihlaste se do svĂ©ho ĂşÄŤtu': 'Přihlaste se do svého účtu',
    'PĹ™ihlĂˇsit se': 'Přihlásit se',
    'PĹ™ihlaĹˇovĂˇnĂ­': 'Přihlašování',
    'NemĂˇte ĂşÄŤet?': 'Nemáte účet?',
    'NesprĂˇvnĂ˝': 'Nesprávný',
    'pĹ™ipojenĂ­': 'připojení',
    'VytvoĹ™it ĂşÄŤet': 'Vytvořit účet',
    'ZaÄŤnÄ›te pouĹľĂ­vat': 'Začněte používat',
    'JmĂ©no a pĹ™Ă­jmenĂ­': 'Jméno a příjmení',
    'PotvrÄŹte heslo': 'Potvrďte heslo',
    'JiĹľ mĂˇte ĂşÄŤet?': 'Již máte účet?',
    'neshodujĂ­': 'neshodují',
    'VaĹˇe jmĂ©no': 'Vaše jméno',
    'RozumĂ­m, Ĺľe': 'Rozumím, že',
    'nĂˇstroj': 'nástroj',
    'prĂˇvnĂ­k': 'právník',
    'NEPOSKYTUJE prĂˇvnĂ­ poradenstvĂ­': 'NEPOSKYTUJE právní poradenství',
    'pouĹľĂ­vĂˇnĂ­': 'používání',
    'NEVYTVĂĹĂŤ': 'NEVYTVÁŘÍ',
    'advokĂˇt': 'advokát',
    'pĹ™ijmout vĹˇechna potvrzenĂ­': 'přijmout všechna potvrzení',
    'VĹˇechna potvrzenĂ­ jsou povinnĂˇ': 'Všechna potvrzení jsou povinná',
    'mĹŻĹľete': 'můžete',
    'ĂşspÄ›ĹˇnĂˇ': 'úspěšná',
    'NynĂ­ se': 'Nyní se',
    'ProsĂ­m': 'Prosím',
    'nĂˇkupu': 'nákupu',
    'pĹ™edplatnĂ©ho': 'předplatného',
    'â€˘â€˘â€˘â€˘â€˘â€˘â€˘â€˘': '••••••••',
    'âš ď¸Ź PovinnĂ©': '⚠️ Povinné',
    'potvrzenĂ­': 'potvrzení',
    'NastavenĂ­': 'Nastavení',
    'OdhlĂˇsit se': 'Odhlásit se',
    'ĂşÄŤet': 'účet',
}

def fix_file_encoding(file_path, fixes):
    """Fix encoding issues in a translation file"""
    try:
        # Read file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply fixes
        original_content = content
        for old, new in fixes.items():
            content = content.replace(old, new)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

# Fix Czech
cs_file = os.path.join(locales_path, 'cs', 'common.json')
print("Fixing Czech translations...")
if fix_file_encoding(cs_file, czech_fixes):
    print("  - Czech file updated")
else:
    print("  - Czech file already correct")

# Fix Slovak (uses similar characters)
sk_file = os.path.join(locales_path, 'sk', 'common.json')
print("Fixing Slovak translations...")
if fix_file_encoding(sk_file, czech_fixes):
    print("  - Slovak file updated")
else:
    print("  - Slovak file already correct")

print("\nAll translation files processed!")
print("Please restart the Next.js development server to see changes.")
