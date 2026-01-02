# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
All endpoints require authentication via Bearer token (except health check).
```
Authorization: Bearer <token>
```

---

## Endpoints

### Health Check
```
GET /health
```
Check service status.

**Response (200):**
```json
{
  "status": "healthy",
  "service": "School Identity Vault Backend",
  "timestamp": "2025-01-02T10:30:00Z",
  "uptime": 3600
}
```

---

### Document Upload
```
POST /documents/upload
```
Upload and process a school document (certificate, report card, ID, etc.).

**Request:**
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Body**:
  - `file` (File): Image or PDF document
  - `documentType` (string): Type - `certificate`, `report_card`, `id`, `handwritten_note`
  - `childId` (string): Child identifier
  - `sourceCountry` (string): Country of origin

**Example:**
```bash
curl -X POST http://localhost:5000/api/documents/upload \
  -F "file=@report_card.jpg" \
  -F "documentType=report_card" \
  -F "childId=child_123" \
  -F "sourceCountry=Syria"
```

**Response (200):**
```json
{
  "success": true,
  "documentId": "doc_abc123",
  "ocrText": "Grade 3 Completed...",
  "extractedData": {
    "gradeLevel": 3,
    "subjects": {
      "reading": {"performance": "good", "score": null},
      "mathematics": {"performance": "average", "score": null}
    },
    "certificateIssued": 2019,
    "institution": "School X",
    "sourceCountry": "Syria"
  },
  "confidence": {
    "overall": 0.85,
    "gradeLevel": 0.90,
    "subjects": 0.80
  }
}
```

**Error (400):**
```json
{
  "error": "No file provided"
}
```

---

### Create Learning Profile
```
POST /profiles
```
Create a learning profile from one or more documents.

**Request:**
```json
{
  "childName": "Ahmed Al-Hassan",
  "childId": "child_123",
  "documentIds": ["doc_abc123", "doc_def456"],
  "sourceCountry": "Syria"
}
```

**Response (201):**
```json
{
  "success": true,
  "profile": {
    "profileId": "profile_xyz789",
    "childName": "Ahmed Al-Hassan",
    "childId": "child_123",
    "sourceCountry": "Syria",
    "documentIds": ["doc_abc123", "doc_def456"],
    "mergedData": {
      "gradeLevel": 3,
      "subjects": {...},
      "institutions": ["School X"],
      "confidenceScores": {...}
    },
    "summary": {
      "textSummary": "This student has likely completed primary school...",
      "standardizedFormat": {
        "educationLevel": "primary",
        "estimatedGrade": 3,
        "subjects": {...}
      }
    },
    "createdAt": "2025-01-02T10:30:00Z",
    "verifications": [],
    "blockchainStatus": "pending"
  }
}
```

---

### Get Learning Profile
```
GET /profiles/:profileId
```
Retrieve a learning profile with all reconstructed data.

**Response (200):**
```json
{
  "success": true,
  "profile": {
    "profileId": "profile_xyz789",
    ...
  }
}
```

**Error (404):**
```json
{
  "error": "Profile not found"
}
```

---

### Update Profile
```
PUT /profiles/:profileId
```
Update profile with corrections.

**Request:**
```json
{
  "corrections": {
    "gradeLevel": 4,
    "notes": "School confirmed Grade 4"
  },
  "verifiedBy": "school_001"
}
```

**Response (200):**
```json
{
  "success": true,
  "profile": {
    "profileId": "profile_xyz789",
    "corrections": {...},
    "verifiedBy": "school_001",
    "verificationDate": "2025-01-02T10:35:00Z",
    "lastModified": "2025-01-02T10:35:00Z"
  }
}
```

---

### Merge Documents
```
POST /profiles/:profileId/merge
```
Merge conflicting information from multiple documents.

**Request:**
```json
{
  "documentIds": ["doc_abc123", "doc_def456"],
  "strategy": "confidence"
}
```

Strategy options:
- `confidence`: Weight by confidence scores
- `latest`: Use most recent document
- `manual`: Return conflicts for manual resolution

**Response (200):**
```json
{
  "success": true,
  "profile": {
    "profileId": "profile_xyz789",
    "mergeStrategy": "confidence",
    "mergedAt": "2025-01-02T10:40:00Z"
  }
}
```

---

### Verify Profile
```
POST /verification/verify
```
Verify a learning profile.

