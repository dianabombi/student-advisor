#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Housing AI prompts - ensure all 11 languages talk about housing, not jobs
"""

import re

filepath = '/app/services/housing_chat_service.py'

# Read file
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replacements to fix job-related text to housing-related text
replacements = {
    # Ukrainian
    'шукаю підробіток': 'шукаю житло',
    'шукаєте роботу': 'шукаєте житло',
    'Шукаю роботу': 'Шукаю житло',
    'студентська робота': 'студентське житло',
    'про підробіток': 'про житло',
    'студенческую работу': 'студенческое жилье',
    
    # Russian
    'ищу работу': 'ищу жилье',
    'ищете работу': 'ищете жилье',
    'Ищу работу': 'Ищу жилье',
    'о подработке': 'о жилье',
    'студенческую работу': 'студенческое жилье',
    
    # Czech
    'hledám práci': 'hledám bydlení',
    'hledáte práci': 'hledáte bydlení',
    'Hledám práci': 'Hledám bydlení',
    'studentskou práci': 'studentské bydlení',
    'o brigádách': 'o bydlení',
    
    # Slovak
    'hľadám prácu': 'hľadám bývanie',
    'hľadáte prácu': 'hľadáte bývanie',
    'Hľadám prácu': 'Hľadám bývanie',
    'študentskú prácu': 'študentské bývanie',
    'o brigádach': 'o bývaní',
    
    # Polish
    'szukam pracy': 'szukam mieszkania',
    'szukasz pracy': 'szukasz mieszkania',
    'Szukam pracy': 'Szukam mieszkania',
    'pracę studencką': 'mieszkanie studenckie',
    'o pracy dorywczej': 'o mieszkaniu',
    
    # English
    'looking for work': 'looking for housing',
    'looking for a job': 'looking for housing',
    'student job': 'student housing',
    'about jobs': 'about housing',
    
    # German
    'suche Arbeit': 'suche Wohnung',
    'suchen Sie Arbeit': 'suchen Sie Wohnung',
    'Suche Arbeit': 'Suche Wohnung',
    'Studentenjob': 'Studentenwohnung',
    'über Jobs': 'über Wohnungen',
    
    # French
    'cherche du travail': 'cherche un logement',
    'cherchez du travail': 'cherchez un logement',
    'Cherche du travail': 'Cherche un logement',
    'travail étudiant': 'logement étudiant',
    'sur les emplois': 'sur le logement',
    
    # Spanish
    'busco trabajo': 'busco vivienda',
    'buscas trabajo': 'buscas vivienda',
    'Busco trabajo': 'Busco vivienda',
    'trabajo estudiantil': 'vivienda estudiantil',
    'sobre trabajos': 'sobre vivienda',
    
    # Italian
    'cerco lavoro': 'cerco alloggio',
    'cerchi lavoro': 'cerchi alloggio',
    'Cerco lavoro': 'Cerco alloggio',
    'lavoro studente': 'alloggio studente',
    'sui lavori': 'sugli alloggi',
    
    # Portuguese
    'procuro trabalho': 'procuro moradia',
    'procura trabalho': 'procura moradia',
    'Procuro trabalho': 'Procuro moradia',
    'trabalho estudante': 'moradia estudante',
    'sobre trabalhos': 'sobre moradia',
}

# Apply replacements
modified = False
for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        modified = True
        print(f"✅ Replaced: {old} → {new}")

if modified:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n✅ Updated {filepath}")
else:
    print("⚠️ No changes needed")
