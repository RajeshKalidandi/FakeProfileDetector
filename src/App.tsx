import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import Dashboard from './components/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';
import LandingPage from './components/LandingPage';
import NotFound from './components/NotFound';
import ProfileAnalysis from './components/ProfileAnalysis';
import HistoryReports from './components/HistoryReports';
import FullRealTimeAnalysis from './components/FullRealTimeAnalysis';

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/register" element={<RegisterForm />} />
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/profile-analysis" element={<ProfileAnalysis />} />
            <Route path="/history" element={<HistoryReports />} />
            <Route path="/real-time-analysis" element={<FullRealTimeAnalysis />} />
          </Route>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
