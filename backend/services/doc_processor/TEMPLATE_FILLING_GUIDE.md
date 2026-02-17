# Template Filling System - Usage Guide

## Overview

Comprehensive template filling system with DOCX templates, placeholder substitution, PDF generation, and MinIO storage.

## Quick Start

### Fill Template with Data

```python
from services.doc_processor import fill_template

# Prepare data
data = {
    'contract_number': 'ZML-001/2024',
    'contract_date': '15.12.2024',
    'employer': 'ABC s.r.o.',
    'employee': 'Ján Novák',
    'position': 'Programátor',
    'salary': '2000 EUR',
    'start_date': '01.01.2025'
}

# Fill template and save to MinIO
result = fill_template(
    template_name='employment_contract.docx',
    data=data,
    output_filename='contract_jan_novak.docx',
    save_to_minio=True
)

print(f"Local path: {result['local_path']}")
print(f"MinIO URL: {result['url']}")
```

### Generate Document from Data

```python
from services.doc_processor import generate_document

# Generate without template
result = generate_document(
    document_type='employment_contract',
    data=extracted_data,
    output_filename='generated_contract.docx',
    save_to_minio=True
)
```

## Template Format

### DOCX Templates with Placeholders

Templates use `{{placeholder}}` format:

```
PRACOVNÁ ZMLUVA
Číslo zmluvy: {{contract_number}}
Dátum: {{contract_date}}

Zamestnávateľ: {{employer}}
Zamestnanec: {{employee}}
Pracovná pozícia: {{position}}
Mzda: {{salary}}
Dátum nástupu: {{start_date}}
```

### Creating Templates

1. Create DOCX file in Word/LibreOffice
2. Use `{{field_name}}` for placeholders
3. Save as `.docx`
4. Upload to MinIO or save locally

## Advanced Usage

### Using TemplateFiller Class

```python
from services.doc_processor import TemplateFiller

filler = TemplateFiller()

# Fill template
result = filler.fill_and_save(
    template_name='complaint.docx',
    data={
        'complainant': 'Ján Novák',
        'date': '15.12.2024',
        'subject': 'Reklamácia produktu',
        'description': 'Produkt je poškodený...'
    },
    output_filename='complaint_jan_novak.docx',
    save_to_minio=True
)
```

### Template Management

```python
filler = TemplateFiller()

# List available templates
templates = filler.list_templates()
print(f"Available templates: {templates}")

# Upload new template
filler.upload_template(
    template_path='path/to/template.docx',
    template_name='new_template.docx',
    template_type='contract'
)
```

### PDF Conversion (Optional)

```python
# Convert DOCX to PDF (requires LibreOffice)
pdf_path = filler.convert_to_pdf(
    docx_path='contract.docx',
    pdf_path='contract.pdf'
)
```

## MinIO Integration

### Automatic Storage

```python
# Automatically saves to MinIO filled-docs bucket
result = fill_template(
    template_name='template.docx',
    data=data,
    output_filename='output.docx',
    save_to_minio=True  # Default
)

# Access via presigned URL
print(result['url'])  # Valid for 1 hour
```

### Manual Storage Control

```python
# Save locally only
result = fill_template(
    template_name='template.docx',
    data=data,
    output_filename='output.docx',
    save_to_minio=False
)

# Manual upload later
with open(result['local_path'], 'rb') as f:
    storage = MinIOStorage()
    storage.upload_filled_document(
        file_data=f.read(),
        filename='output.docx',
        template_name='template.docx'
    )
```

## Template Examples

### 1. Employment Contract

**Template:** `employment_contract.docx`

```
PRACOVNÁ ZMLUVA č. {{contract_number}}

uzavretá dňa {{contract_date}}

Zamestnávateľ:
{{employer}}
IČO: {{employer_ico}}

Zamestnanec:
{{employee}}
Rodné číslo: {{employee_id}}

Pracovná pozícia: {{position}}
Mzda: {{salary}}
Dátum nástupu: {{start_date}}
Typ zmluvy: {{contract_type}}
```

