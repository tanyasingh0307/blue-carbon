import React, { useState } from 'react';
import { mrvAPI, creditsAPI } from '../services/api';
import { 
  Shield, 
  CheckCircle, 
  Clock, 
  FileText, 
  TrendingUp, 
  AlertCircle,
  Download,
  ExternalLink,
  Award,
  BarChart3,
  Eye
} from 'lucide-react';

export function AuditorDashboard() {
  const [selectedReport, setSelectedReport] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const [reports] = useState([
    {
      id: 1,
      projectName: 'Mangrove Restoration Bay Area',
      ngo: 'Blue Ocean Foundation',
      submittedDate: '2024-06-14',
      co2Estimated: 450,
      area: 25.5,
      status: 'Pending Review',
      priority: 'High',
      methodology: 'Biomass sampling + Satellite imagery',
      dataPoints: 156,
      confidence: 94
    },
    {
      id: 2,
      projectName: 'Seagrass Recovery Project',
      ngo: 'Coastal Restoration Initiative',
      submittedDate: '2024-06-12',
      co2Estimated: 280,
      area: 18.2,
      status: 'Under Review',
      priority: 'Medium',
      methodology: 'Core sampling + Remote sensing',
      dataPoints: 89,
      confidence: 87
    },
    {
      id: 3,
      projectName: 'Salt Marsh Conservation',
      ngo: 'Marine Conservation Society',
      submittedDate: '2024-06-10',
      co2Estimated: 180,
      area: 12.8,
      status: 'Approved',
      priority: 'Low',
      methodology: 'Field measurements + LiDAR',
      dataPoints: 203,
      confidence: 96
    }
  ]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Pending Review':
        return 'bg-yellow-100 text-yellow-800';
      case 'Under Review':
        return 'bg-blue-100 text-blue-800';
      case 'Approved':
        return 'bg-green-100 text-green-800';
      case 'Rejected':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'High':
        return 'bg-red-100 text-red-800';
      case 'Medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'Low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const handleApproveReport = (reportId: number) => {
    handleApproveAndMint(reportId);
  };

  const handleApproveAndMint = async (reportId: number) => {
    setLoading(true);
    try {
      // First approve the report
      await mrvAPI.verifyReport(reportId.toString(), {
        status: 'approved',
        auditor_notes: 'Report approved after thorough review'
      });
      
      // Then mint carbon credits
      await creditsAPI.mintCredits({
        mrv_report_id: reportId.toString(),
        total_supply: 320, // Based on CO2 tons
        price_per_credit: 12.50,
        quality_grade: 'premium'
      });
      
      alert('Report approved and carbon credits minted successfully!');
      // Refresh the page to show updated status
      window.location.reload();
    } catch (error) {
      console.error('Error approving report:', error);
      alert('Error approving report. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-800 mb-2">Auditor Portal</h1>
          <p className="text-slate-600">Review and verify MRV reports for carbon credit minting</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-yellow-100 p-3 rounded-lg">
                <Clock className="w-6 h-6 text-yellow-600" />
              </div>
              <span className="text-yellow-600 text-sm font-medium">+2 new</span>
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">8</h3>
            <p className="text-slate-600">Pending Reviews</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-green-100 p-3 rounded-lg">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
              <span className="text-green-600 text-sm font-medium">This month</span>
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">24</h3>
            <p className="text-slate-600">Reports Approved</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-purple-100 p-3 rounded-lg">
                <Award className="w-6 h-6 text-purple-600" />
              </div>
              <span className="text-purple-600 text-sm font-medium">5.2K tons</span>
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">3,840</h3>
            <p className="text-slate-600">Credits Minted</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-blue-100 p-3 rounded-lg">
                <BarChart3 className="w-6 h-6 text-blue-600" />
              </div>
              <span className="text-blue-600 text-sm font-medium">96.2%</span>
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">4.8</h3>
            <p className="text-slate-600">Avg Quality Score</p>
          </div>
        </div>

        {/* Reports Queue */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="p-6 border-b border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800">MRV Reports Queue</h2>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50">
                <tr>
                  <th className="text-left py-3 px-6 text-sm font-medium text-slate-600">Project & NGO</th>
                  <th className="text-left py-3 px-6 text-sm font-medium text-slate-600">Data Quality</th>
                  <th className="text-left py-3 px-6 text-sm font-medium text-slate-600">CO₂ Estimate</th>
                  <th className="text-left py-3 px-6 text-sm font-medium text-slate-600">Status</th>
                  <th className="text-left py-3 px-6 text-sm font-medium text-slate-600">Priority</th>
                  <th className="text-left py-3 px-6 text-sm font-medium text-slate-600">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {reports.map((report) => (
                  <tr key={report.id} className="hover:bg-slate-50">
                    <td className="py-4 px-6">
                      <div>
                        <h3 className="font-medium text-slate-800">{report.projectName}</h3>
                        <p className="text-sm text-slate-600">{report.ngo}</p>
                        <p className="text-xs text-slate-500 mt-1">
                          Submitted {new Date(report.submittedDate).toLocaleDateString()}
                        </p>
                      </div>
                    </td>
                    <td className="py-4 px-6">
                      <div>
                        <div className="flex items-center space-x-2 mb-1">
                          <div className="w-full bg-slate-200 rounded-full h-2">
                            <div 
                              className="bg-green-500 h-2 rounded-full" 
                              style={{ width: `${report.confidence}%` }}
                            />
                          </div>
                          <span className="text-sm font-medium text-slate-700">{report.confidence}%</span>
                        </div>
                        <p className="text-xs text-slate-600">{report.dataPoints} data points</p>
                        <p className="text-xs text-slate-500">{report.methodology}</p>
                      </div>
                    </td>
                    <td className="py-4 px-6">
                      <div>
                        <p className="text-slate-800 font-medium">{report.co2Estimated} tons</p>
                        <p className="text-sm text-slate-600">{report.area} hectares</p>
                      </div>
                    </td>
                    <td className="py-4 px-6">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(report.status)}`}>
                        {report.status}
                      </span>
                    </td>
                    <td className="py-4 px-6">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(report.priority)}`}>
                        {report.priority}
                      </span>
                    </td>
                    <td className="py-4 px-6">
                      <div className="flex items-center space-x-2">
                        <button className="text-blue-600 hover:text-blue-700 p-2 rounded-lg hover:bg-blue-50 transition-colors">
                          <Eye className="w-4 h-4" />
                        </button>
                        <button className="text-slate-600 hover:text-slate-700 p-2 rounded-lg hover:bg-slate-50 transition-colors">
                          <Download className="w-4 h-4" />
                        </button>
                        {report.status === 'Pending Review' && (
                          <button
                            onClick={() => handleApproveReport(report.id)}
                            disabled={loading}
                            className="bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white px-3 py-1 rounded-lg text-sm font-medium transition-colors"
                          >
                            {loading ? 'Processing...' : 'Approve & Mint'}
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Quality Metrics */}
        <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Verification Standards */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <h3 className="text-lg font-semibold text-slate-800 mb-6">Verification Standards</h3>
            
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <div>
                    <h4 className="font-medium text-slate-800">Data Quality</h4>
                    <p className="text-sm text-slate-600">Minimum 85% confidence required</p>
                  </div>
                </div>
                <span className="text-green-600 font-semibold">✓</span>
              </div>

              <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <Shield className="w-5 h-5 text-blue-600" />
                  <div>
                    <h4 className="font-medium text-slate-800">Methodology</h4>
                    <p className="text-sm text-slate-600">IPCC compliant calculations</p>
                  </div>
                </div>
                <span className="text-blue-600 font-semibold">✓</span>
              </div>

              <div className="flex items-center justify-between p-4 bg-purple-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <FileText className="w-5 h-5 text-purple-600" />
                  <div>
                    <h4 className="font-medium text-slate-800">Documentation</h4>
                    <p className="text-sm text-slate-600">Complete audit trail required</p>
                  </div>
                </div>
                <span className="text-purple-600 font-semibold">✓</span>
              </div>
            </div>
          </div>

          {/* Blockchain Integration */}
          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <h3 className="text-lg font-semibold text-slate-800 mb-6">Blockchain Integration</h3>
            
            <div className="space-y-4">
              <div className="p-4 bg-slate-50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-slate-800">Smart Contract</span>
                  <ExternalLink className="w-4 h-4 text-slate-600" />
                </div>
                <p className="text-sm text-slate-600">ERC-1155 Carbon Credits</p>
                <p className="text-xs text-slate-500 font-mono mt-1">0x742d...8f3a</p>
              </div>

              <div className="p-4 bg-slate-50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-slate-800">Network</span>
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                </div>
                <p className="text-sm text-slate-600">Polygon Mumbai Testnet</p>
                <p className="text-xs text-slate-500">Gas fee: ~$0.001</p>
              </div>

              <div className="p-4 bg-slate-50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium text-slate-800">IPFS Storage</span>
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                </div>
                <p className="text-sm text-slate-600">MRV data immutably stored</p>
                <p className="text-xs text-slate-500">Decentralized verification</p>
              </div>
            </div>

            <button className="w-full mt-4 bg-teal-600 hover:bg-teal-700 text-white py-2 rounded-lg font-medium transition-colors">
              View Contract on PolygonScan
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}