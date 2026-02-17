# Document Processing API

Complete API documentation for document upload, processing, and template management.

## Table of Contents

- [Authentication](#authentication)
- [Document Processing](#document-processing)
- [Template Management](#template-management)
- [Request Examples](#request-examples)
- [Response Formats](#response-formats)
- [Error Handling](#error-handling)

---

## Authentication

All endpoints require JWT authentication.

### Get Token

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Usage:**
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Document Processing

### Upload Document

Upload document for OCR and processing.

```http
POST /api/documents/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: (binary)
auto_process: true
```

**Supported Formats:**
- PDF (`.pdf`)
- Images (`.jpg`, `.jpeg`, `.png`, `.tiff`, `.tif`)

**Parameters:**
- `file` (required): Document file
- `auto_process` (optional): Start processing immediately (default: true)

**Response (200 OK):**
```json
{
  "success": true,
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Document 'contract.pdf' uploaded successfully",
  "status": "processing"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8001/api/documents/upload" \
  -H "Authorization: Bearer {token}" \
  -F "file=@contract.pdf" \
  -F "auto_process=true"
```

**Python Example:**
```python
import requests

url = "http://localhost:8001/api/documents/upload"
headers = {"Authorization": f"Bearer {token}"}
files = {"file": open("contract.pdf", "rb")}
data = {"auto_process": "true"}

response = requests.post(url, headers=headers, files=files, data=data)
print(response.json())
```

---

### Get Processing Status

Check document processing status.

```http
GET /api/documents/{document_id}/status
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "filename": "contract.pdf",
  "uploaded_at": "2024-12-04T20:00:00Z",
  "processed_at": null,
  "progress": 50
}
```

**Status Values:**
- `pending` - Waiting to start
- `processing` - Currently processing
- `completed` - Finished successfully
- `failed` - Processing failed

**Progress:**
- `0-30%` - OCR extraction
- `30-50%` - Document classification
- `50-70%` - Field extraction
- `70-90%` - Saving results
- `90-100%` - Generating summary

**cURL Example:**
```bash
curl -X GET "http://localhost:8001/api/documents/{document_id}/status" \
  -H "Authorization: Bearer {token}"
```

---

### Get Processing Result

Get complete processing result.

```http
GET /api/documents/{document_id}
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "document_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "contract.pdf",
  "status": "completed",
  "document_type": "employment_contract",
  "confidence": 0.85,
  "extracted_fields": {
    "contract_number": "ZML-001/2024",
    "contract_date": "15.12.2024",
    "employer": "ABC s.r.o.",
    "employee": "Ján Novák",
    "position": "Programátor",
    "salary": "2000 EUR",
    "_metadata": {
      "document_type": "employment_contract",
      "extracted_at": "2024-12-04T20:05:00Z",
      "field_count": 6
    }
  },
  "raw_document_url": "http://minio:9000/raw-docs/user_1/contract.pdf?...",
  "processed_document_url": "http://minio:9000/processed-docs/contract_processed.txt?...",
  "filled_template_url": null,
  "summary": "Pracovná zmluva typu employment_contract.\nStrany: ABC s.r.o., Ján Novák\nDátum: 15.12.2024"
}
```

**Document Types:**
- `employment_contract` - Pracovná zmluva
- `invoice` - Faktúra
- `lease_agreement` - Nájomná zmluva
- `service_contract` - Zmluva o dielo
- `purchase_agreement` - Kúpna zmluva
- And 9 more types...

---

### List Documents

List user's documents with optional filtering.

```http
GET /api/documents/?status={status}&limit={limit}
Authorization: Bearer {token}
```

**Query Parameters:**
- `status` (optional): Filter by status (pending, processing, completed, failed)
- `limit` (optional): Max results (default: 50, max: 100)

**Response (200 OK):**
```json
[
  {
    "document_id": "550e8400-e29b-41d4-a716-446655440000",
    "status": "completed",
    "filename": "contract.pdf",
    "uploaded_at": "2024-12-04T20:00:00Z",
    "processed_at": "2024-12-04T20:05:00Z",
    "progress": 100
  },
  {
    "document_id": "660e8400-e29b-41d4-a716-446655440001",
    "status": "processing",
    "filename": "invoice.pdf",
    "uploaded_at": "2024-12-04T20:10:00Z",
    "processed_at": null,
    "progress": 45
  }
]
```

**cURL Examples:**
```bash
# All documents
curl -X GET "http://localhost:8001/api/documents/" \
  -H "Authorization: Bearer {token}"

# Only completed
curl -X GET "http://localhost:8001/api/documents/?status=completed" \
  -H "Authorization: Bearer {token}"

# Limit 10
curl -X GET "http://localhost:8001/api/documents/?limit=10" \
  -H "Authorization: Bearer {token}"
```

---

### Delete Document

Delete document and all associated data.

```http
DELETE /api/documents/{document_id}
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Document deleted successfully"
}
```

**Deletes:**
- Database record
- Raw document from MinIO
- Processed text from MinIO
- Filled templates (if any)

---

## Template Management

**Note:** Requires admin role.

### List Templates

List all available templates.

```http
GET /api/templates/
Authorization: Bearer {admin_token}
```

**Response (200 OK):**
```json
{
  "templates": [
    {
      "name": "employment_contract_template.docx",
      "type": "contract",
      "size": 45678,
      "last_modified": "2024-12-04T15:00:00Z",
      "url": "http://minio:9000/templates/employment_contract_template.docx?..."
    }
  ],
  "total": 1
}
```

---

### Upload Template

Upload new DOCX template.

```http
POST /api/templates/upload
Authorization: Bearer {admin_token}
Content-Type: multipart/form-data

file: (binary)
template_type: contract
```

**Template Types:**
- `contract` - Zmluvy
- `legal` - Právne dokumenty
- `administrative` - Administratívne
- `correspondence` - Korešpondencia
- `general` - Všeobecné

**Template Format:**

Use `{{placeholder}}` syntax in DOCX:
```
{{contract_number}}
{{employer}}
{{employee}}
{{date}}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Template uploaded successfully",
  "template_name": "employment_contract_template.docx"
}
```

---

### Get Template Details

Get template metadata and download URL.

```http
GET /api/templates/{template_name}
Authorization: Bearer {admin_token}
```

**Response (200 OK):**
```json
{
  "name": "employment_contract_template.docx",
  "type": "contract",
  "size": 45678,
  "last_modified": "2024-12-04T15:00:00Z",
  "download_url": "http://minio:9000/templates/employment_contract_template.docx?..."
}
```

---

### Delete Template

Delete template.

```http
DELETE /api/templates/{template_name}
Authorization: Bearer {admin_token}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Template deleted successfully"
}
```

---

## Complete Workflow Example

### JavaScript/TypeScript

```typescript
const API_URL = 'http://localhost:8001';
let token: string;

// 1. Login
async function login() {
  const response = await fetch(`${API_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'user@example.com',
      password: 'password123'
    })
  });
  const data = await response.json();
  token = data.access_token;
}

// 2. Upload document
async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('auto_process', 'true');

  const response = await fetch(`${API_URL}/api/documents/upload`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  });
  
  const data = await response.json();
  return data.document_id;
}

