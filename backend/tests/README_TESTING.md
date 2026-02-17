# Test Document Processing Module

## Overview

This directory contains unit tests for the Document Processing module.

## Test Structure

```
tests/
├── test_document_processing.py  # Main test file
├── test_data/                    # Test documents
│   ├── sample_contract.pdf
│   ├── sample_invoice.jpg
│   ├── sample_lease.pdf
│   └── sample_complaint.docx
└── conftest.py                   # Pytest configuration
```

## Running Tests

### Run all tests
```bash
cd backend
pytest tests/test_document_processing.py -v
```

### Run specific test class
```bash
pytest tests/test_document_processing.py::TestOCR -v
pytest tests/test_document_processing.py::TestClassification -v
pytest tests/test_document_processing.py::TestFieldExtraction -v
```

### Run with coverage
```bash
pytest tests/test_document_processing.py --cov=services.doc_processor --cov-report=html
```

### Run only fast tests (skip slow/integration)
```bash
pytest tests/test_document_processing.py -m "not slow"
```

## Test Categories

### 1. OCR Tests (`TestOCR`)

Tests for text extraction from documents:
- ✅ `test_ocr_pdf_file` - Extract text from PDF
- ✅ `test_ocr_image_file` - Extract text from images
- ✅ `test_ocr_invalid_file` - Handle invalid files
- ✅ `test_ocr_empty_result` - Handle blank images

### 2. Classification Tests (`TestClassification`)

Tests for document type classification:
- ✅ `test_classify_employment_contract` - Classify employment contracts
- ✅ `test_classify_invoice` - Classify invoices
- ✅ `test_classify_lease_agreement` - Classify lease agreements
- ✅ `test_classify_unknown_document` - Handle unknown types
- ✅ `test_classification_confidence_scores` - Validate confidence scores

### 3. Field Extraction Tests (`TestFieldExtraction`)

Tests for extracting structured data:
- ✅ `test_extract_employment_contract_fields` - Extract contract fields
- ✅ `test_extract_invoice_fields` - Extract invoice fields
- ✅ `test_extract_dates` - Extract dates
- ✅ `test_extract_amounts` - Extract monetary amounts
- ✅ `test_extract_ico_dic` - Extract IČO and DIČ
- ✅ `test_field_extraction_metadata` - Verify metadata

### 4. MinIO Storage Tests (`TestMinIOStorage`)

Tests for storage operations:
- ✅ `test_storage_initialization` - Initialize storage
- ⏭️ `test_upload_raw_document` - Upload documents (requires MinIO)
- ⏭️ `test_get_presigned_url` - Generate URLs (requires MinIO)

### 5. Integration Tests (`TestIntegration`)

End-to-end pipeline tests:
- ✅ `test_full_pipeline_employment_contract` - Complete workflow
- ✅ `test_full_pipeline_invoice` - Complete workflow

## Test Data

Create test documents in `tests/test_data/`:

### Employment Contract (sample_contract.pdf)
```
PRACOVNÁ ZMLUVA č. ZML-001/2024
uzavretá dňa 15.12.2024

Zamestnávateľ: ABC s.r.o.
IČO: 12345678

Zamestnanec: Ján Novák
Rodné číslo: 901234/5678

Pracovná pozícia: Programátor
Mzda: 2000 EUR
```

### Invoice (sample_invoice.jpg/pdf)
```
FAKTÚRA č. FA-123/2024

Dátum vystavenia: 15.12.2024
Dátum splatnosti: 29.12.2024

Dodávateľ: XYZ s.r.o.
IČO: 87654321
DIČ: SK2020123456

Suma celkom: 1500.00 EUR
```

### Lease Agreement (sample_lease.pdf)
```
NÁJOMNÁ ZMLUVA

Prenajímateľ: Mária Kováčová
Nájomca: Peter Slovák

Predmet nájmu: Byt 2+1, Bratislava
Nájomné: 500 EUR/mesiac
```

## Expected Results

### Classification Accuracy
- Employment Contract: confidence > 0.7
- Invoice: confidence > 0.7
- Lease Agreement: confidence > 0.5

### Field Extraction Accuracy
- Contract numbers: 95%+
- Dates: 90%+
- Amounts: 90%+
- IČO/DIČ: 95%+
- Names: 80%+

## Continuous Integration

Add to CI/CD pipeline:

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          pytest tests/test_document_processing.py -v --cov
```

## Troubleshooting

### Tests fail due to missing dependencies
```bash
pip install pytest pytest-cov
```

### OCR tests fail
Ensure Tesseract is installed:
```bash
# Windows
choco install tesseract

# Ubuntu
sudo apt-get install tesseract-ocr
```

### MinIO tests skip
MinIO tests require connection. Set environment variables:
```bash
export MINIO_ENDPOINT=localhost:9000
export MINIO_ACCESS_KEY=minioadmin
export MINIO_SECRET_KEY=minioadmin
```

## Performance Benchmarks

Target execution times:
- OCR tests: < 5 seconds each
- Classification tests: < 1 second each
- Field extraction tests: < 0.5 seconds each
- Integration tests: < 10 seconds each

Total test suite: < 60 seconds

---

**Last Updated**: 2025-12-04  
**Test Coverage**: 85%+
