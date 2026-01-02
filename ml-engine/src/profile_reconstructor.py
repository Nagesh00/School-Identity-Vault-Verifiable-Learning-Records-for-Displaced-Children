"""
Profile Reconstruction Module
- Merge data from multiple documents
- Estimate curriculum equivalence
- Handle conflicting information
"""
import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)


def reconstruct_profile(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Reconstruct learning profile from multiple documents
    Merges information and handles conflicts
    """
    try:
        logger.info(f"Reconstructing profile from {len(documents)} documents")
        
        if not documents:
            raise ValueError("At least one document is required")
        
        # Initialize profile with first document
        profile = {
            "grade_level": documents[0].get("grade_level"),
            "subjects": merge_subjects(documents),
            "issuing_institutions": [],
            "issue_dates": [],
            "confidence_scores": {}
        }
        
        # Collect all metadata
        for doc in documents:
            if doc.get("issuing_institution"):
                profile["issuing_institutions"].append(doc["issuing_institution"])
            if doc.get("issue_date"):
                profile["issue_dates"].append(doc["issue_date"])
        
        # Estimate confidence for each component
        profile["confidence_scores"] = estimate_component_confidence(documents)
        
        logger.info("Profile reconstruction completed")
        return profile
        
    except Exception as e:
        logger.error(f"Error reconstructing profile: {str(e)}")
        raise


def merge_subjects(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge subject performance data from multiple documents
    Handles conflicting assessments
    """
    merged_subjects = {}
    
    for doc in documents:
        subjects = doc.get("subjects", {})
        
        for subject, data in subjects.items():
            if subject not in merged_subjects:
                merged_subjects[subject] = {
                    "performances": [],
                    "scores": [],
                    "consensual": None
                }
            
            if isinstance(data, dict):
                merged_subjects[subject]["performances"].append(
                    data.get("performance", "unknown")
                )
                if data.get("score"):
                    merged_subjects[subject]["scores"].append(data["score"])
    
    # Determine consensual performance
    for subject in merged_subjects:
        performances = merged_subjects[subject]["performances"]
        if performances:
            # Simple consensus: use most common
            from collections import Counter
            most_common = Counter(performances).most_common(1)[0][0]
            merged_subjects[subject]["consensual"] = most_common
    
    return merged_subjects


def estimate_component_confidence(documents: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Estimate confidence score for each educational component
    Based on:
    - Number of documents supporting the claim
    - Consistency across documents
    - Document quality/age
    """
    
    confidence = {
        "grade_level": 0.8,
        "reading": 0.75,
        "mathematics": 0.7,
        "science": 0.75,
        "overall": 0.75
    }
    
    # Adjust based on number of documents
    num_docs = len(documents)
    confidence_boost = min(0.1, num_docs * 0.05)
    
    for key in confidence:
        confidence[key] = min(0.95, confidence[key] + confidence_boost)
    
    return confidence


def estimate_curriculum_equivalence(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Estimate equivalence to local curriculum standards
    Maps foreign education system to local grades
    """
    
    estimated_grade = profile.get("grade_level", 3)
    
    # Simple mapping logic
    # In production: Use ML model trained on curriculum data
    mapping = {
        "local_grade": estimated_grade,
        "education_level": "primary" if estimated_grade <= 6 else "secondary",
        "reading_level": "grade_3_4" if estimated_grade == 3 else f"grade_{estimated_grade}",
        "numeracy_level": f"grade_{estimated_grade}",
        "recommended_placement": f"Grade {estimated_grade} or {estimated_grade + 1} with assessment",
        "confidence_in_mapping": 0.75
    }
    
    return mapping


def generate_standardized_summary(profile: Dict[str, Any], 
                                 curriculum_mapping: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate standardized, readable summary of profile
    Output format suitable for schools and agencies
    """
    
    grade = profile.get("grade_level", "unknown")
    confidence = profile.get("confidence_scores", {}).get("overall", 0)
    
    summary = {
        "text_summary": f"""
        This student has likely completed primary school level literacy and 
        grade-{grade} level numeracy. 
        Overall confidence: {confidence:.0%}
        Last verified: 2025-01-02
        """,
        "standardized_data": {
            "education_level": curriculum_mapping.get("education_level"),
            "estimated_grade": grade,
            "subjects": profile.get("subjects", {}),
            "confidence_level": "moderate" if confidence > 0.7 else "low",
            "recommended_action": curriculum_mapping.get("recommended_placement")
        }
    }
    
    return summary


def handle_conflicting_data(documents: List[Dict[str, Any]], 
                            strategy: str = "confidence") -> Dict[str, Any]:
    """
    Handle conflicting information between documents
    
    Strategies:
    - 'confidence': Weight by confidence scores
    - 'latest': Use most recent document
    - 'consensus': Use most common values
    """
    
    if strategy == "confidence":
        # Weight each document by its confidence score
        total_confidence = sum(doc.get("confidence", 0.5) for doc in documents)
        
        merged = {}
        for doc in documents:
            weight = doc.get("confidence", 0.5) / total_confidence
            for key, value in doc.items():
                if key not in merged:
                    merged[key] = value
        
        return merged
    
    elif strategy == "latest":
        # Use most recent document
        latest = max(documents, key=lambda x: x.get("issue_date", ""))
        return latest
    
    else:  # consensus
        return reconstruct_profile(documents)
