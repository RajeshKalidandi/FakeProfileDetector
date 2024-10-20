import React from 'react';
import RealTimeAnalysis from './RealTimeAnalysis';

const FullRealTimeAnalysis: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Real-Time Profile Analysis</h1>
      <RealTimeAnalysis />
    </div>
  );
};

export default FullRealTimeAnalysis;
