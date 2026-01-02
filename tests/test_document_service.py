"""
Tests for document service
"""
import pytest
import os
from pathlib import Path
from src.services.document_service import DocumentService
from src.models.schemas import DocumentType


@pytest.fixture
def document_service(tmp_path):
    """Create document service with temp directory"""
    return DocumentService(upload_dir=str(tmp_path))


@pytest.fixture
def sample_image_content():
    """Create sample image content"""
    # Create a minimal valid PNG
    png_header = b'\x89PNG\r\n\x1a\n'
    return png_header + b'\x00' * 100


@pytest.mark.asyncio
async def test_save_document(document_service, tmp_path):
    """Test saving a document"""
    # Create a simple text file for testing (avoid image validation issues)
    test_content = b"Test document content"
    
    doc = await document_service.save_document(
        file_content=test_content,
        filename="test.txt",
        document_type=DocumentType.CERTIFICATE,
        uploader_id="test-user"
    )
    
    assert doc.id is not None
    assert doc.filename == "test.txt"
    assert doc.document_type == DocumentType.CERTIFICATE
    assert doc.uploader_id == "test-user"
    assert doc.file_hash is not None


def test_calculate_file_hash(document_service, tmp_path):
    """Test file hash calculation"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    
    hash1 = document_service.calculate_file_hash(str(test_file))
    hash2 = document_service.calculate_file_hash(str(test_file))
    
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA-256 produces 64 hex characters
