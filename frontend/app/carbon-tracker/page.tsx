'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { Leaf, TrendingDown, Target, Zap, AlertCircle, CheckCircle } from 'lucide-react';

export default function CarbonTrackerPage() {
  const [carbonData, setCarbonData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    // Fetch carbon tracking data
    const fetchCarbonData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/analytics/carbon/tracking?fleet_size=156');
        const data = await response.json();
        setCarbonData(data);
      } catch (error) {
        console.error('Error fetching carbon data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchCarbonData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin">
            <Leaf className="w-12 h-12 text-green-600" />
          </div>
          <p className="mt-4 text-gray-600">Loading carbon data...</p>
        </div>
      </div>
    );
  }

  // Simulated historical emissions data
  const emissionsHistory = [
    { year: '2024', diesel: 850, ev: 105, total: 955 },
    { year: '2025', diesel: 760, ev: 210, total: 970 },
    { year: '2026', diesel: 680, ev: 315, total: 995 },
    { year: '2027', diesel: 550, ev: 420, total: 970 },
    { year: '2028', diesel: 420, ev: 525, total: 945 },
    { year: '2029', diesel: 250, ev: 630, total: 880 },
    { year: '2030', diesel: 85, ev: 735, total: 820 },
    { year: '2035', diesel: 10, ev: 1050, total: 1060 },
  ];

  // Net zero roadmap
  const roadmapMilestones = [
    { year: 2026, target: '30% EV', status: 'on-track', emissions_reduction: '15%' },
    { year: 2028, target: '50% EV', status: 'on-track', emissions_reduction: '25%' },
    { year: 2030, target: '85% EV', status: 'planned', emissions_reduction: '42%' },
    { year: 2035, target: '95% EV', status: 'planned', emissions_reduction: '92%' },
  ];

  const fleetEmissions = carbonData?.emissions || {
    diesel_fleet_annual_tons_co2: 850,
    ev_fleet_annual_tons_co2: 105,
    total_annual_emissions_tons_co2: 955
  };

  const fleetComposition = carbonData?.current_fleet || {
    diesel_vehicles: 100,
    ev_vehicles: 56,
    total_vehicles: 156
  };

  const pieData = [
    { name: 'Diesel Vehicles', value: fleetComposition.diesel_vehicles, color: '#ef4444' },
    { name: 'EV Vehicles', value: fleetComposition.ev_vehicles, color: '#10b981' },
  ];

  const reductionPotential = carbonData?.carbon_reduction || {
    potential_annual_reduction_tons_co2: 473,
    potential_reduction_percent: 64.2
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-50">
      {/* Header */}
      <header className="bg-white border-b border-green-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-green-600 to-emerald-600 rounded-lg p-2">
                <Leaf className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Net Zero Tracker</h1>
                <p className="text-xs text-gray-500">Carbon Emissions & Reduction Roadmap</p>
              </div>
            </div>
            <Link href="/" className="text-gray-600 hover:text-gray-900 font-medium">← Back</Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <div className="bg-white rounded-lg border border-green-200 p-6 hover:shadow-lg transition">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Current Annual Emissions</p>
                <p className="text-3xl font-bold text-red-600 mt-2">{fleetEmissions.total_annual_emissions_tons_co2}t</p>
                <p className="text-xs text-gray-500 mt-1">CO2 per year</p>
              </div>
              <AlertCircle className="w-10 h-10 text-red-500 opacity-20" />
            </div>
          </div>

          <div className="bg-white rounded-lg border border-green-200 p-6 hover:shadow-lg transition">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Reduction Potential</p>
                <p className="text-3xl font-bold text-green-600 mt-2">{reductionPotential.potential_reduction_percent}%</p>
                <p className="text-xs text-gray-500 mt-1">{reductionPotential.potential_annual_reduction_tons_co2}t saved</p>
              </div>
              <TrendingDown className="w-10 h-10 text-green-500 opacity-20" />
            </div>
          </div>

          <div className="bg-white rounded-lg border border-green-200 p-6 hover:shadow-lg transition">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">EV Fleet Percentage</p>
                <p className="text-3xl font-bold text-blue-600 mt-2">{((fleetComposition.ev_vehicles / fleetComposition.total_vehicles) * 100).toFixed(1)}%</p>
                <p className="text-xs text-gray-500 mt-1">{fleetComposition.ev_vehicles} of {fleetComposition.total_vehicles} vehicles</p>
              </div>
              <Zap className="w-10 h-10 text-blue-500 opacity-20" />
            </div>
          </div>

          <div className="bg-white rounded-lg border border-green-200 p-6 hover:shadow-lg transition">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Net Zero Target</p>
                <p className="text-3xl font-bold text-purple-600 mt-2">2035</p>
                <p className="text-xs text-gray-500 mt-1">95% EV Fleet Target</p>
              </div>
              <Target className="w-10 h-10 text-purple-500 opacity-20" />
            </div>
          </div>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg border border-green-200 mb-12">
          <div className="flex border-b border-green-100">
            {[
              { id: 'overview', label: 'Overview', icon: '📊' },
              { id: 'roadmap', label: 'Net Zero Roadmap', icon: '🎯' },
              { id: 'comparision', label: 'Diesel vs EV', icon: '⚡' },
              { id: 'impact', label: 'Environmental Impact', icon: '🌱' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-6 py-4 font-medium transition ${
                  activeTab === tab.id
                    ? 'text-green-600 border-b-2 border-green-600'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <span>{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>

          <div className="p-8">
            {/* Overview Tab */}
            {activeTab === 'overview' && (
              <div className="space-y-8">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-6">Historical & Projected Emissions Trend</h3>
                  <ResponsiveContainer width="100%" height={400}>
                    <AreaChart data={emissionsHistory}>
                      <defs>
                        <linearGradient id="colorDiesel" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                        </linearGradient>
                        <linearGradient id="colorEV" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="year" />
                      <YAxis />
                      <Tooltip formatter={(value) => `${value}t CO2`} />
                      <Legend />
                      <Area
                        type="monotone"
                        dataKey="diesel"
                        stackId="1"
                        stroke="#ef4444"
                        fillOpacity={1}
                        fill="url(#colorDiesel)"
                        name="Diesel Fleet"
                      />
                      <Area
                        type="monotone"
                        dataKey="ev"
                        stackId="1"
                        stroke="#10b981"
                        fillOpacity={1}
                        fill="url(#colorEV)"
                        name="EV Fleet"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                  <p className="text-sm text-gray-600 mt-4">
                    The chart shows projected emissions trajectory with progressive EV adoption. Peak emissions occur during transition period (2026-2027) when both diesel and EV vehicles operate simultaneously.
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-6">Current Fleet Composition</h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <PieChart>
                        <Pie
                          data={pieData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={(entry) => `${entry.name}: ${entry.value}`}
                          outerRadius={100}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {pieData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip formatter={(value) => `${value} vehicles`} />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-6">Annual Emissions by Fleet Type</h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={[
                        { name: 'Diesel', emissions: fleetEmissions.diesel_fleet_annual_tons_co2, color: '#ef4444' },
                        { name: 'EV', emissions: fleetEmissions.ev_fleet_annual_tons_co2, color: '#10b981' },
                      ]}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip formatter={(value) => `${value}t CO2`} />
                        <Bar dataKey="emissions" fill="#3b82f6" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>
            )}

            {/* Roadmap Tab */}
            {activeTab === 'roadmap' && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-8">Net Zero Transition Roadmap</h3>
                <div className="space-y-6">
                  {roadmapMilestones.map((milestone, index) => (
                    <div key={index} className="flex items-start gap-6">
                      <div className="flex-shrink-0 w-24">
                        <div className={`text-center py-3 rounded-lg ${
                          milestone.status === 'on-track' 
                            ? 'bg-green-100 border border-green-300' 
                            : 'bg-blue-100 border border-blue-300'
                        }`}>
                          <p className="text-2xl font-bold text-gray-900">{milestone.year}</p>
                        </div>
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-2">
                          <div>
                            <h4 className="text-lg font-semibold text-gray-900">{milestone.target}</h4>
                            <p className="text-sm text-gray-600">
                              {milestone.emissions_reduction} emissions reduction
                            </p>
                          </div>
                          <div className="flex items-center gap-2">
                            {milestone.status === 'on-track' ? (
                              <>
                                <CheckCircle className="w-5 h-5 text-green-600" />
                                <span className="text-sm font-semibold text-green-600">On Track</span>
                              </>
                            ) : (
                              <>
                                <Target className="w-5 h-5 text-blue-600" />
                                <span className="text-sm font-semibold text-blue-600">Planned</span>
                              </>
                            )}
                          </div>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-3">
                          <div 
                            className={`h-3 rounded-full ${milestone.status === 'on-track' ? 'bg-green-600' : 'bg-blue-600'}`}
                            style={{ width: `${(milestone.year - 2024) / (2035 - 2024) * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="bg-green-50 border border-green-200 rounded-lg p-6 mt-8">
                  <h4 className="font-semibold text-gray-900 mb-3">Key Success Factors</h4>
                  <ul className="space-y-2 text-sm text-gray-700">
                    <li className="flex items-start gap-2">
                      <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                      <span>Continuous infrastructure expansion aligned with vehicle deployment phases</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                      <span>Supply chain optimization to reduce battery costs and improve availability</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                      <span>Driver training and operational efficiency improvements</span>
                    </li>
                  </ul>
                </div>
              </div>
            )}

            {/* Comparison Tab */}
            {activeTab === 'comparision' && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-8">Operational Comparison: Diesel vs Electric</h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-50 border-b border-gray-200">
                      <tr>
                        <th className="px-6 py-3 text-left font-semibold text-gray-900">Metric</th>
                        <th className="px-6 py-3 text-center font-semibold text-red-600">Diesel Vehicle</th>
                        <th className="px-6 py-3 text-center font-semibold text-green-600">EV Vehicle</th>
                        <th className="px-6 py-3 text-center font-semibold text-blue-600">Advantage</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      <tr>
                        <td className="px-6 py-3 text-gray-900 font-medium">Annual CO2 Emissions</td>
                        <td className="px-6 py-3 text-center text-red-600 font-semibold">8.5 tons</td>
                        <td className="px-6 py-3 text-center text-green-600 font-semibold">2.1 tons</td>
                        <td className="px-6 py-3 text-center text-green-600 font-semibold">75% less</td>
                      </tr>
                      <tr className="bg-gray-50">
                        <td className="px-6 py-3 text-gray-900 font-medium">Annual Operating Cost</td>
                        <td className="px-6 py-3 text-center text-red-600 font-semibold">6.0 L</td>
                        <td className="px-6 py-3 text-center text-green-600 font-semibold">2.8 L</td>
                        <td className="px-6 py-3 text-center text-green-600 font-semibold">53% savings</td>
                      </tr>
                      <tr>
                        <td className="px-6 py-3 text-gray-900 font-medium">Fuel Efficiency</td>
                        <td className="px-6 py-3 text-center text-gray-600">4.2 km/liter</td>
                        <td className="px-6 py-3 text-center text-gray-600">5.5 km/kWh</td>
                        <td className="px-6 py-3 text-center text-green-600 font-semibold">More efficient</td>
                      </tr>
                      <tr className="bg-gray-50">
                        <td className="px-6 py-3 text-gray-900 font-medium">Maintenance Cost</td>
                        <td className="px-6 py-3 text-center text-gray-600">1.2 L/year</td>
                        <td className="px-6 py-3 text-center text-gray-600">0.4 L/year</td>
                        <td className="px-6 py-3 text-center text-green-600 font-semibold">67% less</td>
                      </tr>
                      <tr>
                        <td className="px-6 py-3 text-gray-900 font-medium">Lifetime Emissions</td>
                        <td className="px-6 py-3 text-center text-red-600 font-semibold">85 tons</td>
                        <td className="px-6 py-3 text-center text-green-600 font-semibold">21 tons</td>
                        <td className="px-6 py-3 text-center text-green-600 font-semibold">75% reduction</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Environmental Impact Tab */}
            {activeTab === 'impact' && (
              <div className="space-y-8">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-6">Environmental Impact Summary</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                      <h4 className="font-semibold text-gray-900 mb-4">2024 Baseline (Current)</h4>
                      <div className="space-y-3 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Total CO2 Emissions</span>
                          <span className="font-semibold text-red-600">955 tons/year</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Diesel Fleet Emissions</span>
                          <span className="font-semibold text-red-600">850 tons/year</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">EV Fleet Emissions</span>
                          <span className="font-semibold text-green-600">105 tons/year</span>
                        </div>
                      </div>
                    </div>

                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                      <h4 className="font-semibold text-gray-900 mb-4">2035 Net Zero Target</h4>
                      <div className="space-y-3 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Projected Total Emissions</span>
                          <span className="font-semibold text-green-600">1,060 tons/year</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Diesel Fleet Emissions</span>
                          <span className="font-semibold text-yellow-600">10 tons/year (1%)</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">EV Fleet Emissions</span>
                          <span className="font-semibold text-green-600">1,050 tons/year (99%)</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg p-8">
                  <h3 className="text-lg font-semibold text-gray-900 mb-6">Equivalent Environmental Impact</h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="text-center">
                      <p className="text-3xl font-bold text-green-600 mb-2">9,450</p>
                      <p className="text-sm text-gray-600">Trees planted equivalent</p>
                      <p className="text-xs text-gray-500 mt-2">By 2030 transition</p>
                    </div>
                    <div className="text-center">
                      <p className="text-3xl font-bold text-green-600 mb-2">1.2M</p>
                      <p className="text-sm text-gray-600">Kg plastic avoided</p>
                      <p className="text-xs text-gray-500 mt-2">Through reduced emissions</p>
                    </div>
                    <div className="text-center">
                      <p className="text-3xl font-bold text-green-600 mb-2">₹85Cr</p>
                      <p className="text-sm text-gray-600">External cost avoided</p>
                      <p className="text-xs text-gray-500 mt-2">Health + environmental damage</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Recommendations */}
        <div className="bg-white rounded-lg border border-green-200 p-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Recommended Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="border-l-4 border-green-600 pl-4">
              <h4 className="font-semibold text-gray-900">Accelerate Phase 2 Deployment</h4>
              <p className="text-sm text-gray-600 mt-2">Deploy 50 additional EV vehicles in Q3 2025 to reach 30% fleet electrification target ahead of schedule.</p>
              <p className="text-xs text-green-600 font-semibold mt-2">Impact: 180 tons CO2 reduction/year</p>
            </div>
            <div className="border-l-4 border-blue-600 pl-4">
              <h4 className="font-semibold text-gray-900">Charging Infrastructure Expansion</h4>
              <p className="text-sm text-gray-600 mt-2">Establish 15 new fast-charging stations to support 50% fleet EV transition by 2028.</p>
              <p className="text-xs text-blue-600 font-semibold mt-2">Investment: ₹3.5 Cr (payback: 3.8 years)</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
