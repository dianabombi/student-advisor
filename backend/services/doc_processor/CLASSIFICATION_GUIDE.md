# Document Classification Model - Usage Guide

## Overview

Hybrid classification model combining rule-based keyword matching with optional transformer support.

## Quick Start

### Basic Classification

```python
from services.doc_processor.classification_model import classify_document

# Classify document
text = """
Pracovná zmluva
uzavretá dňa 15.12.2024
medzi zamestnávateľom ABC s.r.o.
a zamestnancom Ján Novák
"""

result = classify_document(text)

print(f"Type: {result['document_type'].value}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Method: {result['method']}")
```

### With All Scores

```python
result = classify_document(text, return_all_scores=True)

print(f"Best match: {result['document_type'].value}")
print(f"Confidence: {result['confidence']:.2%}")

print("\nAll scores:")
for doc_type, score in result['all_scores'].items():
    print(f"  {doc_type}: {score:.2%}")
```

## Advanced Usage

### Using the Model Class

```python
from services.doc_processor.classification_model import DocumentClassificationModel

# Initialize model
classifier = DocumentClassificationModel()

# Classify
result = classifier.classify_document(text)
```

### With Context

```python
# Use filename and metadata for better accuracy
result = classifier.classify_with_context(
    text=text,
    filename="employment_contract_2024.pdf",
    metadata={'document_type': 'employment_contract'}
)

# Confidence is boosted if filename/metadata matches
print(f"Confidence: {result['confidence']:.2%}")
```

### Batch Classification

```python
texts = [
    "Kúpna zmluva...",
    "Faktúra č. 123...",
    "Nájomná zmluva..."
]

results = classifier.batch_classify(texts)

for i, result in enumerate(results):
    print(f"Document {i+1}: {result['document_type'].value} ({result['confidence']:.2%})")
```

### Get Explanation

```python
# Classify document
result = classifier.classify_document(text)

# Get explanation
explanation = classifier.get_classification_explanation(text, result)

print(f"Matched keywords:")
for kw in explanation['matched_keywords']:
    print(f"  - {kw['keyword']}: {kw['count']} times")

print(f"\nTotal matches: {explanation['total_matches']}")
print(f"Explanation: {explanation['explanation']}")
```

## Supported Document Types

The classifier can identify:

- **Employment Contract** - Pracovná zmluva
- **Purchase Agreement** - Kúpna zmluva
- **Lease Agreement** - Nájomná zmluva
- **Service Contract** - Zmluva o poskytovaní služieb
- **Work Contract** - Zmluva o dielo
- **Invoice** - Faktúra
- **Power of Attorney** - Plná moc
- **Court Decision** - Súdne rozhodnutie
- **Lawsuit** - Žaloba
- **Act** - Protokol
- **Letter** - List
- **Application** - Žiadosť
- **Complaint** - Sťažnosť
- **Certificate** - Osvedčenie

## Classification Methods

### Rule-Based (Default)

Uses keyword matching with weighted scoring:

```python
classifier = DocumentClassificationModel(use_transformers=False)
result = classifier.classify_document(text)
# method: 'rule_based'
```

**Advantages:**
- Fast (milliseconds)
- No external dependencies
- Explainable results
- Works offline

**Disadvantages:**
- Limited to predefined keywords
- May miss context
- Lower accuracy for ambiguous documents

### Transformer-Based (Optional)

Uses BERT multilingual model:

```python
classifier = DocumentClassificationModel(use_transformers=True)
result = classifier.classify_document(text)
# method: 'transformer' (if available)
```

**Advantages:**
- Higher accuracy
- Understands context
- Better for ambiguous cases

**Disadvantages:**
- Slower (seconds)
- Requires transformers library
- Needs more memory
- Requires fine-tuning for best results

## Confidence Scores

Confidence is calculated based on:

1. **Keyword matches** - More matches = higher confidence
2. **Match strength** - Unique keywords weighted higher
3. **Score gap** - Large gap between top 2 = higher confidence
4. **Context boost** - Filename/metadata match = +20-30%

**Confidence Levels:**
- `0.8 - 1.0` - High confidence, very likely correct
- `0.5 - 0.8` - Medium confidence, probably correct
- `0.3 - 0.5` - Low confidence, uncertain
- `0.0 - 0.3` - Very low confidence, likely incorrect

