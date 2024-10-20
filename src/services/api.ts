import axios, { AxiosError } from 'axios';
import { auth } from '../firebase';
import { signInWithPopup, GoogleAuthProvider } from 'firebase/auth';

const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const login = (email: string, password: string) => 
  api.post('/auth/login', { email, password });

export const register = (username: string, email: string, password: string) => 
  api.post('/auth/register', { username, email, password });

export const getUserProfile = () => 
  api.get('/user/profile');

export const updateUserProfile = (data: any) => 
  api.put('/user/profile', data);

export const getFeatureFlags = () => 
  api.get('/features');

export const analyzeProfile = (profileData: any) => 
  api.post('/analyze/profile', profileData);

export const getUserStats = async (): Promise<{ data: UserStats }> => {
  const response = await axios.get(`${API_URL}/user/stats`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('token')}`,
    },
  });
  return response.data;
};

export const contributeData = (contributionData: any) =>
  api.post('/contribute', contributionData);

export const signInWithGoogle = async () => {
  const provider = new GoogleAuthProvider();
  try {
    const result = await signInWithPopup(auth, provider);
    return result.user;
  } catch (error) {
    console.error("Error signing in with Google", error);
    throw error;
  }
};

export const analyzeProfileRealtime = (profileData: any) =>
  api.post('/analyze/profile/realtime', profileData);

export const getRecentAnalyses = (): Promise<{ data: RecentAnalysis[] }> => 
  api.get('/recent-analyses');

export const submitFeedback = (analysisId: string, feedback: string) =>
  api.post('/feedback', { analysis_id: analysisId, feedback });

// New endpoints
export const createProfile = (profileData: any) =>
  api.post('/api/profiles', profileData);

export const getProfile = (profileId: string) =>
  api.get(`/api/profiles/${profileId}`);

export const createAnalysisResult = (resultData: any) =>
  api.post('/api/analysis_results', resultData);

export const getAnalysisResult = (resultId: string) =>
  api.get(`/api/analysis_results/${resultId}`);

export const createFeedbackReport = (feedbackData: any) =>
  api.post('/api/feedback_reports', feedbackData);

export const getFeedbackReport = (reportId: string) =>
  api.get(`/api/feedback_reports/${reportId}`);

export default api;

export interface UserStats {
  tier: string;
  dailyScans: number;
  contributions: {
    verifiedProfiles: number;
    validReports: number;
    feedbackCount: number;
  };
  rewards: any[];
  networkScore: number;
  followerFollowingRatio: number;
  degreeCentrality: number;
  betweennessCentrality: number;
  closenessCentrality: number;
  clusteringCoefficient: number;
  accountAge: number;
  postingFrequency: number;
  activityVariance: number;
  nightDayRatio: number;
}

export interface RecentAnalysis {
  profile_url: string;
  result: string;
  confidence: number;
  created_at: string;
}

export interface Profile {
  id: string;
  platform: string;
  profile_url: string;
  username: string;
  bio?: string;
  post_count: number;
  follower_count: number;
  following_count: number;
  profile_picture_url?: string;
}

export interface AnalysisResult {
  id: string;
  profile_id: string;
  result: string;
  confidence: number;
  features_used: string[];
  model_version: string;
  created_at: string;
}

export interface FeedbackReport {
  id: string;
  analysis_id: string;
  feedback: string;
  additional_comments?: string;
  created_at: string;
}
