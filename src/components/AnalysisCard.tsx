import React from 'react';

interface AnalysisCardProps {
  tier: string;
  dailyScans: number;
}

const AnalysisCard: React.FC<AnalysisCardProps> = ({ tier, dailyScans }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Analysis Summary</h2>
      <p>Tier: {tier}</p>
      <p>Daily Scans: {dailyScans}</p>
      {/* Add more analysis details here */}
    </div>
  );
};

export default AnalysisCard;
