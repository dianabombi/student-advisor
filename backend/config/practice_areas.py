"""
CODEX Legal Platform - Practice Areas Configuration

Defines legal practice areas, their categories, and relevant legal codes
for different jurisdictions.
"""

PRACTICE_AREAS = {
    "civil": {
        "name_sk": "Civilné právo",
        "name_en": "Civil Law",
        "name_uk": "Цивільне право",
        "name_ru": "Гражданское право",
        "description_sk": "Právne vzťahy medzi fyzickými a právnickými osobami",
        "categories": [
            "contract",           # Zmluvy
            "property",           # Vlastníctvo
            "family",            # Rodinné právo
            "inheritance",       # Dedičské právo
            "obligations",       # Záväzkové právo
            "tort"              # Deliktné právo
        ],
        "relevant_codes_sk": [
            "Občiansky zákonník (40/1964 Zb.)",
            "Občiansky súdny poriadok (99/1963 Zb.)"
        ]
    },
    
    "criminal": {
        "name_sk": "Trestné právo",
        "name_en": "Criminal Law",
        "name_uk": "Кримінальне право",
        "name_ru": "Уголовное право",
        "description_sk": "Trestné činy a trestná zodpovednosť",
        "categories": [
            "offense",           # Trestný čin
            "defense",           # Obhajoba
            "procedure",         # Trestné konanie
            "penalty"           # Tresty
        ],
        "relevant_codes_sk": [
            "Trestný zákon (300/2005 Z.z.)",
            "Trestný poriadok (301/2005 Z.z.)"
        ]
    },
    
    "commercial": {
        "name_sk": "Obchodné právo",
        "name_en": "Commercial Law",
        "name_uk": "Комерційне право",
        "name_ru": "Коммерческое право",
        "description_sk": "Obchodné vzťahy a podnikanie",
        "categories": [
            "company",           # Obchodné spoločnosti
            "trade",            # Obchod
            "bankruptcy",       # Konkurz a reštrukturalizácia
            "commercial_contracts"  # Obchodné zmluvy
        ],
        "relevant_codes_sk": [
            "Obchodný zákonník (513/1991 Zb.)",
            "Zákon o konkurze a reštrukturalizácii (7/2005 Z.z.)"
        ]
    },
    
    "labor": {
        "name_sk": "Pracovné právo",
        "name_en": "Labor Law",
        "name_uk": "Трудове право",
        "name_ru": "Трудовое право",
        "description_sk": "Pracovnoprávne vzťahy",
        "categories": [
            "employment",        # Pracovný pomer
            "dismissal",        # Skončenie pracovného pomeru
            "wages",           # Mzdy a odmeny
            "workplace_safety"  # Bezpečnosť práce
        ],
        "relevant_codes_sk": [
            "Zákonník práce (311/2001 Z.z.)"
        ]
    },
    
    "administrative": {
        "name_sk": "Správne právo",
        "name_en": "Administrative Law",
        "name_uk": "Адміністративне право",
        "name_ru": "Административное право",
        "description_sk": "Vzťahy medzi občanmi a verejnou správou",
        "categories": [
            "administrative_procedure",  # Správne konanie
            "building_law",             # Stavebné právo
            "environmental_law",        # Životné prostredie
            "tax_law"                   # Daňové právo
        ],
        "relevant_codes_sk": [
            "Správny poriadok (71/1967 Zb.)",
            "Stavebný zákon (50/1976 Zb.)"
        ]
    },
    
    "real_estate": {
        "name_sk": "Nehnuteľnosti",
        "name_en": "Real Estate Law",
        "name_uk": "Нерухомість",
        "name_ru": "Недвижимость",
        "description_sk": "Právne vzťahy týkajúce sa nehnuteľností",
        "categories": [
            "purchase",          # Kúpa/predaj
            "lease",            # Prenájom
            "ownership",        # Vlastníctvo
            "cadastre"         # Kataster nehnuteľností
        ],
        "relevant_codes_sk": [
            "Občiansky zákonník (40/1964 Zb.)",
            "Zákon o katastri nehnuteľností (162/1995 Z.z.)"
        ]
    }
}

