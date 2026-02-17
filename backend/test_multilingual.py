#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced city detection with transliteration support
Handles all 10 platform languages automatically
"""

def normalize_text(text):
    """Remove diacritics and normalize text for matching"""
    import unicodedata
    # Normalize unicode
    text = unicodedata.normalize('NFD', text)
    # Remove diacritics
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
    return text.lower()

def extract_city_multilingual(message, country_code='SK'):
    """
    Extract city from message in ANY of 10 languages
    Supports: sk, cs, pl, en, de, fr, es, uk, it, ru
    """
    if country_code != 'SK':
        return None
    
    # City names in multiple languages
    # Format: canonical_name -> [variants in all languages]
    cities_multilingual = {
        'Bratislava': [
            'bratislav', 'bratislava', 'bratislavě',  # SK, CS
            'bratysław', 'bratysławy',  # PL
            'bratislava',  # EN, DE, FR, ES, IT
            'братислав', 'братиславі', 'братиславе',  # UK, RU
        ],
        'Košice': [
            'košic', 'košice', 'košicích', 'koši',  # SK, CS
            'koszyce', 'koszyc',  # PL
            'kosice', 'kaschau',  # EN, DE
            'кошиц', 'кошице', 'кошицях',  # UK, RU
        ],
        'Prešov': [
            'prešov', 'prešově', 'prjašev',  # SK, CS
            'preszów', 'preszow',  # PL
            'presov', 'preschau', 'eperies',  # EN, DE
            'пряшів', 'прешов', 'пряшеві',  # UK, RU
        ],
        'Žilina': [
            'žilin', 'žilina', 'žilině', 'zilin', 'zilina',  # SK, CS
            'żylina', 'zylin',  # PL
            'zilina', 'sillein',  # EN, DE
            'жилін', 'жилина', 'жиліні',  # UK, RU
        ],
        'Banská Bystrica': [
            'bansk', 'banská', 'bystric', 'banskej bystrici',  # SK, CS
            'bańska bystrzyca',  # PL
            'banska bystrica', 'neusohl',  # EN, DE
            'банськ', 'банска', 'бистриц',  # UK, RU
        ],
        'Nitra': [
            'nitra', 'nitře', 'nitr',  # SK, CS
            'nitry', 'nitrze',  # PL
            'nitra', 'neutra',  # EN, DE
            'нітр', 'нитр', 'нітрі',  # UK, RU
        ],
        'Trnava': [
            'trnav', 'trnava', 'trnavě',  # SK, CS
            'trnawa', 'trnaw',  # PL
            'trnava', 'tyrnau',  # EN, DE
            'трнав', 'трнава', 'трнаві',  # UK, RU
        ],
        'Trenčín': [
            'trenčín', 'trencin', 'trenčíně',  # SK, CS
            'trenczyn', 'trenczin',  # PL
            'trencin', 'trentschin',  # EN, DE
            'тренчін', 'тренчин', 'тренчіні',  # UK, RU
        ],
        'Poprad': [
            'poprad', 'popradě', 'poprad',  # SK, CS
            'poprad', 'popradu',  # PL
            'poprad', 'deutschendorf',  # EN, DE
            'попрад', 'попраді',  # UK, RU
        ],
        'Martin': [
            'martin', 'martině', 'martin',  # SK, CS
            'martin', 'martinie',  # PL
            'martin', 'turz',  # EN, DE
            'мартін', 'мартин', 'мартіні',  # UK, RU
        ],
    }
    
    message_lower = message.lower()
    message_normalized = normalize_text(message)
    
    # Check each city
    for city_name, variants in cities_multilingual.items():
        for variant in variants:
            variant_normalized = normalize_text(variant)
            # Check both original and normalized
            if variant in message_lower or variant_normalized in message_normalized:
                return city_name
    
    return None


# Test
if __name__ == "__main__":
    test_cases = [
        # Slovak
        ("Hľadám prácu v Bratislave", "Bratislava"),
        ("brigáda v Košiciach", "Košice"),
        
        # Ukrainian
        ("Шукаю роботу в Кошицях", "Košice"),
        ("в Братиславі", "Bratislava"),
        ("робота в Пряшеві", "Prešov"),
        
        # Russian
        ("работа в Кошице", "Košice"),
        ("в Братиславе", "Bratislava"),
        
        # English
        ("work in Bratislava", "Bratislava"),
        ("job in Kosice", "Košice"),
        
        # Polish
        ("praca w Koszycach", "Košice"),
        ("w Bratysławie", "Bratislava"),
        
        # Czech
        ("práce v Košicích", "Košice"),
        ("v Bratislavě", "Bratislava"),
    ]
    
    print("Testing multilingual city detection:")
    print("="*60)
    
    for message, expected in test_cases:
        detected = extract_city_multilingual(message)
        status = "✅" if detected == expected else "❌"
        print(f"{status} '{message}' -> {detected} (expected: {expected})")