**Data:**
```python
{
    'contract_number': 'ZML-001/2024',
    'contract_date': '15.12.2024',
    'employer': 'ABC s.r.o.',
    'employer_ico': '12345678',
    'employee': 'Ján Novák',
    'employee_id': '901234/5678',
    'position': 'Programátor',
    'salary': '2000 EUR',
    'start_date': '01.01.2025',
    'contract_type': 'neurčitý čas'
}
```

### 2. Complaint Letter

**Template:** `complaint.docx`

```
SŤAŽNOSŤ

Dátum: {{date}}
Vec: {{subject}}

Sťažovateľ:
{{complainant}}
Adresa: {{address}}

Popis problému:
{{description}}

Požadované riešenie:
{{requested_solution}}

Podpis: _________________
```

### 3. Notice

**Template:** `notice.docx`

```
OZNÁMENIE

Dátum: {{date}}
Číslo: {{notice_number}}

Adresát:
{{recipient}}

Vec: {{subject}}

{{content}}

S pozdravom,
{{sender}}
```

## Integration with Document Processor

```python
from services.doc_processor import DocumentProcessor

processor = DocumentProcessor()

# Process document and fill template
result = processor.process_document(
    file_data=pdf_bytes,
    filename='contract.pdf'
)

# Extract fields
fields = result['extracted_fields']

# Fill template with extracted data
filled = fill_template(
    template_name='contract_template.docx',
    data=fields,
    output_filename='filled_contract.docx'
)
```

## Complete Workflow Example

```python
from services.doc_processor import (
    perform_ocr,
    classify_document,
    extract_document_fields,
    fill_template,
    DocumentType
)

# 1. OCR
text = perform_ocr('scanned_contract.pdf')

# 2. Classify
classification = classify_document(text)
doc_type = classification['document_type']

# 3. Extract fields
fields = extract_document_fields(text, doc_type)

# 4. Fill template
result = fill_template(
    template_name=f'{doc_type.value}_template.docx',
    data=fields,
    output_filename='processed_contract.docx',
    save_to_minio=True
)

print(f"Document URL: {result['url']}")
```

## Template Storage Locations

### Local Templates
```
backend/services/doc_processor/templates/
├── employment_contract.docx
├── complaint.docx
├── notice.docx
└── ...
```

### MinIO Templates
```
Bucket: templates
├── contract/
│   ├── employment_contract.docx
│   └── service_contract.docx
├── legal/
│   ├── complaint.docx
│   └── lawsuit.docx
└── general/
    ├── notice.docx
    └── letter.docx
```

## Error Handling

```python
try:
    result = fill_template(
        template_name='template.docx',
        data=data,
        output_filename='output.docx'
    )
except FileNotFoundError:
    print("Template not found")
except Exception as e:
    print(f"Error: {e}")
```

## Best Practices

### 1. Template Naming

```python
# Use descriptive names
'employment_contract_sk.docx'  # Good
'template1.docx'                # Bad
```

### 2. Data Validation

```python
# Validate data before filling
required_fields = ['contract_number', 'date', 'parties']

for field in required_fields:
    if field not in data:
        raise ValueError(f"Missing required field: {field}")

result = fill_template(template_name, data, output_filename)
```

### 3. Placeholder Consistency

```python
# Use consistent naming
{{contract_number}}  # Good
{{ContractNumber}}   # Avoid
{{contract-number}}  # Avoid
```

### 4. Template Versioning

```python
# Include version in template name
filler.upload_template(
    'employment_contract_v2.docx',
    template_type='contract'
)
```

## Troubleshooting

### Template Not Found

```python
# List available templates
filler = TemplateFiller()
templates = filler.list_templates()
print(f"Available: {templates}")
```

### Placeholders Not Replaced

```python
# Check placeholder format
# Correct: {{field_name}}
# Incorrect: {field_name}, [[field_name]]
```

### PDF Conversion Fails

```bash
# Install LibreOffice
# Ubuntu/Debian:
sudo apt-get install libreoffice

# Windows: Download from libreoffice.org
```

---

**Last Updated**: 2025-12-04  
**Version**: 1.0
