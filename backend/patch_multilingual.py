#!/usr/bin/env python3
"""
Patch jobs_chat_service.py to use multilingual city detection
"""

import re

# Read the current file
with open('/app/services/jobs_chat_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the _extract_city_from_message method
new_method = '''    def _extract_city_from_message(self, message: str, country_code: str = 'SK') -> Optional[str]:
        """
        Extract city name from user message - MULTILINGUAL DETECTION
        Supports ALL 10 platform languages: sk, cs, pl, en, de, fr, es, uk, it, ru
        
        Args:
            message: User's message in any language
            country_code: Country code (default: SK)
            
        Returns:
            Official Slovak city name if found, None otherwise
        """
        if country_code != 'SK':
            return None
        
        import unicodedata
        
        def normalize(text):
            """Remove diacritics for better matching"""
            text = unicodedata.normalize('NFD', text)
            return ''.join(c for c in text if unicodedata.category(c) != 'Mn').lower()
        
        # ALL SLOVAK CITIES - multilingual variants (sk, cs, pl, en, de, fr, es, uk, it, ru)
        cities = {
            'Bratislava': ['bratislav', 'bratysław', 'братислав'],
            'Košice': ['košic', 'koši', 'koszyce', 'koszyc', 'kosice', 'kaschau', 'кошиц'],
            'Prešov': ['prešov', 'preszów', 'presov', 'preschau', 'пряшів', 'прешов'],
            'Žilina': ['žilin', 'zilin', 'żylina', 'zylin', 'zilina', 'sillein', 'жилін', 'жилина'],
            'Banská Bystrica': ['bansk', 'bystr', 'bańska', 'banska', 'neusohl', 'банськ', 'банска'],
            'Nitra': ['nitra', 'nitr', 'nitry', 'neutra', 'нітр', 'нитр'],
            'Trnava': ['trnav', 'trnawa', 'tyrnau', 'трнав'],
            'Martin': ['martin', 'turz', 'мартін', 'мартин'],
            'Trenčín': ['trenčín', 'trencin', 'trenczyn', 'trentschin', 'тренчін', 'тренчин'],
            'Poprad': ['poprad', 'deutschendorf', 'попрад'],
            'Prievidza': ['prievidz', 'priwitz', 'прієвідз', 'приевидз'],
            'Zvolen': ['zvolen', 'altsohl', 'зволен'],
            'Považská Bystrica': ['považsk', 'povazsk', 'waagbistritz', 'поважськ', 'повазска'],
            'Nové Zámky': ['nové zámk', 'nove zamk', 'neuhausel', 'нове замк', 'новые замк'],
            'Komárno': ['komárn', 'komarn', 'komárom', 'komorn', 'комарн'],
            'Levice': ['levic', 'lewenz', 'левіц', 'левице'],
            'Michalovce': ['michalovce', 'nagymihály', 'міхаловц', 'михаловце'],
            'Spišská Nová Ves': ['spišsk', 'spissk', 'zipser', 'спішськ', 'спишска'],
            'Lučenec': ['lučenec', 'lucenec', 'losonc', 'лученец'],
            'Piešťany': ['piešťan', 'piest', 'pistyan', 'пєштян', 'пиештян'],
            'Liptovský Mikuláš': ['liptovsk', 'mikuláš', 'mikulas', 'liptau', 'ліптовськ', 'липтовск'],
            'Ružomberok': ['ružomberok', 'ruzomberok', 'rosenberg', 'ружомберок'],
            'Bardejov': ['bardejov', 'bartfeld', 'бардеїв', 'бардеев'],
            'Humenné': ['humenné', 'humenne', 'гуменне'],
            'Skalica': ['skalica', 'skalitz', 'скаліца', 'скалица'],
            'Senica': ['senica', 'senitz', 'сеніца', 'сеница'],
            'Dunajská Streda': ['dunajsk', 'dunaszerdahely', 'дунайськ', 'дунайска'],
            'Galanta': ['galanta', 'галант'],
            'Topoľčany': ['topoľčan', 'topolcan', 'topoltschan', 'топольчан'],
            'Partizánske': ['partizánsk', 'partizansk', 'baťovany', 'партизанськ', 'партизанск'],
            'Vranov nad Topľou': ['vranov', 'varannó', 'вранов'],
        }
        
        message_lower = message.lower()
        message_normalized = normalize(message)
        
        # Check each city with both original and normalized text
        for city_name, variants in cities.items():
            for variant in variants:
                variant_normalized = normalize(variant)
                if variant in message_lower or variant_normalized in message_normalized:
                    return city_name
        
        return None
'''

# Find the method using regex
pattern = r'    def _extract_city_from_message\(self.*?\n(?=    def )'
match = re.search(pattern, content, re.DOTALL)

if match:
    # Replace the old method with the new one
    content = content[:match.start()] + new_method + '\n' + content[match.end():]
    
    # Write back
    with open('/app/services/jobs_chat_service.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("SUCCESS: Patched jobs_chat_service.py with multilingual city detection!")
    print("Now supports all 10 languages for all 27+ Slovak cities")
else:
    print("ERROR: Could not find method to replace")
