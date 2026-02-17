# Document Classification Module - Usage Guide

## Overview

The Document Classification module automatically analyzes legal documents to:
- Classify document type (contract, application, decision, etc.)
- Detect practice area (civil, criminal, commercial, etc.)
- Extract key fields (dates, amounts, parties)
- Use AI for enhanced extraction

## Quick Start

### Basic Usage

```python
from services.document_classifier import analyze_document

# Analyze a document
text = "Kúpna zmluva uzavretá dňa 15.12.2024..."
result = analyze_document(text)

print(result['classification']['document_type'])  # 'kupna_zmluva'
print(result['classification']['practice_area'])   # 'civil'
print(result['extracted_fields']['dates'])         # [{'date': '15.12.2024', ...}]
```

### With API Key (AI-Enhanced)

```python
result = analyze_document(text, api_key="sk-...")

# AI-extracted fields
print(result['ai_extracted'])
```

## Classification Results

### Document Types

Supported types:
- `zmluva` - General contract
- `kupna_zmluva` - Purchase agreement
- `najomna_zmluva` - Lease agreement
- `zmluva_o_dielo` - Contract for work
- `ziadost` - Application/Request
- `rozhodnutie` - Decision/Verdict
- `navrh` - Proposal/Draft
- `plna_moc` - Power of Attorney
- `faktura` - Invoice
- `other` - Unclassified

### Practice Areas

- `civil` - Civil law
- `criminal` - Criminal law
- `commercial` - Commercial law
- `labor` - Labor law
- `administrative` - Administrative law

## Extracted Fields

### Dates

```python
{
    'date': '15.12.2024',
    'context': '...uzavretá dňa 15.12.2024 medzi...',
    'position': 123
}
```

### Amounts

```python
{
    'amount': '10 000 EUR',
    'context': '...kúpna cena vo výške 10 000 EUR...',
    'position': 456
}
```

### Parties

```python
['Ján Novák', 'Mária Kováčová']
```

## API Endpoint

### Upload with Classification

```bash
curl -X POST http://localhost:8001/api/documents/upload-with-classification \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@contract.pdf"
```

**Response:**

```json
{
  "document_id": 123,
  "filename": "contract.pdf",
  "classification": {
    "document_type": "kupna_zmluva",
    "type_confidence": 0.8,
    "practice_area": "civil",
    "area_confidence": 0.7
  },
  "extracted_fields": {
    "dates": [
      {"date": "15.12.2024", "context": "..."}
    ],
    "amounts": [
      {"amount": "10 000 EUR", "context": "..."}
    ],
    "parties": ["Ján Novák", "Mária Kováčová"]
  },
  "ai_extracted": {
    "title": "Kúpna zmluva",
    "subject": "Predaj nehnuteľnosti",
    "validity": "od 15.12.2024"
  }
}
```

## Advanced Usage

### Custom Classifier

```python
from services.document_classifier import DocumentClassifier

classifier = DocumentClassifier(api_key="sk-...")

# Classify only
doc_type, confidence = classifier.classify_document_type(text)

# Detect practice area
area, confidence = classifier.detect_practice_area(text)

# Extract specific fields
dates = classifier.extract_dates(text)
amounts = classifier.extract_amounts(text)
parties = classifier.extract_parties(text)

# AI extraction
ai_fields = classifier.extract_key_fields_ai(text, doc_type)
```

## Configuration

### Environment Variables

```env
OPENAI_API_KEY=sk-your-key-here  # For AI-enhanced extraction
```

### Customizing Patterns

Edit `document_classifier.py`:

```python
DOCUMENT_TYPES = {
    'custom_type': ['keyword1', 'keyword2'],
    # ...
}

PRACTICE_AREAS = {
    'custom_area': ['keyword1', 'keyword2'],
    # ...
}
```

## Performance

### Rule-Based Classification
- Speed: ~10ms per document
- Accuracy: ~70-80%
- No API costs

### AI-Enhanced Extraction
- Speed: ~2-3 seconds per document
- Accuracy: ~90-95%
- Cost: ~$0.001 per document (GPT-3.5-turbo)

## Error Handling

```python
try:
    result = analyze_document(text)
except Exception as e:
    print(f"Classification error: {e}")
    # Fallback to manual classification
```

## Integration with Upload

The classification module is automatically used when uploading documents via:

```
POST /api/documents/upload-with-classification
```

All uploaded documents are:
1. Text extracted (OCR if needed)
2. Classified automatically
3. Key fields extracted
4. Stored with metadata

## Logging

```python
import logging
logging.basicConfig(level=logging.INFO)

# Logs include:
# - Document analysis start/end
# - Classification results
# - Extraction results
# - Errors and warnings
```

## Testing

```python
# Test classification
text = """
Kúpna zmluva
uzavretá dňa 15.12.2024
medzi Ján Novák a Mária Kováčová
kúpna cena: 100 000 EUR
"""

result = analyze_document(text)

assert result['classification']['document_type'] == 'kupna_zmluva'
assert result['classification']['practice_area'] == 'civil'
assert len(result['extracted_fields']['dates']) > 0
assert len(result['extracted_fields']['amounts']) > 0
```

## Troubleshooting

### Low Confidence Scores

- Add more keywords to patterns
- Use AI-enhanced extraction
- Provide more context in document

### Missing Fields

- Check regex patterns
- Verify text extraction quality
- Use AI extraction for complex documents

### Slow Performance

- Disable AI extraction for bulk processing
- Use rule-based classification only
- Cache results for similar documents

## Future Enhancements

- [ ] Support for more document types
- [ ] Multi-language support
- [ ] Custom field extraction templates
- [ ] Batch processing
- [ ] Machine learning model training

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-04
