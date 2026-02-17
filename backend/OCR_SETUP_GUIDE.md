# OCR and Classification Setup Guide

## System Dependencies

Before building the Docker container, ensure these system packages are installed:

### For Tesseract OCR

```dockerfile
# Add to Dockerfile
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-slk \
    tesseract-ocr-ces \
    tesseract-ocr-pol \
    tesseract-ocr-rus \
    tesseract-ocr-ukr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*
```

### For PaddleOCR

PaddleOCR works out of the box with pip installation, no additional system dependencies needed.

## Installation

### 1. Update requirements.txt

Already done! The file includes:
- `pytesseract` - Tesseract OCR wrapper
- `paddleocr` - PaddleOCR (better Cyrillic support)
- `opencv-python` - Image preprocessing
- `pdfplumber` - Advanced PDF extraction
- `transformers` - ML-based classification
- `scikit-learn` - Traditional ML

### 2. Rebuild Docker Container

```bash
docker compose build --no-cache backend
docker compose up -d
```

## Usage Examples

### Tesseract OCR

```python
import pytesseract
from PIL import Image

# Simple OCR
image = Image.open('document.jpg')
text = pytesseract.image_to_string(image, lang='slk+ces+rus')
print(text)

# With configuration
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(image, lang='slk', config=custom_config)
```

### PaddleOCR (Recommended for Cyrillic)

```python
from paddleocr import PaddleOCR

# Initialize
ocr = PaddleOCR(use_angle_cls=True, lang='cyrillic')

# Perform OCR
result = ocr.ocr('document.jpg', cls=True)

# Extract text
text = '\n'.join([line[1][0] for line in result[0]])
print(text)
```

### Image Preprocessing with OpenCV

```python
import cv2
import numpy as np

# Load image
img = cv2.imread('document.jpg')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Denoise
denoised = cv2.fastNlMeansDenoising(gray)

# Threshold
_, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Save preprocessed image
cv2.imwrite('preprocessed.jpg', thresh)
```

### PDF Text Extraction with pdfplumber

```python
import pdfplumber

with pdfplumber.open('document.pdf') as pdf:
    text = ''
    for page in pdf.pages:
        text += page.extract_text()
    print(text)
```

### Document Classification with Transformers

```python
from transformers import pipeline

# Load classifier
classifier = pipeline('text-classification', 
                     model='bert-base-multilingual-cased')

# Classify document
text = "Kúpna zmluva uzavretá dňa..."
result = classifier(text)
print(result)
```

### Traditional ML Classification with sklearn

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Train classifier
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(training_texts)
clf = MultinomialNB()
clf.fit(X_train, training_labels)

# Predict
X_test = vectorizer.transform([new_text])
prediction = clf.predict(X_test)
```

## Language Support

### Tesseract Languages

- `slk` - Slovak
- `ces` - Czech
- `pol` - Polish
- `rus` - Russian
- `ukr` - Ukrainian
- `eng` - English

### PaddleOCR Languages

- `cyrillic` - Cyrillic script (Russian, Ukrainian, etc.)
- `latin` - Latin script (Slovak, Czech, Polish, etc.)
- `en` - English

## Performance Optimization

### 1. Image Preprocessing

```python
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray)
    _, thresh = cv2.threshold(denoised, 0, 255, 
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh
```

### 2. Batch Processing

```python
from concurrent.futures import ThreadPoolExecutor

def process_documents(file_paths):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(extract_text, file_paths)
    return list(results)
```

### 3. Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def classify_document(text_hash):
    # Classification logic
    pass
```

## Troubleshooting

### Tesseract not found

```bash
# Check installation
tesseract --version

# If not found, install:
apt-get install tesseract-ocr
```

### PaddleOCR model download issues

```python
# Manually specify model directory
ocr = PaddleOCR(use_angle_cls=True, 
                lang='cyrillic',
                det_model_dir='./models/det',
                rec_model_dir='./models/rec')
```

### Out of memory errors

```python
# Reduce image size
img = cv2.resize(img, None, fx=0.5, fy=0.5)

# Or use lower resolution
ocr = PaddleOCR(use_gpu=False, show_log=False)
```

## Docker Configuration

### Dockerfile additions

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-slk \
    tesseract-ocr-rus \
    tesseract-ocr-ukr \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download PaddleOCR models (optional)
RUN python -c "from paddleocr import PaddleOCR; PaddleOCR(lang='cyrillic')"
```

## Integration with CODEX

The OCR and classification libraries are now integrated with:

1. **Document Upload** - Automatic OCR for images
2. **Document Classifier** - ML-based classification
3. **Key Field Extraction** - Enhanced with OCR

See `document_classifier.py` and `document_upload.py` for usage.

---

**Last Updated**: 2025-12-04
