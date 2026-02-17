# OCR Optimization - Usage Guide

## Overview

Advanced OCR optimization with automatic image preprocessing and quality validation.

## Quick Start

### Basic Usage

```python
from services.doc_processor import OCROptimizer, perform_ocr

# Initialize optimizer
optimizer = OCROptimizer()

# Preprocess image
optimized_path = optimizer.preprocess_image('scan.jpg')

# Perform OCR on optimized image
text = perform_ocr(optimized_path)
```

### Automatic Optimization with Validation

```python
from services.doc_processor import OCROptimizer, perform_ocr

optimizer = OCROptimizer()

# Optimize and validate with automatic retry
result = optimizer.optimize_and_validate(
    image_path='scan.jpg',
    ocr_function=perform_ocr,
    max_retries=3
)

print(f"Text: {result['text']}")
print(f"Confidence: {result['validation']['confidence']:.2%}")
print(f"Attempts: {result['attempts']}")
print(f"Method: {result['method']}")
```

## Image Preprocessing

### Full Preprocessing

```python
optimizer = OCROptimizer()

optimized = optimizer.preprocess_image(
    'scan.jpg',
    auto_rotate=True,      # Auto-detect and fix rotation
    enhance_contrast=True,  # Enhance contrast with CLAHE
    denoise=True,          # Remove noise
    binarize=True,         # Convert to black/white
    deskew=True            # Fix skewed text
)
```

### Selective Preprocessing

```python
# Only binarization and contrast
optimized = optimizer.preprocess_image(
    'scan.jpg',
    auto_rotate=False,
    enhance_contrast=True,
    denoise=False,
    binarize=True,
    deskew=False
)
```

## OCR Validation

### Validate OCR Result

```python
optimizer = OCROptimizer()

# Perform OCR
text = perform_ocr('document.pdf')

# Validate result
validation = optimizer.validate_ocr_result(text)

if validation['is_valid']:
    print(f"✓ Valid OCR (confidence: {validation['confidence']:.2%})")
else:
    print(f"✗ Invalid OCR")
    print(f"Issues: {', '.join(validation['issues'])}")
    
    if validation['needs_retry']:
        print("Recommendation: Retry with preprocessing")
```

### Validation Metrics

```python
validation = optimizer.validate_ocr_result(text)

print(f"Characters: {validation['char_count']}")
print(f"Words: {validation['word_count']}")
print(f"Lines: {validation['line_count']}")
print(f"Alphanumeric ratio: {validation['alphanumeric_ratio']:.2%}")
print(f"Special char ratio: {validation['special_char_ratio']:.2%}")
print(f"Confidence: {validation['confidence']:.2%}")
```

## Automatic Retry Logic

### With Default Settings

```python
optimizer = OCROptimizer()

result = optimizer.optimize_and_validate(
    image_path='poor_quality_scan.jpg',
    ocr_function=perform_ocr
)

# Automatically tries:
# 1. Original image
# 2. Basic preprocessing (if needed)
# 3. Full preprocessing (if needed)

print(f"Best result from {result['attempts']} attempts")
print(f"Method used: {result['method']}")
```

### Custom Retry Strategy

```python
# Only 2 attempts
result = optimizer.optimize_and_validate(
    image_path='scan.jpg',
    ocr_function=perform_ocr,
    max_retries=2
)

# View all attempts
for attempt in result.get('all_attempts', []):
    print(f"Attempt {attempt['attempt']}: {attempt['method']}")
    print(f"  Confidence: {attempt['validation']['confidence']:.2%}")
```

## Advanced Preprocessing

### Auto-Rotation

```python
optimizer = OCROptimizer()

# Detects and corrects rotation automatically
rotated = optimizer._auto_rotate(image_array)
```

### Deskewing

```python
# Fix skewed text
deskewed = optimizer._deskew(image_array)
```

### Contrast Enhancement

```python
# CLAHE (Contrast Limited Adaptive Histogram Equalization)
enhanced = optimizer._enhance_contrast(image_array)
```

### Binarization

```python
# Otsu's method for optimal threshold
binary = optimizer._binarize(image_array)
```

