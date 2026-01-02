import React from 'react';

interface LearningProfileSummaryProps {
  profile: {
    childName: string;
    summary: {
      textSummary: string;
      standardizedFormat: {
        educationLevel: string;
        estimatedGrade: number;
        subjects: Record<string, any>;
        confidenceLevel: string;
      };
    };
  };
}

export const LearningProfileSummary: React.FC<LearningProfileSummaryProps> = ({ profile }) => {
  return (
    <div className="learning-profile-summary">
      <h2>Learning Profile: {profile.childName}</h2>
      
      <div className="summary-text">
        <p>{profile.summary.textSummary}</p>
      </div>

      <div className="standardized-format">
        <h3>Standardized Information</h3>
        <table>
          <tbody>
            <tr>
              <td>Education Level</td>
              <td>{profile.summary.standardizedFormat.educationLevel}</td>
            </tr>
            <tr>
              <td>Estimated Grade</td>
              <td>{profile.summary.standardizedFormat.estimatedGrade}</td>
            </tr>
            <tr>
              <td>Confidence</td>
              <td>{profile.summary.standardizedFormat.confidenceLevel}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="subjects">
        <h3>Subject Performance</h3>
        {Object.entries(profile.summary.standardizedFormat.subjects).map(([subject, data]: [string, any]) => (
          <div key={subject} className="subject-item">
            <strong>{subject}</strong>: {data.performance || 'N/A'}
          </div>
        ))}
      </div>
    </div>
  );
};
