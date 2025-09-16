import React, { useState } from 'react';
import { marketplaceAPI } from '../services/api';
import { 
  TrendingUp, 
  ShoppingCart, 
  Award, 
  Filter,
  Search,
  ExternalLink,
  CheckCircle,
  MapPin,
  Calendar,
  Leaf,
  DollarSign
} from 'lucide-react';

export function Marketplace() {
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(false);
  
  const [credits] = useState([
    {
      id: 1,
      tokenId: 'BC-001',
      projectName: 'Mangrove Restoration Bay Area',
      location: 'Florida Keys, USA',
      type: 'Mangroves',
      totalCredits: 320,
      availableCredits: 180,
      price: 12.50,
      vintage: 2024,
      verificationDate: '2024-06-15',
      ngo: 'Blue Ocean Foundation',
      quality: 'Premium',
      txHash: '0x8f4b...7c2d'
    },
    {
      id: 2,
      tokenId: 'BC-002',
      projectName: 'Salt Marsh Conservation',
      location: 'San Francisco Bay, USA',
      type: 'Salt Marshes',
      totalCredits: 175,
      availableCredits: 175,
      price: 10.75,
      vintage: 2024,
      verificationDate: '2024-06-12',
      ngo: 'Marine Conservation Society',
      quality: 'Standard',
      txHash: '0x3a2f...9b8e'
    },
    {
      id: 3,
      tokenId: 'BC-003',
      projectName: 'Coastal Seagrass Restoration',
      location: 'Chesapeake Bay, USA',
      type: 'Seagrass',
      totalCredits: 240,
      availableCredits: 90,
      price: 15.25,
      vintage: 2024,
      verificationDate: '2024-06-08',
      ngo: 'Coastal Restoration Initiative',
      quality: 'Premium',
      txHash: '0x7d1c...4f5a'
    },
    {
      id: 4,
      tokenId: 'BC-004',
      projectName: 'Mangrove Reforestation Pacific',
      location: 'Costa Rica Pacific Coast',
      type: 'Mangroves',
      totalCredits: 450,
      availableCredits: 300,
      price: 9.80,
      vintage: 2024,
      verificationDate: '2024-06-05',
      ngo: 'Tropical Conservation Fund',
      quality: 'Standard',
      txHash: '0x6e4a...2b9c'
    }
  ]);

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'Mangroves':
        return 'bg-emerald-100 text-emerald-800';
      case 'Seagrass':
        return 'bg-blue-100 text-blue-800';
      case 'Salt Marshes':
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getQualityColor = (quality: string) => {
    return quality === 'Premium' 
      ? 'bg-yellow-100 text-yellow-800' 
      : 'bg-gray-100 text-gray-800';
  };

  const filteredCredits = credits.filter(credit => {
    const matchesFilter = filter === 'all' || credit.type.toLowerCase().includes(filter.toLowerCase());
    const matchesSearch = credit.projectName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         credit.location.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         credit.ngo.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const marketStats = {
    totalCredits: credits.reduce((sum, credit) => sum + credit.totalCredits, 0),
    availableCredits: credits.reduce((sum, credit) => sum + credit.availableCredits, 0),
    avgPrice: credits.reduce((sum, credit) => sum + credit.price, 0) / credits.length,
    totalProjects: credits.length
  };

  const handlePurchaseCredits = async (creditId: string, quantity: number, maxPrice: number) => {
    setLoading(true);
    try {
      await marketplaceAPI.purchaseCredits({
        carbon_credit_id: creditId,
        quantity: quantity,
        max_price_per_credit: maxPrice
      });
      
      alert(`Successfully purchased ${quantity} carbon credits!`);
      // Refresh the marketplace
      window.location.reload();
    } catch (error) {
      console.error('Error purchasing credits:', error);
      alert('Error purchasing credits. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRetireCredits = async (creditId: string, quantity: number) => {
    setLoading(true);
    try {
      await marketplaceAPI.retireCredits({
        carbon_credit_id: creditId,
        quantity: quantity,
        retirement_reason: 'Corporate carbon neutrality commitment'
      });
      
      alert(`Successfully retired ${quantity} carbon credits for climate impact!`);
      // Refresh the marketplace
      window.location.reload();
    } catch (error) {
      console.error('Error retiring credits:', error);
      alert('Error retiring credits. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-800 mb-2">Carbon Credit Marketplace</h1>
          <p className="text-slate-600">Buy and retire verified blue carbon credits from ocean restoration projects</p>
        </div>

        {/* Market Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-blue-100 p-3 rounded-lg">
                <Award className="w-6 h-6 text-blue-600" />
              </div>
              <span className="text-blue-600 text-sm font-medium">Total</span>
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">{marketStats.totalCredits.toLocaleString()}</h3>
            <p className="text-slate-600">Credits Minted</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-emerald-100 p-3 rounded-lg">
                <ShoppingCart className="w-6 h-6 text-emerald-600" />
              </div>
              <span className="text-emerald-600 text-sm font-medium">Available</span>
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">{marketStats.availableCredits.toLocaleString()}</h3>
            <p className="text-slate-600">For Purchase</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-purple-100 p-3 rounded-lg">
                <DollarSign className="w-6 h-6 text-purple-600" />
              </div>
              <span className="text-purple-600 text-sm font-medium">USD</span>
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">${marketStats.avgPrice.toFixed(2)}</h3>
            <p className="text-slate-600">Avg Price/Credit</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-teal-100 p-3 rounded-lg">
                <Leaf className="w-6 h-6 text-teal-600" />
              </div>
              <span className="text-teal-600 text-sm font-medium">Active</span>
            </div>
            <h3 className="text-2xl font-bold text-slate-800 mb-1">{marketStats.totalProjects}</h3>
            <p className="text-slate-600">Projects</p>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="bg-white rounded-xl shadow-sm p-6 border border-slate-200 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search projects, locations, or NGOs..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                />
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Filter className="w-5 h-5 text-slate-600" />
                <span className="text-sm font-medium text-slate-700">Filter by type:</span>
              </div>
              
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="px-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
              >
                <option value="all">All Types</option>
                <option value="mangroves">Mangroves</option>
                <option value="seagrass">Seagrass</option>
                <option value="salt marshes">Salt Marshes</option>
              </select>
            </div>
          </div>
        </div>

        {/* Credits Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
          {filteredCredits.map((credit) => (
            <div key={credit.id} className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-lg transition-shadow">
              {/* Card Header */}
              <div className="p-6 border-b border-slate-200">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-slate-800 mb-1">{credit.projectName}</h3>
                    <p className="text-sm text-slate-600 flex items-center">
                      <MapPin className="w-4 h-4 mr-1" />
                      {credit.location}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-teal-600">${credit.price}</div>
                    <div className="text-sm text-slate-500">per credit</div>
                  </div>
                </div>

                <div className="flex items-center space-x-2 mb-3">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(credit.type)}`}>
                    {credit.type}
                  </span>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${getQualityColor(credit.quality)}`}>
                    {credit.quality}
                  </span>
                  <span className="px-2 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-800">
                    {credit.vintage}
                  </span>
                </div>

                <p className="text-sm text-slate-600">{credit.ngo}</p>
              </div>

              {/* Credit Details */}
              <div className="p-6">
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <p className="text-sm text-slate-600 mb-1">Available</p>
                    <p className="text-lg font-semibold text-slate-800">{credit.availableCredits}</p>
                  </div>
                  <div>
                    <p className="text-sm text-slate-600 mb-1">Total Minted</p>
                    <p className="text-lg font-semibold text-slate-800">{credit.totalCredits}</p>
                  </div>
                </div>

                <div className="flex items-center justify-between text-sm text-slate-600 mb-4">
                  <div className="flex items-center">
                    <CheckCircle className="w-4 h-4 mr-1 text-green-600" />
                    <span>Verified</span>
                  </div>
                  <div className="flex items-center">
                    <Calendar className="w-4 h-4 mr-1" />
                    <span>{new Date(credit.verificationDate).toLocaleDateString()}</span>
                  </div>
                </div>

                {/* Progress Bar */}
                <div className="mb-4">
                  <div className="flex justify-between text-sm text-slate-600 mb-1">
                    <span>Sold</span>
                    <span>{Math.round((credit.totalCredits - credit.availableCredits) / credit.totalCredits * 100)}%</span>
                  </div>
                  <div className="w-full bg-slate-200 rounded-full h-2">
                    <div 
                      className="bg-teal-500 h-2 rounded-full" 
                      style={{ width: `${(credit.totalCredits - credit.availableCredits) / credit.totalCredits * 100}%` }}
                    />
                  </div>
                </div>

                {/* Actions */}
                <div className="flex space-x-3">
                  <button 
                    onClick={() => handlePurchaseCredits(credit.id.toString(), 10, credit.price)}
                    disabled={loading}
                    className="flex-1 bg-teal-600 hover:bg-teal-700 disabled:bg-teal-400 text-white py-2 px-4 rounded-lg font-medium transition-colors flex items-center justify-center space-x-2"
                  >
                    <ShoppingCart className="w-4 h-4" />
                    <span>{loading ? 'Processing...' : 'Purchase'}</span>
                  </button>
                  <button 
                    onClick={() => handleRetireCredits(credit.id.toString(), 5)}
                    disabled={loading}
                    className="px-4 py-2 text-teal-600 border border-teal-600 rounded-lg hover:bg-teal-50 disabled:opacity-50 transition-colors"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </button>
                </div>

                {/* Blockchain Info */}
                <div className="mt-4 pt-4 border-t border-slate-200">
                  <div className="flex items-center justify-between text-xs text-slate-500">
                    <span>Token ID: {credit.tokenId}</span>
                    <span className="font-mono">{credit.txHash}</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Empty State */}
        {filteredCredits.length === 0 && (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Search className="w-8 h-8 text-slate-400" />
            </div>
            <h3 className="text-lg font-medium text-slate-800 mb-2">No credits found</h3>
            <p className="text-slate-600">Try adjusting your search or filter criteria</p>
          </div>
        )}
      </div>
    </div>
  );
}