**Request:**
```json
{
  "profileId": "profile_xyz789",
  "schoolId": "school_001",
  "schoolName": "Local Secondary School",
  "isVerified": true,
  "verificationNotes": "Profile matches school records. Student ready for Grade 5."
}
```

**Response (201):**
```json
{
  "success": true,
  "verification": {
    "verificationId": "verify_001",
    "profileId": "profile_xyz789",
    "schoolId": "school_001",
    "schoolName": "Local Secondary School",
    "isVerified": true,
    "verificationNotes": "...",
    "verificationDate": "2025-01-02T10:45:00Z",
    "status": "unsigned",
    "signature": null,
    "blockchainStatus": "pending"
  }
}
```

---

### Sign Verification
```
POST /verification/:verificationId/sign
```
Add cryptographic signature to verification.

**Request:**
```json
{
  "schoolPrivateKey": "0x..."
}
```

**Response (200):**
```json
{
  "success": true,
  "signature": {
    "verificationId": "verify_001",
    "signature": "0xabc123...",
    "signedAt": "2025-01-02T10:46:00Z",
    "status": "signed",
    "verificationStatus": "cryptographically_verified"
  }
}
```

---

### Get Verification History
```
GET /verification/:profileId/history
```
Get verification history for a profile.

**Response (200):**
```json
{
  "success": true,
  "history": [
    {
      "verificationId": "verify_001",
      "schoolName": "Local Secondary School",
      "verificationDate": "2025-01-02T10:45:00Z",
      "isVerified": true,
      "status": "signed"
    }
  ],
  "totalVerifications": 1
}
```

---

### Submit Verification to Blockchain
```
POST /verification/:verificationId/blockchain
```
Record verification on blockchain.

**Response (201):**
```json
{
  "success": true,
  "blockchainRecord": {
    "verificationId": "verify_001",
    "transactionHash": "0xabcd1234...",
    "blockNumber": 12345,
    "gasUsed": 125000,
    "status": "confirmed",
    "timestamp": "2025-01-02T10:47:00Z",
    "blockchainNetwork": "Azure Blockchain"
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request parameters",
  "status": 400
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication required",
  "status": 401
}
```

### 403 Forbidden
```json
{
  "error": "Access denied",
  "status": 403
}
```

### 404 Not Found
```json
{
  "error": "Resource not found",
  "status": 404
}
```

### 500 Internal Server Error
```json
{
  "error": "An unexpected error occurred",
  "status": 500
}
```

---

## Rate Limiting
- **API Calls**: 1000 requests per hour per API key
- **Document Upload**: 100 MB per request maximum

---

## Example Workflow

```bash
# 1. Upload first document
curl -X POST http://localhost:5000/api/documents/upload \
  -F "file=@certificate.jpg" \
  -F "documentType=certificate" \
  -F "childId=child_123"
# Returns: documentId = "doc_abc123"

# 2. Upload second document for cross-verification
curl -X POST http://localhost:5000/api/documents/upload \
  -F "file=@report_card.jpg" \
  -F "documentType=report_card" \
  -F "childId=child_123"
# Returns: documentId = "doc_def456"

# 3. Create profile from documents
curl -X POST http://localhost:5000/api/profiles \
  -H "Content-Type: application/json" \
  -d '{
    "childName": "Ahmed Al-Hassan",
    "childId": "child_123",
    "documentIds": ["doc_abc123", "doc_def456"],
    "sourceCountry": "Syria"
  }'
# Returns: profileId = "profile_xyz789"

# 4. Get profile
curl http://localhost:5000/api/profiles/profile_xyz789

# 5. School verifies profile
curl -X POST http://localhost:5000/api/verification/verify \
  -H "Content-Type: application/json" \
  -d '{
    "profileId": "profile_xyz789",
    "schoolId": "school_001",
    "schoolName": "Local School",
    "isVerified": true
  }'
# Returns: verificationId = "verify_001"

# 6. Sign verification
curl -X POST http://localhost:5000/api/verification/verify_001/sign \
  -H "Content-Type: application/json" \
  -d '{"schoolPrivateKey": "0x..."}'

# 7. Submit to blockchain
curl -X POST http://localhost:5000/api/verification/verify_001/blockchain

# 8. View verification history
curl http://localhost:5000/api/verification/profile_xyz789/history
```