LEGAL_DOCUMENT_TYPES = {
    "contract": {
        "name_sk": "Zmluva",
        "name_en": "Contract",
        "name_uk": "Договір",
        "name_ru": "Договор",
        "practice_areas": ["civil", "commercial", "real_estate", "labor"]
    },
    "lawsuit": {
        "name_sk": "Žaloba",
        "name_en": "Lawsuit",
        "name_uk": "Позов",
        "name_ru": "Иск",
        "practice_areas": ["civil", "commercial", "labor"]
    },
    "complaint": {
        "name_sk": "Sťažnosť",
        "name_en": "Complaint",
        "name_uk": "Скарга",
        "name_ru": "Жалоба",
        "practice_areas": ["administrative", "criminal"]
    },
    "power_of_attorney": {
        "name_sk": "Plná moc",
        "name_en": "Power of Attorney",
        "name_uk": "Довіреність",
        "name_ru": "Доверенность",
        "practice_areas": ["civil", "commercial", "real_estate"]
    },
    "court_decision": {
        "name_sk": "Súdne rozhodnutie",
        "name_en": "Court Decision",
        "name_uk": "Судове рішення",
        "name_ru": "Судебное решение",
        "practice_areas": ["civil", "criminal", "commercial", "administrative"]
    },
    "legal_opinion": {
        "name_sk": "Právny posudok",
        "name_en": "Legal Opinion",
        "name_uk": "Правовий висновок",
        "name_ru": "Правовое заключение",
        "practice_areas": ["civil", "criminal", "commercial", "administrative"]
    },
    "agreement": {
        "name_sk": "Dohoda",
        "name_en": "Agreement",
        "name_uk": "Угода",
        "name_ru": "Соглашение",
        "practice_areas": ["civil", "commercial", "labor"]
    },
    "notarial_deed": {
        "name_sk": "Notárska zápisnica",
        "name_en": "Notarial Deed",
        "name_uk": "Нотаріальний акт",
        "name_ru": "Нотариальный акт",
        "practice_areas": ["civil", "real_estate"]
    },
    "appeal": {
        "name_sk": "Odvolanie",
        "name_en": "Appeal",
        "name_uk": "Апеляція",
        "name_ru": "Апелляция",
        "practice_areas": ["civil", "criminal", "administrative"]
    },
    "other_legal": {
        "name_sk": "Iný právny dokument",
        "name_en": "Other Legal Document",
        "name_uk": "Інший юридичний документ",
        "name_ru": "Другой юридический документ",
        "practice_areas": ["civil", "criminal", "commercial", "administrative", "labor", "real_estate"]
    }
}

JURISDICTIONS = {
    "SK": {
        "name": "Slovakia",
        "name_local": "Slovensko",
        "language": "sk",
        "currency": "EUR",
        "legal_system": "Civil Law",
        "enabled": True,
        "practice_areas": ["civil", "criminal", "commercial", "labor", "administrative", "real_estate"]
    },
    "CZ": {
        "name": "Czech Republic",
        "name_local": "Česká republika",
        "language": "cs",
        "currency": "CZK",
        "legal_system": "Civil Law",
        "enabled": False,  # To be enabled later
        "practice_areas": ["civil", "criminal", "commercial", "labor", "administrative", "real_estate"]
    },
    "PL": {
        "name": "Poland",
        "name_local": "Polska",
        "language": "pl",
        "currency": "PLN",
        "legal_system": "Civil Law",
        "enabled": False,  # To be enabled later
        "practice_areas": ["civil", "criminal", "commercial", "labor", "administrative", "real_estate"]
    }
}

def get_practice_area_name(area_code: str, language: str = "sk") -> str:
    """Get practice area name in specified language"""
    if area_code not in PRACTICE_AREAS:
        return area_code
    
    key = f"name_{language}"
    return PRACTICE_AREAS[area_code].get(key, PRACTICE_AREAS[area_code]["name_en"])

def get_document_type_name(doc_type: str, language: str = "sk") -> str:
    """Get document type name in specified language"""
    if doc_type not in LEGAL_DOCUMENT_TYPES:
        return doc_type
    
    key = f"name_{language}"
    return LEGAL_DOCUMENT_TYPES[doc_type].get(key, LEGAL_DOCUMENT_TYPES[doc_type]["name_en"])

def get_enabled_jurisdictions() -> dict:
    """Get only enabled jurisdictions"""
    return {k: v for k, v in JURISDICTIONS.items() if v.get("enabled", False)}
