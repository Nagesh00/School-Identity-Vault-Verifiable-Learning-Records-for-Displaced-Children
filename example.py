#!/usr/bin/env python3
"""
Example usage script for School Identity Vault
Demonstrates the complete workflow using Microsoft Azure AI Services (Imagine Cup 2026)

Note: This demo uses fallback mode for testing without Azure credentials.
For full Azure AI functionality, configure Azure credentials in .env file.
"""
import asyncio
import os
from pathlib import Path

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from src.models.schemas import DocumentType, VerificationStatus
from src.services import (
    DocumentService,
    AIExtractionService,
    LearningProfileService,
    VerificationService,
    BlockchainService
)


async def main():
    """Demonstrate the School Identity Vault workflow"""
    print("=" * 70)
    print("School Identity Vault - Example Workflow")
    print("Microsoft Imagine Cup 2026 - Azure AI Services")
    print("=" * 70)
    print()
    
    # Initialize services with Azure AI (will use fallback if not configured)
    print("1. Initializing services...")
    print("   Note: Demo mode - configure Azure credentials for full AI features")
    document_service = DocumentService(upload_dir="./uploads")
    extraction_service = AIExtractionService(
        azure_doc_endpoint=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"),
        azure_doc_key=os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY"),
        azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_openai_key=os.getenv("AZURE_OPENAI_KEY"),
        azure_openai_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT")
    )
    profile_service = LearningProfileService()
    verification_service = VerificationService()
    blockchain_service = BlockchainService()
    print("   ✓ All services initialized")
    print()
    
    # Step 1: Upload document (simulated)
    print("2. Document Upload Simulation")
    print("   Simulating upload of a student report card...")
    
    # Create a simulated document
    simulated_text = """
    ABC International School
    
    Student Report Card
    
    Name: Ahmed Khan
    Student ID: STU-2024-001
    Grade: 8
    Date: 15/06/2023
    
    Subject Grades:
    Mathematics        A
    Science            B+
    English            A-
    History            B
    Physical Education A
    """
    
    # For demonstration, we'll create a simple text file
    demo_file = Path("./uploads/demo_report.txt")
    demo_file.parent.mkdir(exist_ok=True)
    demo_file.write_text(simulated_text)
    
    # Simulate document upload
    with open(demo_file, 'rb') as f:
        content = f.read()
    
    document = await document_service.save_document(
        file_content=content,
        filename="ahmed_report_card.txt",
        document_type=DocumentType.REPORT_CARD,
        uploader_id="NGO-001"
    )
    
    print(f"   ✓ Document uploaded: {document.id}")
    print(f"   ✓ File hash: {document.file_hash[:16]}...")
    print()
    
    # Step 2: Extract data using Microsoft Azure AI
    print("3. Microsoft Azure AI Data Extraction")
    print("   Using Azure Document Intelligence + Azure OpenAI Service...")
    print("   (Fallback mode active - configure Azure for full features)")
    
    # For text file, we'll use the text directly
    parsed_data = extraction_service.parse_educational_data(simulated_text)
    
    from src.models.schemas import ExtractedData
    extracted = ExtractedData(
        document_id=document.id,
        student_name=parsed_data.get('student_name'),
        student_id=parsed_data.get('student_id'),
        institution_name=parsed_data.get('institution_name'),
        issue_date=parsed_data.get('issue_date'),
        subjects=parsed_data.get('subjects', []),
        grades=parsed_data.get('grades', []),
        raw_text=simulated_text,
        confidence_score=0.85
    )
    
    print(f"   ✓ Student Name: {extracted.student_name}")
    print(f"   ✓ Student ID: {extracted.student_id}")
    print(f"   ✓ Institution: {extracted.institution_name}")
    print(f"   ✓ Subjects found: {len(extracted.subjects)}")
    print(f"   ✓ Confidence Score: {extracted.confidence_score:.2%}")
    print()
    
    # Step 3: Create Learning Profile
    print("4. Learning Profile Reconstruction")
    print("   Creating learning profile with curriculum mapping...")
    
    profile = profile_service.reconstruct_learning_profile(
        student_name=extracted.student_name or "Ahmed Khan",
        extractions=[extracted],
        target_curriculum="International",
        student_id=extracted.student_id
    )
    
    print(f"   ✓ Profile ID: {profile.profile_id}")
    print(f"   ✓ Student: {profile.student_name}")
    print(f"   ✓ Subjects completed: {len(profile.subjects_completed)}")
    print(f"   ✓ Overall confidence: {profile.overall_confidence:.2%}")
    print()
    
    print("   Curriculum Mappings:")
    for mapping in profile.curriculum_mappings[:3]:
        print(f"     • {mapping.original_subject} → {mapping.mapped_subject}")
        print(f"       Equivalence: {mapping.equivalence_level:.0%}")
    print()
    
    # Step 4: School Verification
    print("5. School Verification")
    print("   Creating verification record...")
    
    verification = verification_service.create_verification(
        document_id=document.id,
        profile_id=profile.profile_id,
        verifier_id="SCHOOL-001",
        verifier_name="Lincoln High School",
        status=VerificationStatus.VERIFIED,
        notes="Documents verified and accepted for enrollment"
    )
    
    print(f"   ✓ Verification ID: {verification.verification_id}")
    print(f"   ✓ Verifier: {verification.verifier_name}")
    print(f"   ✓ Status: {verification.status.value}")
    print()
    
    # Step 5: Blockchain Storage
    print("6. Blockchain Integration")
    print("   Storing cryptographic hash and signature...")
    
    blockchain_record = await blockchain_service.store_on_blockchain(profile)
    
    print(f"   ✓ Record ID: {blockchain_record.record_id}")
    print(f"   ✓ Document Hash: {blockchain_record.document_hash[:32]}...")
    print(f"   ✓ Digital Signature: {blockchain_record.signature[:32]}...")
    if blockchain_record.transaction_hash:
        print(f"   ✓ Transaction Hash: {blockchain_record.transaction_hash}")
    else:
        print(f"   ℹ Blockchain not connected (simulation mode)")
    print()
    
    # Step 6: Verification
    print("7. Record Verification")
    print("   Verifying blockchain record integrity...")
    
    is_valid = blockchain_service.verify_blockchain_record(
        blockchain_record,
        profile
    )
    
    print(f"   ✓ Record is valid: {is_valid}")
    print()
    
    # Summary
    print("=" * 70)
    print("Workflow Complete!")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  • Documents processed: 1")
    print(f"  • Students with profiles: 1")
    print(f"  • Verifications completed: 1")
    print(f"  • Blockchain records created: 1")
    print()
    print("The learning profile is now:")
    print("  ✓ Extracted from uploaded documents")
    print("  ✓ Mapped to target curriculum")
    print("  ✓ Verified by school officials")
    print("  ✓ Secured with cryptographic signatures")
    print("  ✓ Stored on blockchain (tamper-proof)")
    print()
    print("This profile is portable and can be used to prove educational")
    print("credentials for displaced children worldwide.")
    print()


if __name__ == "__main__":
    asyncio.run(main())
