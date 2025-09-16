import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { Navigation } from './components/Navigation';
import { Dashboard } from './pages/Dashboard';
import { NGODashboard } from './pages/NGODashboard';
import { AuditorDashboard } from './pages/AuditorDashboard';
import { Marketplace } from './pages/Marketplace';
import { ProjectDetails } from './pages/ProjectDetails';
import { Landing } from './pages/Landing';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
          <Navigation />
          <main className="pt-16">
            <Routes>
              <Route path="/" element={<Landing />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/ngo" element={<NGODashboard />} />
              <Route path="/auditor" element={<AuditorDashboard />} />
              <Route path="/marketplace" element={<Marketplace />} />
              <Route path="/project/:id" element={<ProjectDetails />} />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;