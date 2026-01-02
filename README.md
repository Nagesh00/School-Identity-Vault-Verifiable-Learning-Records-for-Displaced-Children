# School Identity Vault: Verifiable Learning Records for Displaced Children

> 🏆 **Microsoft Imagine Cup 2026 Project**  
> Uses Azure AI Document Intelligence + Azure OpenAI Service

## Overview

School Identity Vault is a comprehensive system that preserves education records for displaced children, ensuring their learning credentials are portable, verifiable, and tamper-proof. Built with **Microsoft Azure AI services** to compete in Imagine Cup 2026, this solution helps 48 million displaced children worldwide maintain their educational records across borders.

The system enables NGOs and families to upload photos of certificates or report cards, uses **Microsoft AI** to extract and reconstruct learning profiles, maps them to local curricula with confidence levels, allows schools to verify results, and stores cryptographic hashes with digital signatures on a permissioned blockchain.

## 🎯 Microsoft Imagine Cup 2026 Compliance

This project meets all Imagine Cup 2026 requirements:

✅ **Two Microsoft AI Services**:
1. **Azure AI Document Intelligence** - OCR and document analysis
2. **Azure OpenAI Service** - Intelligent text processing and extraction

✅ **Commercial Viability**: Clear revenue model targeting $1.8B refugee education market  
✅ **Technical MVP**: Full working solution with 10+ API endpoints  
✅ **Social Impact**: Helps 48 million displaced children access education  

📄 [Full Imagine Cup Compliance Document](IMAGINE_CUP_2026.md)

## Key Features

### 1. **Document Upload System**
- Upload photos of certificates, report cards, transcripts, and diplomas
- Support for multiple image formats (JPG, PNG, PDF)
- Secure file storage with hash verification
- Document type classification

### 2. **AI-Powered Data Extraction** (Microsoft Azure AI)
- **Azure AI Document Intelligence** for OCR and layout analysis
- **Azure OpenAI Service** for intelligent text processing
- Intelligent parsing of student information
- Subject and grade extraction
- Confidence scoring for data quality

### 3. **Learning Profile Reconstruction**
- Automatic creation of comprehensive student profiles
- Multi-document aggregation
- Historical record tracking
- Student identity preservation

### 4. **Curriculum Mapping**
- Map subjects to standard curricula
- Support for multiple curriculum frameworks
- Equivalence level calculation
- Cross-border education compatibility

### 5. **School Verification**
- Verification workflow for school officials
- Multi-level approval system
- Verification audit trail
- Status tracking (pending, verified, rejected)

### 6. **Blockchain Integration**
- Cryptographic hashing of profiles
- Digital signature generation
- Permissioned blockchain storage
- Tamper-proof record keeping
- Transaction verification

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     School Identity Vault                    │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Document   │     │  AI Extract  │     │   Profile    │
│   Service    │────▶│   Service    │────▶│   Service    │
└──────────────┘     └──────────────┘     └──────────────┘
        │                     │                     │
        │                     │                     ▼
        │                     │            ┌──────────────┐
        │                     │            │ Verification │
        │                     │            │   Service    │
        │                     │            └──────────────┘
        │                     │                     │
        │                     │                     ▼
        │                     │            ┌──────────────┐
        │                     └───────────▶│  Blockchain  │
        │                                  │   Service    │
        └─────────────────────────────────▶└──────────────┘
```

## Installation

### Prerequisites
- Python 3.8 or higher
- **Microsoft Azure Account** (for Imagine Cup AI services)
- Azure AI Document Intelligence resource
- Azure OpenAI Service resource
- Tesseract OCR (optional, for fallback)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Nagesh00/School-Identity-Vault-Verifiable-Learning-Records-for-Displaced-Children.git
cd School-Identity-Vault-Verifiable-Learning-Records-for-Displaced-Children
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. **Configure Microsoft Azure AI Services** (Required for Imagine Cup):

   a. Create Azure AI Document Intelligence resource:
   - Go to [Azure Portal](https://portal.azure.com)
   - Create "Azure AI Document Intelligence" resource
   - Copy endpoint and key

   b. Create Azure OpenAI Service resource:
   - Create "Azure OpenAI" resource
   - Deploy a model (e.g., gpt-4 or gpt-3.5-turbo)
   - Copy endpoint, key, and deployment name

5. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Azure credentials:
# AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
# AZURE_DOCUMENT_INTELLIGENCE_KEY=your_key
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_KEY=your_key
# AZURE_OPENAI_DEPLOYMENT=your_deployment_name
```

