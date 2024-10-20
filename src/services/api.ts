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
