import React from 'react';
import ProfileForm from './ProfileForm';
import RealTimeAnalysis from './RealTimeAnalysis';
import AnalysisResultsList from './AnalysisResultsList';

const Dashboard: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <h2 className="text-2xl font-semibold mb-4">Create Profile</h2>
          <ProfileForm />
        </div>
        <div>
          <RealTimeAnalysis />
        </div>
      </div>
      <div className="mt-8">
        <AnalysisResultsList />
      </div>
    </div>
  );
};

export default Dashboard;
