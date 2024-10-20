import React from 'react';
import { motion } from 'framer-motion';
import { BarChart, Users, AlertTriangle } from 'lucide-react';
import AnalysisCard from './AnalysisCard';

const Dashboard: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="font-heading text-3xl font-bold mb-8"
      >
        Welcome back, User!
      </motion.h1>

      <div className="grid md:grid-cols-3 gap-6 mb-8">
        {[
          { icon: BarChart, title: 'Total Analyses', value: '1,234' },
          { icon: Users, title: 'Fake Profiles Detected', value: '567' },
          { icon: AlertTriangle, title: 'Accuracy Rate', value: '99%' },
        ].map((stat, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-white p-6 rounded-lg shadow-md"
          >
            <div className="flex items-center mb-4">
              <stat.icon className="w-8 h-8 text-primary mr-3" />
              <h2 className="font-heading text-xl font-semibold">{stat.title}</h2>
            </div>
            <p className="text-3xl font-bold">{stat.value}</p>
          </motion.div>
        ))}
      </div>

      <h2 className="font-heading text-2xl font-semibold mb-4">Recent Analyses</h2>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, index) => (
          <AnalysisCard key={index} />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;