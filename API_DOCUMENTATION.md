# API Documentation

## School Identity Vault API

Base URL: `http://localhost:8000`

## Authentication

Currently, the API does not require authentication. In production, implement appropriate authentication mechanisms.

## Endpoints

### Health Check

#### GET /api/health

Check the health status of all services.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "document": "operational",
    "extraction": "operational",
    "profile": "operational",
    "verification": "operational",
    "blockchain": "operational"
  }
}
```

---

### Document Management

#### POST /api/documents/upload

Upload an educational document (certificate, report card, etc.)

**Parameters:**
- `file` (multipart/form-data): The document file
- `document_type` (form field): Type of document (certificate, report_card, transcript, diploma, other)
- `uploader_id` (form field): ID of the uploader

**Example:**
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@student_certificate.jpg" \
  -F "document_type=certificate" \
  -F "uploader_id=NGO-001"
```

**Response:**
```json
{
  "id": "uuid-here",
  "filename": "student_certificate.jpg",
  "document_type": "certificate",
  "upload_date": "2024-01-02T10:00:00Z",
  "uploader_id": "NGO-001",
  "file_path": "/path/to/file",
  "file_hash": "sha256-hash-here"
}
```

#### POST /api/documents/{document_id}/extract

Extract data from an uploaded document using AI/OCR.

**Parameters:**
- `document_id` (path): ID of the document to extract

**Example:**
```bash
curl -X POST "http://localhost:8000/api/documents/abc-123/extract"
```

**Response:**
```json
{
  "document_id": "abc-123",
  "student_name": "Ahmed Khan",
  "student_id": "STU-2024-001",
  "institution_name": "ABC International School",
  "issue_date": "15/06/2023",
  "subjects": [
    {"name": "Mathematics", "grade": "A"},
    {"name": "Science", "grade": "B+"}
  ],
  "grades": [...],
  "raw_text": "...",
  "confidence_score": 0.85,
  "extraction_date": "2024-01-02T10:05:00Z"
}
```

---

### Learning Profile Management

#### POST /api/profiles/create

Create a learning profile from extracted document data.

**Parameters:**
- `student_name` (form field): Name of the student
- `document_ids` (form field): Comma-separated list of document IDs
- `target_curriculum` (form field, optional): Target curriculum (default: "standard")
- `student_id` (form field, optional): Student ID

**Example:**
```bash
curl -X POST "http://localhost:8000/api/profiles/create" \
  -F "student_name=Ahmed Khan" \
  -F "document_ids=doc-id-1,doc-id-2" \
  -F "target_curriculum=International" \
  -F "student_id=STU-001"
```

**Response:**
```json
{
  "profile_id": "profile-uuid",
  "student_name": "Ahmed Khan",
  "student_id": "STU-001",
  "documents": ["doc-id-1", "doc-id-2"],
  "subjects_completed": [
    {"name": "Mathematics", "grade": "A"}
  ],
  "curriculum_mappings": [
    {
      "original_subject": "Mathematics",
      "mapped_subject": "Mathematics",
      "equivalence_level": 0.85,
      "target_curriculum": "International"
    }
  ],
  "overall_confidence": 0.87,
  "created_date": "2024-01-02T10:10:00Z",
  "last_updated": "2024-01-02T10:10:00Z"
}
```

#### GET /api/profiles/{profile_id}

Get a learning profile by ID.

**Example:**
```bash
curl -X GET "http://localhost:8000/api/profiles/profile-uuid"
```

---

### Verification

#### POST /api/verification/create

Create a verification record for a profile.

**Parameters:**
- `document_id` (form field): Document ID
- `profile_id` (form field): Profile ID
- `verifier_id` (form field): Verifier ID
- `verifier_name` (form field): Verifier name
- `status` (form field): Status (pending, verified, rejected)
- `notes` (form field, optional): Verification notes

**Example:**
```bash
curl -X POST "http://localhost:8000/api/verification/create" \
  -F "document_id=doc-id-1" \
  -F "profile_id=profile-uuid" \
  -F "verifier_id=SCHOOL-001" \
  -F "verifier_name=Lincoln High School" \
  -F "status=verified" \
  -F "notes=Documents verified and accepted"
```

**Response:**
```json
{
  "verification_id": "verification-uuid",
  "document_id": "doc-id-1",
  "profile_id": "profile-uuid",
  "verifier_id": "SCHOOL-001",
  "verifier_name": "Lincoln High School",
  "status": "verified",
  "notes": "Documents verified and accepted",
  "verification_date": "2024-01-02T10:15:00Z"
}
```

#### GET /api/verification/profile/{profile_id}

Get all verifications for a profile.

**Example:**
```bash
curl -X GET "http://localhost:8000/api/verification/profile/profile-uuid"
```

**Response:**
```json
{
  "profile_id": "profile-uuid",
  "verifications": [...],
  "summary": {
    "total": 1,
    "verified": 1,
    "pending": 0,
    "rejected": 0
  }
}
```

---

### Blockchain

#### POST /api/blockchain/store

Store a learning profile on blockchain.

**Parameters:**
- `profile_id` (form field): Profile ID to store

**Example:**
```bash
curl -X POST "http://localhost:8000/api/blockchain/store" \
  -F "profile_id=profile-uuid"
```

**Response:**
```json
{
  "record_id": "record-uuid",
  "profile_id": "profile-uuid",
  "document_hash": "sha256-hash",
  "signature": "digital-signature",
  "transaction_hash": "blockchain-tx-hash",
  "block_number": 12345,
  "timestamp": "2024-01-02T10:20:00Z"
}
```

#### GET /api/blockchain/verify/{record_id}

Verify a blockchain record.

**Example:**
```bash
curl -X GET "http://localhost:8000/api/blockchain/verify/record-uuid"
```

**Response:**
```json
{
  "record_id": "record-uuid",
  "profile_id": "profile-uuid",
  "is_valid": true,
  "transaction_hash": "blockchain-tx-hash",
  "block_number": 12345
}
```

---

## Interactive API Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "detail": "Error message here"
}
```

Common HTTP status codes:
- `200 OK`: Successful request
- `400 Bad Request`: Invalid input
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limiting

Currently, no rate limiting is implemented. In production, implement appropriate rate limiting.

## Data Retention

Document files and profile data are stored locally. Implement appropriate data retention policies based on your requirements.

## Security Considerations

1. Implement authentication and authorization
2. Use HTTPS in production
3. Validate all input data
4. Implement rate limiting
5. Regular security audits
6. Data encryption at rest
7. Secure blockchain key management
