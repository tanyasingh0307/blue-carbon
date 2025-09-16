import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Waves, 
  Shield, 
  TrendingUp, 
  Globe, 
  CheckCircle, 
  ArrowRight,
  Leaf,
  Users,
  BarChart3,
  Award
} from 'lucide-react';

export function Landing() {
  const features = [
    {
      icon: <Leaf className="w-8 h-8 text-emerald-600" />,
      title: "Blue Carbon Projects",
      description: "Register and monitor mangrove, seagrass, and salt marsh restoration projects with AI-powered MRV analysis."
    },
    {
      icon: <Shield className="w-8 h-8 text-blue-600" />,
      title: "Blockchain Verification",
      description: "Transparent and immutable verification of carbon credits using ERC-1155 smart contracts on Polygon."
    },
    {
      icon: <TrendingUp className="w-8 h-8 text-teal-600" />,
      title: "Carbon Trading",
      description: "Secure marketplace for buying, selling, and retiring verified blue carbon credits."
    },
    {
      icon: <Users className="w-8 h-8 text-purple-600" />,
      title: "Multi-Stakeholder",
      description: "Purpose-built for NGOs, auditors, corporates, and government agencies to collaborate effectively."
    }
  ];

  const stats = [
    { value: "50+", label: "Active Projects", icon: <Globe className="w-5 h-5" /> },
    { value: "12K", label: "Tons CO₂ Sequestered", icon: <BarChart3 className="w-5 h-5" /> },
    { value: "25", label: "Verified Auditors", icon: <Award className="w-5 h-5" /> },
    { value: "100%", label: "Blockchain Verified", icon: <Shield className="w-5 h-5" /> }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-teal-600 via-blue-700 to-indigo-800 text-white py-24">
        <div className="absolute inset-0 bg-black opacity-20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex justify-center mb-8">
              <div className="flex items-center space-x-3 bg-white/10 backdrop-blur-md rounded-full px-6 py-3">
                <Waves className="w-8 h-8 text-teal-300" />
                <Leaf className="w-6 h-6 text-emerald-400" />
                <span className="text-lg font-semibold">Blue Carbon MRV Platform</span>
              </div>
            </div>
            
            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
              Restore Oceans,
              <br />
              <span className="text-teal-300">Verify Impact</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-blue-100 mb-8 max-w-3xl mx-auto">
              The world's first comprehensive platform for blue carbon project monitoring, 
              verification, and carbon credit trading powered by AI and blockchain technology.
            </p>
            
            <div className="flex flex-col sm:flex-row justify-center gap-4 mb-12">
              <Link
                to="/dashboard"
                className="bg-teal-500 hover:bg-teal-600 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-colors flex items-center justify-center space-x-2"
              >
                <span>Get Started</span>
                <ArrowRight className="w-5 h-5" />
              </Link>
              
              <Link
                to="/marketplace"
                className="bg-white/10 hover:bg-white/20 backdrop-blur-md border border-white/20 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-colors"
              >
                Explore Marketplace
              </Link>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
              {stats.map((stat, index) => (
                <div key={index} className="bg-white/10 backdrop-blur-md rounded-lg p-6">
                  <div className="flex items-center justify-center mb-2 text-teal-300">
                    {stat.icon}
                  </div>
                  <div className="text-2xl font-bold mb-1">{stat.value}</div>
                  <div className="text-blue-200 text-sm">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-800 mb-4">
              Complete Blue Carbon Solution
            </h2>
            <p className="text-xl text-slate-600 max-w-3xl mx-auto">
              From project registration to carbon credit trading, our platform provides 
              end-to-end tools for the blue carbon ecosystem.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-slate-50 rounded-xl p-6 hover:shadow-lg transition-shadow">
                <div className="mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-slate-800 mb-3">
                  {feature.title}
                </h3>
                <p className="text-slate-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-gradient-to-br from-slate-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-800 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-slate-600">
              Simple, transparent, and verifiable process from restoration to credits
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-emerald-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Leaf className="w-8 h-8 text-emerald-600" />
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-3">1. Register Projects</h3>
              <p className="text-slate-600">
                NGOs register blue carbon restoration projects with location data, 
                baseline measurements, and project documentation.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <BarChart3 className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-3">2. AI-Powered MRV</h3>
              <p className="text-slate-600">
                Our machine learning models analyze project data to calculate 
                CO₂ sequestration and generate verification reports.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-teal-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Shield className="w-8 h-8 text-teal-600" />
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-3">3. Mint & Trade</h3>
              <p className="text-slate-600">
                Verified auditors approve reports and mint carbon credits as 
                blockchain tokens for transparent trading.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-teal-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Make an Impact?
          </h2>
          <p className="text-xl text-teal-100 mb-8 max-w-2xl mx-auto">
            Join the global movement to restore our oceans and fight climate change 
            through verified blue carbon projects.
          </p>
          
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link
              to="/dashboard"
              className="bg-white text-teal-600 hover:bg-teal-50 px-8 py-4 rounded-lg font-semibold text-lg transition-colors flex items-center justify-center space-x-2"
            >
              <span>Start Your Project</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}