import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart, Users, AlertTriangle, Zap, Shield, Award } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import Header from './Header';
import AnalysisCard from './AnalysisCard';
import ContributionPanel from './ContributionPanel';
import HistoryReports from './HistoryReports';
import Notifications from './Notifications';
import ErrorMessage from './ErrorMessage';
import { getUserStats } from '../services/api';

const Dashboard: React.FC = () => {
  const { currentUser } = useAuth();
  const [userStats, setUserStats] = useState({
    tier: 'free',
    dailyScans: 0,
    contributions: {
      verifiedProfiles: 0,
      validReports: 0,
      feedbackCount: 0
    },
    rewards: []
  });
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUserStats = async () => {
      if (!currentUser) return;

      try {
        const response = await getUserStats();
        setUserStats(response.data);
      } catch (error) {
        console.error('Error fetching user stats:', error);
        setError('Failed to fetch user statistics. Please try again later.');
      }
    };

    fetchUserStats();
  }, [currentUser]);

  if (!currentUser) {
    return (
      <div className="flex items-center justify-center h-screen">
        <motion.div
          initial={{ opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
          className="text-2xl font-semibold text-gray-700"
        >
          Loading...
        </motion.div>
      </div>
    );
  }

  const stats = [
    { icon: BarChart, title: 'Total Analyses', value: userStats.dailyScans.toString() },
    { icon: Users, title: 'Fake Profiles Detected', value: userStats.contributions.verifiedProfiles.toString() },
    { icon: AlertTriangle, title: 'Accuracy Rate', value: '99%' },
    { icon: Zap, title: 'Quick Scans', value: '50+' },
    { icon: Shield, title: 'Protected Users', value: '1000+' },
    { icon: Award, title: 'User Rank', value: userStats.tier.charAt(0).toUpperCase() + userStats.tier.slice(1) },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      <Header username={currentUser.displayName || 'User'} />
      <main className="container mx-auto px-4 py-8">
        {error && <ErrorMessage message={error} />}
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-bold mb-8 text-gray-800"
        >
          Welcome back, {currentUser.displayName || 'User'}!
        </motion.h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300"
            >
              <div className="flex items-center mb-4">
                <stat.icon className="w-8 h-8 text-primary mr-3" />
                <h2 className="text-xl font-semibold text-gray-700">{stat.title}</h2>
              </div>
              <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
            </motion.div>
          ))}
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <AnalysisCard tier={userStats.tier} dailyScans={userStats.dailyScans} />
          </motion.div>
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.3 }}
          >
            <ContributionPanel contributions={userStats.contributions} />
          </motion.div>
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
          >
            <HistoryReports />
          </motion.div>
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5 }}
            className="lg:col-span-3"
          >
            <Notifications rewards={userStats.rewards} dailyScans={userStats.dailyScans} />
          </motion.div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
