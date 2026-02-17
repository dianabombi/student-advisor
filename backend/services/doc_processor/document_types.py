"""
Document Types and Field Definitions

Comprehensive structure for supported document types and their key fields.
"""

from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass, field


class DocumentType(str, Enum):
    """Supported document types."""
    
    # Contracts
    EMPLOYMENT_CONTRACT = "employment_contract"
    PURCHASE_AGREEMENT = "purchase_agreement"
    LEASE_AGREEMENT = "lease_agreement"
    SERVICE_CONTRACT = "service_contract"
    WORK_CONTRACT = "work_contract"
    LOAN_AGREEMENT = "loan_agreement"
    
    # Financial
    INVOICE = "invoice"
    RECEIPT = "receipt"
    PAYMENT_ORDER = "payment_order"
    
    # Legal
    POWER_OF_ATTORNEY = "power_of_attorney"
    COURT_DECISION = "court_decision"
    LAWSUIT = "lawsuit"
    COMPLAINT = "complaint"
    
    # Administrative
    ACT = "act"
    PROTOCOL = "protocol"
    CERTIFICATE = "certificate"
    PERMIT = "permit"
    
    # Correspondence
    LETTER = "letter"
    EMAIL = "email"
    NOTICE = "notice"
    
    # Other
    APPLICATION = "application"
    STATEMENT = "statement"
    OTHER = "other"


class FieldType(str, Enum):
    """Field data types."""
    
    TEXT = "text"
    DATE = "date"
    AMOUNT = "amount"
    PERSON = "person"
    ORGANIZATION = "organization"
    ADDRESS = "address"
    IDENTIFIER = "identifier"
    PERIOD = "period"
    BOOLEAN = "boolean"


@dataclass
class FieldDefinition:
    """Definition of a document field."""
    
    name: str
    field_type: FieldType
    required: bool = False
    description: str = ""
    validation_pattern: Optional[str] = None
    examples: List[str] = field(default_factory=list)


