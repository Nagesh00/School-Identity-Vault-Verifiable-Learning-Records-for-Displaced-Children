"""
Tests for extraction service
"""
import pytest
from src.services.extraction_service import AIExtractionService


@pytest.fixture
def extraction_service():
    """Create extraction service"""
    return AIExtractionService()


def test_parse_educational_data(extraction_service):
    """Test parsing educational data from text"""
    text = """
    ABC School
    Student Name: John Doe
    Student ID: STU-001
    Date: 01/01/2023
    
    Mathematics A
    Science B+
    English A-
    """
    
    data = extraction_service.parse_educational_data(text)
    
    assert data['student_name'] == 'John Doe'
    assert data['student_id'] == 'STU-001'
    assert len(data['subjects']) > 0


def test_calculate_confidence_score(extraction_service):
    """Test confidence score calculation"""
    data = {
        'student_name': 'John Doe',
        'student_id': 'STU-001',
        'institution_name': 'ABC School',
        'issue_date': '01/01/2023',
        'subjects': [{'name': 'Math', 'grade': 'A'}]
    }
    
    score = extraction_service.calculate_confidence_score(data, "sample text")
    
    assert 0.0 <= score <= 1.0
    assert score > 0.0  # Should have some confidence with this data
