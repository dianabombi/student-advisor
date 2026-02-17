#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add language detection method to housing_chat_service.py
"""

import re

filepath = '/app/services/housing_chat_service.py'

# Read file
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find where to insert the method (after the chat method)
# Look for the end of chat method and insert before next method

method_code = '''
    def _detect_message_language(self, message: str):
        """
        Detect language from message content
        Returns language code (sk, cs, pl, en, de, fr, es, uk, it, ru, pt) or None
        """
        message_lower = message.lower()
        
        # Check for Cyrillic script (Ukrainian/Russian)
        has_cyrillic = any('\\u0400' <= char <= '\\u04FF' for char in message)
        
        if has_cyrillic:
            # Ukrainian-specific: і, ї, є, ґ
            ukrainian_chars = ['і', 'ї', 'є', 'ґ']
            ukrainian_words = ['шукаю', 'житло', 'квартиру', 'гуртожиток', 'пиши', 'українською']
            
            if any(char in message_lower for char in ukrainian_chars) or \\
               any(word in message_lower for word in ukrainian_words):
                return 'uk'
            
            # Russian-specific: ы, э, ъ
            russian_words = ['ищу', 'жилье', 'квартиру', 'общежитие', 'пиши', 'по-русски']
            if any(word in message_lower for word in russian_words):
                return 'ru'
            
            # Default Cyrillic to Ukrainian (more common on platform)
            return 'uk'
        
        # Check for specific language keywords
        lang_keywords = {
            'sk': ['hľadám', 'bývanie', 'byt', 'slovensky', 'slovenčina'],
            'cs': ['hledám', 'bydlení', 'česky', 'čeština'],
            'pl': ['szukam', 'mieszkania', 'po polsku', 'polski'],
            'de': ['suche', 'wohnung', 'auf deutsch', 'deutsch'],
            'fr': ['cherche', 'logement', 'en français', 'français'],
            'es': ['busco', 'vivienda', 'en español', 'español'],
            'it': ['cerco', 'alloggio', 'in italiano', 'italiano'],
            'pt': ['procuro', 'moradia', 'em português', 'português'],
        }
        
        for lang, keywords in lang_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return lang
        
        # No clear language detected
        return None

'''

# Find a good insertion point - after class definition line
# Insert after "class HousingChatService:" and before first method
insertion_point = content.find('    async def chat(')

if insertion_point > 0:
    # Insert before the chat method
    content = content[:insertion_point] + method_code + '\n' + content[insertion_point:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Added _detect_message_language method to housing_chat_service.py")
else:
    print("❌ Could not find insertion point")
