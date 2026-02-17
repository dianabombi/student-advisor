"""
OCR/IDP Service for document processing
Supports multiple providers: Mindee, Tesseract, Veryfi, etc.
"""

import os
from typing import Dict, Any, Optional
from enum import Enum
import requests
import pytesseract
from PIL import Image
import io

class OCRProvider(Enum):
    MINDEE = "mindee"
    TESSERACT = "tesseract"
    VERYFI = "veryfi"
    KLIPPA = "klippa"

class OCRService:
    def __init__(self, provider: OCRProvider = OCRProvider.MINDEE):
        self.provider = provider
        self.mindee_api_key = os.getenv("MINDEE_API_KEY")
        self.veryfi_api_key = os.getenv("VERYFI_API_KEY")
        self.klippa_api_key = os.getenv("KLIPPA_API_KEY")
    
    async def process_document(self, file_path: str, document_type: str = "invoice") -> Dict[str, Any]:
        """
        Process document using selected OCR provider
        
        Args:
            file_path: Path to the document file
            document_type: Type of document (invoice, receipt, tax_form, etc.)
        
        Returns:
            Extracted data as dictionary
        """
        if self.provider == OCRProvider.MINDEE:
            return await self._process_with_mindee(file_path, document_type)
        elif self.provider == OCRProvider.TESSERACT:
            return await self._process_with_tesseract(file_path)
        elif self.provider == OCRProvider.VERYFI:
            return await self._process_with_veryfi(file_path)
        elif self.provider == OCRProvider.KLIPPA:
            return await self._process_with_klippa(file_path)
        else:
            raise ValueError(f"Unsupported OCR provider: {self.provider}")
    
    async def _process_with_mindee(self, file_path: str, document_type: str) -> Dict[str, Any]:
        """
        Process document with Mindee API
        Mindee has specialized models for invoices, receipts, tax forms
        """
        if not self.mindee_api_key:
            raise ValueError("MINDEE_API_KEY not set")
        
        # Mindee API endpoints for different document types
        endpoints = {
            "invoice": "https://api.mindee.net/v1/products/mindee/invoices/v4/predict",
            "receipt": "https://api.mindee.net/v1/products/mindee/expense_receipts/v5/predict",
            "tax_form": "https://api.mindee.net/v1/products/mindee/financial_document/v1/predict"
        }
        
        endpoint = endpoints.get(document_type, endpoints["invoice"])
        
        with open(file_path, 'rb') as file:
            files = {'document': file}
            headers = {'Authorization': f'Token {self.mindee_api_key}'}
            
            response = requests.post(endpoint, files=files, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_mindee_response(data, document_type)
    
    def _parse_mindee_response(self, data: Dict, document_type: str) -> Dict[str, Any]:
        """Parse Mindee API response into standardized format"""
        prediction = data.get('document', {}).get('inference', {}).get('prediction', {})
        
        if document_type == "invoice":
            return {
                "document_type": "invoice",
                "supplier_name": prediction.get('supplier_name', {}).get('value'),
                "supplier_address": prediction.get('supplier_address', {}).get('value'),
                "customer_name": prediction.get('customer_name', {}).get('value'),
                "invoice_number": prediction.get('invoice_number', {}).get('value'),
                "invoice_date": prediction.get('date', {}).get('value'),
                "due_date": prediction.get('due_date', {}).get('value'),
                "total_amount": prediction.get('total_amount', {}).get('value'),
                "total_tax": prediction.get('total_tax', {}).get('value'),
                "currency": prediction.get('locale', {}).get('currency'),
                "line_items": [
                    {
                        "description": item.get('description'),
                        "quantity": item.get('quantity'),
                        "unit_price": item.get('unit_price'),
                        "total_amount": item.get('total_amount'),
                        "tax_rate": item.get('tax_rate')
                    }
                    for item in prediction.get('line_items', [])
                ],
                "confidence": data.get('document', {}).get('inference', {}).get('pages', [{}])[0].get('prediction', {}).get('confidence', 0)
            }
        
        elif document_type == "receipt":
            return {
                "document_type": "receipt",
                "merchant_name": prediction.get('supplier_name', {}).get('value'),
                "date": prediction.get('date', {}).get('value'),
                "time": prediction.get('time', {}).get('value'),
                "total_amount": prediction.get('total_amount', {}).get('value'),
                "total_tax": prediction.get('total_tax', {}).get('value'),
                "category": prediction.get('category', {}).get('value'),
                "payment_method": prediction.get('payment_method', {}).get('value'),
                "confidence": data.get('document', {}).get('inference', {}).get('pages', [{}])[0].get('prediction', {}).get('confidence', 0)
            }
        
        return {"raw_data": prediction}
    
    async def _process_with_tesseract(self, file_path: str) -> Dict[str, Any]:
        """
        Process document with Tesseract OCR (open-source)
        Good for basic text extraction, requires additional ML for structured data
        """
        try:
            image = Image.open(file_path)
            
            # Extract text
            text = pytesseract.image_to_string(image, lang='slk+eng')  # Slovak + English
            
            # Extract structured data using pytesseract
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            # Basic parsing (you can add ML model here for better extraction)
            return {
                "document_type": "unknown",
                "raw_text": text,
                "confidence": self._calculate_tesseract_confidence(data),
                "extracted_data": self._extract_structured_data(text)
            }
        except Exception as e:
            raise ValueError(f"Tesseract processing failed: {str(e)}")
    
    def _calculate_tesseract_confidence(self, data: Dict) -> float:
        """Calculate average confidence from Tesseract output"""
        confidences = [int(conf) for conf in data['conf'] if conf != '-1']
        return sum(confidences) / len(confidences) if confidences else 0
    
    def _extract_structured_data(self, text: str) -> Dict[str, Any]:
        """
        Basic structured data extraction from text
        In production, use ML model or regex patterns for better accuracy
        """
        import re
        
        # Simple regex patterns for common fields
        patterns = {
            'invoice_number': r'(?:Invoice|Faktúra|č\.|No\.?)\s*:?\s*([A-Z0-9-]+)',
            'date': r'(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})',
            'total': r'(?:Total|Celkom|Spolu)\s*:?\s*€?\s*([\d,]+\.?\d*)',
            'tax': r'(?:VAT|DPH)\s*:?\s*€?\s*([\d,]+\.?\d*)'
        }
        
        extracted = {}
        for field, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                extracted[field] = match.group(1)
        
        return extracted
    
    async def _process_with_veryfi(self, file_path: str) -> Dict[str, Any]:
        """
        Process document with Veryfi API
        Veryfi specializes in receipts and invoices
        """
        if not self.veryfi_api_key:
            raise ValueError("VERYFI_API_KEY not set")
        
        # Veryfi API implementation
        # https://docs.veryfi.com/
        url = "https://api.veryfi.com/api/v8/partner/documents"
        
        with open(file_path, 'rb') as file:
            files = {'file': file}
            headers = {
                'CLIENT-ID': os.getenv('VERYFI_CLIENT_ID'),
                'AUTHORIZATION': f'apikey {self.veryfi_api_key}'
            }
            
            response = requests.post(url, files=files, headers=headers)
            response.raise_for_status()
            
            return response.json()
    
    async def _process_with_klippa(self, file_path: str) -> Dict[str, Any]:
        """
        Process document with Klippa API
        Klippa supports European invoices and receipts
        """
        if not self.klippa_api_key:
            raise ValueError("KLIPPA_API_KEY not set")
        
        # Klippa API implementation
        # https://custom-ocr.klippa.com/api/v1/parseDocument
        url = "https://custom-ocr.klippa.com/api/v1/parseDocument"
        
        with open(file_path, 'rb') as file:
            files = {'document': file}
            headers = {'X-Auth-Key': self.klippa_api_key}
            
            response = requests.post(url, files=files, headers=headers)
            response.raise_for_status()
            
            return response.json()

# Helper function for document classification
async def classify_document(file_path: str) -> str:
    """
    Classify document type using simple heuristics or ML
    Returns: invoice, receipt, tax_form, contract, other
    """
    # Simple classification based on file content
    # In production, use ML model for better accuracy
    
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang='slk+eng').lower()
        
        if any(word in text for word in ['faktúra', 'invoice', 'faktura']):
            return 'invoice'
        elif any(word in text for word in ['pokladničný', 'receipt', 'účtenka']):
            return 'receipt'
        elif any(word in text for word in ['daňové priznanie', 'tax return', 'danove priznanie']):
            return 'tax_form'
        elif any(word in text for word in ['zmluva', 'contract', 'dohoda']):
            return 'contract'
        else:
            return 'other'
    except:
        return 'unknown'
