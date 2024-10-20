import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart, Users, AlertTriangle, Zap, Shield, Award, Network, Clock, Search } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import Header from './Header';
import AnalysisCard from './AnalysisCard';
import ContributionPanel from './ContributionPanel';
import HistoryReports from './HistoryReports';
import Notifications from './Notifications';
import ErrorMessage from './ErrorMessage';
import RealTimeAnalysis from './RealTimeAnalysis';
import { getUserStats, getRecentAnalyses, UserStats, RecentAnalysis } from '../services/api';
import { Link } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const { currentUser } = useAuth();
  const [userStats, setUserStats] = useState<UserStats>({
    tier: 'free',
    dailyScans: 0,
    contributions: {
      verifiedProfiles: 0,
      validReports: 0,
      feedbackCount: 0
    },
    rewards: [],
    networkScore: 0,
    followerFollowingRatio: 0,
    degreeCentrality: 0,
    betweennessCentrality: 0,
    closenessCentrality: 0,
    clusteringCoefficient: 0,
    accountAge: 0,
    postingFrequency: 0,
    activityVariance: 0,
    nightDayRatio: 0
  });
  const [error, setError] = useState<string | null>(null);
  const [recentAnalyses, setRecentAnalyses] = useState<RecentAnalysis[]>([]);

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

  useEffect(() => {
    const fetchRecentAnalyses = async () => {
      try {
        const response = await getRecentAnalyses();
        setRecentAnalyses(response.data);
      } catch (error) {
        console.error('Error fetching recent analyses:', error);
      }
    };

    fetchRecentAnalyses();
  }, []);

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
    { icon: Network, title: 'Network Score', value: userStats.networkScore.toFixed(2) },
    { icon: Clock, title: 'Account Age (days)', value: userStats.accountAge.toString() },
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

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
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

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.6 }}
          className="bg-white p-6 rounded-lg shadow-md mt-6"
        >
          <h2 className="text-2xl font-semibold mb-4">Network Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <p className="font-semibold">Follower-Following Ratio:</p>
              <p>{userStats.followerFollowingRatio.toFixed(2)}</p>
            </div>
            <div>
              <p className="font-semibold">Degree Centrality:</p>
              <p>{userStats.degreeCentrality.toFixed(4)}</p>
            </div>
            <div>
              <p className="font-semibold">Betweenness Centrality:</p>
              <p>{userStats.betweennessCentrality.toFixed(4)}</p>
            </div>
            <div>
              <p className="font-semibold">Closeness Centrality:</p>
              <p>{userStats.closenessCentrality.toFixed(4)}</p>
            </div>
            <div>
              <p className="font-semibold">Clustering Coefficient:</p>
              <p>{userStats.clusteringCoefficient.toFixed(4)}</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.7 }}
          className="bg-white p-6 rounded-lg shadow-md mt-6"
        >
          <h2 className="text-2xl font-semibold mb-4">Temporal Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <p className="font-semibold">Posting Frequency (posts/day):</p>
              <p>{userStats.postingFrequency.toFixed(2)}</p>
            </div>
            <div>
              <p className="font-semibold">Activity Variance:</p>
              <p>{userStats.activityVariance.toFixed(2)}</p>
            </div>
            <div>
              <p className="font-semibold">Night/Day Activity Ratio:</p>
              <p>{userStats.nightDayRatio.toFixed(2)}</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.8 }}
          className="bg-white p-6 rounded-lg shadow-md mt-6"
        >
          <h2 className="text-2xl font-semibold mb-4">Recent Analyses</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {recentAnalyses.map((analysis, index) => (
              <div key={index} className="bg-gray-100 p-4 rounded-lg">
                <p className="font-semibold">{analysis.profile_url}</p>
                <p className={analysis.result === 'fake' ? 'text-red-500' : 'text-green-500'}>
                  {analysis.result.charAt(0).toUpperCase() + analysis.result.slice(1)}
                </p>
                <p>Confidence: {(analysis.confidence * 100).toFixed(2)}%</p>
              </div>
            ))}
          </div>
          <Link to="/real-time-analysis" className="mt-4 inline-block bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
            Go to Real-Time Analysis
          </Link>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.9 }}
          className="mt-6"
        >
          <RealTimeAnalysis />
        </motion.div>
      </main>
    </div>
  );
};

export default Dashboard;