# Document type field definitions
DOCUMENT_FIELDS: Dict[DocumentType, List[FieldDefinition]] = {
    
    # Employment Contract
    DocumentType.EMPLOYMENT_CONTRACT: [
        FieldDefinition(
            name="contract_number",
            field_type=FieldType.IDENTIFIER,
            required=True,
            description="Číslo zmluvy",
            examples=["123/2024", "ZML-001-2024"]
        ),
        FieldDefinition(
            name="contract_date",
            field_type=FieldType.DATE,
            required=True,
            description="Dátum uzavretia zmluvy",
            examples=["15.12.2024", "2024-12-15"]
        ),
        FieldDefinition(
            name="employer",
            field_type=FieldType.ORGANIZATION,
            required=True,
            description="Zamestnávateľ",
            examples=["ABC s.r.o.", "XYZ a.s."]
        ),
        FieldDefinition(
            name="employee",
            field_type=FieldType.PERSON,
            required=True,
            description="Zamestnanec",
            examples=["Ján Novák", "Mária Kováčová"]
        ),
        FieldDefinition(
            name="position",
            field_type=FieldType.TEXT,
            required=True,
            description="Pracovná pozícia",
            examples=["Programátor", "Účtovník"]
        ),
        FieldDefinition(
            name="salary",
            field_type=FieldType.AMOUNT,
            required=True,
            description="Mzda",
            examples=["2000 EUR", "1500,00 €"]
        ),
        FieldDefinition(
            name="start_date",
            field_type=FieldType.DATE,
            required=True,
            description="Dátum nástupu",
            examples=["01.01.2025"]
        ),
        FieldDefinition(
            name="contract_type",
            field_type=FieldType.TEXT,
            required=False,
            description="Typ zmluvy (určitý/neurčitý čas)",
            examples=["neurčitý čas", "určitý čas do 31.12.2025"]
        ),
    ],
    
    # Purchase Agreement
    DocumentType.PURCHASE_AGREEMENT: [
        FieldDefinition(
            name="contract_number",
            field_type=FieldType.IDENTIFIER,
            required=True,
            description="Číslo zmluvy"
        ),
        FieldDefinition(
            name="contract_date",
            field_type=FieldType.DATE,
            required=True,
            description="Dátum uzavretia"
        ),
        FieldDefinition(
            name="seller",
            field_type=FieldType.PERSON,
            required=True,
            description="Predávajúci"
        ),
        FieldDefinition(
            name="buyer",
            field_type=FieldType.PERSON,
            required=True,
            description="Kupujúci"
        ),
        FieldDefinition(
            name="purchase_price",
            field_type=FieldType.AMOUNT,
            required=True,
            description="Kúpna cena"
        ),
        FieldDefinition(
            name="subject",
            field_type=FieldType.TEXT,
            required=True,
            description="Predmet kúpy",
            examples=["Nehnuteľnosť", "Vozidlo", "Tovar"]
        ),
        FieldDefinition(
            name="payment_terms",
            field_type=FieldType.TEXT,
            required=False,
            description="Platobné podmienky"
        ),
    ],
    
    # Lease Agreement
    DocumentType.LEASE_AGREEMENT: [
        FieldDefinition(
            name="contract_number",
            field_type=FieldType.IDENTIFIER,
            required=True,
            description="Číslo zmluvy"
        ),
        FieldDefinition(
            name="contract_date",
            field_type=FieldType.DATE,
            required=True,
            description="Dátum uzavretia"
        ),
        FieldDefinition(
            name="lessor",
            field_type=FieldType.PERSON,
            required=True,
            description="Prenajímateľ"
        ),
        FieldDefinition(
            name="lessee",
            field_type=FieldType.PERSON,
            required=True,
            description="Nájomca"
        ),
        FieldDefinition(
            name="property_address",
            field_type=FieldType.ADDRESS,
            required=True,
            description="Adresa nehnuteľnosti"
        ),
        FieldDefinition(
            name="monthly_rent",
            field_type=FieldType.AMOUNT,
            required=True,
            description="Mesačné nájomné"
        ),
        FieldDefinition(
            name="lease_period",
            field_type=FieldType.PERIOD,
            required=True,
            description="Doba nájmu",
            examples=["od 01.01.2025 do 31.12.2025", "neurčitý čas"]
        ),
        FieldDefinition(
            name="deposit",
            field_type=FieldType.AMOUNT,
            required=False,
            description="Kaucia"
        ),
    ],
    
    # Invoice
    DocumentType.INVOICE: [
        FieldDefinition(
            name="invoice_number",
            field_type=FieldType.IDENTIFIER,
            required=True,
            description="Číslo faktúry",
            examples=["2024001", "FA-123/2024"]
        ),
        FieldDefinition(
            name="invoice_date",
            field_type=FieldType.DATE,
            required=True,
            description="Dátum vystavenia"
        ),
        FieldDefinition(
            name="due_date",
            field_type=FieldType.DATE,
            required=True,
            description="Dátum splatnosti"
        ),
        FieldDefinition(
            name="supplier",
            field_type=FieldType.ORGANIZATION,
            required=True,
            description="Dodávateľ"
        ),
        FieldDefinition(
            name="customer",
            field_type=FieldType.ORGANIZATION,
            required=True,
            description="Odberateľ"
        ),
        FieldDefinition(
            name="total_amount",
            field_type=FieldType.AMOUNT,
            required=True,
            description="Celková suma"
        ),
        FieldDefinition(
            name="vat_amount",
            field_type=FieldType.AMOUNT,
            required=False,
            description="DPH"
        ),
        FieldDefinition(
            name="supplier_ico",
            field_type=FieldType.IDENTIFIER,
            required=False,
            description="IČO dodávateľa"
        ),
        FieldDefinition(
            name="supplier_dic",
            field_type=FieldType.IDENTIFIER,
            required=False,
            description="DIČ dodávateľa"
        ),
    ],
    
    # Power of Attorney
    DocumentType.POWER_OF_ATTORNEY: [
        FieldDefinition(
            name="document_date",
            field_type=FieldType.DATE,
            required=True,
            description="Dátum vyhotovenia"
        ),
        FieldDefinition(
            name="principal",
            field_type=FieldType.PERSON,
            required=True,
            description="Splnomocniteľ"
        ),
        FieldDefinition(
            name="attorney",
            field_type=FieldType.PERSON,
            required=True,
            description="Splnomocnenec"
        ),
        FieldDefinition(
            name="scope",
            field_type=FieldType.TEXT,
            required=True,
            description="Rozsah splnomocnenia"
        ),
        FieldDefinition(
            name="validity_period",
            field_type=FieldType.PERIOD,
            required=False,
            description="Doba platnosti"
        ),
    ],
    
    # Court Decision
    DocumentType.COURT_DECISION: [
        FieldDefinition(
            name="case_number",
            field_type=FieldType.IDENTIFIER,
            required=True,
            description="Spisová značka",
            examples=["1C/123/2024"]
        ),
        FieldDefinition(
            name="decision_date",
            field_type=FieldType.DATE,
            required=True,
            description="Dátum rozhodnutia"
        ),
        FieldDefinition(
            name="court_name",
            field_type=FieldType.ORGANIZATION,
            required=True,
            description="Názov súdu"
        ),
        FieldDefinition(
            name="plaintiff",
            field_type=FieldType.PERSON,
            required=True,
            description="Žalobca"
        ),
        FieldDefinition(
            name="defendant",
            field_type=FieldType.PERSON,
            required=True,
            description="Žalovaný"
        ),
        FieldDefinition(
            name="decision_type",
            field_type=FieldType.TEXT,
            required=False,
            description="Typ rozhodnutia",
            examples=["Rozsudok", "Uznesenie"]
        ),
    ],
    
    # Act
    DocumentType.ACT: [
        FieldDefinition(
            name="act_number",
            field_type=FieldType.IDENTIFIER,
            required=True,
            description="Číslo aktu"
        ),
        FieldDefinition(
            name="act_date",
            field_type=FieldType.DATE,
            required=True,
            description="Dátum vyhotovenia"
        ),
        FieldDefinition(
            name="act_type",
            field_type=FieldType.TEXT,
            required=True,
            description="Typ aktu",
            examples=["Odovzdávací protokol", "Preberací protokol", "Kontrolný záznam"]
        ),
        FieldDefinition(
            name="parties",
            field_type=FieldType.TEXT,
            required=True,
            description="Účastníci"
        ),
        FieldDefinition(
            name="subject",
            field_type=FieldType.TEXT,
            required=True,
            description="Predmet aktu"
        ),
    ],
    
    # Letter/Correspondence
    DocumentType.LETTER: [
        FieldDefinition(
            name="letter_date",
            field_type=FieldType.DATE,
            required=True,
            description="Dátum listu"
        ),
        FieldDefinition(
            name="sender",
            field_type=FieldType.PERSON,
            required=True,
            description="Odosielateľ"
        ),
        FieldDefinition(
            name="recipient",
            field_type=FieldType.PERSON,
            required=True,
            description="Príjemca"
        ),
        FieldDefinition(
            name="subject",
            field_type=FieldType.TEXT,
            required=False,
            description="Predmet"
        ),
        FieldDefinition(
            name="reference_number",
            field_type=FieldType.IDENTIFIER,
            required=False,
            description="Číslo jednania"
        ),
    ],
    
    # Application
    DocumentType.APPLICATION: [
        FieldDefinition(
            name="application_date",
            field_type=FieldType.DATE,
            required=True,
            description="Dátum podania"
        ),
        FieldDefinition(
            name="applicant",
            field_type=FieldType.PERSON,
            required=True,
            description="Žiadateľ"
        ),
        FieldDefinition(
            name="recipient_authority",
            field_type=FieldType.ORGANIZATION,
            required=True,
            description="Príslušný orgán"
        ),
        FieldDefinition(
            name="application_type",
            field_type=FieldType.TEXT,
            required=True,
            description="Typ žiadosti"
        ),
        FieldDefinition(
            name="subject",
            field_type=FieldType.TEXT,
            required=True,
            description="Predmet žiadosti"
        ),
    ],
}


