"""
AI-powered data extraction from educational documents
"""
import re
import json
from typing import Dict, List, Optional
from datetime import datetime
from PIL import Image

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from ..models.schemas import ExtractedData


class AIExtractionService:
    """Service for extracting data from educational documents using AI/OCR"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_client = None
        if openai_api_key and OPENAI_AVAILABLE:
            try:
                self.openai_client = OpenAI(api_key=openai_api_key)
            except Exception:
                pass
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from image using OCR"""
        if not TESSERACT_AVAILABLE:
            return "OCR not available. Please install pytesseract."
        
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def parse_educational_data(self, text: str) -> Dict:
        """Parse educational data from extracted text"""
        data = {
            'student_name': None,
            'student_id': None,
            'institution_name': None,
            'issue_date': None,
            'subjects': [],
            'grades': []
        }
        
        # Parse student name (look for common patterns)
        name_patterns = [
            r'(?:Name|Student Name|Student):\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'(?:Name|Student Name|Student)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        ]
        for pattern in name_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['student_name'] = match.group(1).strip()
                break
        
        # Parse student ID
        id_patterns = [
            r'(?:Student ID|ID No|Roll No|Registration No):\s*([A-Z0-9]+)',
            r'(?:Student ID|ID No|Roll No|Registration No)\s+([A-Z0-9]+)',
        ]
        for pattern in id_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['student_id'] = match.group(1).strip()
                break
        
        # Parse institution name
        institution_patterns = [
            r'(?:School|College|University|Institution):\s*([A-Z][^\n]+)',
            r'([A-Z][^\n]+(?:School|College|University|Institute))',
        ]
        for pattern in institution_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data['institution_name'] = match.group(1).strip()
                break
        
        # Parse date
        date_patterns = [
            r'(?:Date|Issue Date|Issued on):\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
        ]
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                data['issue_date'] = match.group(1).strip()
                break
        
        # Parse subjects and grades (simplified)
        # Look for lines with subject and grade patterns
        lines = text.split('\n')
        for line in lines:
            # Pattern: Subject name followed by grade
            grade_match = re.search(
                r'([A-Za-z\s]+)\s+([A-F][\+\-]?|\d{1,3}%?|Pass|Fail)',
                line,
                re.IGNORECASE
            )
            if grade_match:
                subject = grade_match.group(1).strip()
                grade = grade_match.group(2).strip()
                if len(subject) > 3 and len(subject) < 50:  # Reasonable subject name length
                    data['subjects'].append({'name': subject, 'grade': grade})
                    data['grades'].append({'subject': subject, 'grade': grade})
        
        return data
    
    def calculate_confidence_score(
        self,
        extracted_data: Dict,
        raw_text: str
    ) -> float:
        """Calculate confidence score based on extracted data quality"""
        score = 0.0
        max_score = 5.0
        
        # Check for key fields
        if extracted_data.get('student_name'):
            score += 1.0
        if extracted_data.get('student_id'):
            score += 0.5
        if extracted_data.get('institution_name'):
            score += 1.0
        if extracted_data.get('issue_date'):
            score += 0.5
        if extracted_data.get('subjects'):
            score += min(len(extracted_data['subjects']) * 0.2, 2.0)
        
        # Adjust based on text quality
        if len(raw_text) > 50:
            score += 0.5
        
        return min(score / max_score, 1.0)
    
    async def extract_from_document(
        self,
        document_id: str,
        file_path: str
    ) -> ExtractedData:
        """Extract data from educational document"""
        # Extract text from image
        raw_text = self.extract_text_from_image(file_path)
        
        # Parse educational data
        parsed_data = self.parse_educational_data(raw_text)
        
        # Calculate confidence score
        confidence = self.calculate_confidence_score(parsed_data, raw_text)
        
        # Create ExtractedData object
        extracted = ExtractedData(
            document_id=document_id,
            student_name=parsed_data.get('student_name'),
            student_id=parsed_data.get('student_id'),
            institution_name=parsed_data.get('institution_name'),
            issue_date=parsed_data.get('issue_date'),
            subjects=parsed_data.get('subjects', []),
            grades=parsed_data.get('grades', []),
            raw_text=raw_text,
            confidence_score=confidence
        )
        
        return extracted
