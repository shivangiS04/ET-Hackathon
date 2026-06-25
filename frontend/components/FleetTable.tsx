'use client';

import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { TrendingUp, Zap, CheckCircle, AlertCircle } from 'lucide-react';

export default function FleetTable() {
  const [fleetData, setFleetData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/fleet/vehicles');
        const data = await response.json();
        setFleetData(data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching fleet data:', error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading fleet data...</p>
        </div>
      </div>
    );
  }

  const readinessData = [
    { route: 'Delhi-IP', readiness: 94.5 },
    { route: 'Mum-Pune', readiness: 91.2 },
    { route: 'Urban MG', readiness: 98.0 },
    { route: 'Long-haul', readiness: 65.3 }
  ];

  const transitionTimeline = [
    { phase: 'Q1 2025', vehicles: 15, investment: 45, charging: 8 },
    { phase: 'Q2-Q3 2025', vehicles: 20, investment: 60, charging: 12 },
    { phase: 'Q4 2025', vehicles: 15, investment: 45, charging: 10 }
  ];

  return (
    <div className="space-y-6">
      {/* Fleet Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <p className="text-sm text-gray-600">Fleet Size</p>
          <p className="text-3xl font-bold text-green-600 mt-2">{fleetData?.fleet_size || 58}</p>
          <p className="text-xs text-gray-500 mt-2">Total vehicles</p>
        </div>

        <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-6">
          <p className="text-sm text-gray-600">EV Ready</p>
          <p className="text-3xl font-bold text-emerald-600 mt-2">{fleetData?.ready_percent || 72.4}%</p>
          <p className="text-xs text-gray-500 mt-2">{fleetData?.ready_count || 42} vehicles</p>
        </div>

        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <p className="text-sm text-gray-600">Conditional</p>
          <p className="text-3xl font-bold text-yellow-600 mt-2">{fleetData?.conditional_count || 12}</p>
          <p className="text-xs text-gray-500 mt-2">With 6-12 month timeline</p>
        </div>

        <div className="bg-orange-50 border border-orange-200 rounded-lg p-6">
          <p className="text-sm text-gray-600">CO₂ Reduction Potential</p>
          <p className="text-3xl font-bold text-orange-600 mt-2">{fleetData?.co2_reduction_potential_tons_annual || 1250}</p>
          <p className="text-xs text-gray-500 mt-2">tons annually</p>
        </div>
      </div>

      {/* Readiness Scoring */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Readiness Scores by Route */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">EV Readiness Scores by Route</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={readinessData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="route" />
              <YAxis domain={[0, 100]} />
              <Tooltip formatter={(value) => `${value}%`} />
              <Bar dataKey="readiness" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Investment Timeline */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Investment Phase Timeline</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={transitionTimeline}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="phase" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Legend />
              <Bar yAxisId="left" dataKey="vehicles" fill="#3b82f6" name="Vehicles" />
              <Bar yAxisId="right" dataKey="investment" fill="#8b5cf6" name="Investment (₹Cr)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Fleet Status Table */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Fleet Status & Recommendations</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-4 py-2 text-left font-semibold text-gray-700">VID</th>
                <th className="px-4 py-2 text-left font-semibold text-gray-700">Route</th>
                <th className="px-4 py-2 text-left font-semibold text-gray-700">EV Model</th>
                <th className="px-4 py-2 text-center font-semibold text-gray-700">Readiness</th>
                <th className="px-4 py-2 text-left font-semibold text-gray-700">Status</th>
              </tr>
            </thead>
            <tbody>
              {fleetData?.vehicles?.map((vehicle: any) => (
                <tr key={vehicle.vehicle_id} className="border-b border-gray-200 hover:bg-gray-50">
                  <td className="px-4 py-3 font-bold text-gray-900">{vehicle.vehicle_id}</td>
                  <td className="px-4 py-3 text-gray-700">{vehicle.route}</td>
                  <td className="px-4 py-3 text-gray-700">{vehicle.ev_model}</td>
                  <td className="px-4 py-3 text-center">
                    <div className="flex items-center justify-center gap-1">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div
                          className="h-2 rounded-full"
                          style={{
                            width: `${vehicle.readiness_score}%`,
                            backgroundColor: vehicle.readiness_score >= 90 ? '#10b981' : vehicle.readiness_score >= 70 ? '#f59e0b' : '#ef4444'
                          }}
                        />
                      </div>
                      <span className="text-xs font-semibold text-gray-700 w-10">{vehicle.readiness_score}%</span>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-1">
                      {vehicle.status === '✓' ? (
                        <CheckCircle className="w-4 h-4 text-green-600" />
                      ) : (
                        <AlertCircle className="w-4 h-4 text-orange-600" />
                      )}
                      <span className="text-xs font-semibold text-gray-700">{vehicle.readiness_level}</span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Financial Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Zap className="w-5 h-5 text-blue-600" />
            Financial Projections
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center pb-2 border-b border-blue-100">
              <span className="text-gray-700">Total Investment Required</span>
              <span className="font-bold text-gray-900">₹200 Cr</span>
            </div>
            <div className="flex justify-between items-center pb-2 border-b border-blue-100">
              <span className="text-gray-700">Annual Fuel Savings</span>
              <span className="font-bold text-green-600">₹35 Cr</span>
            </div>
            <div className="flex justify-between items-center pb-2 border-b border-blue-100">
              <span className="text-gray-700">Maintenance Savings</span>
              <span className="font-bold text-green-600">₹8 Cr</span>
            </div>
            <div className="flex justify-between items-center pt-2">
              <span className="font-semibold text-gray-900">Payback Period</span>
              <span className="text-2xl font-bold text-blue-600">4.8 years</span>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-green-600" />
            Infrastructure Requirements
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center pb-2 border-b border-green-100">
              <span className="text-gray-700">Fast Charging Stations</span>
              <span className="font-bold text-gray-900">15</span>
            </div>
            <div className="flex justify-between items-center pb-2 border-b border-green-100">
              <span className="text-gray-700">Medium Charging Points</span>
              <span className="font-bold text-gray-900">20</span>
            </div>
            <div className="flex justify-between items-center pb-2 border-b border-green-100">
              <span className="text-gray-700">Depot Slow Charging</span>
              <span className="font-bold text-gray-900">45</span>
            </div>
            <div className="flex justify-between items-center pt-2">
              <span className="font-semibold text-gray-900">Peak Power Requirement</span>
              <span className="text-2xl font-bold text-green-600">8.5 MW</span>
            </div>
          </div>
        </div>
      </div>

      {/* Key Recommendations */}
      <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Strategic Recommendations</h3>
        <ul className="space-y-2">
          <li className="flex gap-3 text-gray-700">
            <span className="text-purple-600 font-bold">✓</span>
            <span><strong>Q1 2025:</strong> Start with 15 urban vehicles (highest readiness scores)</span>
          </li>
          <li className="flex gap-3 text-gray-700">
            <span className="text-purple-600 font-bold">✓</span>
            <span><strong>Subsidy Strategy:</strong> Leverage FAME-II for ₹40 Cr grant support</span>
          </li>
          <li className="flex gap-3 text-gray-700">
            <span className="text-purple-600 font-bold">✓</span>
            <span><strong>Long-term Contracts:</strong> Secure battery pricing with 3-year lock-in</span>
          </li>
          <li className="flex gap-3 text-gray-700">
            <span className="text-purple-600 font-bold">✓</span>
            <span><strong>Charging Partner:</strong> Collaborate with existing charging networks (Fortum, Shell)</span>
          </li>
        </ul>
      </div>
    </div>
  );
}
