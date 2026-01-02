"""
ML Engine - Document Processing and Profile Reconstruction
"""
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import logging
import os
from dotenv import load_dotenv

# Import service modules
from src.document_processor import extract_text_from_image, parse_education_data
from src.profile_reconstructor import reconstruct_profile, estimate_curriculum_equivalence
from src.confidence_scorer import calculate_confidence

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="School Identity Vault - ML Engine")

# Configuration
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ML Engine",
        "version": "1.0.0"
    }


@app.post("/api/process-document")
async def process_document(file: UploadFile, document_type: str = "report_card"):
    """
    Process a school document (photo, scan, etc.)
    
    Returns:
    - OCR text extracted from image
    - Parsed education data
    - Confidence scores
    """
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")

        # Read file
        contents = await file.read()
        logger.info(f"Processing document: {file.filename}")

        # Step 1: Extract text from image (OCR)
        ocr_text = extract_text_from_image(contents)
        logger.info("OCR extraction completed")

        # Step 2: Parse education data
        education_data = parse_education_data(ocr_text, document_type)
        logger.info("Education data parsing completed")

        # Step 3: Calculate confidence
        confidence = calculate_confidence(education_data)
        logger.info(f"Confidence score: {confidence['overall']}")

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "ocrText": ocr_text,
                "educationData": education_data,
                "confidence": confidence,
                "documentType": document_type
            }
        )

    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/reconstruct-profile")
async def reconstruct_profile_endpoint(document_data_list: list):
    """
    Reconstruct learning profile from multiple documents
    
    Input: List of extracted education data from multiple documents
    Output: Merged profile with standardized format
    """
    try:
        if not document_data_list:
            raise HTTPException(status_code=400, detail="At least one document is required")

        logger.info(f"Reconstructing profile from {len(document_data_list)} documents")

        # Reconstruct profile
        profile = reconstruct_profile(document_data_list)
        logger.info("Profile reconstruction completed")

        # Estimate curriculum equivalence
        curriculum_mapping = estimate_curriculum_equivalence(profile)
        logger.info("Curriculum equivalence estimation completed")

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "profile": profile,
                "curriculumMapping": curriculum_mapping,
                "summary": generate_profile_summary(profile, curriculum_mapping)
            }
        )

    except Exception as e:
        logger.error(f"Error reconstructing profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def generate_profile_summary(profile: dict, curriculum_mapping: dict) -> str:
    """Generate human-readable profile summary using AI"""
    # TODO: Call Azure OpenAI to generate summary
    
    grade = profile.get("estimated_grade", "Unknown")
    confidence = profile.get("confidence_level", "Unknown")
    
    return f"""
    This student has likely completed primary school level literacy and grade-{grade} level numeracy.
    Confidence Level: {confidence}
    Last verified: {profile.get('last_verified_date', 'Not yet verified')}
    """


@app.post("/api/merge-documents")
async def merge_documents(documents: list, strategy: str = "confidence"):
    """
    Merge conflicting information from multiple documents
    
    Strategy options:
    - 'confidence': Weight by confidence scores
    - 'latest': Use most recent document
    - 'manual': Return conflicts for manual resolution
    """
    try:
        if not documents:
            raise HTTPException(status_code=400, detail="At least one document is required")

        logger.info(f"Merging {len(documents)} documents using {strategy} strategy")

        if strategy == "confidence":
            merged = merge_by_confidence(documents)
        elif strategy == "latest":
            merged = merge_by_latest(documents)
        else:
            merged = documents[0]  # Default: return first document

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "mergedData": merged,
                "strategy": strategy
            }
        )

    except Exception as e:
        logger.error(f"Error merging documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def merge_by_confidence(documents: list) -> dict:
    """Merge documents weighted by confidence scores"""
    # Simple averaging by confidence weight
    total_weight = sum(doc.get("confidence", 0) for doc in documents)
    if total_weight == 0:
        return documents[0]

    merged = {}
    for doc in documents:
        weight = doc.get("confidence", 0) / total_weight
        # Weight document values accordingly
        for key, value in doc.items():
            if key not in merged:
                merged[key] = value
            elif isinstance(value, (int, float)):
                merged[key] = merged.get(key, 0) + (value * weight)

    return merged


def merge_by_latest(documents: list) -> dict:
    """Use most recent document"""
    return max(documents, key=lambda x: x.get("upload_date", ""))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
