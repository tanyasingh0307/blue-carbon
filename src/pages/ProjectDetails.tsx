import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  ArrowLeft,
  MapPin, 
  Calendar, 
  TrendingUp, 
  Award, 
  FileText,
  ExternalLink,
  CheckCircle,
  Download,
  Leaf,
  BarChart3
} from 'lucide-react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';

export function ProjectDetails() {
  const { id } = useParams();

  // Mock project data - in a real app, this would be fetched based on the ID
  const project = {
    id: 1,
    name: 'Mangrove Restoration Bay Area',
    description: 'Large-scale mangrove restoration project aimed at sequestering carbon while providing coastal protection and biodiversity habitat in the Florida Keys region.',
    location: 'Florida Keys, USA',
    coordinates: { lat: 25.0760, lng: -80.2730 },
    type: 'Mangroves',
    area: 25.5,
    startDate: '2024-01-15',
    ngo: 'Blue Ocean Foundation',
    status: 'Active',
    co2Estimated: 450,
    co2Verified: 320,
    creditsIssued: 320,
    methodology: 'IPCC Wetlands Supplement + Remote Sensing',
    verificationDate: '2024-06-15',
    auditor: 'Verified Carbon Solutions',
    blockchainTx: '0x8f4b7c2d9a1e...',
    ipfsHash: 'QmX4z9Kj2mN8pR...'
  };

  const timeSeriesData = [
    { date: '2024-01', biomass: 120, co2: 50 },
    { date: '2024-02', biomass: 145, co2: 68 },
    { date: '2024-03', biomass: 180, co2: 89 },
    { date: '2024-04', biomass: 220, co2: 115 },
    { date: '2024-05', biomass: 275, co2: 145 },
    { date: '2024-06', biomass: 320, co2: 180 }
  ];

  const milestones = [
    { date: '2024-01-15', title: 'Project Registration', status: 'completed', description: 'Initial project setup and baseline data collection' },
    { date: '2024-02-01', title: 'Seedling Planting', status: 'completed', description: '10,000 mangrove seedlings planted across 5 hectares' },
    { date: '2024-03-15', title: 'First Monitoring', status: 'completed', description: 'Initial growth monitoring and survival rate assessment' },
    { date: '2024-05-01', title: 'MRV Analysis', status: 'completed', description: 'AI-powered biomass estimation and CO₂ calculation' },
    { date: '2024-06-15', title: 'Verification Complete', status: 'completed', description: 'Third-party audit completed, credits minted' },
    { date: '2024-09-01', title: 'Next Monitoring', status: 'upcoming', description: 'Quarterly monitoring and growth assessment' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <Link 
            to="/dashboard" 
            className="inline-flex items-center text-teal-600 hover:text-teal-700 mb-4 transition-colors"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Dashboard
          </Link>
          
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
            <div>
              <h1 className="text-3xl font-bold text-slate-800 mb-2">{project.name}</h1>
              <div className="flex items-center space-x-4 text-slate-600">
                <div className="flex items-center">
                  <MapPin className="w-4 h-4 mr-1" />
                  <span>{project.location}</span>
                </div>
                <div className="flex items-center">
                  <Calendar className="w-4 h-4 mr-1" />
                  <span>Started {new Date(project.startDate).toLocaleDateString()}</span>
                </div>
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800">
                  {project.type}
                </span>
              </div>
            </div>
            
            <div className="mt-4 md:mt-0">
              <div className="text-right">
                <div className="text-2xl font-bold text-teal-600">{project.creditsIssued}</div>
                <div className="text-sm text-slate-600">Carbon Credits Issued</div>
              </div>
            </div>
          </div>
        </div>

        {/* Key Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-emerald-100 p-3 rounded-lg">
                <Leaf className="w-6 h-6 text-emerald-600" />
              </div>
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">{project.area} ha</h3>
            <p className="text-slate-600">Total Area</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-blue-100 p-3 rounded-lg">
                <TrendingUp className="w-6 h-6 text-blue-600" />
              </div>
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">{project.co2Estimated}</h3>
            <p className="text-slate-600">CO₂ Tons Estimated</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-green-100 p-3 rounded-lg">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">{project.co2Verified}</h3>
            <p className="text-slate-600">CO₂ Tons Verified</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-purple-100 p-3 rounded-lg">
                <Award className="w-6 h-6 text-purple-600" />
              </div>
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">{project.creditsIssued}</h3>
            <p className="text-slate-600">Credits Minted</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* Project Timeline Chart */}
          <div className="lg:col-span-2 bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-6">CO₂ Sequestration Progress</h2>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={timeSeriesData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="date" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '1px solid #e2e8f0',
                    borderRadius: '8px'
                  }}
                />
                <Area 
                  type="monotone" 
                  dataKey="co2" 
                  stroke="#0d9488" 
                  fill="#0d9488" 
                  fillOpacity={0.6}
                  name="CO₂ Sequestered (tons)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* Project Info */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-6">Project Information</h2>
            
            <div className="space-y-4">
              <div>
                <h3 className="font-medium text-slate-800 mb-1">Organization</h3>
                <p className="text-slate-600">{project.ngo}</p>
              </div>

              <div>
                <h3 className="font-medium text-slate-800 mb-1">Methodology</h3>
                <p className="text-slate-600">{project.methodology}</p>
              </div>

              <div>
                <h3 className="font-medium text-slate-800 mb-1">Status</h3>
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                  <CheckCircle className="w-3 h-3 mr-1" />
                  {project.status}
                </span>
              </div>

              <div>
                <h3 className="font-medium text-slate-800 mb-1">Verified By</h3>
                <p className="text-slate-600">{project.auditor}</p>
              </div>

              <div>
                <h3 className="font-medium text-slate-800 mb-1">Verification Date</h3>
                <p className="text-slate-600">{new Date(project.verificationDate).toLocaleDateString()}</p>
              </div>
            </div>

            <div className="mt-6 pt-6 border-t border-slate-200">
              <h3 className="font-medium text-slate-800 mb-3">Blockchain Verification</h3>
              <div className="space-y-2">
                <button className="w-full text-left p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors flex items-center justify-between">
                  <span className="text-sm text-slate-700">View on Blockchain</span>
                  <ExternalLink className="w-4 h-4 text-slate-600" />
                </button>
                <button className="w-full text-left p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors flex items-center justify-between">
                  <span className="text-sm text-slate-700">IPFS Data Storage</span>
                  <ExternalLink className="w-4 h-4 text-slate-600" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Project Description and Milestones */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Description */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">Project Description</h2>
            <p className="text-slate-600 leading-relaxed mb-6">{project.description}</p>
            
            <div className="flex items-center space-x-4">
              <button className="bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2">
                <Download className="w-4 h-4" />
                <span>Download Report</span>
              </button>
              <button className="text-teal-600 hover:text-teal-700 px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2">
                <FileText className="w-4 h-4" />
                <span>View MRV Data</span>
              </button>
            </div>
          </div>

          {/* Timeline */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-6">Project Timeline</h2>
            
            <div className="space-y-4">
              {milestones.map((milestone, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className={`flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center ${
                    milestone.status === 'completed' ? 'bg-green-100' : 'bg-slate-100'
                  }`}>
                    {milestone.status === 'completed' ? (
                      <CheckCircle className="w-4 h-4 text-green-600" />
                    ) : (
                      <div className="w-2 h-2 bg-slate-400 rounded-full" />
                    )}
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <h3 className="font-medium text-slate-800">{milestone.title}</h3>
                      <span className="text-sm text-slate-500">{new Date(milestone.date).toLocaleDateString()}</span>
                    </div>
                    <p className="text-sm text-slate-600">{milestone.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}