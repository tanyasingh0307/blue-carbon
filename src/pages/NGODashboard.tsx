import React, { useState } from 'react';
import { projectsAPI, mrvAPI } from '../services/api';
import { 
  Plus, 
  Upload, 
  MapPin, 
  Calendar, 
  TrendingUp, 
  FileText,
  CheckCircle,
  Clock,
  AlertCircle,
  Leaf,
  BarChart3
} from 'lucide-react';

export function NGODashboard() {
  const [showNewProjectModal, setShowNewProjectModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [projects] = useState([
    {
      id: 1,
      name: 'Mangrove Restoration Bay Area',
      location: 'Florida Keys, USA',
      type: 'Mangroves',
      area: 25.5,
      startDate: '2024-01-15',
      status: 'Active',
      co2Estimated: 450,
      co2Verified: 320,
      lastUpdate: '2024-06-15'
    },
    {
      id: 2,
      name: 'Seagrass Recovery Project',
      location: 'Chesapeake Bay, USA',
      type: 'Seagrass',
      area: 18.2,
      startDate: '2024-03-01',
      status: 'Under Review',
      co2Estimated: 280,
      co2Verified: 0,
      lastUpdate: '2024-06-10'
    },
    {
      id: 3,
      name: 'Salt Marsh Conservation',
      location: 'San Francisco Bay, USA',
      type: 'Salt Marshes',
      area: 12.8,
      startDate: '2024-02-20',
      status: 'Verified',
      co2Estimated: 180,
      co2Verified: 175,
      lastUpdate: '2024-06-12'
    }
  ]);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'Active':
        return <TrendingUp className="w-4 h-4 text-green-600" />;
      case 'Under Review':
        return <Clock className="w-4 h-4 text-yellow-600" />;
      case 'Verified':
        return <CheckCircle className="w-4 h-4 text-blue-600" />;
      default:
        return <AlertCircle className="w-4 h-4 text-gray-600" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Active':
        return 'bg-green-100 text-green-800';
      case 'Under Review':
        return 'bg-yellow-100 text-yellow-800';
      case 'Verified':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const handleCreateProject = async (formData: any) => {
    setLoading(true);
    try {
      const projectData = {
        name: formData.name,
        description: formData.description,
        location: formData.location,
        latitude: parseFloat(formData.latitude) || null,
        longitude: parseFloat(formData.longitude) || null,
        project_type: formData.project_type,
        area_hectares: parseFloat(formData.area_hectares),
        start_date: new Date().toISOString(),
        baseline_data: formData.baseline_data || {}
      };
      
      await projectsAPI.createProject(projectData);
      setShowNewProjectModal(false);
      // Refresh projects list
      window.location.reload();
    } catch (error) {
      console.error('Error creating project:', error);
      alert('Error creating project. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRunMRV = async (projectId: string) => {
    setLoading(true);
    try {
      const reportData = {
        report_period_start: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000).toISOString(),
        report_period_end: new Date().toISOString(),
        methodology: 'AI-powered biomass estimation + satellite analysis'
      };
      
      await mrvAPI.generateReport(projectId, reportData);
      alert('MRV analysis completed successfully!');
    } catch (error) {
      console.error('Error running MRV:', error);
      alert('Error running MRV analysis. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-slate-800 mb-2">NGO Project Portal</h1>
            <p className="text-slate-600">Manage your blue carbon restoration projects</p>
          </div>
          <button
            onClick={() => setShowNewProjectModal(true)}
            className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-3 rounded-lg font-medium flex items-center space-x-2 transition-colors mt-4 md:mt-0"
          >
            <Plus className="w-5 h-5" />
            <span>New Project</span>
          </button>
        </div>

        {/* Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-emerald-100 p-3 rounded-lg">
                <Leaf className="w-6 h-6 text-emerald-600" />
              </div>
              <span className="text-emerald-600 text-sm font-medium">+15%</span>
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">3</h3>
            <p className="text-slate-600">Active Projects</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-blue-100 p-3 rounded-lg">
                <BarChart3 className="w-6 h-6 text-blue-600" />
              </div>
              <span className="text-blue-600 text-sm font-medium">910 tons</span>
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">56.5</h3>
            <p className="text-slate-600">Total Area (hectares)</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-purple-100 p-3 rounded-lg">
                <TrendingUp className="w-6 h-6 text-purple-600" />
              </div>
              <span className="text-purple-600 text-sm font-medium">495 verified</span>
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">910</h3>
            <p className="text-slate-600">CO₂ Tons Estimated</p>
          </div>
        </div>

        {/* Projects Table */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="p-6 border-b border-slate-200">
            <h2 className="text-xl font-semibold text-slate-800">Your Projects</h2>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50">
                <tr>
                  <th className="text-left py-3 px-6 text-sm font-medium text-slate-600">Project</th>
                  <th className="text-left py-3 px-6 text-sm font-medium text-slate-600">Type & Location</th>
                  <th className="text-left py-3 px-6 text-sm font-medium text-slate-600">Area</th>
                  <th className="text-left py-3 px-6 text-sm font-medium text-slate-600">CO₂ Impact</th>
                  <th className="text-left py-3 px-6 text-sm font-medium text-slate-600">Status</th>
                  <th className="text-left py-3 px-6 text-sm font-medium text-slate-600">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {projects.map((project) => (
                  <tr key={project.id} className="hover:bg-slate-50">
                    <td className="py-4 px-6">
                      <div>
                        <h3 className="font-medium text-slate-800">{project.name}</h3>
                        <p className="text-sm text-slate-600 flex items-center mt-1">
                          <Calendar className="w-4 h-4 mr-1" />
                          Started {new Date(project.startDate).toLocaleDateString()}
                        </p>
                      </div>
                    </td>
                    <td className="py-4 px-6">
                      <div>
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800 mb-1">
                          {project.type}
                        </span>
                        <p className="text-sm text-slate-600 flex items-center">
                          <MapPin className="w-4 h-4 mr-1" />
                          {project.location}
                        </p>
                      </div>
                    </td>
                    <td className="py-4 px-6">
                      <span className="text-slate-800 font-medium">{project.area} ha</span>
                    </td>
                    <td className="py-4 px-6">
                      <div>
                        <p className="text-slate-800 font-medium">{project.co2Estimated} tons estimated</p>
                        <p className="text-sm text-slate-600">{project.co2Verified} tons verified</p>
                      </div>
                    </td>
                    <td className="py-4 px-6">
                      <span className={`inline-flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(project.status)}`}>
                        {getStatusIcon(project.status)}
                        <span>{project.status}</span>
                      </span>
                    </td>
                    <td className="py-4 px-6">
                      <div className="flex items-center space-x-2">
                        <button className="text-teal-600 hover:text-teal-700 text-sm font-medium">
                          View Details
                        </button>
                        <button 
                          onClick={() => handleRunMRV(project.id.toString())}
                          disabled={loading}
                          className="text-blue-600 hover:text-blue-700 text-sm font-medium disabled:opacity-50"
                        >
                          Run MRV
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* New Project Modal */}
      {showNewProjectModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="p-8">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-slate-800">Register New Project</h2>
                <button
                  onClick={() => setShowNewProjectModal(false)}
                  className="text-slate-400 hover:text-slate-600"
                >
                  ×
                </button>
              </div>

              <form className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Project Name
                  </label>
                  <input
                    type="text"
                    id="project-name"
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                    placeholder="Enter project name"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">
                      Project Type
                    </label>
                    <select 
                      id="project-type"
                      className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                    >
                      <option value="">Select type</option>
                      <option value="mangroves">Mangroves</option>
                      <option value="seagrass">Seagrass</option>
                      <option value="salt_marshes">Salt Marshes</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">
                      Area (hectares)
                    </label>
                    <input
                      type="number"
                      step="0.1"
                      id="area-hectares"
                      className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                      placeholder="0.0"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Location
                  </label>
                  <input
                    type="text"
                    id="location"
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                    placeholder="Enter project location"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    GPS Coordinates
                  </label>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <input
                      type="text"
                      id="latitude"
                      className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                      placeholder="Latitude"
                    />
                    <input
                      type="text"
                      id="longitude"
                      className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                      placeholder="Longitude"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Project Description
                  </label>
                  <textarea
                    rows={4}
                    id="description"
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                    placeholder="Describe your restoration project goals and methodology"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Upload Project Data
                  </label>
                  <div className="border-2 border-dashed border-slate-300 rounded-lg p-6">
                    <div className="text-center">
                      <Upload className="w-8 h-8 text-slate-400 mx-auto mb-2" />
                      <p className="text-slate-600 mb-2">Upload baseline data, photos, or documents</p>
                      <p className="text-sm text-slate-500">CSV, JSON, PDF, or image files</p>
                      <button
                        type="button"
                        className="mt-4 bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-lg font-medium transition-colors"
                      >
                        Choose Files
                      </button>
                    </div>
                  </div>
                </div>

                <div className="flex justify-end space-x-4 pt-6">
                  <button
                    type="button"
                    onClick={() => setShowNewProjectModal(false)}
                    className="px-6 py-3 text-slate-600 hover:text-slate-700 font-medium transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={loading}
                    className="bg-teal-600 hover:bg-teal-700 disabled:bg-teal-400 text-white px-6 py-3 rounded-lg font-medium transition-colors"
                    onClick={(e) => {
                      e.preventDefault();
                      const formData = {
                        name: (document.getElementById('project-name') as HTMLInputElement)?.value,
                        project_type: (document.getElementById('project-type') as HTMLSelectElement)?.value,
                        area_hectares: (document.getElementById('area-hectares') as HTMLInputElement)?.value,
                        location: (document.getElementById('location') as HTMLInputElement)?.value,
                        latitude: (document.getElementById('latitude') as HTMLInputElement)?.value,
                        longitude: (document.getElementById('longitude') as HTMLInputElement)?.value,
                        description: (document.getElementById('description') as HTMLTextAreaElement)?.value,
                      };
                      handleCreateProject(formData);
                    }}
                  >
                    {loading ? 'Creating...' : 'Register Project'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}