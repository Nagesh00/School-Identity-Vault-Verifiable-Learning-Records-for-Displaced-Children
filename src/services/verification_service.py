"""
School verification service
"""
import uuid
from typing import List, Optional, Dict
from datetime import datetime, timezone

from ..models.schemas import (
    VerificationRecord,
    VerificationStatus,
    LearningProfile
)


class VerificationService:
    """Service for school verification of learning profiles"""
    
    def __init__(self):
        self.verifications: Dict[str, VerificationRecord] = {}
    
    def create_verification(
        self,
        document_id: str,
        profile_id: str,
        verifier_id: str,
        verifier_name: str,
        status: VerificationStatus,
        notes: Optional[str] = None
    ) -> VerificationRecord:
        """Create a new verification record"""
        verification_id = str(uuid.uuid4())
        
        verification = VerificationRecord(
            verification_id=verification_id,
            document_id=document_id,
            profile_id=profile_id,
            verifier_id=verifier_id,
            verifier_name=verifier_name,
            status=status,
            notes=notes
        )
        
        self.verifications[verification_id] = verification
        return verification
    
    def get_verification(self, verification_id: str) -> Optional[VerificationRecord]:
        """Get verification record by ID"""
        return self.verifications.get(verification_id)
    
    def get_verifications_for_profile(
        self,
        profile_id: str
    ) -> List[VerificationRecord]:
        """Get all verifications for a profile"""
        return [
            v for v in self.verifications.values()
            if v.profile_id == profile_id
        ]
    
    def update_verification_status(
        self,
        verification_id: str,
        status: VerificationStatus,
        notes: Optional[str] = None
    ) -> Optional[VerificationRecord]:
        """Update verification status"""
        verification = self.verifications.get(verification_id)
        if verification:
            verification.status = status
            if notes:
                verification.notes = notes
            verification.verification_date = datetime.now(timezone.utc)
        return verification
    
    def is_profile_verified(self, profile_id: str) -> bool:
        """Check if profile has at least one verified record"""
        verifications = self.get_verifications_for_profile(profile_id)
        return any(v.status == VerificationStatus.VERIFIED for v in verifications)
    
    def get_verification_summary(self, profile_id: str) -> Dict:
        """Get summary of verifications for a profile"""
        verifications = self.get_verifications_for_profile(profile_id)
        
        return {
            'total': len(verifications),
            'verified': sum(1 for v in verifications if v.status == VerificationStatus.VERIFIED),
            'pending': sum(1 for v in verifications if v.status == VerificationStatus.PENDING),
            'rejected': sum(1 for v in verifications if v.status == VerificationStatus.REJECTED)
        }
