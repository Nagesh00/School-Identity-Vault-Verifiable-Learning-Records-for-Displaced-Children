import React, { useState } from 'react';
import { DocumentUpload } from './components/DocumentUpload';
import { LearningProfileSummary } from './components/LearningProfileSummary';
import { VerificationPanel } from './components/VerificationPanel';
import { profilesAPI } from './services/apiClient';

function App() {
  const [profile, setProfile] = useState<any>(null);
  const [documents, setDocuments] = useState<string[]>([]);

  const handleDocumentUploadSuccess = async (documentId: string, extractedData: any) => {
    setDocuments([...documents, documentId]);

    // Create profile after first document
    if (documents.length === 0) {
      try {
        const response = await profilesAPI.create({
          childName: 'Child Name',
          childId: 'child-123',
          documentIds: [documentId],
          sourceCountry: 'Syria'
        });
        setProfile(response.data.profile);
      } catch (error) {
        console.error('Failed to create profile', error);
      }
    }
  };

  return (
    <div className="App">
      <header>
        <h1>School Identity Vault</h1>
        <p>Verifiable Learning Records for Displaced Children</p>
      </header>

      <main>
        <DocumentUpload
          childId="child-123"
          sourceCountry="Syria"
          onUploadSuccess={handleDocumentUploadSuccess}
        />

        {profile && (
          <>
            <LearningProfileSummary profile={profile} />
            <VerificationPanel
              profileId={profile.profileId}
              onVerificationComplete={(verification) => {
                console.log('Verification completed:', verification);
              }}
            />
          </>
        )}
      </main>
    </div>
  );
}

export default App;
