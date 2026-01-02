"""
Main FastAPI application for School Identity Vault
"""
import os
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from ..models.schemas import (
    DocumentType,
    VerificationStatus,
    UploadedDocument,
    ExtractedData,
    LearningProfile,
    VerificationRecord,
    BlockchainRecord
)
from ..services import (
    DocumentService,
    AIExtractionService,
    LearningProfileService,
    VerificationService,
    BlockchainService
)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="School Identity Vault API",
    description="Verifiable Learning Records for Displaced Children",
    version="1.0.0"
)

# Initialize services
document_service = DocumentService(
    upload_dir=os.getenv("UPLOAD_DIR", "./uploads")
)
extraction_service = AIExtractionService(
    openai_api_key=os.getenv("OPENAI_API_KEY")
)
profile_service = LearningProfileService()
verification_service = VerificationService()
blockchain_service = BlockchainService(
    rpc_url=os.getenv("BLOCKCHAIN_RPC_URL"),
    private_key=os.getenv("BLOCKCHAIN_PRIVATE_KEY")
)

# In-memory storage (in production, use a database)
documents_db = {}
extractions_db = {}
profiles_db = {}
blockchain_records_db = {}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "School Identity Vault API",
        "version": "1.0.0",
        "description": "Verifiable Learning Records for Displaced Children"
    }


@app.post("/api/documents/upload", response_model=UploadedDocument)
async def upload_document(
    file: UploadFile = File(...),
    document_type: DocumentType = Form(...),
    uploader_id: str = Form(...)
):
    """Upload an educational document (certificate, report card, etc.)"""
    try:
        # Read file content
        content = await file.read()
        
        # Save document
        document = await document_service.save_document(
            file_content=content,
            filename=file.filename,
            document_type=document_type,
            uploader_id=uploader_id
        )
        
        # Store in database
        documents_db[document.id] = document
        
        return document
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/documents/{document_id}/extract", response_model=ExtractedData)
async def extract_document_data(document_id: str):
    """Extract data from an uploaded document using AI/OCR"""
    # Get document
    document = documents_db.get(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        # Extract data
        extracted = await extraction_service.extract_from_document(
            document_id=document_id,
            file_path=document.file_path
        )
        
        # Store extraction
        extractions_db[document_id] = extracted
        
        return extracted
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/profiles/create", response_model=LearningProfile)
async def create_learning_profile(
    student_name: str = Form(...),
    document_ids: str = Form(...),
    target_curriculum: str = Form("standard"),
    student_id: Optional[str] = Form(None)
):
    """Create a learning profile from extracted document data"""
    # Parse document IDs
    doc_ids = [d.strip() for d in document_ids.split(",")]
    
    # Get extractions
    extractions = []
    for doc_id in doc_ids:
        extraction = extractions_db.get(doc_id)
        if extraction:
            extractions.append(extraction)
    
    if not extractions:
        raise HTTPException(
            status_code=400,
            detail="No extracted data found for provided document IDs"
        )
    
    try:
        # Create profile
        profile = profile_service.reconstruct_learning_profile(
            student_name=student_name,
            extractions=extractions,
            target_curriculum=target_curriculum,
            student_id=student_id
        )
        
        # Store profile
        profiles_db[profile.profile_id] = profile
        
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/profiles/{profile_id}", response_model=LearningProfile)
async def get_learning_profile(profile_id: str):
    """Get a learning profile by ID"""
    profile = profiles_db.get(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@app.post("/api/verification/create", response_model=VerificationRecord)
async def create_verification(
    document_id: str = Form(...),
    profile_id: str = Form(...),
    verifier_id: str = Form(...),
    verifier_name: str = Form(...),
    status: VerificationStatus = Form(...),
    notes: Optional[str] = Form(None)
):
    """Create a verification record for a profile"""
    # Check if profile exists
    if profile_id not in profiles_db:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    try:
        verification = verification_service.create_verification(
            document_id=document_id,
            profile_id=profile_id,
            verifier_id=verifier_id,
            verifier_name=verifier_name,
            status=status,
            notes=notes
        )
        return verification
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/verification/profile/{profile_id}")
async def get_profile_verifications(profile_id: str):
    """Get all verifications for a profile"""
    verifications = verification_service.get_verifications_for_profile(profile_id)
    summary = verification_service.get_verification_summary(profile_id)
    
    return {
        "profile_id": profile_id,
        "verifications": verifications,
        "summary": summary
    }


@app.post("/api/blockchain/store", response_model=BlockchainRecord)
async def store_on_blockchain(profile_id: str = Form(...)):
    """Store a learning profile on blockchain"""
    # Get profile
    profile = profiles_db.get(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    try:
        # Store on blockchain
        record = await blockchain_service.store_on_blockchain(profile)
        
        # Store record
        blockchain_records_db[record.record_id] = record
        
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/blockchain/verify/{record_id}")
async def verify_blockchain_record(record_id: str):
    """Verify a blockchain record"""
    record = blockchain_records_db.get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    profile = profiles_db.get(record.profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    is_valid = blockchain_service.verify_blockchain_record(record, profile)
    
    return {
        "record_id": record_id,
        "profile_id": record.profile_id,
        "is_valid": is_valid,
        "transaction_hash": record.transaction_hash,
        "block_number": record.block_number
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "document": "operational",
            "extraction": "operational",
            "profile": "operational",
            "verification": "operational",
            "blockchain": "operational"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000))
    )
