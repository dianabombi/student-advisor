"""
City extraction utility for Jobs Chat Service
Add this method to JobsChatService class
"""

def _extract_city_from_message(self, message: str, country_code: str = 'SK'):
    """
    Extract city name from user message
    
    Args:
        message: User's message
        country_code: Country code (default: SK)
        
    Returns:
        City name if found, None otherwise
    """
    # Slovak cities - patterns to detect
    slovak_cities = {
        'bratislav': 'Bratislava',
        'košic': 'Košice', 
        'koši': 'Košice',
        'prešov': 'Prešov',
        'žilin': 'Žilina',
        'zilin': 'Žilina',
        'bansk': 'Banská Bystrica',
        'nitra': 'Nitra',
        'trnav': 'Trnava',
        'martin': 'Martin',
        'trenčín': 'Trenčín',
        'trencin': 'Trenčín',
        'poprad': 'Poprad'
    }
    
    message_lower = message.lower()
    
    # Check for city mentions
    for pattern, city in slovak_cities.items():
        if pattern in message_lower:
            print(f"Detected city: {city} from message")
            return city
    
    return None


# Also update the chat() method to use this:
# Add after line 44:
#
# # Extract city from user message if not provided
# if db and not city:
#     city = self._extract_city_from_message(message, jurisdiction)
