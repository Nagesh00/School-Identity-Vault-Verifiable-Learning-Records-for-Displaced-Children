# Architecture & Technical Design

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    User Interfaces                              │
│            Web App / Mobile App / NGO Portal                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   API Gateway / Load Balancer                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────▼────────┐ ┌────▼────────┐ ┌────▼─────────┐
│  Backend API   │ │  ML Engine   │ │  Blockchain  │
│  (Node.js)     │ │  (FastAPI)   │ │  Service     │
│                │ │              │ │  (Web3)      │
└───────┬────────┘ └────┬─────────┘ └────┬─────────┘
        │                │                │
┌───────┴────────┬───────┴─────────┬──────┴─────────┐
│                │                 │                │
▼                ▼                 ▼                ▼
┌──────────────────────────────────────────────────────┐
│        Azure Services                                │
│  ┌─────────────────────────────────────────────┐    │
│  │ AI Services                                 │    │
│  │ - Computer Vision (OCR)                     │    │
│  │ - Language Understanding                    │    │
│  │ - OpenAI Integration                        │    │
│  │ - ML Model Training & Inference             │    │
│  └─────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────┐    │
│  │ Storage & Database                          │    │
│  │ - Blob Storage (encrypted documents)        │    │
│  │ - PostgreSQL (metadata)                     │    │
│  │ - Cosmos DB (document hashes)               │    │
│  └─────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────┐    │
│  │ Security                                    │    │
│  │ - Key Vault                                 │    │
│  │ - Azure AD / OAuth2                         │    │
│  └─────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────┐
│   Permissioned Blockchain            │
│   (Azure Blockchain / Hyperledger)   │
│                                      │
│   - Verification records             │
│   - Document hashes                  │
│   - Signature verification chain     │
└──────────────────────────────────────┘
```

## Component Details

### 1. Frontend Layer
- **Web Application** (React/TypeScript)
- **Mobile Application** (React Native)
- Real-time UI for document upload and verification
- Responsive design for various devices

### 2. Backend API (Node.js)
**Endpoints:**
- `POST /api/documents/upload` - Upload document
- `POST /api/profiles` - Create learning profile
- `GET /api/profiles/:id` - Retrieve profile
- `POST /api/verification/verify` - Submit verification
- `GET /api/verification/:profileId/history` - Get verification audit trail

**Responsibilities:**
- Request routing and validation
- Session management
- API orchestration
- Blockchain interaction coordination

### 3. ML Engine (FastAPI)
**Key Operations:**
- Document OCR and text extraction
- Education data parsing
- Profile reconstruction and merging
- Confidence scoring
- Curriculum equivalence mapping

**Pipeline:**
```
Document Image → OCR → Text Parsing → Data Extraction → Normalization → Scoring
```

### 4. Azure Cognitive Services Integration

#### Azure Computer Vision
- **Function**: OCR on low-quality, multi-language documents
- **Input**: Image (photo, scan)
- **Output**: Extracted text, layout information

#### Azure Language Service
- **Function**: Entity extraction, text understanding
- **Input**: OCR text
- **Output**: Structured education data

#### Azure OpenAI
- **Function**: Data interpretation and summary generation
- **Input**: Extracted data
- **Output**: Human-readable profile summary

#### Azure ML
- **Function**: Confidence scoring and curriculum mapping
- **Input**: Educational data
- **Output**: Confidence scores, equivalence mapping

### 5. Blockchain Layer (Solidity Smart Contract)

**Contract: VerificationRecord**

**Key Functions:**
- `recordDocument()` - Store document hash
- `createProfile()` - Initialize learner profile
- `recordVerification()` - Log verification action
- `signVerification()` - Add cryptographic signature

**Data Stored:**
- Document hashes (not full documents)
- Verification timestamps
- Verifier signatures
- Audit trail of all actions

**Benefits:**
- Immutable verification history
- Cryptographic proof of validation
- Transparent audit trail
- No single point of failure

## Data Flow

### Document Upload Flow
```
1. User uploads image
   ↓
2. Backend stores in encrypted Azure Blob Storage
   ↓
3. ML Engine receives document for processing
   ↓
4. Document Processor performs OCR (Azure Vision)
   ↓
5. Text extracted → Language Service for parsing
   ↓
6. Structured education data extracted
   ↓
7. Confidence scorer evaluates reliability
   ↓
8. Document hash recorded on blockchain
   ↓
9. Response returned to frontend with:
   - OCR text
   - Extracted structured data
   - Confidence scores
   - Document ID
```

### Profile Creation Flow
```
1. User initiates profile creation with multiple documents
   ↓
2. Backend retrieves all document data
   ↓
3. ML Engine merge service combines information
   ↓
4. Confidence-weighted merging (handles conflicts)
   ↓
5. Profile Reconstructor creates standardized profile
   ↓
6. Curriculum Equivalence Mapper generates grade mapping
   ↓
7. Azure OpenAI generates human-readable summary
   ↓
8. Profile hash created
   ↓
9. Profile recorded on blockchain
   ↓
10. Profile returned with:
    - Merged education data
    - Confidence levels
    - Standardized summary
    - Curriculum equivalence
```

### Verification & Blockchain Flow
```
1. School/Agency reviews profile
   ↓
2. Verifier submits verification decision
   ↓
3. Backend creates verification record
   ↓
4. Cryptographic signature generated
   ↓
5. Verification details + signature sent to blockchain
   ↓
6. Smart contract records on distributed ledger
   ↓
7. Transaction hash returned
   ↓
8. Verification audit trail accessible to all parties
```

## Security Considerations

### Document Security
- **Encryption at Rest**: Azure Blob Storage encryption
- **Encryption in Transit**: TLS/HTTPS for all communications
- **Access Control**: Role-based access to documents
- **PII Protection**: Personal data encrypted separately

### Blockchain Security
- **Permissioned Access**: Only authorized verifiers can sign
- **Smart Contract Audit**: Code audited before deployment
- **Key Management**: Private keys stored in Azure Key Vault
- **Non-Repudiation**: Cryptographic signatures prevent denial

### API Security
- **Authentication**: Azure AD / OAuth2
- **Authorization**: Role-based access control
- **Rate Limiting**: Prevent abuse
- **Input Validation**: All inputs validated server-side

## Scalability

### Horizontal Scaling
- **API**: Load-balanced Node.js instances
- **ML Engine**: FastAPI with async processing
- **Blockchain**: Permissioned network with optimized consensus

### Vertical Scaling
- **Database**: Azure Database for PostgreSQL (managed scaling)
- **Storage**: Azure Blob Storage (unlimited capacity)
- **Compute**: Auto-scaling for API and ML services

## Disaster Recovery

- **Data Backup**: Multi-region replication
- **Service Redundancy**: Multiple instances across regions
- **Blockchain**: Distributed ledger ensures data persistence
- **Recovery Time Objective**: < 1 hour
- **Recovery Point Objective**: < 15 minutes

## Performance Targets

- **Document OCR**: < 5 seconds (small documents)
- **Profile Creation**: < 10 seconds (3 documents)
- **Verification Recording**: < 2 seconds
- **Blockchain Confirmation**: < 30 seconds (depends on network)
- **API Response Time**: < 500ms (95th percentile)
