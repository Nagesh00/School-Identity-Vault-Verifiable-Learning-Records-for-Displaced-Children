"""
Tests for blockchain service
"""
import pytest
from src.services.blockchain_service import BlockchainService
from src.services.profile_service import LearningProfileService
from src.models.schemas import ExtractedData


@pytest.fixture
def blockchain_service():
    """Create blockchain service"""
    return BlockchainService()


@pytest.fixture
def sample_profile():
    """Create sample learning profile"""
    profile_service = LearningProfileService()
    extraction = ExtractedData(
        document_id="doc-001",
        student_name="Test Student",
        subjects=[{'name': 'Math', 'grade': 'A'}],
        grades=[],
        raw_text="Test",
        confidence_score=0.8
    )
    return profile_service.reconstruct_learning_profile(
        student_name="Test Student",
        extractions=[extraction]
    )


def test_hash_profile(blockchain_service, sample_profile):
    """Test profile hashing"""
    hash1 = blockchain_service.hash_profile(sample_profile)
    hash2 = blockchain_service.hash_profile(sample_profile)
    
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA-256


def test_sign_and_verify(blockchain_service):
    """Test signature creation and verification"""
    test_hash = "test_hash_value"
    
    signature = blockchain_service.sign_hash(test_hash)
    is_valid = blockchain_service.verify_signature(test_hash, signature)
    
    assert is_valid
    
    # Test with wrong hash
    is_valid_wrong = blockchain_service.verify_signature("wrong_hash", signature)
    assert not is_valid_wrong


@pytest.mark.asyncio
async def test_store_on_blockchain(blockchain_service, sample_profile):
    """Test blockchain storage"""
    record = await blockchain_service.store_on_blockchain(sample_profile)
    
    assert record.profile_id == sample_profile.profile_id
    assert record.document_hash is not None
    assert record.signature is not None


def test_verify_blockchain_record(blockchain_service, sample_profile):
    """Test blockchain record verification"""
    import asyncio
    
    # Create record
    record = asyncio.run(blockchain_service.store_on_blockchain(sample_profile))
    
    # Verify
    is_valid = blockchain_service.verify_blockchain_record(record, sample_profile)
    assert is_valid
