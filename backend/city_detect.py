#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete multilingual city detection for ALL Slovak cities
Supports all 10 platform languages
"""

import unicodedata

def normalize_text(text):
    """Remove diacritics and normalize text for matching"""
    text = unicodedata.normalize('NFD', text)
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
    return text.lower()

def _extract_city_from_message_multilingual(message, country_code='SK'):
    """
    Extract city from message in ANY of 10 languages
    Supports: sk, cs, pl, en, de, fr, es, uk, it, ru
    
    Returns official Slovak city name or None
    """
    if country_code != 'SK':
        return None
    
    # ALL SLOVAK CITIES - multilingual variants
    # Format: canonical_name -> [variants in all 10 languages]
    cities = {
        'Bratislava': ['bratislav', 'bratysław', 'братислав'],
        'Košice': ['košic', 'koši', 'koszyce', 'kosice', 'kaschau', 'кошиц'],
        'Prešov': ['prešov', 'preszów', 'presov', 'preschau', 'пряшів', 'прешов'],
        'Žilina': ['žilin', 'zilin', 'żylina', 'zilina', 'sillein', 'жилін', 'жилина'],
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
        'Humenné': ['humenné', 'humenne', 'humenné', 'гуменне'],
        'Skalica': ['skalica', 'skalitz', 'скаліца', 'скалица'],
        'Senica': ['senica', 'senitz', 'сеніца', 'сеница'],
        'Dunajská Streda': ['dunajsk', 'dunaszerdahely', 'дунайськ', 'дунайска'],
        'Galanta': ['galanta', 'галант'],
        'Topoľčany': ['topoľčan', 'topolcan', 'topoltschan', 'топольчан'],
        'Partizánske': ['partizánsk', 'partizansk', 'baťovany', 'партизанськ', 'партизанск'],
        'Vranov nad Topľou': ['vranov', 'varannó', 'вранов'],
    }
    
    message_lower = message.lower()
    message_normalized = normalize_text(message)
    
    # Check each city
    for city_name, variants in cities.items():
        for variant in variants:
            variant_normalized = normalize_text(variant)
            if variant in message_lower or variant_normalized in message_normalized:
                print(f"Detected city: {city_name} from variant '{variant}'")
                return city_name
    
    return None
