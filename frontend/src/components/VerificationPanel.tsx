import React, { useState, useEffect } from 'react';
import { verificationAPI } from '../services/apiClient';

interface VerificationProps {
  profileId: string;
  onVerificationComplete: (verificationData: any) => void;
}

export const VerificationPanel: React.FC<VerificationProps> = ({
  profileId,
  onVerificationComplete
}) => {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [isVerified, setIsVerified] = useState(false);
  const [notes, setNotes] = useState('');

  useEffect(() => {
    loadVerificationHistory();
  }, [profileId]);

  const loadVerificationHistory = async () => {
    try {
      const response = await verificationAPI.getHistory(profileId);
      setHistory(response.data.history);
    } catch (error) {
      console.error('Failed to load verification history', error);
    }
  };

  const handleVerify = async () => {
    setLoading(true);
    try {
      const response = await verificationAPI.verify({
        profileId,
        schoolId: 'school-123',
        schoolName: 'Local School Name',
        isVerified,
        verificationNotes: notes
      });

      const verificationId = response.data.verification.verificationId;

      // Sign the verification
      await verificationAPI.addSignature(verificationId, 'mock-private-key');

      // Submit to blockchain
      await verificationAPI.submitToBlockchain(verificationId);

      onVerificationComplete(response.data.verification);
      loadVerificationHistory();
    } catch (error) {
      console.error('Verification failed', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="verification-panel">
      <h2>Profile Verification</h2>
      
      <div className="verification-form">
        <label>
          <input
            type="checkbox"
            checked={isVerified}
            onChange={(e) => setIsVerified(e.target.checked)}
          />
          I verify this profile is accurate
        </label>

        <textarea
          placeholder="Verification notes..."
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />

        <button onClick={handleVerify} disabled={loading}>
          {loading ? 'Verifying...' : 'Submit Verification'}
        </button>
      </div>

      <div className="verification-history">
        <h3>Verification History</h3>
        {history.map((v) => (
          <div key={v.verificationId} className="verification-entry">
            <p>
              <strong>{v.schoolName}</strong> - {new Date(v.verificationDate).toLocaleDateString()}
            </p>
            <p>Status: <span className={v.isVerified ? 'verified' : 'unverified'}>{v.status}</span></p>
          </div>
        ))}
      </div>
    </div>
  );
};
