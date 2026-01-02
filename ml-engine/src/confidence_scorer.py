"""
Confidence Scoring Module
- Calculate confidence scores for extracted data
- Assess reliability of information
- Identify uncertain areas
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def calculate_confidence(education_data: Dict[str, Any]) -> Dict[str, float]:
    """
    Calculate confidence score for each extracted component
    
    Returns:
    {
        "overall": 0.85,
        "grade_level": 0.9,
        "subjects": 0.8,
        "details": "..."
    }
    """
    try:
        logger.info("Calculating confidence scores")
        
        confidence = {
            "overall": 0.8,
            "grade_level": 0.85,
            "reading": 0.75,
            "mathematics": 0.75,
            "science": 0.75,
            "subjects": 0.8,
            "source_reliability": 0.85
        }
        
        # Adjust based on available data
        if not education_data.get("grade_level"):
            confidence["grade_level"] = 0.4
            
        if not education_data.get("subjects"):
            confidence["subjects"] = 0.3
        elif len(education_data.get("subjects", {})) >= 3:
            confidence["subjects"] = 0.9
        
        # Adjust overall confidence
        component_scores = [v for k, v in confidence.items() if k != "overall"]
        confidence["overall"] = sum(component_scores) / len(component_scores)
        
        logger.info(f"Confidence calculated: {confidence['overall']:.2%}")
        return confidence
        
    except Exception as e:
        logger.error(f"Error calculating confidence: {str(e)}")
        raise


def assess_document_quality(ocr_text: str, image_metadata: Dict = None) -> Dict[str, Any]:
    """
    Assess quality of document based on:
    - OCR clarity (character recognition rate)
    - Image quality
    - Document age
    - Completeness
    """
    
    quality_score = {
        "ocr_clarity": assess_ocr_clarity(ocr_text),
        "image_quality": assess_image_quality(image_metadata or {}),
        "document_completeness": assess_completeness(ocr_text),
        "overall_quality": 0.8
    }
    
    # Calculate overall quality
    scores = [v for k, v in quality_score.items() if k != "overall_quality"]
    if scores:
        quality_score["overall_quality"] = sum(scores) / len(scores)
    
    return quality_score


def assess_ocr_clarity(ocr_text: str) -> float:
    """
    Assess OCR clarity based on:
    - Presence of common words
    - Consistent spacing
    - Absence of corrupted characters
    """
    
    if not ocr_text:
        return 0.0
    
    # Check for common keywords indicating successful OCR
    keywords = ["grade", "school", "performance", "certificate", "student"]
    found_keywords = sum(1 for kw in keywords if kw.lower() in ocr_text.lower())
    
    # Simple heuristic
    clarity = 0.5 + (found_keywords * 0.1)
    return min(1.0, max(0.0, clarity))


def assess_image_quality(metadata: Dict) -> float:
    """
    Assess quality of original image
    Based on resolution, blur, brightness, etc.
    """
    
    # Simple quality assessment
    # In production: Use image analysis models
    
    quality = 0.7  # Default reasonable quality
    
    # Adjust based on metadata if available
    if metadata.get("resolution_low"):
        quality -= 0.2
    if metadata.get("document_damaged"):
        quality -= 0.3
    if metadata.get("handwritten"):
        quality -= 0.1
    
    return max(0.0, min(1.0, quality))


def assess_completeness(ocr_text: str) -> float:
    """
    Assess document completeness
    Checks for presence of key information fields
    """
    
    required_fields = [
        ("grade", ["grade", "class", "level"]),
        ("name", ["name", "student", "child"]),
        ("date", ["date", "year", "issued"]),
        ("institution", ["school", "institution", "issued by"])
    ]
    
    found_fields = 0
    text_lower = ocr_text.lower()
    
    for field_name, field_keywords in required_fields:
        if any(kw in text_lower for kw in field_keywords):
            found_fields += 1
    
    completeness = found_fields / len(required_fields)
    return max(0.0, min(1.0, completeness))


def identify_uncertain_areas(confidence_scores: Dict[str, float]) -> Dict[str, Any]:
    """
    Identify areas where confidence is low
    Flags information needing verification
    """
    
    uncertain_areas = []
    threshold = 0.7
    
    for component, score in confidence_scores.items():
        if score < threshold:
            uncertain_areas.append({
                "component": component,
                "confidence": score,
                "recommendation": f"Recommend verification of {component}"
            })
    
    return {
        "has_uncertain_areas": len(uncertain_areas) > 0,
        "uncertain_components": uncertain_areas,
        "verification_needed": len(uncertain_areas) > 0
    }


def estimate_verification_difficulty(education_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Estimate how difficult it will be to verify this profile
    Based on:
    - Document age
    - Clarity of information
    - Completeness
    """
    
    difficulty = "moderate"
    difficulty_score = 0.5
    
    # Old documents are harder to verify
    issue_date = education_data.get("issue_date")
    if issue_date:
        from datetime import datetime
        doc_age = (datetime.now() - datetime.fromisoformat(issue_date)).days
        if doc_age > 365 * 5:  # More than 5 years old
            difficulty_score += 0.3
            difficulty = "difficult"
    
    return {
        "difficulty": difficulty,
        "difficulty_score": min(1.0, difficulty_score),
        "verification_required": True,
        "recommended_actions": ["Cross-reference with school records", "Request official documents"]
    }
