import React from 'react';

interface ContributionPanelProps {
  contributions: {
    verifiedProfiles: number;
    validReports: number;
    feedbackCount: number;
  };
}

const ContributionPanel: React.FC<ContributionPanelProps> = ({ contributions }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Your Contributions</h2>
      <ul>
        <li>Verified Profiles: {contributions.verifiedProfiles}</li>
        <li>Valid Reports: {contributions.validReports}</li>
        <li>Feedback Count: {contributions.feedbackCount}</li>
      </ul>
    </div>
  );
};

export default ContributionPanel;
