import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Download, Filter } from 'lucide-react';
import AnalysisCard from './AnalysisCard';

const HistoryReports: React.FC = () => {
  const [filter, setFilter] = useState('all');

  const analyses = [...Array(12)].map((_, index) => ({
    id: index + 1,
    date: new Date(Date.now() - Math.random() * 10000000000).toLocaleDateString(),
    result: Math.random() > 0.5 ? 'real' : 'fake',
  }));

  const filteredAnalyses = analyses.filter(analysis => {
    if (filter === 'all') return true;
    return analysis.result === filter;
  });

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="font-heading text-3xl font-bold">Analysis History</h1>
        <div className="flex space-x-4">
          <button className="flex items-center px-4 py-2 bg-primary text-white rounded-md hover:bg-blue-600 transition duration-300">
            <Download className="w-5 h-5 mr-2" />
            Export
          </button>
          <div className="relative">
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="appearance-none bg-white border border-gray-300 rounded-md pl-3 pr-10 py-2 focus:outline-none focus:ring-primary focus:border-primary"
            >
              <option value="all">All</option>
              <option value="real">Real</option>
              <option value="fake">Fake</option>
            </select>
            <Filter className="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400 pointer-events-none" />
          </div>
        </div>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredAnalyses.map((analysis, index) => (
          <motion.div
            key={analysis.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.05 }}
          >
            <AnalysisCard />
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default HistoryReports;