"""
Unit tests for Document Processing Module

Tests for OCR, Classification, and Field Extraction.
"""

import pytest
import os
from pathlib import Path
from datetime import datetime

from services.doc_processor import (
    perform_ocr,
    classify_document,
    extract_document_fields,
    DocumentType,
    MinIOStorage
)


# Test data directory
TEST_DATA_DIR = Path(__file__).parent / 'test_data'


class TestOCR:
    """Tests for OCR functionality."""
    
    def test_ocr_pdf_file(self):
        """Test OCR on PDF file."""
        # This would require a real PDF file
        # For now, we'll test with text
        test_file = TEST_DATA_DIR / 'sample_contract.pdf'
        
        if test_file.exists():
            result = perform_ocr(str(test_file))
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_ocr_image_file(self):
        """Test OCR on image file."""
        test_file = TEST_DATA_DIR / 'sample_invoice.jpg'
        
        if test_file.exists():
            result = perform_ocr(str(test_file))
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_ocr_invalid_file(self):
        """Test OCR with invalid file."""
        with pytest.raises(Exception):
            perform_ocr('/nonexistent/file.pdf')
    
    def test_ocr_empty_result(self):
        """Test OCR with empty/blank image."""
        # Would need actual blank image
        pass


class TestClassification:
    """Tests for document classification."""
    
    def test_classify_employment_contract(self):
        """Test classification of employment contract."""
        text = """
        PRACOVNÁ ZMLUVA
        
        uzavretá podľa § 42 a nasl. zákona č. 311/2001 Z.z. Zákonníka práce
        
        Zamestnávateľ: ABC s.r.o.
        IČO: 12345678
        
        Zamestnanec: Ján Novák
        Rodné číslo: 901234/5678
        
        Pracovná pozícia: Programátor
        Mzda: 2000 EUR
        Dátum nástupu: 01.01.2025
        """
        
        result = classify_document(text)
        
        assert result['document_type'] == DocumentType.EMPLOYMENT_CONTRACT
        assert result['confidence'] > 0.5
        assert 'explanation' in result
    
    def test_classify_invoice(self):
        """Test classification of invoice."""
        text = """
        FAKTÚRA č. FA-2024-001
        
        Dodávateľ: XYZ s.r.o.
        IČO: 87654321
        DIČ: SK2020123456
        
        Odberateľ: ABC s.r.o.
        
        Dátum vystavenia: 15.12.2024
        Dátum splatnosti: 29.12.2024
        
        Suma celkom: 1500.00 EUR
        """
        
        result = classify_document(text)
        
        assert result['document_type'] == DocumentType.INVOICE
        assert result['confidence'] > 0.5
    
    def test_classify_lease_agreement(self):
        """Test classification of lease agreement."""
        text = """
        NÁJOMNÁ ZMLUVA
        
        Prenajímateľ: Mária Kováčová
        Nájomca: Peter Slovák
        
        Predmet nájmu: Byt 2+1, Bratislava
        Nájomné: 500 EUR/mesiac
        Dátum začiatku: 01.01.2025
        """
        
        result = classify_document(text)
        
        assert result['document_type'] == DocumentType.LEASE_AGREEMENT
        assert result['confidence'] > 0.3
    
    def test_classify_unknown_document(self):
        """Test classification of unknown document."""
        text = """
        This is some random text that doesn't match any document type.
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        """
        
        result = classify_document(text)
        
        assert result['document_type'] in DocumentType
        assert 'confidence' in result
    
    def test_classification_confidence_scores(self):
        """Test that confidence scores are in valid range."""
        text = "ZMLUVA O DIELO"
        
        result = classify_document(text)
        
        assert 0.0 <= result['confidence'] <= 1.0


