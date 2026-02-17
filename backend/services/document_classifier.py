"""
Document Classification and Key Field Extraction Module

Uses AI to automatically classify legal documents and extract key fields.
"""

import os
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)


class DocumentClassifier:
    """
    Classifies legal documents and extracts key fields using AI.
    
    Supports:
    - Document type classification
    - Practice area detection
    - Key field extraction (dates, parties, amounts, etc.)
    - Confidence scoring
    """
    
    # Document type patterns
    DOCUMENT_TYPES = {
        'zmluva': ['zmluva', 'contract', 'agreement', 'dohoda'],
        'ziadost': ['žiadosť', 'žiadost', 'application', 'request', 'podanie'],
        'rozhodnutie': ['rozhodnutie', 'decision', 'verdict', 'rozsudok'],
        'navrh': ['návrh', 'navrh', 'proposal', 'draft'],
        'plna_moc': ['plná moc', 'plna moc', 'power of attorney', 'splnomocnenie'],
        'faktura': ['faktúra', 'faktura', 'invoice'],
        'zmluva_o_dielo': ['zmluva o dielo', 'contract for work'],
        'kupna_zmluva': ['kúpna zmluva', 'kupna zmluva', 'purchase agreement'],
        'najomna_zmluva': ['nájomná zmluva', 'najomna zmluva', 'lease agreement', 'rental agreement']
    }
    
    # Practice areas
    PRACTICE_AREAS = {
        'civil': ['občianske', 'civil', 'zmluva', 'vlastníctvo', 'dedičstvo'],
        'criminal': ['trestné', 'criminal', 'obvinenie', 'trestný'],
        'commercial': ['obchodné', 'commercial', 'podnikanie', 'spoločnosť'],
        'labor': ['pracovné', 'labor', 'employment', 'zamestnanie'],
        'administrative': ['správne', 'administrative', 'úrad', 'správa']
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize classifier.
        
        Args:
            api_key: OpenAI API key (defaults to env variable)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
    
    def classify_document_type(self, text: str) -> Tuple[str, float]:
        """
        Classify document type based on content.
        
        Args:
            text: Document text
            
        Returns:
            Tuple of (document_type, confidence)
        """
        text_lower = text.lower()
        
        # Rule-based classification
        scores = {}
        for doc_type, keywords in self.DOCUMENT_TYPES.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[doc_type] = score
        
        if scores:
            best_type = max(scores, key=scores.get)
            confidence = min(scores[best_type] * 0.2, 1.0)
            return best_type, confidence
        
        return 'other', 0.3
    
    def detect_practice_area(self, text: str) -> Tuple[str, float]:
        """
        Detect practice area from document content.
        
        Args:
            text: Document text
            
        Returns:
            Tuple of (practice_area, confidence)
        """
        text_lower = text.lower()
        
        scores = {}
        for area, keywords in self.PRACTICE_AREAS.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[area] = score
        
        if scores:
            best_area = max(scores, key=scores.get)
            confidence = min(scores[best_area] * 0.15, 1.0)
            return best_area, confidence
        
        return 'civil', 0.5  # Default to civil law
    
    def extract_dates(self, text: str) -> List[Dict[str, str]]:
        """
        Extract dates from document.
        
        Args:
            text: Document text
            
        Returns:
            List of extracted dates with context
        """
        dates = []
        
        # Slovak date patterns
        patterns = [
            r'(\d{1,2})\.\s*(\d{1,2})\.\s*(\d{4})',  # DD.MM.YYYY
            r'(\d{1,2})/(\d{1,2})/(\d{4})',          # DD/MM/YYYY
            r'(\d{4})-(\d{2})-(\d{2})'               # YYYY-MM-DD
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                date_str = match.group(0)
                # Get context (20 chars before and after)
                start = max(0, match.start() - 20)
                end = min(len(text), match.end() + 20)
                context = text[start:end].strip()
                
                dates.append({
                    'date': date_str,
                    'context': context,
                    'position': match.start()
                })
        
        return dates
    
    def extract_amounts(self, text: str) -> List[Dict[str, str]]:
        """
        Extract monetary amounts from document.
        
        Args:
            text: Document text
            
        Returns:
            List of extracted amounts with context
        """
        amounts = []
        
        # Amount patterns
        patterns = [
            r'(\d+(?:\s?\d+)*(?:[,\.]\d{2})?)\s*(?:€|EUR|Eur)',
            r'(\d+(?:\s?\d+)*(?:[,\.]\d{2})?)\s*(?:Kč|CZK)',
            r'(\d+(?:\s?\d+)*(?:[,\.]\d{2})?)\s*(?:PLN|zł)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                amount_str = match.group(0)
                # Get context
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 30)
                context = text[start:end].strip()
                
                amounts.append({
                    'amount': amount_str,
                    'context': context,
                    'position': match.start()
                })
        
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
        
        # Look for common patterns
        patterns = [
            r'(?:zmluvná strana|strana|účastník|účastnik):\s*([A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ][a-záčďéěíňóřšťúůýž\s]+)',
            r'(?:meno|názov|name):\s*([A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ][a-záčďéěíňóřšťúůýž\s]+)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                party = match.group(1).strip()
                if len(party) > 3 and party not in parties:
                    parties.append(party)
        
        return parties[:5]  # Limit to 5 parties
    
    def extract_key_fields_ai(self, text: str, document_type: str) -> Dict:
        """
        Use AI to extract key fields based on document type.
        
        Args:
            text: Document text
            document_type: Type of document
            
        Returns:
            Dictionary of extracted fields
        """
        if not self.client:
            logger.warning("OpenAI client not available - skipping AI extraction")
            return {}
        
        # Truncate text if too long
        max_chars = 3000
        text_sample = text[:max_chars] if len(text) > max_chars else text
        
        prompt = f"""Analyzuj tento právny dokument typu "{document_type}" a vytiahni kľúčové polia.

Dokument:
{text_sample}

Vytiahni nasledujúce informácie (ak sú dostupné):
- Názov dokumentu
- Dátum vytvorenia
- Strany (účastníci)
- Predmet zmluvy/dokumentu
- Suma (ak je uvedená)
- Platnosť od/do

Odpoveď vo formáte JSON."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Si odborník na analýzu právnych dokumentov. Odpovedaj v JSON formáte."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content
            
            # Try to parse JSON
            import json
            try:
                return json.loads(result_text)
            except:
                return {'raw_response': result_text}
        
        except Exception as e:
            logger.error(f"AI extraction error: {e}")
            return {}
    
    def analyze_document(self, text: str, use_ai: bool = True) -> Dict:
        """
        Complete document analysis.
        
        Args:
            text: Document text
            use_ai: Whether to use AI for enhanced extraction
            
        Returns:
            Complete analysis results
        """
        logger.info(f"Analyzing document ({len(text)} chars)")
        
        # Basic classification
        doc_type, type_confidence = self.classify_document_type(text)
        practice_area, area_confidence = self.detect_practice_area(text)
        
        # Extract structured data
        dates = self.extract_dates(text)
        amounts = self.extract_amounts(text)
        parties = self.extract_parties(text)
        
        result = {
            'classification': {
                'document_type': doc_type,
                'type_confidence': type_confidence,
                'practice_area': practice_area,
                'area_confidence': area_confidence
            },
            'extracted_fields': {
                'dates': dates,
                'amounts': amounts,
                'parties': parties
            },
            'metadata': {
                'text_length': len(text),
                'analyzed_at': datetime.utcnow().isoformat()
            }
        }
        
        # AI-enhanced extraction
        if use_ai and self.client:
            ai_fields = self.extract_key_fields_ai(text, doc_type)
            result['ai_extracted'] = ai_fields
        
        logger.info(f"Analysis complete: {doc_type} ({type_confidence:.2f}), {practice_area} ({area_confidence:.2f})")
        
        return result


# Convenience function
def analyze_document(text: str, api_key: Optional[str] = None) -> Dict:
    """
    Analyze a document and extract key information.
    
    Args:
        text: Document text
        api_key: Optional OpenAI API key
        
    Returns:
        Analysis results
    """
    classifier = DocumentClassifier(api_key=api_key)
    return classifier.analyze_document(text)
