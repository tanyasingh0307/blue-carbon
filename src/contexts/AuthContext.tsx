import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

interface User {
  id: string;
  name: string;
  email: string;
  role: 'ngo' | 'auditor' | 'corporate' | 'government';
  organization: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate checking for existing session
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    setLoading(true);
    
    try {
      const response = await authAPI.login(email, password);
      const { access_token, user: userData } = response;
      
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(userData));
      setUser(userData);
    } catch (error: any) {
      // Fallback to demo users if backend is not available
      const demoUsers: Record<string, User> = {
        'ngo@example.com': {
          id: '1',
          name: 'Ocean Restoration NGO',
          email: 'ngo@example.com',
          role: 'ngo',
          organization: 'Blue Ocean Foundation'
        },
        'auditor@example.com': {
          id: '2',
          name: 'Carbon Auditor',
          email: 'auditor@example.com',
          role: 'auditor',
          organization: 'Verified Carbon Solutions'
        },
        'corporate@example.com': {
          id: '3',
          name: 'Corporate Buyer',
          email: 'corporate@example.com',
          role: 'corporate',
          organization: 'EcoTech Industries'
        }
      };

      const demoUser = demoUsers[email];
      if (demoUser && password === 'demo123') {
        setUser(demoUser);
        localStorage.setItem('user', JSON.stringify(demoUser));
      } else {
        throw new Error('Invalid credentials');
      }
    }
    
    setLoading(false);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}