## Examples

### Example 1: Employment Contract

```python
text = """
PRACOVNÁ ZMLUVA
uzavretá podľa § 42 a nasl. Zákonníka práce

Zamestnávateľ: ABC s.r.o.
Zamestnanec: Ján Novák
Pracovná pozícia: Programátor
Mzda: 2000 EUR
"""

result = classify_document(text)
# document_type: EMPLOYMENT_CONTRACT
# confidence: ~0.85
```

### Example 2: Invoice

```python
text = """
FAKTÚRA č. FA-2024-001
Dátum vystavenia: 01.12.2024
Dátum splatnosti: 15.12.2024

Dodávateľ: XYZ s.r.o.
IČO: 12345678
DIČ: 1234567890

Odberateľ: ABC a.s.
Suma k úhrade: 1200 EUR
DPH 20%: 240 EUR
"""

result = classify_document(text)
# document_type: INVOICE
# confidence: ~0.92
```

### Example 3: Ambiguous Document

```python
text = """
Vážený pán,

týmto Vám oznamujem...
"""

result = classify_document(text, return_all_scores=True)
# document_type: LETTER
# confidence: ~0.45 (low - could be letter or notice)

# Check alternatives
for doc_type, score in sorted(result['all_scores'].items(), key=lambda x: x[1], reverse=True)[:3]:
    print(f"{doc_type}: {score:.2%}")
# letter: 45%
# notice: 38%
# application: 22%
```

## Integration with DocumentProcessor

```python
from services.doc_processor import DocumentProcessor
from services.doc_processor.classification_model import DocumentClassificationModel

class SmartDocumentProcessor(DocumentProcessor):
    def __init__(self):
        super().__init__()
        self.classifier = DocumentClassificationModel()
    
    def process_document(self, file_data, filename):
        # Extract text
        text = self._extract_text(file_data, filename)
        
        # Classify with context
        classification = self.classifier.classify_with_context(
            text=text,
            filename=filename
        )
        
        # Get explanation
        explanation = self.classifier.get_classification_explanation(
            text, classification
        )
        
        return {
            'text': text,
            'classification': classification,
            'explanation': explanation
        }
```

## Custom Keywords

To add custom keywords for better accuracy:

```python
from services.doc_processor.classification_model import DocumentClassificationModel
from services.doc_processor.document_types import DocumentType

classifier = DocumentClassificationModel()

# Add custom keywords
classifier.CLASSIFICATION_RULES[DocumentType.EMPLOYMENT_CONTRACT]['keywords'].extend([
    'pracovný pomer',
    'skúšobná doba',
    'výpovedná lehota'
])

# Classify with custom keywords
result = classifier.classify_document(text)
```

## Performance Tips

### 1. Batch Processing

```python
# Process multiple documents at once
results = classifier.batch_classify(texts)
```

### 2. Cache Results

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_classify(text_hash):
    return classifier.classify_document(text)

# Use hash for caching
import hashlib
text_hash = hashlib.md5(text.encode()).hexdigest()
result = cached_classify(text_hash)
```

### 3. Early Exit

```python
result = classifier.classify_document(text)

if result['confidence'] > 0.9:
    # High confidence, no need for additional validation
    return result
else:
    # Low confidence, may need manual review
    return result
```

## Troubleshooting

### Low Confidence Scores

```python
# Get explanation to see what matched
explanation = classifier.get_classification_explanation(text, result)

if len(explanation['matched_keywords']) < 3:
    print("Too few keyword matches - document may be unclear")
    print("Matched:", explanation['matched_keywords'])
```

### Wrong Classification

```python
# Check all scores to see alternatives
result = classifier.classify_document(text, return_all_scores=True)

sorted_scores = sorted(
    result['all_scores'].items(),
    key=lambda x: x[1],
    reverse=True
)

print("Top 3 matches:")
for doc_type, score in sorted_scores[:3]:
    print(f"  {doc_type}: {score:.2%}")
```

### Improve Accuracy

1. **Add more keywords** for your specific use case
2. **Use context** (filename, metadata)
3. **Fine-tune transformer** model on your documents
4. **Combine with field extraction** for validation

---

**Last Updated**: 2025-12-04  
**Version**: 1.0