def get_document_fields(doc_type: DocumentType) -> List[FieldDefinition]:
    """
    Get field definitions for a document type.
    
    Args:
        doc_type: Document type
        
    Returns:
        List of field definitions
    """
    return DOCUMENT_FIELDS.get(doc_type, [])


def get_required_fields(doc_type: DocumentType) -> List[FieldDefinition]:
    """
    Get required fields for a document type.
    
    Args:
        doc_type: Document type
        
    Returns:
        List of required field definitions
    """
    all_fields = get_document_fields(doc_type)
    return [f for f in all_fields if f.required]


def get_field_by_name(doc_type: DocumentType, field_name: str) -> Optional[FieldDefinition]:
    """
    Get specific field definition.
    
    Args:
        doc_type: Document type
        field_name: Field name
        
    Returns:
        Field definition or None
    """
    all_fields = get_document_fields(doc_type)
    for field_def in all_fields:
        if field_def.name == field_name:
            return field_def
    return None


def get_all_document_types() -> List[DocumentType]:
    """Get list of all supported document types."""
    return list(DocumentType)


def get_document_type_info() -> Dict:
    """
    Get comprehensive information about all document types.
    
    Returns:
        Dictionary with document type information
    """
    info = {}
    
    for doc_type in DocumentType:
        fields = get_document_fields(doc_type)
        required_fields = [f.name for f in fields if f.required]
        optional_fields = [f.name for f in fields if not f.required]
        
        info[doc_type.value] = {
            'name': doc_type.value,
            'total_fields': len(fields),
            'required_fields': required_fields,
            'optional_fields': optional_fields,
            'field_definitions': [
                {
                    'name': f.name,
                    'type': f.field_type.value,
                    'required': f.required,
                    'description': f.description
                }
                for f in fields
            ]
        }
    
    return info
