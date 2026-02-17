# OCR Service - Usage Examples

## Quick Start

### Simple OCR

```python
from services.doc_processor import perform_ocr

# OCR a PDF
text = perform_ocr('contract.pdf')
print(text)

# OCR an image
text = perform_ocr('scan.jpg')
print(text)
```

### OCR with Page Information

```python
# Get page-by-page results
pages = perform_ocr('document.pdf', return_pages=True)

for page in pages:
    print(f"Page {page['page_number']}:")
    print(f"  Characters: {page['char_count']}")
    print(f"  Method: {page['method']}")
    print(f"  Text: {page['text'][:100]}...")
```

### Specify Languages

```python
# Slovak and Czech
text = perform_ocr('document.pdf', languages=['slk', 'ces'])

# Russian and Ukrainian
text = perform_ocr('document.pdf', languages=['rus', 'ukr'])

# English only
text = perform_ocr('document.pdf', languages=['eng'])
```

### Choose OCR Engine

```python
# Use Tesseract (faster)
text = perform_ocr('document.pdf', engine='tesseract')

# Use PaddleOCR (better for Cyrillic)
text = perform_ocr('document.pdf', engine='paddle')

# Auto-select best engine
text = perform_ocr('document.pdf', engine='auto')
```

### Disable Preprocessing

```python
# Skip image preprocessing (faster but less accurate)
text = perform_ocr('clean_scan.jpg', preprocess=False)
```

## Batch Processing

```python
from services.doc_processor import perform_ocr_batch

# Process multiple files
files = ['doc1.pdf', 'doc2.pdf', 'scan1.jpg']
results = perform_ocr_batch(files, languages=['slk'])

for result in results:
    if result['success']:
        print(f"{result['filename']}: {len(result['result'])} chars")
    else:
        print(f"{result['filename']}: ERROR - {result['error']}")
```

## Check Available Engines

```python
from services.doc_processor import get_ocr_info

info = get_ocr_info()

print(f"Tesseract available: {info['tesseract']}")
print(f"Tesseract languages: {info['tesseract_languages']}")
print(f"PaddleOCR available: {info['paddle']}")
```

## Convenience Functions

```python
from services.doc_processor.ocr_service import ocr_pdf, ocr_image, ocr_pdf_pages

# OCR PDF (returns text)
text = ocr_pdf('document.pdf')

# OCR image (returns text)
text = ocr_image('scan.jpg')

# OCR PDF with pages (returns list)
pages = ocr_pdf_pages('document.pdf')
```

## Integration with DocumentProcessor

```python
from services.doc_processor import DocumentProcessor

processor = DocumentProcessor()

# Process document (includes OCR automatically)
result = processor.process_document(
    file_data=pdf_bytes,
    filename='contract.pdf'
)

# Text is extracted automatically
print(result['text_length'])
```

## Advanced Usage

### Custom OCR Engine Settings

```python
from services.doc_processor import OCREngine

# Initialize with custom settings
ocr = OCREngine(
    engine='paddle',
    languages=['slk', 'ces', 'rus']
)

# Use custom engine
text = ocr.extract_text('document.jpg', preprocess=True)
```

### Process Specific PDF Pages

```python
from pdf2image import convert_from_path
from services.doc_processor import perform_ocr
import tempfile

# Convert specific pages
images = convert_from_path('document.pdf', first_page=1, last_page=5)

# OCR each page
for i, image in enumerate(images):
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        image.save(tmp.name)
        text = perform_ocr(tmp.name)
        print(f"Page {i+1}: {len(text)} chars")
```

### Handle OCR Errors

```python
try:
    text = perform_ocr('document.pdf')
except FileNotFoundError:
    print("File not found")
except ValueError as e:
    print(f"Unsupported file type: {e}")
except Exception as e:
    print(f"OCR error: {e}")
```

## Performance Tips

### 1. Use Appropriate Engine

```python
# For clean, typed documents (faster)
text = perform_ocr('typed_document.pdf', engine='tesseract')

# For handwritten or low-quality scans (more accurate)
text = perform_ocr('handwritten.jpg', engine='paddle')
```

### 2. Disable Preprocessing for Clean Images

```python
# Clean scans don't need preprocessing
text = perform_ocr('clean_scan.pdf', preprocess=False)
```

### 3. Batch Processing

```python
# Process multiple files in one call
results = perform_ocr_batch(file_list, engine='tesseract')
```

### 4. Limit Languages

```python
# Fewer languages = faster processing
text = perform_ocr('document.pdf', languages=['slk'])  # Only Slovak
```

## Output Formats

### Text Only

```python
text = perform_ocr('document.pdf')
# Returns: "Full text from all pages..."
```

### Page-by-Page

```python
pages = perform_ocr('document.pdf', return_pages=True)
# Returns: [
#   {
#     'page_number': 1,
#     'text': 'Page 1 text...',
#     'char_count': 1234,
#     'method': 'ocr'
#   },
#   ...
# ]
```

### Batch Results

```python
results = perform_ocr_batch(['doc1.pdf', 'doc2.pdf'])
# Returns: [
#   {
#     'filename': 'doc1.pdf',
#     'filepath': '/path/to/doc1.pdf',
#     'result': 'Text...',
#     'success': True
#   },
#   ...
# ]
```

## Supported File Types

- **PDF**: `.pdf`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.tiff`, `.tif`, `.bmp`

## Supported Languages

### Tesseract
- English (`eng`)
- Slovak (`slk`)
- Czech (`ces`)
- Polish (`pol`)
- Russian (`rus`)
- Ukrainian (`ukr`)

### PaddleOCR
- English (`en`)
- Latin script (`latin`) - for Slovak, Czech, Polish
- Cyrillic script (`cyrillic`) - for Russian, Ukrainian

## Troubleshooting

### "Tesseract not found"

```bash
# Check if Tesseract is installed
docker exec codex-backend-1 tesseract --version

# If not, rebuild Docker image
docker compose build --no-cache backend
```

### "PaddleOCR model download failed"

```python
# Manually download models
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')
```

### "Low OCR accuracy"

```python
# Enable preprocessing
text = perform_ocr('document.pdf', preprocess=True)

# Try different engine
text = perform_ocr('document.pdf', engine='paddle')

# Increase DPI for PDF conversion
from pdf2image import convert_from_path
images = convert_from_path('document.pdf', dpi=600)  # Higher DPI
```

---

**Last Updated**: 2025-12-04  
**Version**: 1.0
