import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Waves, User, LogOut, Menu, X, Leaf } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { LoginModal } from './LoginModal';

export function Navigation() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsMenuOpen(false);
  };

  const navItems = user ? [
    { path: '/dashboard', label: 'Dashboard' },
    user.role === 'ngo' && { path: '/ngo', label: 'NGO Portal' },
    user.role === 'auditor' && { path: '/auditor', label: 'Auditor Portal' },
    { path: '/marketplace', label: 'Marketplace' },
  ].filter(Boolean) : [];

  return (
    <>
      <nav className="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-md border-b border-teal-100 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-3 group">
              <div className="relative">
                <Waves className="w-8 h-8 text-teal-600 group-hover:text-teal-700 transition-colors" />
                <Leaf className="w-4 h-4 text-emerald-500 absolute -top-1 -right-1" />
              </div>
              <span className="text-xl font-bold text-slate-800 group-hover:text-teal-700 transition-colors">
                BlueCarbon
              </span>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              {navItems.map((item, index) => (
                <Link
                  key={index}
                  to={item.path}
                  className="text-slate-600 hover:text-teal-600 font-medium transition-colors"
                >
                  {item.label}
                </Link>
              ))}
            </div>

            {/* User Menu */}
            <div className="hidden md:flex items-center space-x-4">
              {user ? (
                <div className="flex items-center space-x-4">
                  <div className="flex items-center space-x-3">
                    <div className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                      Demo Mode
                    </div>
                    <div className="flex items-center justify-center w-8 h-8 bg-teal-100 rounded-full">
                      <User className="w-5 h-5 text-teal-600" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-slate-800">{user.name}</p>
                      <p className="text-xs text-slate-500 capitalize">{user.role}</p>
                    </div>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="flex items-center space-x-2 px-4 py-2 text-slate-600 hover:text-red-600 transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>Logout</span>
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => setShowLoginModal(true)}
                  className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
                >
                  Login
                </button>
              )}
            </div>

            {/* Mobile menu button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden p-2 text-slate-600 hover:text-teal-600 transition-colors"
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden bg-white border-t border-teal-100">
            <div className="px-4 py-4 space-y-4">
              {navItems.map((item, index) => (
                <Link
                  key={index}
                  to={item.path}
                  className="block text-slate-600 hover:text-teal-600 font-medium transition-colors"
                  onClick={() => setIsMenuOpen(false)}
                >
                  {item.label}
                </Link>
              ))}
              
              {user ? (
                <div className="pt-4 border-t border-slate-200">
                  <div className="flex items-center space-x-3 mb-4">
                    <div className="flex items-center justify-center w-8 h-8 bg-teal-100 rounded-full">
                      <User className="w-5 h-5 text-teal-600" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-slate-800">{user.name}</p>
                      <p className="text-xs text-slate-500 capitalize">{user.role}</p>
                    </div>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="flex items-center space-x-2 text-red-600 hover:text-red-700 transition-colors"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>Logout</span>
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => {
                    setShowLoginModal(true);
                    setIsMenuOpen(false);
                  }}
                  className="w-full bg-teal-600 hover:bg-teal-700 text-white px-6 py-2 rounded-lg font-medium transition-colors"
                >
                  Login
                </button>
              )}
            </div>
          </div>
        )}
      </nav>

      <LoginModal 
        isOpen={showLoginModal} 
        onClose={() => setShowLoginModal(false)} 
      />
    </>
  );
}