// 3. Poll for status
async function waitForProcessing(documentId: string) {
  while (true) {
    const response = await fetch(
      `${API_URL}/api/documents/${documentId}/status`,
      { headers: { 'Authorization': `Bearer ${token}` } }
    );
    
    const status = await response.json();
    
    console.log(`Progress: ${status.progress}%`);
    
    if (status.status === 'completed') {
      break;
    } else if (status.status === 'failed') {
      throw new Error('Processing failed');
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

// 4. Get result
async function getResult(documentId: string) {
  const response = await fetch(
    `${API_URL}/api/documents/${documentId}`,
    { headers: { 'Authorization': `Bearer ${token}` } }
  );
  
  return await response.json();
}

// Full workflow
async function processDocument(file: File) {
  await login();
  const documentId = await uploadDocument(file);
  await waitForProcessing(documentId);
  const result = await getResult(documentId);
  
  console.log('Document Type:', result.document_type);
  console.log('Confidence:', result.confidence);
  console.log('Fields:', result.extracted_fields);
}
```

---

## Error Handling

### Error Response Format

All errors follow this structure:

```json
{
  "detail": "Error message here"
}
```

### HTTP Status Codes

**Success:**
- `200 OK` - Request successful
- `201 Created` - Resource created

**Client Errors:**
- `400 Bad Request` - Invalid input (wrong file type, missing fields)
- `401 Unauthorized` - Missing or invalid authentication
- `403 Forbidden` - Insufficient permissions (not admin)
- `404 Not Found` - Resource not found

**Server Errors:**
- `500 Internal Server Error` - Server-side issue

### Common Errors

**Invalid File Type:**
```json
{
  "detail": "Unsupported file type. Allowed: .pdf, .jpg, .jpeg, .png, .tiff, .tif"
}
```

**Unauthorized:**
```json
{
  "detail": "Not authenticated"
}
```

**Document Not Found:**
```json
{
  "detail": "Document not found"
}
```

**Admin Required:**
```json
{
  "detail": "Admin access required"
}
```

---

## Rate Limiting

**Current Limits:**
- Upload: 10 documents per minute per user
- Status checks: 100 requests per minute
- List: 20 requests per minute

**Headers:**
```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1701712800
```

---

## Dependencies

**Backend:**
```txt
fastapi>=0.104.0
python-multipart>=0.0.6
sqlalchemy>=2.0.0
psycopg[binary]>=3.1.0
python-minio>=7.2.0
python-docx>=1.1.0
pytesseract>=0.3.10
pdf2image>=1.16.3
Pillow>=10.1.0
```

**Frontend:**
```json
{
  "react": "^18.2.0",
  "next": "^14.0.0",
  "typescript": "^5.0.0"
}
```

---

## Example Responses

### Employment Contract Result

```json
{
  "document_type": "employment_contract",
  "confidence": 0.87,
  "extracted_fields": {
    "contract_number": "ZML-001/2024",
    "contract_date": "15.12.2024",
    "employer": "ABC s.r.o.",
    "ico": "12345678",
    "employee": "Ján Novák",
    "position": "Programátor",
    "salary": "2000 EUR",
    "start_date": "01.01.2025"
  }
}
```

### Invoice Result

```json
{
  "document_type": "invoice",
  "confidence": 0.92,
  "extracted_fields": {
    "invoice_number": "FA-123/2024",
    "issue_date": "15.12.2024",
    "due_date": "29.12.2024",
    "supplier": "XYZ s.r.o.",
    "ico": "87654321",
    "dic": "SK2020123456",
    "total_amount": "1500.00 EUR"
  }
}
```

---

## Support

For issues or questions:
- GitHub: https://github.com/your-repo/codex
- Email: support@codex.example.com
- Documentation: https://docs.codex.example.com

---

**Version:** 1.0.0  
**Last Updated:** 2024-12-04
