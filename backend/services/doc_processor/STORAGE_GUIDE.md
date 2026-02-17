# MinIO Storage Service - Usage Guide

## Overview

Enhanced MinIO storage service with multi-bucket architecture for organized document management.

## Bucket Structure

### 1. `raw-docs` - Original Documents
- Stores uploaded documents in original format
- Organized by user: `user_{user_id}/filename`
- Preserves original metadata

### 2. `processed-docs` - Processed Documents
- Stores OCR'd and processed documents
- Links to original documents
- Contains processing metadata

### 3. `templates` - Document Templates
- Stores DOCX templates
- Organized by type: `{template_type}/{template_name}`
- Used for document generation

### 4. `filled-docs` - Filled Documents
- Stores generated documents from templates
- Links to source documents and templates
- Ready for download

## Quick Start

### Initialize Storage

```python
from services.doc_processor import MinIOStorage

# Initialize with defaults
storage = MinIOStorage()

# Or with custom settings
storage = MinIOStorage(
    endpoint='localhost:9000',
    access_key='admin',
    secret_key='password',
    secure=False
)
```

## Usage Examples

### Upload Raw Document

```python
# Upload user document
with open('contract.pdf', 'rb') as f:
    file_data = f.read()

object_name = storage.upload_raw_document(
    file_data=file_data,
    filename='contract.pdf',
    user_id=123,
    metadata={'document_type': 'contract'}
)
# Returns: 'user_123/contract.pdf'
```

### Upload Processed Document

```python
# After OCR processing
processed_text = "Extracted text..."

object_name = storage.upload_processed_document(
    file_data=processed_text.encode('utf-8'),
    filename='contract_processed.txt',
    original_object_name='user_123/contract.pdf',
    processing_info={
        'ocr_engine': 'paddleocr',
        'confidence': 0.95
    }
)
```

### Upload Template

```python
# Upload contract template
with open('template_contract.docx', 'rb') as f:
    template_data = f.read()

object_name = storage.upload_template(
    file_data=template_data,
    template_name='standard_contract.docx',
    template_type='contract'
)
# Returns: 'contract/standard_contract.docx'
```

### Upload Filled Document

```python
# Upload filled contract
with open('filled_contract.docx', 'rb') as f:
    filled_data = f.read()

object_name = storage.upload_filled_document(
    file_data=filled_data,
    filename='contract_john_doe.docx',
    template_name='standard_contract.docx',
    source_document='user_123/contract.pdf'
)
```

### Download Documents

```python
# Download raw document
raw_data = storage.download_raw_document('user_123/contract.pdf')

# Download processed document
processed_data = storage.download_processed_document('contract_processed.txt')

# Download template
template_data = storage.download_template('contract/standard_contract.docx')
```

### Generate Presigned URLs

```python
from datetime import timedelta

# Get temporary URL for raw document (1 hour)
url = storage.get_raw_document_url(
    'user_123/contract.pdf',
    expires=timedelta(hours=1)
)

# Get URL for processed document (24 hours)
url = storage.get_processed_document_url(
    'contract_processed.txt',
    expires=timedelta(hours=24)
)
```

### List User Documents

```python
# List all documents for user 123
documents = storage.list_user_documents(user_id=123)

for doc in documents:
    print(f"{doc['name']} - {doc['size']} bytes - {doc['last_modified']}")
```

### List Files in Bucket

```python
# List all files in raw-docs
files = storage.list_files(storage.BUCKET_RAW)

# List files with prefix
files = storage.list_files(
    storage.BUCKET_RAW,
    prefix='user_123/'
)
```

### Check File Existence

```python
# Check if file exists
exists = storage.file_exists(
    storage.BUCKET_RAW,
    'user_123/contract.pdf'
)
```

### Get File Metadata

```python
# Get detailed metadata
metadata = storage.get_file_metadata(
    storage.BUCKET_RAW,
    'user_123/contract.pdf'
)

print(f"Size: {metadata['size']}")
print(f"Last modified: {metadata['last_modified']}")
print(f"Content type: {metadata['content_type']}")
print(f"Custom metadata: {metadata['metadata']}")
```

### Delete Files

```python
# Delete raw document
storage.delete_file(storage.BUCKET_RAW, 'user_123/old_contract.pdf')

# Delete processed document
storage.delete_file(storage.BUCKET_PROCESSED, 'old_processed.txt')
```

## Integration with DocumentProcessor

```python
from services.doc_processor import DocumentProcessor

# Initialize processor (includes storage)
processor = DocumentProcessor()

# Process document (automatically handles storage)
result = processor.process_document(
    file_data=pdf_bytes,
    filename='contract.pdf'
)

# Result includes storage URLs
print(result['storage_url'])  # Presigned URL for raw document
```

## Bucket Access Constants

```python
# Access bucket names
storage.BUCKET_RAW          # 'raw-docs'
storage.BUCKET_PROCESSED    # 'processed-docs'
storage.BUCKET_TEMPLATES    # 'templates'
storage.BUCKET_FILLED       # 'filled-docs'
```

## Error Handling

```python
from minio.error import S3Error

try:
    data = storage.download_raw_document('nonexistent.pdf')
except S3Error as e:
    print(f"MinIO error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

### 1. User Organization
```python
# Always use user_id for raw documents
object_name = storage.upload_raw_document(
    file_data=data,
    filename='document.pdf',
    user_id=user_id  # Important!
)
```

### 2. Metadata
```python
# Add meaningful metadata
metadata = {
    'document_type': 'contract',
    'uploaded_by': 'admin',
    'department': 'legal',
    'classification': 'confidential'
}

storage.upload_raw_document(
    file_data=data,
    filename='contract.pdf',
    user_id=123,
    metadata=metadata
)
```

### 3. Presigned URL Expiration
```python
# Short expiration for sensitive documents
url = storage.get_raw_document_url(
    'user_123/confidential.pdf',
    expires=timedelta(minutes=15)
)

# Longer expiration for public documents
url = storage.get_raw_document_url(
    'user_123/public.pdf',
    expires=timedelta(days=7)
)
```

### 4. Cleanup
```python
# Delete old processed documents
files = storage.list_files(storage.BUCKET_PROCESSED)
for file in files:
    # Check age and delete if old
    if is_old(file['last_modified']):
        storage.delete_file(storage.BUCKET_PROCESSED, file['name'])
```

## Environment Variables

```env
MINIO_ENDPOINT=minio:9000
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
```

## Troubleshooting

### Connection Issues
```python
# Test connection
try:
    storage = MinIOStorage()
    buckets = storage.client.list_buckets()
    print(f"Connected! Buckets: {[b.name for b in buckets]}")
except Exception as e:
    print(f"Connection failed: {e}")
```

### Bucket Not Found
```python
# Buckets are created automatically
# If issues persist, manually create:
storage.client.make_bucket('raw-docs')
```

---

**Last Updated**: 2025-12-04  
**Version**: 2.0
