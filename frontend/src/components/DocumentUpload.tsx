import React, { useState, useCallback } from 'react';
import { documentsAPI } from '../services/apiClient';

interface DocumentUploadProps {
  childId: string;
  sourceCountry: string;
  onUploadSuccess: (documentId: string, processedData: any) => void;
}

export const DocumentUpload: React.FC<DocumentUploadProps> = ({
  childId,
  sourceCountry,
  onUploadSuccess
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileUpload = useCallback(async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const metadata = {
        documentType: 'report_card',
        childId,
        sourceCountry
      };

      const response = await documentsAPI.upload(file, metadata);
      const { documentId, extractedData } = response.data;

      onUploadSuccess(documentId, extractedData);
    } catch (err: any) {
      setError(err.message || 'Failed to upload document');
    } finally {
      setLoading(false);
    }
  }, [childId, sourceCountry, onUploadSuccess]);

  return (
    <div className="document-upload">
      <h2>Upload School Document</h2>
      <input
        type="file"
        accept="image/*,application/pdf"
        onChange={handleFileUpload}
        disabled={loading}
      />
      {loading && <p>Processing document...</p>}
      {error && <p className="error">{error}</p>}
    </div>
  );
};