### Denoising

```python
# Non-local means denoising
clean = optimizer._denoise(image_array)
```

## Custom Validation Thresholds

```python
optimizer = OCROptimizer()

# Set custom thresholds
optimizer.min_text_length = 100  # Minimum 100 characters
optimizer.min_confidence = 0.7   # Minimum 70% confidence

validation = optimizer.validate_ocr_result(text)
```

## Integration with DocumentProcessor

```python
from services.doc_processor import DocumentProcessor, OCROptimizer

class OptimizedDocumentProcessor(DocumentProcessor):
    def __init__(self):
        super().__init__()
        self.optimizer = OCROptimizer()
    
    def _extract_text(self, file_data, filename):
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            tmp.write(file_data)
            tmp_path = tmp.name
        
        try:
            # Use optimized OCR
            result = self.optimizer.optimize_and_validate(
                image_path=tmp_path,
                ocr_function=lambda p: self.ocr.extract_text(p)
            )
            
            return result['text']
        finally:
            os.unlink(tmp_path)
```

## Performance Tips

### 1. Skip Preprocessing for Clean Images

```python
# For high-quality scans
optimized = optimizer.preprocess_image(
    'clean_scan.jpg',
    auto_rotate=False,
    denoise=False,
    deskew=False
)
```

### 2. Use Validation to Decide

```python
# Try without preprocessing first
text = perform_ocr('scan.jpg')
validation = optimizer.validate_ocr_result(text)

if not validation['is_valid']:
    # Only preprocess if needed
    optimized = optimizer.preprocess_image('scan.jpg')
    text = perform_ocr(optimized)
```

### 3. Batch Processing

```python
from concurrent.futures import ThreadPoolExecutor

def process_image(image_path):
    return optimizer.optimize_and_validate(
        image_path=image_path,
        ocr_function=perform_ocr
    )

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(process_image, image_paths)
```

## Troubleshooting

### Low Confidence After All Attempts

```python
result = optimizer.optimize_and_validate('scan.jpg', perform_ocr)

if result['validation']['confidence'] < 0.5:
    print("Possible issues:")
    print("- Image quality too poor")
    print("- Wrong language selected")
    print("- Handwritten text (use PaddleOCR)")
    print("- Non-text content")
```

### Excessive Rotation

```python
# Disable auto-rotation if it's causing issues
optimized = optimizer.preprocess_image(
    'scan.jpg',
    auto_rotate=False  # Disable
)
```

### Over-processing

```python
# Use minimal preprocessing
optimized = optimizer.preprocess_image(
    'scan.jpg',
    auto_rotate=False,
    enhance_contrast=False,
    denoise=False,
    binarize=True,  # Only binarize
    deskew=False
)
```

## Validation Criteria

### What Makes OCR Valid?

1. **Minimum text length**: At least 50 characters
2. **Alphanumeric ratio**: At least 50% alphanumeric characters
3. **Special character ratio**: Less than 30% special characters

### Confidence Calculation

```python
confidence = min(
    alphanumeric_ratio,
    1.0 - special_char_ratio,
    min(char_count / min_text_length, 1.0)
)
```

## Examples

### Example 1: Poor Quality Scan

```python
optimizer = OCROptimizer()

result = optimizer.optimize_and_validate(
    'poor_scan.jpg',
    perform_ocr,
    max_retries=3
)

# Output:
# Attempt 1: Original - Failed (confidence: 0.25)
# Attempt 2: Basic preprocessing - Failed (confidence: 0.45)
# Attempt 3: Full preprocessing - Success (confidence: 0.82)
```

### Example 2: Rotated Document

```python
# Auto-rotation will fix it
optimized = optimizer.preprocess_image(
    'rotated.jpg',
    auto_rotate=True
)

text = perform_ocr(optimized)
```

### Example 3: Low Contrast

```python
# Enhance contrast
optimized = optimizer.preprocess_image(
    'low_contrast.jpg',
    enhance_contrast=True,
    binarize=True
)

text = perform_ocr(optimized)
```

---

**Last Updated**: 2025-12-04  
**Version**: 1.0
