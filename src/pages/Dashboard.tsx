import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { 
  BarChart3, 
  Leaf, 
  Shield, 
  TrendingUp, 
  Users, 
  Globe,
  ArrowUpRight,
  Award,
  Activity
} from 'lucide-react';
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts';

export function Dashboard() {
  const { user } = useAuth();

  const chartData = [
    { month: 'Jan', sequestered: 120, verified: 100 },
    { month: 'Feb', sequestered: 180, verified: 150 },
    { month: 'Mar', sequestered: 250, verified: 220 },
    { month: 'Apr', sequestered: 320, verified: 280 },
    { month: 'May', sequestered: 420, verified: 380 },
    { month: 'Jun', sequestered: 550, verified: 520 }
  ];

  const projectTypes = [
    { name: 'Mangroves', value: 45, color: '#10B981' },
    { name: 'Seagrass', value: 30, color: '#0EA5E9' },
    { name: 'Salt Marshes', value: 25, color: '#8B5CF6' }
  ];

  const stats = [
    {
      title: 'Total Projects',
      value: '47',
      change: '+12%',
      icon: <Globe className="w-6 h-6" />,
      color: 'bg-blue-500'
    },
    {
      title: 'CO₂ Sequestered',
      value: '12.4K tons',
      change: '+8.2%',
      icon: <Leaf className="w-6 h-6" />,
      color: 'bg-emerald-500'
    },
    {
      title: 'Credits Minted',
      value: '8.9K',
      change: '+15%',
      icon: <Award className="w-6 h-6" />,
      color: 'bg-purple-500'
    },
    {
      title: 'Active Auditors',
      value: '24',
      change: '+3',
      icon: <Shield className="w-6 h-6" />,
      color: 'bg-orange-500'
    }
  ];

  const roleBasedCards = {
    ngo: [
      { title: 'Register New Project', description: 'Start a new blue carbon restoration project', link: '/ngo', icon: <Leaf className="w-6 h-6" /> },
      { title: 'Project Analytics', description: 'View detailed analytics for your projects', link: '/ngo', icon: <BarChart3 className="w-6 h-6" /> }
    ],
    auditor: [
      { title: 'Pending Verifications', description: 'Review and verify MRV reports', link: '/auditor', icon: <Shield className="w-6 h-6" /> },
      { title: 'Audit History', description: 'View your verification history', link: '/auditor', icon: <Activity className="w-6 h-6" /> }
    ],
    corporate: [
      { title: 'Browse Marketplace', description: 'Purchase verified carbon credits', link: '/marketplace', icon: <TrendingUp className="w-6 h-6" /> },
      { title: 'Portfolio Overview', description: 'Manage your carbon credit portfolio', link: '/marketplace', icon: <BarChart3 className="w-6 h-6" /> }
    ],
    government: [
      { title: 'Policy Dashboard', description: 'Monitor compliance and regulations', link: '/dashboard', icon: <Users className="w-6 h-6" /> },
      { title: 'Regional Analytics', description: 'View regional restoration progress', link: '/dashboard', icon: <Globe className="w-6 h-6" /> }
    ]
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-800 mb-2">
            Welcome back, {user?.name || 'User'}
            <span className="ml-4 text-sm bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
              Demo Mode - Backend Optional
            </span>
          </h1>
          <p className="text-slate-600">
            {user?.role === 'ngo' && 'Monitor your restoration projects and their impact'}
            {user?.role === 'auditor' && 'Review pending verifications and maintain quality standards'}
            {user?.role === 'corporate' && 'Track your carbon credit purchases and retirements'}
            {user?.role === 'government' && 'Oversee regional blue carbon initiatives and policy compliance'}
            {!user && 'Overview of the global blue carbon ecosystem'}
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <div key={index} className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
              <div className="flex items-center justify-between mb-4">
                <div className={`${stat.color} p-3 rounded-lg text-white`}>
                  {stat.icon}
                </div>
                <div className="text-emerald-600 text-sm font-medium flex items-center">
                  <ArrowUpRight className="w-4 h-4 mr-1" />
                  {stat.change}
                </div>
              </div>
              <h3 className="text-2xl font-bold text-slate-800 mb-1">{stat.value}</h3>
              <p className="text-slate-600 text-sm">{stat.title}</p>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* CO₂ Sequestration Chart */}
          <div className="lg:col-span-2 bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-slate-800">CO₂ Sequestration Trends</h2>
              <div className="flex items-center space-x-4 text-sm">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-teal-500 rounded-full"></div>
                  <span className="text-slate-600">Sequestered</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-emerald-500 rounded-full"></div>
                  <span className="text-slate-600">Verified</span>
                </div>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" stroke="#64748b" />
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
                  dataKey="sequestered" 
                  stackId="1" 
                  stroke="#0d9488" 
                  fill="#0d9488" 
                  fillOpacity={0.6}
                />
                <Area 
                  type="monotone" 
                  dataKey="verified" 
                  stackId="2" 
                  stroke="#10b981" 
                  fill="#10b981" 
                  fillOpacity={0.8}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* Project Types Distribution */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800 mb-6">Project Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={projectTypes}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {projectTypes.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div className="mt-4 space-y-2">
              {projectTypes.map((type, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div 
                      className="w-3 h-3 rounded-full" 
                      style={{ backgroundColor: type.color }}
                    ></div>
                    <span className="text-slate-600">{type.name}</span>
                  </div>
                  <span className="font-medium text-slate-800">{type.value}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Role-based Action Cards */}
        {user && roleBasedCards[user.role] && (
          <div className="mb-8">
            <h2 className="text-2xl font-semibold text-slate-800 mb-6">Quick Actions</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {roleBasedCards[user.role].map((card, index) => (
                <Link
                  key={index}
                  to={card.link}
                  className="bg-white rounded-xl shadow-sm p-6 border border-slate-200 hover:shadow-md hover:border-teal-300 transition-all group"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className="bg-teal-100 p-3 rounded-lg text-teal-600 group-hover:bg-teal-600 group-hover:text-white transition-colors">
                      {card.icon}
                    </div>
                    <ArrowUpRight className="w-5 h-5 text-slate-400 group-hover:text-teal-600 transition-colors" />
                  </div>
                  <h3 className="text-lg font-semibold text-slate-800 mb-2">{card.title}</h3>
                  <p className="text-slate-600">{card.description}</p>
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* Recent Activity */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
          <h2 className="text-xl font-semibold text-slate-800 mb-6">Recent Activity</h2>
          <div className="space-y-4">
            {[
              { 
                action: 'New project "Mangrove Restoration Bay Area" registered',
                time: '2 hours ago',
                type: 'project',
                icon: <Leaf className="w-5 h-5 text-emerald-600" />
              },
              { 
                action: 'MRV report verified for Project #247',
                time: '4 hours ago',
                type: 'verification',
                icon: <Shield className="w-5 h-5 text-blue-600" />
              },
              { 
                action: '500 carbon credits minted to marketplace',
                time: '6 hours ago',
                type: 'minting',
                icon: <Award className="w-5 h-5 text-purple-600" />
              },
              { 
                action: 'Corporate buyer retired 200 credits',
                time: '8 hours ago',
                type: 'retirement',
                icon: <TrendingUp className="w-5 h-5 text-orange-600" />
              }
            ].map((activity, index) => (
              <div key={index} className="flex items-center space-x-4 p-4 bg-slate-50 rounded-lg">
                <div className="bg-white p-2 rounded-full">
                  {activity.icon}
                </div>
                <div className="flex-1">
                  <p className="text-slate-800 font-medium">{activity.action}</p>
                  <p className="text-slate-500 text-sm">{activity.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}