import React from 'react';
import { motion } from 'framer-motion';
import { User, Calendar, Activity } from 'lucide-react';

const AnalysisCard: React.FC = () => {
  const confidenceScore = Math.floor(Math.random() * 100);
  const isReal = confidenceScore > 70;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      className="bg-white rounded-lg shadow-md overflow-hidden"
    >
      <div className="p-4">
        <div className="flex items-center mb-4">
          <img
            src="https://source.unsplash.com/random/100x100?face"
            alt="Profile"
            className="w-12 h-12 rounded-full mr-4"
          />
          <div>
            <h3 className="font-semibold">@username</h3>
            <p className="text-sm text-gray-500">Platform Name</p>
          </div>
        </div>
        <div className="flex items-center text-sm text-gray-500 mb-4">
          <Calendar className="w-4 h-4 mr-2" />
          <span>Created: Jan 1, 2023</span>
        </div>
        <div className="flex items-center text-sm text-gray-500 mb-4">
          <Activity className="w-4 h-4 mr-2" />
          <span>Posts: 123 | Followers: 456</span>
        </div>
        <div className="mt-4">
          <div className="flex justify-between items-center mb-2">
            <span className="font-semibold">Confidence Score</span>
            <span className={`font-bold ${isReal ? 'text-secondary' : 'text-accent'}`}>
              {confidenceScore}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
              className={`h-2.5 rounded-full ${isReal ? 'bg-secondary' : 'bg-accent'}`}
              style={{ width: `${confidenceScore}%` }}
            ></div>
          </div>
        </div>
      </div>
      <div className={`p-3 text-center text-white font-semibold ${isReal ? 'bg-secondary' : 'bg-accent'}`}>
        {isReal ? 'Likely Real' : 'Potentially Fake'}
      </div>
    </motion.div>
  );
};

export default AnalysisCard;