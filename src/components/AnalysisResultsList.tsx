import React, { useState, useEffect } from 'react';
import { getAnalysisResult, AnalysisResult } from '../services/api';

const AnalysisResultsList: React.FC = () => {
  const [results, setResults] = useState<AnalysisResult[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await getAnalysisResult('recent');
        setResults(response.data);
      } catch (error) {
        console.error('Error fetching analysis results:', error);
        setError('Failed to fetch analysis results. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchResults();
  }, []);

  if (isLoading) {
    return <div>Loading analysis results...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Analysis Results</h2>
      {results.length === 0 ? (
        <p>No analysis results found.</p>
      ) : (
        results.map((result) => (
          <div key={result.id} className="bg-gray-100 p-4 rounded-lg mb-4">
            <p><strong>Profile:</strong> {result.profile_id}</p>
            <p><strong>Result:</strong> {result.result}</p>
            <p><strong>Confidence:</strong> {(result.confidence * 100).toFixed(2)}%</p>
            <p><strong>Date:</strong> {new Date(result.created_at).toLocaleString()}</p>
          </div>
        ))
      )}
    </div>
  );
};

export default AnalysisResultsList;
