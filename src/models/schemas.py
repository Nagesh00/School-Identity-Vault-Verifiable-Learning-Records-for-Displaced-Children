"""
Data models for School Identity Vault
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """Types of education documents"""
    CERTIFICATE = "certificate"
    REPORT_CARD = "report_card"
    TRANSCRIPT = "transcript"
    DIPLOMA = "diploma"
    OTHER = "other"


class VerificationStatus(str, Enum):
    """Status of document verification"""
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


class UploadedDocument(BaseModel):
    """Model for uploaded document"""
    id: str
    filename: str
    document_type: DocumentType
    upload_date: datetime = Field(default_factory=datetime.utcnow)
    uploader_id: str
    file_path: str
    file_hash: str


class ExtractedData(BaseModel):
    """Model for data extracted from document"""
    document_id: str
    student_name: Optional[str] = None
    student_id: Optional[str] = None
    institution_name: Optional[str] = None
    issue_date: Optional[str] = None
    subjects: List[Dict[str, any]] = []
    grades: List[Dict[str, any]] = []
    raw_text: str
    confidence_score: float
    extraction_date: datetime = Field(default_factory=datetime.utcnow)


class CurriculumMapping(BaseModel):
    """Model for curriculum mapping"""
    original_subject: str
    mapped_subject: str
    equivalence_level: float
    target_curriculum: str
    notes: Optional[str] = None


class LearningProfile(BaseModel):
    """Model for student learning profile"""
    profile_id: str
    student_name: str
    student_id: Optional[str] = None
    documents: List[str] = []
    subjects_completed: List[Dict[str, any]] = []
    curriculum_mappings: List[CurriculumMapping] = []
    overall_confidence: float
    created_date: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class VerificationRecord(BaseModel):
    """Model for school verification"""
    verification_id: str
    document_id: str
    profile_id: str
    verifier_id: str
    verifier_name: str
    status: VerificationStatus
    notes: Optional[str] = None
    verification_date: datetime = Field(default_factory=datetime.utcnow)


class BlockchainRecord(BaseModel):
    """Model for blockchain record"""
    record_id: str
    profile_id: str
    document_hash: str
    signature: str
    transaction_hash: Optional[str] = None
    block_number: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
