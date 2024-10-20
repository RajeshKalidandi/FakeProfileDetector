import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { Link, Globe, Upload, ChevronRight } from 'lucide-react';
import * as Dialog from '@radix-ui/react-dialog';
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { FreemiumService } from '../lib/freemiumService';
import { User } from '../lib/types';

ChartJS.register(ArcElement, Tooltip, Legend);

const ProfileAnalysis: React.FC = () => {
  const [step, setStep] = useState(1);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const { register, handleSubmit } = useForm();
  const [user, setUser] = useState<User>(/* get user from context or props */);

  const handleAnalysis = async () => {
    const canScan = await FreemiumService.checkScanLimit(user);
    if (!canScan) {
      alert('Daily scan limit reached. Contribute to earn more scans!');
      return;
    }

    // Perform analysis
    await FreemiumService.incrementScanCount(user);
    // Update UI to reflect new scan count
  };

  const onSubmit = (data: any) => {
    setStep(2);
    setTimeout(() => {
      setAnalysisResult({
        confidenceScore: 85,
        models: {
          CNN: 0.87,
          RNN: 0.83,
          SVM: 0.85,
        },
        featureImportance: {
          profilePicture: 0.3,
          postFrequency: 0.25,
          accountAge: 0.2,
          followersCount: 0.15,
          bio: 0.1,
        },
      });
      setStep(3);
    }, 3000);
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <motion.form
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onSubmit={handleSubmit(onSubmit)}
            className="space-y-6"
          >
            <div>
              <label htmlFor="profileUrl" className="block text-sm font-medium text-gray-700 mb-1">
                Profile URL
              </label>
              <div className="mt-1 flex rounded-md shadow-sm">
                <span className="inline-flex items-center px-3 rounded-l-md border border-r-0 border-gray-300 bg-gray-50 text-gray-500 text-sm">
                  <Globe className="h-5 w-5" />
                </span>
                <input
                  type="text"
                  id="profileUrl"
                  {...register('profileUrl', { required: true })}
                  className="focus:ring-primary focus:border-primary flex-1 block w-full rounded-none rounded-r-md sm:text-sm border-gray-300"
                  placeholder="https://example.com/profile"
                />
              </div>
            </div>
            <div>
              <label htmlFor="platform" className="block text-sm font-medium text-gray-700 mb-1">
                Platform
              </label>
              <select
                id="platform"
                {...register('platform', { required: true })}
                className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm rounded-md"
              >
                <option value="">Select a platform</option>
                <option value="twitter">Twitter</option>
                <option value="facebook">Facebook</option>
                <option value="instagram">Instagram</option>
                <option value="linkedin">LinkedIn</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Upload Screenshots (optional)
              </label>
              <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                <div className="space-y-1 text-center">
                  <Upload className="mx-auto h-12 w-12 text-gray-400" />
                  <div className="flex text-sm text-gray-600">
                    <label
                      htmlFor="file-upload"
                      className="relative cursor-pointer bg-white rounded-md font-medium text-primary hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary"
                    >
                      <span>Upload files</span>
                      <input id="file-upload" name="file-upload" type="file" className="sr-only" multiple />
                    </label>
                    <p className="pl-1">or drag and drop</p>
                  </div>
                  <p className="text-xs text-gray-500">PNG, JPG, GIF up to 10MB</p>
                </div>
              </div>
            </div>
            <div>
              <button
                type="submit"
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
              >
                Start Analysis
              </button>
            </div>
          </motion.form>
        );
      case 2:
        return (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="text-center"
          >
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary mx-auto"></div>
            <h2 className="mt-4 font-semibold text-xl">Analyzing Profile</h2>
            <p className="text-gray-500">This may take a few moments...</p>
          </motion.div>
        );
      case 3:
        return (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="space-y-8"
          >
            <div className="text-center">
              <h2 className="text-3xl font-bold mb-2">Analysis Complete</h2>
              <p className="text-xl font-semibold">
                Confidence Score:{' '}
                <span className={analysisResult.confidenceScore > 70 ? 'text-secondary' : 'text-accent'}>
                  {analysisResult.confidenceScore}%
                </span>
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-4">Model Predictions</h3>
              <div className="grid grid-cols-3 gap-4">
                {Object.entries(analysisResult.models).map(([model, score]: [string, number]) => (
                  <div key={model} className="bg-white p-4 rounded-lg shadow">
                    <h4 className="font-semibold">{model}</h4>
                    <p className="text-2xl font-bold">{(score * 100).toFixed(1)}%</p>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-4">Feature Importance</h3>
              <div className="w-full max-w-md mx-auto">
                <Doughnut
                  data={{
                    labels: Object.keys(analysisResult.featureImportance),
                    datasets: [
                      {
                        data: Object.values(analysisResult.featureImportance),
                        backgroundColor: [
                          '#3B82F6',
                          '#10B981',
                          '#F59E0B',
                          '#EF4444',
                          '#6366F1',
                        ],
                      },
                    ],
                  }}
                  options={{
                    responsive: true,
                    plugins: {
                      legend: {
                        position: 'bottom',
                      },
                    },
                  }}
                />
              </div>
            </div>
            <div>
              <Dialog.Root>
                <Dialog.Trigger asChild>
                  <button className="w-full flex justify-center items-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary">
                    View Detailed Analysis
                    <ChevronRight className="ml-2 h-4 w-4" />
                  </button>
                </Dialog.Trigger>
                <Dialog.Portal>
                  <Dialog.Overlay className="fixed inset-0 bg-black bg-opacity-50" />
                  <Dialog.Content className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                    <Dialog.Title className="text-2xl font-bold mb-4">Detailed Analysis</Dialog.Title>
                    <Dialog.Description className="text-gray-500 mb-6">
                      In-depth breakdown of the profile analysis results.
                    </Dialog.Description>
                    {/* Add more detailed analysis content here */}
                    <Dialog.Close asChild>
                      <button className="absolute top-4 right-4 text-gray-400 hover:text-gray-500">
                        <span className="sr-only">Close</span>
                        &times;
                      </button>
                    </Dialog.Close>
                  </Dialog.Content>
                </Dialog.Portal>
              </Dialog.Root>
            </div>
          </motion.div>
        );
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="font-heading text-3xl font-bold mb-8">Profile Analysis</h1>
      <div className="max-w-2xl mx-auto bg-white shadow-md rounded-lg p-6">
        {renderStep()}
      </div>
    </div>
  );
};

export default ProfileAnalysis;
