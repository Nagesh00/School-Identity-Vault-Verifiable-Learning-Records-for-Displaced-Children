"""
Document upload and management service
"""
import os
import hashlib
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional
from PIL import Image

from ..models.schemas import UploadedDocument, DocumentType


class DocumentService:
    """Service for handling document uploads and storage"""
    
    def __init__(self, upload_dir: str = "./uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def validate_image(self, file_path: str) -> bool:
        """Validate that the file is a valid image"""
        try:
            img = Image.open(file_path)
            img.verify()
            return True
        except Exception:
            return False
    
    async def save_document(
        self,
        file_content: bytes,
        filename: str,
        document_type: DocumentType,
        uploader_id: str
    ) -> UploadedDocument:
        """Save uploaded document and create record"""
        # Generate unique document ID
        doc_id = str(uuid.uuid4())
        
        # Create file extension
        file_ext = filename.split('.')[-1] if '.' in filename else 'jpg'
        new_filename = f"{doc_id}.{file_ext}"
        file_path = self.upload_dir / new_filename
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        # Validate if image
        if file_ext.lower() in ['jpg', 'jpeg', 'png']:
            if not self.validate_image(str(file_path)):
                os.remove(file_path)
                raise ValueError("Invalid image file")
        
        # Calculate hash
        file_hash = self.calculate_file_hash(str(file_path))
        
        # Create document record
        document = UploadedDocument(
            id=doc_id,
            filename=filename,
            document_type=document_type,
            uploader_id=uploader_id,
            file_path=str(file_path),
            file_hash=file_hash
        )
        
        return document
    
    def get_document_path(self, document_id: str) -> Optional[str]:
        """Get the file path for a document"""
        # Search for file with matching ID
        for file in self.upload_dir.glob(f"{document_id}.*"):
            return str(file)
        return None
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document file"""
        file_path = self.get_document_path(document_id)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
