import React, { useState } from 'react';
import { analyzeProfileRealtime } from '../services/api';
import AnalysisVisualization from './AnalysisVisualization';
import FeedbackForm from './FeedbackForm';

const RealTimeAnalysis: React.FC = () => {
  const [profileUrl, setProfileUrl] = useState('');
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalysis = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await analyzeProfileRealtime({ profile_url: profileUrl });
      setAnalysisResult(result);
    } catch (err) {
      setError('Failed to analyze profile. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-semibold mb-4">Real-Time Profile Analysis</h2>
      <div className="mb-4">
        <input
          type="text"
          value={profileUrl}
          onChange={(e) => setProfileUrl(e.target.value)}
          placeholder="Enter profile URL"
          className="w-full p-2 border rounded"
        />
      </div>
      <button
        onClick={handleAnalysis}
        disabled={isLoading}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-blue-300"
      >
        {isLoading ? 'Analyzing...' : 'Analyze Profile'}
      </button>
      {error && <p className="text-red-500 mt-2">{error}</p>}
      {analysisResult && (
        <div className="mt-4">
          <h3 className="text-xl font-semibold mb-2">Analysis Result:</h3>
          <AnalysisVisualization
            features={analysisResult.features}
            result={analysisResult.result}
            confidence={analysisResult.confidence}
          />
          <FeedbackForm analysisId={analysisResult.id} />
        </div>
      )}
    </div>
  );
};

export default RealTimeAnalysis;
