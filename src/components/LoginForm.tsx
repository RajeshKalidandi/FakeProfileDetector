import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { login as loginApi, signInWithGoogle } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { FaEnvelope, FaLock, FaGoogle } from 'react-icons/fa';
import ErrorMessage from './ErrorMessage';

const LoginForm: React.FC = () => {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const navigate = useNavigate();
  const { login } = useAuth();
  const [loginError, setLoginError] = useState<string | null>(null);

  const onSubmit = async (data: { email: string; password: string }) => {
    try {
      const response = await loginApi(data.email, data.password);
      const user = response.data.user;
      login(user);
      console.log('Login successful, navigating to dashboard');
      navigate('/dashboard');
    } catch (error) {
      console.error('Login failed:', error);
      setLoginError('Invalid email or password. Please try again.');
    }
  };

  const handleGoogleSignIn = async () => {
    try {
      const user = await signInWithGoogle();
      login(user);
      console.log('Google sign-in successful, navigating to dashboard');
      navigate('/dashboard');
    } catch (error) {
      console.error('Google sign-in failed:', error);
      setLoginError('Google sign-in failed. Please try again.');
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-md mx-auto mt-10 p-6 bg-white rounded-lg shadow-xl"
    >
      <h2 className="text-3xl font-bold mb-6 text-center text-primary">Login to Fake Profile Detector</h2>
      {loginError && <ErrorMessage message={loginError} />}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-text">
            Email
          </label>
          <div className="mt-1 relative rounded-md shadow-sm">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <FaEnvelope className="h-5 w-5 text-gray-400" />
            </div>
            <input
              id="email"
              type="email"
              {...register('email', { required: 'Email is required' })}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              placeholder="you@example.com"
            />
          </div>
          {errors.email && <p className="mt-1 text-sm text-accent">{errors.email.message}</p>}
        </div>
        <div>
          <label htmlFor="password" className="block text-sm font-medium text-text">
            Password
          </label>
          <div className="mt-1 relative rounded-md shadow-sm">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <FaLock className="h-5 w-5 text-gray-400" />
            </div>
            <input
              id="password"
              type="password"
              {...register('password', { required: 'Password is required' })}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"
              placeholder="••••••••"
            />
          </div>
          {errors.password && <p className="mt-1 text-sm text-accent">{errors.password.message}</p>}
        </div>
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <input
              id="remember-me"
              name="remember-me"
              type="checkbox"
              className="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
            />
            <label htmlFor="remember-me" className="ml-2 block text-sm text-text">
              Remember me
            </label>
          </div>
          <div className="text-sm">
            <a href="#" className="font-medium text-primary hover:text-primary-dark">
              Forgot your password?
            </a>
          </div>
        </div>
        <div>
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            Sign In
          </button>
        </div>
      </form>
      <div className="mt-6">
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-text">Or continue with</span>
          </div>
        </div>
        <div className="mt-6">
          <button
            onClick={handleGoogleSignIn}
            className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-text hover:bg-gray-50"
          >
            <FaGoogle className="h-5 w-5 text-red-500 mr-2" />
            <span>Sign in with Google</span>
          </button>
        </div>
      </div>
      <p className="mt-8 text-center text-sm text-text">
        Not a member?{' '}
        <Link to="/register" className="font-medium text-primary hover:text-blue-700">
          Sign up now
        </Link>
      </p>
    </motion.div>
  );
};

export default LoginForm;
