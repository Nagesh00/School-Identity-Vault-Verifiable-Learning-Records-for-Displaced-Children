"""
Learning profile reconstruction and curriculum mapping service
"""
import uuid
from typing import List, Dict, Optional
from datetime import datetime

from ..models.schemas import (
    LearningProfile,
    ExtractedData,
    CurriculumMapping
)


class LearningProfileService:
    """Service for creating and managing learning profiles"""
    
    def __init__(self):
        # Standard curriculum mappings (simplified)
        self.curriculum_mappings = {
            'mathematics': ['math', 'maths', 'algebra', 'geometry', 'calculus', 'arithmetic'],
            'science': ['science', 'biology', 'chemistry', 'physics', 'natural science'],
            'language_arts': ['english', 'literature', 'reading', 'writing', 'language'],
            'social_studies': ['history', 'geography', 'social studies', 'civics', 'government'],
            'physical_education': ['pe', 'physical education', 'sports', 'gym'],
            'arts': ['art', 'music', 'drama', 'fine arts', 'visual arts'],
            'computer_science': ['computer', 'computing', 'it', 'information technology', 'programming']
        }
    
    def map_subject_to_curriculum(
        self,
        subject: str,
        target_curriculum: str = "standard"
    ) -> Optional[CurriculumMapping]:
        """Map a subject to target curriculum"""
        subject_lower = subject.lower().strip()
        
        for standard_subject, variants in self.curriculum_mappings.items():
            for variant in variants:
                if variant in subject_lower or subject_lower in variant:
                    # Calculate equivalence based on exact match
                    equivalence = 1.0 if variant == subject_lower else 0.85
                    
                    return CurriculumMapping(
                        original_subject=subject,
                        mapped_subject=standard_subject.replace('_', ' ').title(),
                        equivalence_level=equivalence,
                        target_curriculum=target_curriculum,
                        notes=f"Mapped from '{subject}'"
                    )
        
        # If no mapping found, return with lower equivalence
        return CurriculumMapping(
            original_subject=subject,
            mapped_subject=subject,
            equivalence_level=0.5,
            target_curriculum=target_curriculum,
            notes="No direct mapping found - requires manual review"
        )
    
    def calculate_overall_confidence(
        self,
        extractions: List[ExtractedData],
        mappings: List[CurriculumMapping]
    ) -> float:
        """Calculate overall confidence score for learning profile"""
        if not extractions:
            return 0.0
        
        # Average confidence from extractions
        avg_extraction_confidence = sum(
            e.confidence_score for e in extractions
        ) / len(extractions)
        
        # Average equivalence from mappings
        avg_mapping_confidence = 1.0
        if mappings:
            avg_mapping_confidence = sum(
                m.equivalence_level for m in mappings
            ) / len(mappings)
        
        # Combined confidence (weighted)
        overall = (avg_extraction_confidence * 0.6 + avg_mapping_confidence * 0.4)
        return round(overall, 2)
    
    def reconstruct_learning_profile(
        self,
        student_name: str,
        extractions: List[ExtractedData],
        target_curriculum: str = "standard",
        student_id: Optional[str] = None
    ) -> LearningProfile:
        """Reconstruct learning profile from extracted data"""
        profile_id = str(uuid.uuid4())
        
        # Collect all subjects from extractions
        all_subjects = []
        document_ids = []
        
        for extraction in extractions:
            document_ids.append(extraction.document_id)
            for subject_data in extraction.subjects:
                all_subjects.append(subject_data)
        
        # Create curriculum mappings
        mappings = []
        for subject_data in all_subjects:
            subject_name = subject_data.get('name', '')
            if subject_name:
                mapping = self.map_subject_to_curriculum(
                    subject_name,
                    target_curriculum
                )
                if mapping:
                    mappings.append(mapping)
        
        # Calculate overall confidence
        overall_confidence = self.calculate_overall_confidence(
            extractions,
            mappings
        )
        
        # Create learning profile
        profile = LearningProfile(
            profile_id=profile_id,
            student_name=student_name,
            student_id=student_id,
            documents=document_ids,
            subjects_completed=all_subjects,
            curriculum_mappings=mappings,
            overall_confidence=overall_confidence
        )
        
        return profile
    
    def update_profile(
        self,
        profile: LearningProfile,
        new_extraction: ExtractedData
    ) -> LearningProfile:
        """Update existing profile with new extraction"""
        # Add new document
        if new_extraction.document_id not in profile.documents:
            profile.documents.append(new_extraction.document_id)
        
        # Add new subjects
        for subject_data in new_extraction.subjects:
            subject_name = subject_data.get('name', '')
            
            # Check if subject already exists
            exists = any(
                s.get('name', '').lower() == subject_name.lower()
                for s in profile.subjects_completed
            )
            
            if not exists:
                profile.subjects_completed.append(subject_data)
                
                # Add curriculum mapping
                mapping = self.map_subject_to_curriculum(subject_name)
                if mapping:
                    profile.curriculum_mappings.append(mapping)
        
        # Update last modified date
        profile.last_updated = datetime.utcnow()
        
        return profile
