"""
Field Extractor

Extracts structured data from documents.
"""

import re
import logging
from typing import Dict, List, Optional
from datetime import datetime
import json

from .document_types import DocumentType, get_document_fields

logger = logging.getLogger(__name__)


class FieldExtractor:
    """
    Extract structured fields from document text.
    
    Extracts:
    - Dates
    - Amounts and currencies
    - Names and parties
    - Addresses
    - Identification numbers (IČO, DIČ, etc.)
    - Contract numbers
    """
    
    def __init__(self):
        """Initialize field extractor."""
        self.patterns = self._compile_patterns()
        self.type_specific_extractors = self._init_type_extractors()
    
    def _compile_patterns(self) -> Dict:
        """Compile regex patterns for field extraction."""
        return {
            'dates': [
                re.compile(r'(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})'),  # DD.MM.YYYY
                re.compile(r'(\d{1,2})/(\d{1,2})/(\d{4})'),          # DD/MM/YYYY
                re.compile(r'(\d{4})-(\d{2})-(\d{2})')               # YYYY-MM-DD
            ],
            'amounts': [
                re.compile(r'(\d+(?:\s?\d+)*(?:[,\.]\d{2})?)\s*(?:€|EUR|Eur)'),
                re.compile(r'(\d+(?:\s?\d+)*(?:[,\.]\d{2})?)\s*(?:Kč|CZK)'),
                re.compile(r'(\d+(?:\s?\d+)*(?:[,\.]\d{2})?)\s*(?:PLN|zł)')
            ],
            'ico': re.compile(r'IČO:?\s*(\d{8})', re.IGNORECASE),
            'dic': re.compile(r'DIČ:?\s*(\d{10})', re.IGNORECASE),
            'contract_number': re.compile(r'(?:č\.|číslo|number|zmluva č\.)[\s:]*([A-Z0-9\-/]+)', re.IGNORECASE),
            'invoice_number': re.compile(r'(?:faktúra|invoice|FA)[\s:]*(č\.)?[\s:]*([A-Z0-9\-/]+)', re.IGNORECASE),
            'case_number': re.compile(r'(?:spisová značka|sp\. zn\.)[\s:]*([A-Z0-9\-/]+)', re.IGNORECASE),
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phone': re.compile(r'(?:\+421|00421)?\s*\d{3}\s*\d{3}\s*\d{3}'),
            'person_name': re.compile(r'(?:meno|name|zamestnanec|employee)[\s:]+([A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ][a-záčďéěíňóřšťúůýž]+\s+[A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ][a-záčďéěíňóřšťúůýž]+)', re.IGNORECASE),
            'organization': re.compile(r'([A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ][a-záčďéěíňóřšťúůýž\s]+(?:s\.r\.o\.|a\.s\.|spol\. s r\.o\.))', re.IGNORECASE),
        }
    
    def extract_dates(self, text: str) -> List[Dict]:
        """
        Extract dates from text.
        
        Args:
            text: Document text
            
        Returns:
            List of date dictionaries
        """
        dates = []
        
        for pattern in self.patterns['dates']:
            for match in pattern.finditer(text):
                # Get context
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 30)
                context = text[start:end].strip()
                
                dates.append({
                    'value': match.group(0),
                    'context': context,
                    'position': match.start()
                })
        
        logger.info(f"Extracted {len(dates)} dates")
        return dates
    
    def extract_amounts(self, text: str) -> List[Dict]:
        """
        Extract monetary amounts from text.
        
        Args:
            text: Document text
            
        Returns:
            List of amount dictionaries
        """
        amounts = []
        
        for pattern in self.patterns['amounts']:
            for match in pattern.finditer(text):
                # Get context
                start = max(0, match.start() - 40)
                end = min(len(text), match.end() + 40)
                context = text[start:end].strip()
                
                # Parse amount
                amount_str = match.group(1).replace(' ', '').replace(',', '.')
                
                amounts.append({
                    'value': match.group(0),
                    'numeric_value': float(amount_str) if amount_str else None,
                    'context': context,
                    'position': match.start()
                })
        
        logger.info(f"Extracted {len(amounts)} amounts")
        return amounts
    
    def extract_parties(self, text: str) -> List[str]:
        """
        Extract party names from document.
        
        Args:
            text: Document text
            
        Returns:
            List of party names
        """
        parties = []
        
        # Patterns for party identification
        patterns = [
            r'(?:zmluvná strana|strana|účastník|účastnik)[\s:]+([A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ][a-záčďéěíňóřšťúůýž\s]+)',
            r'(?:meno|názov|name)[\s:]+([A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ][a-záčďéěíňóřšťúůýž\s]+)',
            r'(?:predávajúci|kupujúci|prenajímateľ|nájomca)[\s:]+([A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ][a-záčďéěíňóřšťúůýž\s]+)'
        ]
        
        for pattern_str in patterns:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            for match in pattern.finditer(text):
                party = match.group(1).strip()
                if len(party) > 3 and party not in parties:
                    parties.append(party)
        
        logger.info(f"Extracted {len(parties)} parties")
        return parties[:10]  # Limit to 10
    
    def extract_identifiers(self, text: str) -> Dict:
        """
        Extract business identifiers (IČO, DIČ, etc.).
        
        Args:
            text: Document text
            
        Returns:
            Dictionary of identifiers
        """
        identifiers = {}
        
        # IČO (Company ID)
        ico_match = self.patterns['ico'].search(text)
        if ico_match:
            identifiers['ico'] = ico_match.group(1)
        
        # DIČ (Tax ID)
        dic_match = self.patterns['dic'].search(text)
        if dic_match:
            identifiers['dic'] = dic_match.group(1)
        
        # Contract number
        contract_match = self.patterns['contract_number'].search(text)
        if contract_match:
            identifiers['contract_number'] = contract_match.group(1)
        
        logger.info(f"Extracted identifiers: {list(identifiers.keys())}")
        return identifiers
    
    def extract_contact_info(self, text: str) -> Dict:
        """
        Extract contact information.
        
        Args:
            text: Document text
            
        Returns:
            Dictionary of contact info
        """
        contact = {}
        
        # Email
        email_match = self.patterns['email'].search(text)
        if email_match:
            contact['email'] = email_match.group(0)
        
        # Phone
        phone_match = self.patterns['phone'].search(text)
        if phone_match:
            contact['phone'] = phone_match.group(0)
        
        logger.info(f"Extracted contact info: {list(contact.keys())}")
        return contact
    
    def extract_all_fields(self, text: str) -> Dict:
        """
        Extract all fields from document.
        
        Args:
            text: Document text
            
        Returns:
            Dictionary with all extracted fields
        """
        logger.info("Extracting all fields from document")
        
        return {
            'dates': self.extract_dates(text),
            'amounts': self.extract_amounts(text),
            'parties': self.extract_parties(text),
            'identifiers': self.extract_identifiers(text),
            'contact': self.extract_contact_info(text),
            'extracted_at': datetime.utcnow().isoformat()
        }
    
    def _init_type_extractors(self) -> Dict:
        """Initialize type-specific extraction methods."""
        return {
            DocumentType.EMPLOYMENT_CONTRACT: self._extract_employment_contract,
            DocumentType.INVOICE: self._extract_invoice,
            DocumentType.PURCHASE_AGREEMENT: self._extract_purchase_agreement,
            DocumentType.LEASE_AGREEMENT: self._extract_lease_agreement,
        }
    
    def extract_fields(self, text: str, document_type: DocumentType) -> Dict:
        """
        Extract fields based on document type.
        
        Args:
            text: Document text
            document_type: Type of document
            
        Returns:
            Dictionary with extracted fields in JSON format
        """
        logger.info(f"Extracting fields for {document_type.value}")
        
        # Get type-specific extractor
        extractor = self.type_specific_extractors.get(document_type)
        
        if extractor:
            fields = extractor(text)
        else:
            fields = self._extract_generic(text)
        
        # Add metadata
        fields['_metadata'] = {
            'document_type': document_type.value,
            'extracted_at': datetime.utcnow().isoformat(),
            'field_count': len([k for k in fields.keys() if not k.startswith('_')])
        }
        
        logger.info(f"Extracted {fields['_metadata']['field_count']} fields")
        return fields
    
    def _extract_employment_contract(self, text: str) -> Dict:
        """Extract fields from employment contract."""
        fields = {}
        
        match = self.patterns['contract_number'].search(text)
        if match:
            fields['contract_number'] = match.group(1)
        
        dates = self.extract_dates(text)
        if dates:
            fields['contract_date'] = dates[0]['value']
            if len(dates) > 1:
                fields['start_date'] = dates[1]['value']
        
        org_match = self.patterns['organization'].search(text)
        if org_match:
            fields['employer'] = org_match.group(1).strip()
        
        person_match = self.patterns['person_name'].search(text)
        if person_match:
            fields['employee'] = person_match.group(1).strip()
        
        amounts = self.extract_amounts(text)
        if amounts:
            fields['salary'] = amounts[0]['value']
        
        return fields
    
    def _extract_invoice(self, text: str) -> Dict:
        """Extract fields from invoice."""
        fields = {}
        
        match = self.patterns['invoice_number'].search(text)
        if match:
            fields['invoice_number'] = match.group(2) if match.lastindex >= 2 else match.group(1)
        
        dates = self.extract_dates(text)
        if dates:
            fields['invoice_date'] = dates[0]['value']
            if len(dates) > 1:
                fields['due_date'] = dates[1]['value']
        
        amounts = self.extract_amounts(text)
        if amounts:
            fields['total_amount'] = amounts[-1]['value']
            if len(amounts) > 1:
                fields['vat_amount'] = amounts[-2]['value']
        
        ico_match = self.patterns['ico'].search(text)
        if ico_match:
            fields['supplier_ico'] = ico_match.group(1)
        
        dic_match = self.patterns['dic'].search(text)
        if dic_match:
            fields['supplier_dic'] = dic_match.group(1)
        
        return fields
    
    def _extract_purchase_agreement(self, text: str) -> Dict:
        """Extract fields from purchase agreement."""
        fields = {}
        
        match = self.patterns['contract_number'].search(text)
        if match:
            fields['contract_number'] = match.group(1)
        
        dates = self.extract_dates(text)
        if dates:
            fields['contract_date'] = dates[0]['value']
        
        amounts = self.extract_amounts(text)
        if amounts:
            fields['purchase_price'] = amounts[0]['value']
        
        return fields
    
    def _extract_lease_agreement(self, text: str) -> Dict:
        """Extract fields from lease agreement."""
        fields = {}
        
        match = self.patterns['contract_number'].search(text)
        if match:
            fields['contract_number'] = match.group(1)
        
        dates = self.extract_dates(text)
        if dates:
            fields['contract_date'] = dates[0]['value']
        
        amounts = self.extract_amounts(text)
        if amounts:
            fields['monthly_rent'] = amounts[0]['value']
            if len(amounts) > 1:
                fields['deposit'] = amounts[1]['value']
        
        return fields
    
    def _extract_generic(self, text: str) -> Dict:
        """Generic extraction for unknown document types."""
        return self.extract_all_fields(text)
    
    def to_json(self, fields: Dict) -> str:
        """Convert extracted fields to JSON string."""
        return json.dumps(fields, ensure_ascii=False, indent=2)


# Convenience function
def extract_fields(text: str, document_type: DocumentType) -> Dict:
    """
    Extract fields from document.
    
    Args:
        text: Document text
        document_type: Type of document
        
    Returns:
        Dictionary with extracted fields
    """
    extractor = FieldExtractor()
    return extractor.extract_fields(text, document_type)
