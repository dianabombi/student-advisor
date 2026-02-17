# -*- coding: utf-8 -*-
import json

# Path to Czech translation file
cs_file = r'C:\Users\info\OneDrive\Dokumenty\CODEX\frontend\locales\cs\common.json'

print("Fixing Czech translation encoding...")

# Read file with UTF-8 encoding
with open(cs_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Common Czech character fixes
replacements = {
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
}

# Apply replacements
for old, new in replacements.items():
    content = content.replace(old, new)

# Write back with UTF-8 encoding
with open(cs_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Czech translation file fixed!")
print("Please restart the Next.js development server.")
