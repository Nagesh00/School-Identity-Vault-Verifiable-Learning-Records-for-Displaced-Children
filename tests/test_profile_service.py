"""
Tests for learning profile service
"""
import pytest
from src.services.profile_service import LearningProfileService
from src.models.schemas import ExtractedData


@pytest.fixture
def profile_service():
    """Create profile service"""
    return LearningProfileService()


@pytest.fixture
def sample_extraction():
    """Create sample extraction data"""
    return ExtractedData(
        document_id="doc-001",
        student_name="Jane Smith",
        student_id="STU-002",
        institution_name="XYZ School",
        issue_date="15/06/2023",
        subjects=[
            {'name': 'Mathematics', 'grade': 'A'},
            {'name': 'Science', 'grade': 'B+'}
        ],
        grades=[
            {'subject': 'Mathematics', 'grade': 'A'},
            {'subject': 'Science', 'grade': 'B+'}
        ],
        raw_text="Sample text",
        confidence_score=0.9
    )


def test_map_subject_to_curriculum(profile_service):
    """Test subject to curriculum mapping"""
    mapping = profile_service.map_subject_to_curriculum("Mathematics", "standard")
    
    assert mapping is not None
    assert mapping.original_subject == "Mathematics"
    assert mapping.equivalence_level > 0.0


def test_reconstruct_learning_profile(profile_service, sample_extraction):
    """Test learning profile reconstruction"""
    profile = profile_service.reconstruct_learning_profile(
        student_name="Jane Smith",
        extractions=[sample_extraction],
        target_curriculum="standard"
    )
    
    assert profile.student_name == "Jane Smith"
    assert len(profile.documents) == 1
    assert len(profile.subjects_completed) == 2
    assert profile.overall_confidence > 0.0


def test_calculate_overall_confidence(profile_service, sample_extraction):
    """Test overall confidence calculation"""
    mappings = [
        profile_service.map_subject_to_curriculum("Mathematics", "standard"),
        profile_service.map_subject_to_curriculum("Science", "standard")
    ]
    
    confidence = profile_service.calculate_overall_confidence(
        [sample_extraction],
        mappings
    )
    
    assert 0.0 <= confidence <= 1.0
