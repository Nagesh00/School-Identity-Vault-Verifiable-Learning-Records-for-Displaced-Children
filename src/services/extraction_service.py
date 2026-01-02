"""
AI-powered data extraction from educational documents using Microsoft Azure AI Services
This implementation uses Azure AI Document Intelligence and Azure OpenAI Service
to comply with Microsoft Imagine Cup 2026 requirements.
"""
import re
import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from PIL import Image

# Microsoft Azure AI Services (Imagine Cup 2026 requirement)
try:
    from azure.ai.formrecognizer import DocumentAnalysisClient
    from azure.core.credentials import AzureKeyCredential
    AZURE_DOCUMENT_INTELLIGENCE_AVAILABLE = True
except ImportError:
    AZURE_DOCUMENT_INTELLIGENCE_AVAILABLE = False

try:
    from openai import AzureOpenAI
    AZURE_OPENAI_AVAILABLE = True
except ImportError:
    AZURE_OPENAI_AVAILABLE = False

# Fallback OCR option
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False

from ..models.schemas import ExtractedData


class AIExtractionService:
    """
    Service for extracting data from educational documents using Microsoft Azure AI Services.
    
    This implementation uses:
    1. Azure AI Document Intelligence for OCR and layout analysis
    2. Azure OpenAI Service for intelligent text processing
    
    These Microsoft AI services are required for Imagine Cup 2026 compliance.
    """
    
    def __init__(
        self,
        azure_doc_endpoint: Optional[str] = None,
        azure_doc_key: Optional[str] = None,
        azure_openai_endpoint: Optional[str] = None,
        azure_openai_key: Optional[str] = None,
        azure_openai_deployment: Optional[str] = None
    ):
        """
        Initialize AI Extraction Service with Microsoft Azure AI Services.
        
        Args:
            azure_doc_endpoint: Azure Document Intelligence endpoint
            azure_doc_key: Azure Document Intelligence key
            azure_openai_endpoint: Azure OpenAI endpoint
            azure_openai_key: Azure OpenAI key
            azure_openai_deployment: Azure OpenAI deployment name
        """
        self.azure_doc_client = None
        self.azure_openai_client = None
        
        # Initialize Azure AI Document Intelligence (Microsoft AI Service #1)
        if azure_doc_endpoint and azure_doc_key and AZURE_DOCUMENT_INTELLIGENCE_AVAILABLE:
            try:
                self.azure_doc_client = DocumentAnalysisClient(
                    endpoint=azure_doc_endpoint,
                    credential=AzureKeyCredential(azure_doc_key)
                )
            except Exception as e:
                print(f"Azure Document Intelligence initialization failed: {e}")
        
        # Initialize Azure OpenAI Service (Microsoft AI Service #2)
        if azure_openai_endpoint and azure_openai_key and AZURE_OPENAI_AVAILABLE:
            try:
                self.azure_openai_client = AzureOpenAI(
                    api_key=azure_openai_key,
                    api_version="2024-02-15-preview",
                    azure_endpoint=azure_openai_endpoint
                )
                self.azure_openai_deployment = azure_openai_deployment
            except Exception as e:
                print(f"Azure OpenAI initialization failed: {e}")
    
    def extract_text_with_azure_document_intelligence(self, image_path: str) -> tuple[str, Dict]:
        """
        Extract text from image using Azure AI Document Intelligence.
        
        This is Microsoft AI Service #1 for Imagine Cup 2026.
        
        Returns:
            Tuple of (extracted_text, structured_data)
        """
        if not self.azure_doc_client:
            return self._fallback_ocr(image_path), {}
        
        try:
            with open(image_path, "rb") as f:
                poller = self.azure_doc_client.begin_analyze_document(
                    "prebuilt-document", document=f
                )
                result = poller.result()
            
            # Extract text content
            text_content = result.content
            
            # Extract structured data (key-value pairs, tables)
            structured_data = {
                'key_value_pairs': {},
                'tables': []
            }
            
            # Extract key-value pairs
            if result.key_value_pairs:
                for kv_pair in result.key_value_pairs:
                    if kv_pair.key and kv_pair.value:
                        key = kv_pair.key.content
                        value = kv_pair.value.content
                        structured_data['key_value_pairs'][key] = value
            
            # Extract tables
            if result.tables:
                for table in result.tables:
                    table_data = []
                    for cell in table.cells:
                        table_data.append({
                            'row': cell.row_index,
                            'col': cell.column_index,
                            'content': cell.content
                        })
                    structured_data['tables'].append(table_data)
            
            return text_content, structured_data
            
        except Exception as e:
            print(f"Azure Document Intelligence extraction failed: {e}")
            return self._fallback_ocr(image_path), {}
    
    def _fallback_ocr(self, image_path: str) -> str:
        """Fallback OCR using Tesseract if Azure services unavailable"""
        if not TESSERACT_AVAILABLE:
            return "OCR not available. Please configure Azure Document Intelligence."
        
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def enhance_extraction_with_azure_openai(self, text: str, structured_data: Dict) -> Dict:
        """
        Enhance extraction using Azure OpenAI Service for intelligent parsing.
        
        This is Microsoft AI Service #2 for Imagine Cup 2026.
        
        Args:
            text: Raw extracted text
            structured_data: Structured data from Document Intelligence
            
        Returns:
            Enhanced parsed data with student information
        """
        if not self.azure_openai_client:
            return self._fallback_parsing(text)
        
        try:
            # Create prompt for Azure OpenAI
            prompt = f"""
Extract the following information from this educational document text:
- Student Name
- Student ID
- Institution Name
- Issue Date
- List of subjects with grades

Text:
{text}

Structured Data:
{json.dumps(structured_data.get('key_value_pairs', {}), indent=2)}

Return the information in JSON format with keys: student_name, student_id, institution_name, issue_date, subjects (array of {{name, grade}})
"""
            
            response = self.azure_openai_client.chat.completions.create(
                model=self.azure_openai_deployment,
                messages=[
                    {"role": "system", "content": "You are an AI assistant that extracts structured data from educational documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            # Parse the response
            result_text = response.choices[0].message.content
            
            # Try to extract JSON from response
            try:
                # Find JSON in the response
                json_start = result_text.find('{')
                json_end = result_text.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = result_text[json_start:json_end]
                    parsed_data = json.loads(json_str)
                    return parsed_data
            except:
                pass
            
            # Fallback to regex parsing
            return self._fallback_parsing(text)
            
        except Exception as e:
            print(f"Azure OpenAI enhancement failed: {e}")
            return self._fallback_parsing(text)
    
    def _fallback_parsing(self, text: str) -> Dict:
        """Fallback parsing using regex patterns"""
        return self.parse_educational_data(text)
    
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
        """
        Extract data from educational document using Microsoft Azure AI Services.
        
        This method uses both Azure AI Document Intelligence and Azure OpenAI Service,
        meeting Imagine Cup 2026 requirement of using at least two Microsoft AI services.
        """
        # Step 1: Extract text using Azure AI Document Intelligence (Microsoft AI Service #1)
        raw_text, structured_data = self.extract_text_with_azure_document_intelligence(file_path)
        
        # Step 2: Enhance extraction using Azure OpenAI Service (Microsoft AI Service #2)
        parsed_data = self.enhance_extraction_with_azure_openai(raw_text, structured_data)
        
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
