import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle API errors and fallback to demo mode
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED' || error.code === 'ERR_NETWORK') {
      console.warn('Backend unavailable, using demo mode');
      return Promise.reject({ ...error, isNetworkError: true });
    }
    return Promise.reject(error);
  }
);

// Demo data for fallback
const demoProjects = [
  {
    id: 1,
    name: "Mangrove Restoration - Philippines",
    location: "Palawan, Philippines",
    ecosystem_type: "mangrove",
    area_hectares: 150,
    status: "active",
    created_at: "2024-01-15T00:00:00Z",
    co2_sequestered: 2250,
    credits_issued: 180
  },
  {
    id: 2,
    name: "Seagrass Conservation - Australia",
    location: "Great Barrier Reef, Australia",
    ecosystem_type: "seagrass",
    area_hectares: 200,
    status: "pending_verification",
    created_at: "2024-02-01T00:00:00Z",
    co2_sequestered: 1800,
    credits_issued: 0
  }
];

const demoReports = [
  {
    id: 1,
    project_id: 1,
    co2_tons: 2250,
    confidence_score: 0.92,
    status: "verified",
    created_at: "2024-03-01T00:00:00Z",
    verified_at: "2024-03-05T00:00:00Z"
  },
  {
    id: 2,
    project_id: 2,
    co2_tons: 1800,
    confidence_score: 0.88,
    status: "pending",
    created_at: "2024-03-10T00:00:00Z"
  }
];

const demoCredits = [
  {
    id: 1,
    token_id: "1",
    project_name: "Mangrove Restoration - Philippines",
    co2_tons: 180,
    price_per_ton: 25,
    total_price: 4500,
    status: "available",
    owner: "0x1234...5678"
  },
  {
    id: 2,
    token_id: "2",
    project_name: "Salt Marsh Protection - USA",
    co2_tons: 120,
    price_per_ton: 30,
    total_price: 3600,
    status: "available",
    owner: "0x8765...4321"
  }
];

// Auth API
export const authAPI = {
  login: async (email: string, password: string) => {
    try {
      const response = await api.post('/auth/login', { email, password });
      return response.data;
    } catch (error: any) {
      if (error.isNetworkError) {
        // Demo login
        const demoUsers = {
          'ngo@example.com': { role: 'ngo', name: 'NGO User', token: 'demo-ngo-token' },
          'auditor@example.com': { role: 'auditor', name: 'Auditor User', token: 'demo-auditor-token' },
          'corporate@example.com': { role: 'corporate', name: 'Corporate User', token: 'demo-corporate-token' },
          'government@example.com': { role: 'government', name: 'Government User', token: 'demo-government-token' }
        };
        
        const user = demoUsers[email as keyof typeof demoUsers];
        if (user && password === 'demo123') {
          return { access_token: user.token, user: { email, role: user.role, name: user.name } };
        }
        throw new Error('Invalid credentials');
      }
      throw error;
    }
  },

  register: async (userData: any) => {
    try {
      const response = await api.post('/auth/register', userData);
      return response.data;
    } catch (error: any) {
      if (error.isNetworkError) {
        return { message: 'Registration successful (demo mode)', user: userData };
      }
      throw error;
    }
  },

  getProfile: async () => {
    try {
      const response = await api.get('/auth/me');
      return response.data;
    } catch (error: any) {
      if (error.isNetworkError) {
        const token = localStorage.getItem('token');
        if (token?.includes('ngo')) return { email: 'ngo@example.com', role: 'ngo', name: 'NGO User' };
        if (token?.includes('auditor')) return { email: 'auditor@example.com', role: 'auditor', name: 'Auditor User' };
        if (token?.includes('corporate')) return { email: 'corporate@example.com', role: 'corporate', name: 'Corporate User' };
        if (token?.includes('government')) return { email: 'government@example.com', role: 'government', name: 'Government User' };
      }
      throw error;
    }
  }
};