6. (Optional) Install Tesseract OCR for fallback:
- **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`
- **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Usage

### Running the API Server

Start the FastAPI server:
```bash
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Running the Example Script

See the complete workflow in action:
```bash
python example.py
```

### API Endpoints

#### Document Management
- `POST /api/documents/upload` - Upload a document
- `POST /api/documents/{document_id}/extract` - Extract data from document

#### Profile Management
- `POST /api/profiles/create` - Create learning profile
- `GET /api/profiles/{profile_id}` - Get profile details

#### Verification
- `POST /api/verification/create` - Create verification record
- `GET /api/verification/profile/{profile_id}` - Get profile verifications

#### Blockchain
- `POST /api/blockchain/store` - Store profile on blockchain
- `GET /api/blockchain/verify/{record_id}` - Verify blockchain record

#### Health Check
- `GET /api/health` - Service health status

## Workflow Example

### 1. Upload Document
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@student_certificate.jpg" \
  -F "document_type=certificate" \
  -F "uploader_id=NGO-001"
```

### 2. Extract Data
```bash
curl -X POST "http://localhost:8000/api/documents/{document_id}/extract"
```

### 3. Create Learning Profile
```bash
curl -X POST "http://localhost:8000/api/profiles/create" \
  -F "student_name=Ahmed Khan" \
  -F "document_ids=doc-id-1,doc-id-2" \
  -F "target_curriculum=International"
```

### 4. Verify Profile
```bash
curl -X POST "http://localhost:8000/api/verification/create" \
  -F "document_id=doc-id-1" \
  -F "profile_id=profile-id" \
  -F "verifier_id=SCHOOL-001" \
  -F "verifier_name=Lincoln High School" \
  -F "status=verified"
```

### 5. Store on Blockchain
```bash
curl -X POST "http://localhost:8000/api/blockchain/store" \
  -F "profile_id=profile-id"
```

## Data Models

### Learning Profile
Contains:
- Student information (name, ID)
- Document references
- Completed subjects with grades
- Curriculum mappings
- Confidence scores
- Timestamps

### Blockchain Record
Contains:
- Profile hash (SHA-256)
- Digital signature
- Transaction hash
- Block number
- Timestamp

## Security Features

1. **Cryptographic Hashing**: SHA-256 hashing of all profiles
2. **Digital Signatures**: RSA-2048 signatures for authenticity
3. **Blockchain Storage**: Immutable record keeping
4. **File Validation**: Image and document integrity checks
5. **Access Control**: Role-based verification system

## Use Cases

### For NGOs
- Upload education documents for displaced children
- Track document processing status
- Coordinate with schools for verification

### For Families
- Submit children's educational records
- Track verification progress
- Access portable credentials

### For Schools
- Verify student credentials
- Accept verified learning profiles
- Map to local curriculum requirements

### For Students
- Portable education credentials
- Verifiable learning history
- Cross-border education continuity

## Technology Stack

### Microsoft AI Services (Imagine Cup 2026)
- **Azure AI Document Intelligence**: OCR and document analysis
- **Azure OpenAI Service**: Intelligent text processing and extraction

### Core Technologies
- **Backend**: FastAPI (Python)
- **Cryptography**: Python cryptography library (RSA-2048, SHA-256)
- **Blockchain**: Web3.py (Ethereum compatible)
- **Data Validation**: Pydantic
- **Image Processing**: Pillow, pdf2image

### Future Azure Integration
- **Azure Storage**: Secure document storage
- **Azure Key Vault**: Credential management
- **Azure Cosmos DB**: Scalable database
- **Azure Blockchain Service**: Enhanced blockchain integration

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Acknowledgments

This system is designed to help displaced children maintain their educational records and continue their education seamlessly across borders. It aims to provide dignity, continuity, and opportunity to children affected by displacement.

---

**Built with ❤️ for displaced children worldwide**