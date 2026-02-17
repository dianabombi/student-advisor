#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update jobs_chat_service.py with cities and portal instructions for remaining countries

This script generates the code snippets needed to add to jobs_chat_service.py:
1. City detection with multilingual variants
2. Country mapping
3. Portal instructions

Run this script and copy the output to the appropriate sections in jobs_chat_service.py
"""

# City detection snippets for each country
CITY_DETECTION = """
            # DANISH CITIES (DK)
            'Copenhagen': [
                'copenhagen', 'københavn',
                'копенгаген', 'копенгагені', 'копенгагеном',  # uk
                'копенгаген', 'копенгагене', 'копенгагеном',  # ru
                'kopenhaga', 'kopenhadze'  # pl
            ],
            'Aarhus': ['aarhus', 'орхус', 'орхусі'],  # uk/ru
            'Odense': ['odense', 'оденсе', 'оденсі'],
            'Aalborg': ['aalborg', 'ольборг', 'ольборзі'],
            'Roskilde': ['roskilde', 'роскілле', 'роскіллі'],
            'Kolding': ['kolding', 'колдінг', 'колдінгу'],
            'Lyngby': ['lyngby', 'люнгбю', 'люнгбі'],

            # NORWEGIAN CITIES (NO)
            'Oslo': [
                'oslo',
                'осло', 'ослі', 'ослом',  # uk
                'осло', 'осле', 'ослом'  # ru
            ],
            'Bergen': ['bergen', 'берген', 'бергені', 'бергеном'],
            'Trondheim': ['trondheim', 'тронгейм', 'тронгеймі'],
            'Stavanger': ['stavanger', 'ставангер', 'ставангері'],
            'Tromsø': ['tromsø', 'tromso', 'тромсе', 'тромсі'],
            'Ås': ['ås', 'as', 'ос', 'осі'],

            # FINNISH CITIES (FI)
            'Helsinki': [
                'helsinki',
                'гельсінкі', 'гельсінкі',  # uk
                'хельсинки', 'хельсинки'  # ru
            ],
            'Espoo': ['espoo', 'еспоо', 'еспоо'],
            'Tampere': ['tampere', 'тампере', 'тампері'],
            'Turku': ['turku', 'турку', 'турку'],
            'Oulu': ['oulu', 'оулу', 'оулу'],
            'Jyväskylä': ['jyväskylä', 'jyvaskyla', 'ювяскюля', 'ювяскюлі'],
            'Joensuu': ['joensuu', 'йоенсуу', 'йоенсуу'],

            # GREEK CITIES (GR)
            'Athens': [
                'athens', 'athína', 'αθήνα',
                'афіни', 'афінах', 'афінами',  # uk
                'афины', 'афинах', 'афинами'  # ru
            ],
            'Thessaloniki': ['thessaloniki', 'θεσσαλονίκη', 'салоніки', 'салонікі'],
            'Heraklion': ['heraklion', 'ηράκλειο', 'іракліон', 'іракліоні'],
            'Volos': ['volos', 'βόλος', 'волос', 'волосі'],
            'Ioannina': ['ioannina', 'ιωάννινα', 'яніна', 'яніні'],

            # HUNGARIAN CITIES (HU)
            'Budapest': [
                'budapest',
                'будапешт', 'будапешті', 'будапештом',  # uk
                'будапешт', 'будапеште', 'будапештом'  # ru
            ],
            'Debrecen': ['debrecen', 'дебрецен', 'дебрецені'],
            'Szeged': ['szeged', 'сегед', 'сегеді'],
            'Pécs': ['pécs', 'pecs', 'печ', 'печі'],

            # SLOVENIAN CITIES (SI)
            'Ljubljana': [
                'ljubljana',
                'любляна', 'люблян', 'любляною',  # uk
                'любляна', 'любляне', 'любляной'  # ru
            ],
            'Maribor': ['maribor', 'марібор', 'маріборі'],
            'Koper': ['koper', 'копер', 'коперу'],
            'Nova Gorica': ['nova gorica', 'нова горіца', 'нова гориця'],

            # CROATIAN CITIES (HR)
            'Zagreb': [
                'zagreb',
                'загреб', 'загребі', 'загребом',  # uk
                'загреб', 'загребе', 'загребом'  # ru
            ],
            'Split': ['split', 'спліт', 'спліті'],
            'Rijeka': ['rijeka', 'рієка', 'рієці'],
            'Osijek': ['osijek', 'осієк', 'осієку'],