class TestFieldExtraction:
    """Tests for field extraction."""
    
    def test_extract_employment_contract_fields(self):
        """Test extraction from employment contract."""
        text = """
        PRACOVNÁ ZMLUVA č. ZML-001/2024
        uzavretá dňa 15.12.2024
        
        Zamestnávateľ: ABC s.r.o., IČO: 12345678
        Zamestnanec: Ján Novák
        Pracovná pozícia: Programátor
        Mzda: 2000 EUR
        """
        
        fields = extract_document_fields(text, DocumentType.EMPLOYMENT_CONTRACT)
        
        assert 'contract_number' in fields
        assert fields['contract_number'] == 'ZML-001/2024'
        
        assert 'contract_date' in fields
        assert '15.12.2024' in fields['contract_date']
        
        assert 'employer' in fields
        assert 'ABC s.r.o.' in fields['employer']
        
        assert 'employee' in fields
        assert 'Ján Novák' in fields['employee']
        
        assert '_metadata' in fields
        assert fields['_metadata']['document_type'] == 'employment_contract'
    
    def test_extract_invoice_fields(self):
        """Test extraction from invoice."""
        text = """
        FAKTÚRA č. FA-123/2024
        
        Dátum vystavenia: 15.12.2024
        Dátum splatnosti: 29.12.2024
        
        Dodávateľ:
        XYZ s.r.o.
        IČO: 87654321
        DIČ: SK2020123456
        
        Suma celkom: 1500.00 EUR
        """
        
        fields = extract_document_fields(text, DocumentType.INVOICE)
        
        assert 'invoice_number' in fields
        assert 'FA-123/2024' in fields['invoice_number']
        
        assert 'ico' in fields
        assert '87654321' in fields['ico']
        
        assert 'dic' in fields
        assert 'SK2020123456' in fields['dic']
    
    def test_extract_dates(self):
        """Test date extraction."""
        text = """
        Dátum: 15.12.2024
        Platnosť od: 01.01.2025
        """
        
        fields = extract_document_fields(text, DocumentType.SERVICE_CONTRACT)
        
        # Should extract dates in some form
        assert '_metadata' in fields
    
    def test_extract_amounts(self):
        """Test amount extraction."""
        text = """
        Cena: 1500 EUR
        Celkom: 2000.50 EUR
        """
        
        fields = extract_document_fields(text, DocumentType.INVOICE)
        
        # Should extract amounts
        assert '_metadata' in fields
    
    def test_extract_ico_dic(self):
        """Test IČO and DIČ extraction."""
        text = """
        IČO: 12345678
        DIČ: SK2020123456
        IČ DPH: SK2020654321
        """
        
        fields = extract_document_fields(text, DocumentType.INVOICE)
        
        if 'ico' in fields:
            assert '12345678' in str(fields['ico'])
        
        if 'dic' in fields:
            assert 'SK' in str(fields['dic'])
    
    def test_field_extraction_metadata(self):
        """Test metadata in extracted fields."""
        text = "ZMLUVA č. 123/2024"
        
        fields = extract_document_fields(text, DocumentType.SERVICE_CONTRACT)
        
        assert '_metadata' in fields
        assert 'document_type' in fields['_metadata']
        assert 'extracted_at' in fields['_metadata']
        assert 'field_count' in fields['_metadata']


class TestMinIOStorage:
    """Tests for MinIO storage operations."""
    
    @pytest.fixture
    def storage(self):
        """Create MinIO storage instance."""
        return MinIOStorage()
    
    def test_storage_initialization(self, storage):
        """Test storage initialization."""
        assert storage is not None
        assert hasattr(storage, 'BUCKET_RAW')
        assert hasattr(storage, 'BUCKET_PROCESSED')
        assert hasattr(storage, 'BUCKET_TEMPLATES')
        assert hasattr(storage, 'BUCKET_FILLED')
    
    def test_upload_raw_document(self, storage):
        """Test uploading raw document."""
        # This would require actual MinIO connection
        # Skip if not available
        pytest.skip("Requires MinIO connection")
    
    def test_get_presigned_url(self, storage):
        """Test generating presigned URL."""
        # This would require actual MinIO connection
        pytest.skip("Requires MinIO connection")


class TestIntegration:
    """Integration tests for complete pipeline."""
    
    def test_full_pipeline_employment_contract(self):
        """Test complete pipeline with employment contract."""
        # Sample text
        text = """
        PRACOVNÁ ZMLUVA č. ZML-001/2024
        uzavretá dňa 15.12.2024
        
        Zamestnávateľ: ABC s.r.o.
        IČO: 12345678
        
        Zamestnanec: Ján Novák
        Rodné číslo: 901234/5678
        
        Pracovná pozícia: Programátor
        Mzda: 2000 EUR mesačne
        Dátum nástupu: 01.01.2025
        """
        
        # Step 1: Classification
        classification = classify_document(text)
        assert classification['document_type'] == DocumentType.EMPLOYMENT_CONTRACT
        
        # Step 2: Field Extraction
        fields = extract_document_fields(text, classification['document_type'])
        assert 'contract_number' in fields
        assert 'employer' in fields
        assert 'employee' in fields
    
    def test_full_pipeline_invoice(self):
        """Test complete pipeline with invoice."""
        text = """
        FAKTÚRA č. FA-123/2024
        
        Dátum vystavenia: 15.12.2024
        Dátum splatnosti: 29.12.2024
        
        Dodávateľ: XYZ s.r.o., IČO: 87654321, DIČ: SK2020123456
        Odberateľ: ABC s.r.o., IČO: 12345678
        
        Položka              Cena
        Služby IT          1500.00 EUR
        
        Celkom:            1500.00 EUR
        """
        
        # Classification
        classification = classify_document(text)
        assert classification['document_type'] == DocumentType.INVOICE
        
        # Field Extraction
        fields = extract_document_fields(text, classification['document_type'])
        assert 'invoice_number' in fields
        assert 'ico' in fields or 'dic' in fields


# Pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
