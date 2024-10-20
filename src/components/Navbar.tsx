import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navbar: React.FC = () => {
  const { currentUser, logout } = useAuth();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="bg-primary text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0 text-xl font-bold">
              Fake Profile Detector
            </Link>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <Link
                  to="/"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    isActive('/') ? 'bg-blue-700 text-white' : 'text-white hover:bg-blue-600'
                  }`}
                >
                  Home
                </Link>
                {currentUser && (
                  <>
                    <Link
                      to="/dashboard"
                      className={`px-3 py-2 rounded-md text-sm font-medium ${
                        isActive('/dashboard') ? 'bg-blue-700 text-white' : 'text-white hover:bg-blue-600'
                      }`}
                    >
                      Dashboard
                    </Link>
                    <Link
                      to="/profile-analysis"
                      className={`px-3 py-2 rounded-md text-sm font-medium ${
                        isActive('/profile-analysis') ? 'bg-blue-700 text-white' : 'text-white hover:bg-blue-600'
                      }`}
                    >
                      Profile Analysis
                    </Link>
                    <Link
                      to="/history"
                      className={`px-3 py-2 rounded-md text-sm font-medium ${
                        isActive('/history') ? 'bg-blue-700 text-white' : 'text-white hover:bg-blue-600'
                      }`}
                    >
                      History
                    </Link>
                  </>
                )}
              </div>
            </div>
          </div>
          <div className="hidden md:block">
            <div className="ml-4 flex items-center md:ml-6">
              {currentUser ? (
                <button
                  onClick={logout}
                  className="px-3 py-2 rounded-md text-sm font-medium text-white hover:bg-blue-600"
                >
                  Logout
                </button>
              ) : (
                <>
                  <Link
                    to="/login"
                    className={`px-3 py-2 rounded-md text-sm font-medium ${
                      isActive('/login') ? 'bg-blue-700 text-white' : 'text-white hover:bg-blue-600'
                    }`}
                  >
                    Login
                  </Link>
                  <Link
                    to="/register"
                    className={`ml-2 px-3 py-2 rounded-md text-sm font-medium ${
                      isActive('/register') ? 'bg-blue-700 text-white' : 'text-white hover:bg-blue-600'
                    }`}
                  >
                    Register
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
