"""
Translation loader for marketplace API
Loads translations based on user's preferred language
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional

# Supported languages
SUPPORTED_LANGUAGES = ["sk", "cs", "pl", "en", "de", "fr", "es", "it", "uk", "ru"]
DEFAULT_LANGUAGE = "sk"

# Cache for loaded translations
_translation_cache: Dict[str, Dict] = {}


def load_translations(language: str = DEFAULT_LANGUAGE) -> Dict:
    """
    Load marketplace translations for specified language
    
    Args:
        language: Language code (sk, cs, pl, en, etc.)
    
    Returns:
        Dictionary with translations
    """
    # Validate language
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE
    
    # Check cache
    if language in _translation_cache:
        return _translation_cache[language]
    
    # Load from file
    base_dir = Path(__file__).parent
    translation_file = base_dir / language / "marketplace.json"
    
    try:
        with open(translation_file, 'r', encoding='utf-8') as f:
            translations = json.load(f)
            _translation_cache[language] = translations
            return translations
    except FileNotFoundError:
        # Fallback to default language
        if language != DEFAULT_LANGUAGE:
            return load_translations(DEFAULT_LANGUAGE)
        return {}
    except json.JSONDecodeError:
        return {}


def get_translation(key: str, language: str = DEFAULT_LANGUAGE, **kwargs) -> str:
    """
    Get translated string by key
    
    Args:
        key: Translation key (e.g., "marketplace.lawyer.registration.success")
        language: Language code
        **kwargs: Format arguments for string interpolation
    
    Returns:
        Translated string
    
    Example:
        >>> get_translation("marketplace.lawyer.profile.not_found", "sk")
        "Advokát nenájdený"
    """
    translations = load_translations(language)
    
    # Navigate through nested dict
    keys = key.split('.')
    value = translations
    
    try:
        for k in keys:
            value = value[k]
        
        # Format string if kwargs provided
        if kwargs:
            return value.format(**kwargs)
        
        return value
    except (KeyError, TypeError):
        # Return key if translation not found
        return key


def t(key: str, language: str = DEFAULT_LANGUAGE, **kwargs) -> str:
    """
    Shorthand for get_translation
    
    Example:
        >>> t("marketplace.lawyer.registration.success", "en")
        "Registration successful. Your application will be verified within 48 hours."
    """
    return get_translation(key, language, **kwargs)


# Convenience functions for common translations
def success_message(key: str, language: str = DEFAULT_LANGUAGE) -> str:
    """Get success message"""
    return t(f"marketplace.lawyer.{key}.success", language)


def error_message(key: str, language: str = DEFAULT_LANGUAGE) -> str:
    """Get error message"""
    return t(f"marketplace.lawyer.{key}.error", language)
