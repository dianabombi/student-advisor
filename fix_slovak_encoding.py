# -*- coding: utf-8 -*-
import json

# Path to Slovak translation file
sk_file = r'C:\Users\info\OneDrive\Dokumenty\CODEX\frontend\locales\sk\common.json'

print("Fixing Slovak translation encoding...")

# Read file with UTF-8 encoding
with open(sk_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Common Slovak character fixes
replacements = {
    'Prehľad': 'Prehľad',  # This should already be correct
    'Prihlásenie': 'Prihlásenie',
    'Vitajte späť!': 'Vitajte späť!',
    'Prihláste sa do svojho účtu': 'Prihláste sa do svojho účtu',
    'Prihlásiť sa': 'Prihlásiť sa',
    'Prihlasovanie': 'Prihlasovanie',
    'Nemáte účet?': 'Nemáte účet?',
    'Nesprávny': 'Nesprávny',
    'pripojenia': 'pripojenia',
    'Vytvoriť účet': 'Vytvoriť účet',
    'Začnite používať': 'Začnite používať',
    'Meno a priezvisko': 'Meno a priezvisko',
    'Potvrďte heslo': 'Potvrďte heslo',
    'Už máte účet?': 'Už máte účet?',
    'nezhodujú': 'nezhodujú',
    'Vaše meno': 'Vaše meno',
    'Rozumiem, že': 'Rozumiem, že',
    'nástroj': 'nástroj',
    'právnik': 'právnik',
    'NEPOSKYTUJE právne poradenstvo': 'NEPOSKYTUJE právne poradenstvo',
    'používanie': 'používanie',
    'NEVYTVÁRA': 'NEVYTVÁRA',
    'advokát': 'advokát',
    'potvrdiť všetky potvrdenia': 'potvrdiť všetky potvrdenia',
    'Všetky potvrdenia sú povinné': 'Všetky potvrdenia sú povinné',
    'môžete': 'môžete',
    'úspešná': 'úspešná',
    'Teraz sa': 'Teraz sa',
    'Prosím': 'Prosím',
    'nákup': 'nákup',
    'predplatného': 'predplatného',
}

# Apply replacements
for old, new in replacements.items():
    content = content.replace(old, new)

# Write back with UTF-8 encoding
with open(sk_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Slovak translation file fixed!")
print("Please restart the Next.js development server.")