// Projects API
export const projectsAPI = {
  getProjects: async () => {
    try {
      const response = await api.get('/projects/');
      return response.data;
    } catch (error: any) {
      if (error.isNetworkError) {
        return demoProjects;
      }
      throw error;
    }
  },

  createProject: async (projectData: any) => {
    try {
      const response = await api.post('/projects/', projectData);
      return response.data;
    } catch (error: any) {
      if (error.isNetworkError) {
        const newProject = {
          id: Date.now(),
          ...projectData,
          status: 'active',
          created_at: new Date().toISOString(),
          co2_sequestered: 0,
          credits_issued: 0
        };
        return newProject;
      }
      throw error;
    }
  },

  getProject: async (id: number) => {
    try {
      const response = await api.get(`/projects/${id}`);
      return response.data;
    } catch (error: any) {
      if (error.isNetworkError) {
        return demoProjects.find(p => p.id === id) || demoProjects[0];
      }
      throw error;
    }
  },

  uploadMonitoringData: async (projectId: number, formData: FormData) => {
    try {
      const response = await api.post(`/projects/${projectId}/monitoring-data`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return response.data;
    } catch (error: any) {
      if (error.isNetworkError) {
        return { message: 'Monitoring data uploaded successfully (demo mode)', id: Date.now() };
      }
      throw error;
    }
  }
};

// MRV API
export const mrvAPI = {
  runAnalysis: async (projectId: number) => {
    try {
      const response = await api.post(`/mrv/run-analysis/${projectId}`);
      return response.data;
    } catch (error: any) {
      if (error.isNetworkError) {
        // Simulate analysis delay
        await new Promise(resolve => setTimeout(resolve, 2000));
        return {
          id: Date.now(),
          project_id: projectId,
          co2_tons: Math.floor(Math.random() * 3000) + 1000,
          confidence_score: 0.85 + Math.random() * 0.1,
          status: 'completed',
          created_at: new Date().toISOString(),
          methodology: 'IPCC 2019 Wetlands Supplement',
          data_sources: ['Satellite imagery', 'Field measurements', 'Water quality sensors']
        };
      }
      throw error;
    }
  },

  getReports: async () => {
    try {
      const response = await api.get('/mrv/reports');
      return response.data;
    } catch (error: any) {
      if (error.isNetworkError) {
        return demoReports;
      }
      throw error;
    }
  },

  verifyReport: async (reportId: number) => {
    try {
      const response = await api.post(`/mrv/verify/${reportId}`);
      return response.data;
    } catch (error: any) {
      if (error.isNetworkError) {
        return {
          message: 'Report verified and credits minted successfully (demo mode)',
          transaction_hash: '0x' + Math.random().toString(16).substr(2, 64),
          credits_minted: Math.floor(Math.random() * 200) + 50
        };
      }
      throw error;
    }
  }
};

// Marketplace API
export const marketplaceAPI = {
  getCredits: async () => {
    try {
      const response = await api.get('/marketplace/credits');
      return response.data;
    } catch (error: any) {
      if (error.isNetworkError) {
        return demoCredits;
      }
      throw error;
    }
  },

  purchaseCredits: async (tokenId: string, amount: number) => {
    try {
      const response = await api.post('/marketplace/purchase', { token_id: tokenId, amount });
      return response.data;
    } catch (error: any) {
      if (error.isNetworkError) {
        return {
          message: 'Credits purchased successfully (demo mode)',
          transaction_hash: '0x' + Math.random().toString(16).substr(2, 64),
          amount,
          total_cost: amount * 25
        };
      }
      throw error;
    }
  },

  retireCredits: async (tokenId: string, amount: number) => {
    try {
      const response = await api.post('/marketplace/retire', { token_id: tokenId, amount });
      return response.data;
    } catch (error: any) {
      if (error.isNetworkError) {
        return {
          message: 'Credits retired successfully (demo mode)',
          transaction_hash: '0x' + Math.random().toString(16).substr(2, 64),
          amount,
          retirement_certificate: 'CERT-' + Date.now()
        };
      }
      throw error;
    }
  },

  getUserPortfolio: async () => {
    try {
      const response = await api.get('/marketplace/portfolio');
      return response.data;
    } catch (error: any) {
      if (error.isNetworkError) {
        return {
          total_credits: 450,
          total_value: 11250,
          retired_credits: 120,
          active_credits: 330,
          credits: [
            { token_id: '1', project_name: 'Mangrove Restoration - Philippines', amount: 180, value: 4500 },
            { token_id: '3', project_name: 'Seagrass Conservation - Mexico', amount: 150, value: 3750 }
          ]
        };
      }
      throw error;
    }
  }
};

// Credits API
export const creditsAPI = {
  mintCredits: async (reportId: number, amount: number) => {
    try {
      const response = await api.post('/credits/mint', { report_id: reportId, amount });
      return response.data;
    } catch (error: any) {
      if (error.isNetworkError) {
        return {
          message: 'Credits minted successfully (demo mode)',
          transaction_hash: '0x' + Math.random().toString(16).substr(2, 64),
          token_id: Date.now().toString(),
          amount,
          project_name: 'Demo Project'
        };
      }
      throw error;
    }
  }
};

export default api;