"""
Jurisdiction Configuration
Centralized configuration for all supported jurisdictions in CODEX marketplace

This file makes it easy to add new jurisdictions without modifying core code.
Simply add a new entry to SUPPORTED_JURISDICTIONS dict.
"""

from typing import Dict, List
from pydantic import BaseModel


class JurisdictionConfig(BaseModel):
    """Configuration for a single jurisdiction"""
    code: str  # ISO 3166-1 alpha-2 code
    name: str  # Full name in English
    name_local: str  # Full name in local language
    flag_emoji: str  # Flag emoji
    default_language: str  # Default language code
    supported_languages: List[str]  # All supported languages
    is_active: bool = True  # Whether jurisdiction is currently active
    currency: str = "EUR"  # Default currency
    
    # Legal system info (for future use)
    legal_system: str = "civil_law"  # civil_law, common_law, mixed
    bar_association_url: str = ""  # Official bar association website


# ============================================
# SUPPORTED JURISDICTIONS
# ============================================
# To add a new jurisdiction, simply add a new entry here
# No other code changes needed!

SUPPORTED_JURISDICTIONS: Dict[str, JurisdictionConfig] = {
    # Central Europe
    "SK": JurisdictionConfig(
        code="SK",
        name="Slovakia",
        name_local="Slovenská Republika",
        flag_emoji="🇸🇰",
        default_language="sk",
        supported_languages=["sk", "en", "cs", "de"],
        currency="EUR",
        legal_system="civil_law",
        bar_association_url="https://www.sak.sk"
    ),
    
    "CZ": JurisdictionConfig(
        code="CZ",
        name="Czech Republic",
        name_local="Česká Republika",
        flag_emoji="🇨🇿",
        default_language="cs",
        supported_languages=["cs", "sk", "en", "de"],
        currency="CZK",
        legal_system="civil_law",
        bar_association_url="https://www.cak.cz"
    ),
    
    "PL": JurisdictionConfig(
        code="PL",
        name="Poland",
        name_local="Polska",
        flag_emoji="🇵🇱",
        default_language="pl",
        supported_languages=["pl", "en", "de"],
        currency="PLN",
        legal_system="civil_law",
        bar_association_url="https://www.adwokatura.pl"
    ),
    
    # Western Europe (Future expansion)
    "DE": JurisdictionConfig(
        code="DE",
        name="Germany",
        name_local="Deutschland",
        flag_emoji="🇩🇪",
        default_language="de",
        supported_languages=["de", "en"],
        currency="EUR",
        legal_system="civil_law",
        is_active=False,  # Not yet active
        bar_association_url="https://www.brak.de"
    ),
    
    "AT": JurisdictionConfig(
        code="AT",
        name="Austria",
        name_local="Österreich",
        flag_emoji="🇦🇹",
        default_language="de",
        supported_languages=["de", "en"],
        currency="EUR",
        legal_system="civil_law",
        is_active=False,  # Not yet active
        bar_association_url="https://www.rechtsanwaelte.at"
    ),
    
    "FR": JurisdictionConfig(
        code="FR",
        name="France",
        name_local="France",
        flag_emoji="🇫🇷",
        default_language="fr",
        supported_languages=["fr", "en"],
        currency="EUR",
        legal_system="civil_law",
        is_active=False,  # Not yet active
        bar_association_url="https://www.cnb.avocat.fr"
    ),
    
    # Eastern Europe (Future expansion)
    "HU": JurisdictionConfig(
        code="HU",
        name="Hungary",
        name_local="Magyarország",
        flag_emoji="🇭🇺",
        default_language="hu",
        supported_languages=["hu", "en", "de"],
        currency="HUF",
        legal_system="civil_law",
        is_active=False,  # Not yet active
        bar_association_url="https://www.magyarugyvedikamara.hu"
    ),
    
    "RO": JurisdictionConfig(
        code="RO",
        name="Romania",
        name_local="România",
        flag_emoji="🇷🇴",
        default_language="ro",
        supported_languages=["ro", "en"],
        currency="RON",
        legal_system="civil_law",
        is_active=False,  # Not yet active
        bar_association_url="https://www.unbr.ro"
    ),
    
    "UA": JurisdictionConfig(
        code="UA",
        name="Ukraine",
        name_local="Україна",
        flag_emoji="🇺🇦",
        default_language="uk",
        supported_languages=["uk", "en", "ru"],
        currency="UAH",
        legal_system="civil_law",
        is_active=False,  # Not yet active
        bar_association_url="https://unba.org.ua"
    ),
    
    # International (for lawyers with multiple jurisdictions)
    "EN": JurisdictionConfig(
        code="EN",
        name="International (English)",
        name_local="International",
        flag_emoji="🌍",
        default_language="en",
        supported_languages=["en"],
        currency="EUR",
        legal_system="mixed",
        is_active=False,  # Not yet active
        bar_association_url=""
    ),
}


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_active_jurisdictions() -> Dict[str, JurisdictionConfig]:
    """Get all active jurisdictions"""
    return {
        code: config 
        for code, config in SUPPORTED_JURISDICTIONS.items() 
        if config.is_active
    }


def get_jurisdiction(code: str) -> JurisdictionConfig:
    """Get jurisdiction config by code"""
    jurisdiction = SUPPORTED_JURISDICTIONS.get(code.upper())
    if not jurisdiction:
        raise ValueError(f"Unsupported jurisdiction: {code}")
    return jurisdiction


def is_jurisdiction_active(code: str) -> bool:
    """Check if jurisdiction is active"""
    try:
        jurisdiction = get_jurisdiction(code)
        return jurisdiction.is_active
    except ValueError:
        return False


def get_jurisdiction_codes() -> List[str]:
    """Get list of all jurisdiction codes"""
    return list(SUPPORTED_JURISDICTIONS.keys())


def get_active_jurisdiction_codes() -> List[str]:
    """Get list of active jurisdiction codes"""
    return [code for code, config in SUPPORTED_JURISDICTIONS.items() if config.is_active]


# ============================================
# VALIDATION
# ============================================

def validate_jurisdictions(jurisdictions: List[str]) -> bool:
    """
    Validate that all jurisdictions in list are supported and active
    
    Args:
        jurisdictions: List of jurisdiction codes (e.g., ["SK", "CZ"])
    
    Returns:
        True if all jurisdictions are valid and active
    
    Raises:
        ValueError: If any jurisdiction is invalid or inactive
    """
    if not jurisdictions:
        raise ValueError("At least one jurisdiction is required")
    
    for code in jurisdictions:
        code_upper = code.upper()
        if code_upper not in SUPPORTED_JURISDICTIONS:
            raise ValueError(f"Unsupported jurisdiction: {code}")
        
        if not SUPPORTED_JURISDICTIONS[code_upper].is_active:
            raise ValueError(f"Jurisdiction {code} is not currently active")
    
    return True


# ============================================
# CONSTANTS FOR EASY ACCESS
# ============================================

# Active jurisdiction codes (for validation)
ACTIVE_JURISDICTION_CODES = get_active_jurisdiction_codes()

# All jurisdiction codes (for reference)
ALL_JURISDICTION_CODES = get_jurisdiction_codes()

# Default jurisdiction
DEFAULT_JURISDICTION = "SK"