"""

# Country mapping
COUNTRY_MAPPING = """
            # DK
            'Copenhagen': 'DK', 'Aarhus': 'DK', 'Odense': 'DK', 'Aalborg': 'DK',
            'Roskilde': 'DK', 'Kolding': 'DK', 'Lyngby': 'DK',
            
            # NO
            'Oslo': 'NO', 'Bergen': 'NO', 'Trondheim': 'NO', 'Stavanger': 'NO',
            'Tromsø': 'NO', 'Ås': 'NO',
            
            # FI
            'Helsinki': 'FI', 'Espoo': 'FI', 'Tampere': 'FI', 'Turku': 'FI',
            'Oulu': 'FI', 'Jyväskylä': 'FI', 'Joensuu': 'FI',
            
            # GR
            'Athens': 'GR', 'Thessaloniki': 'GR', 'Heraklion': 'GR',
            'Volos': 'GR', 'Ioannina': 'GR',
            
            # HU
            'Budapest': 'HU', 'Debrecen': 'HU', 'Szeged': 'HU', 'Pécs': 'HU',
            
            # SI
            'Ljubljana': 'SI', 'Maribor': 'SI', 'Koper': 'SI', 'Nova Gorica': 'SI',
            
            # HR
            'Zagreb': 'HR', 'Split': 'HR', 'Rijeka': 'HR', 'Osijek': 'HR'
"""

# Portal instructions
PORTAL_INSTRUCTIONS = """
                # Danish portals (DK)
                elif 'jobindex' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'jobindex {city}'\\\\n"
                elif 'randstad.dk' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'randstad.dk job {city}'\\\\n"
                elif 'manpower.dk' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'manpower.dk job {city}'\\\\n"
                
                # Norwegian portals (NO)
                elif 'finn.no' in portal_name:
                    context += f"  Instructions: Open website, search 'Jobb' in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'finn.no jobb {city}'\\\\n"
                elif 'randstad.no' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'randstad.no jobb {city}'\\\\n"
                elif 'manpower.no' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'manpower.no jobb {city}'\\\\n"
                
                # Finnish portals (FI)
                elif 'mol.fi' in portal_name:
                    context += f"  Instructions: Open website, search 'Työpaikat' in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'mol.fi työ {city}'\\\\n"
                elif 'randstad.fi' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'randstad.fi työ {city}'\\\\n"
                elif 'manpower.fi' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'manpower.fi työ {city}'\\\\n"
                
                # Greek portals (GR)
                elif 'kariera.gr' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'kariera.gr εργασία {city}'\\\\n"
                elif 'randstad.gr' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'randstad.gr εργασία {city}'\\\\n"
                elif 'manpower.gr' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'manpower.gr εργασία {city}'\\\\n"
                
                # Hungarian portals (HU)
                elif 'profession.hu' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'profession.hu állás {city}'\\\\n"
                elif 'randstad.hu' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'randstad.hu állás {city}'\\\\n"
                elif 'manpower.hu' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'manpower.hu állás {city}'\\\\n"
                
                # Slovenian portals (SI)
                elif 'mojedelo' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'mojedelo zaposlitev {city}'\\\\n"
                elif 'randstad.si' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'randstad.si zaposlitev {city}'\\\\n"
                elif 'manpower.si' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'manpower.si zaposlitev {city}'\\\\n"
                
                # Croatian portals (HR)
                elif 'mojposao' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'mojposao posao {city}'\\\\n"
                elif 'randstad.hr' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'randstad.hr posao {city}'\\\\n"
                elif 'manpower.hr' in portal_name:
                    context += f"  Instructions: Open website, search jobs in '{city}'.\\\\n"
                    context += f"  Alternative: If blocked, search Google for 'manpower.hr posao {city}'\\\\n"
"""

def main():
    print("=" * 80)
    print("CITY DETECTION - Add before UK CITIES section:")
    print("=" * 80)
    print(CITY_DETECTION)
    
    print("\n" + "=" * 80)
    print("COUNTRY MAPPING - Add after SE mapping:")
    print("=" * 80)
    print(COUNTRY_MAPPING)
    
    print("\n" + "=" * 80)
    print("PORTAL INSTRUCTIONS - Add before 'else:' clause:")
    print("=" * 80)
    print(PORTAL_INSTRUCTIONS)
    
    print("\n" + "=" * 80)
    print("✅ Copy these snippets to jobs_chat_service.py")
    print("=" * 80)

if __name__ == "__main__":
    main()
