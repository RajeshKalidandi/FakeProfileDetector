import React from 'react';
import { Bar, Radar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, registerables } from 'chart.js';

ChartJS.register(...registerables);

interface AnalysisVisualizationProps {
  features: any;
  result: string;
  confidence: number;
}

const AnalysisVisualization: React.FC<AnalysisVisualizationProps> = ({ features, result, confidence }) => {
  const networkFeatures = {
    labels: ['Follower-Following Ratio', 'Degree Centrality', 'Betweenness Centrality', 'Closeness Centrality', 'Clustering Coefficient'],
    datasets: [{
      label: 'Network Features',
      data: [
        features.follower_following_ratio,
        features.degree_centrality,
        features.betweenness_centrality,
        features.closeness_centrality,
        features.clustering_coefficient
      ],
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1
    }]
  };

  const temporalFeatures = {
    labels: ['Account Age', 'Posting Frequency', 'Activity Variance', 'Night/Day Ratio'],
    datasets: [{
      label: 'Temporal Features',
      data: [
        features.account_age,
        features.posting_frequency,
        features.activity_variance,
        features.night_day_ratio
      ],
      backgroundColor: 'rgba(255, 99, 132, 0.6)',
      borderColor: 'rgba(255, 99, 132, 1)',
      borderWidth: 1
    }]
  };

  const resultData = {
    labels: ['Genuine', 'Fake'],
    datasets: [{
      data: [100 - confidence * 100, confidence * 100],
      backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(255, 99, 132, 0.6)'],
      borderColor: ['rgba(75, 192, 192, 1)', 'rgba(255, 99, 132, 1)'],
      borderWidth: 1
    }]
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <h3 className="text-xl font-semibold mb-2">Network Features</h3>
        <Radar data={networkFeatures} />
      </div>
      <div>
        <h3 className="text-xl font-semibold mb-2">Temporal Features</h3>
        <Bar data={temporalFeatures} />
      </div>
      <div className="md:col-span-2">
        <h3 className="text-xl font-semibold mb-2">Analysis Result</h3>
        <div className="flex items-center">
          <Pie data={resultData} options={{ aspectRatio: 2 }} />
          <div className="ml-4">
            <p className="text-lg font-semibold">Result: {result}</p>
            <p className="text-lg">Confidence: {(confidence * 100).toFixed(2)}%</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisVisualization;
