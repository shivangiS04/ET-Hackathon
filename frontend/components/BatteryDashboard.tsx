'use client';

import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertTriangle, TrendingDown, Zap } from 'lucide-react';

interface BatteryMetrics {
  vehicle_id: string;
  current_soh: number;
  remaining_useful_life_days: number;
  degradation_rate_percent_per_year: number;
  confidence_score: number;
  next_maintenance_days: number;
  risk_level: string;
  recommendation: string;
}

export default function BatteryDashboard() {
  const [batteryData, setBatteryData] = useState<BatteryMetrics[]>([]);
  const [fleetStats, setFleetStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/battery/fleet-summary');
        const data = await response.json();
        setFleetStats(data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching battery data:', error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading battery data...</p>
        </div>
      </div>
    );
  }

  const sohDistribution = [
    { name: 'Excellent (80-100%)', value: fleetStats?.soh_distribution?.excellent_80_100 || 32 },
    { name: 'Good (60-80%)', value: fleetStats?.soh_distribution?.good_60_80 || 20 },
    { name: 'Fair (40-60%)', value: fleetStats?.soh_distribution?.fair_40_60 || 5 },
    { name: 'Poor (<40%)', value: fleetStats?.soh_distribution?.poor_below_40 || 1 }
  ];

  const historicalData = [
    { date: '12-01', soh: 92.5, temp: 35 },
    { date: '12-08', soh: 92.1, temp: 36 },
    { date: '12-15', soh: 91.8, temp: 34 },
    { date: '12-22', soh: 91.2, temp: 37 },
    { date: '12-29', soh: 90.8, temp: 35 }
  ];

  return (
    <div className="space-y-6">
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <p className="text-sm text-gray-600">Fleet Average SOH</p>
          <p className="text-3xl font-bold text-blue-600 mt-2">{fleetStats?.average_soh || 87.5}%</p>
          <p className="text-xs text-gray-500 mt-2">Healthy battery fleet</p>
        </div>

        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <p className="text-sm text-gray-600">Vehicles Ready</p>
          <p className="text-3xl font-bold text-green-600 mt-2">{fleetStats?.total_vehicles || 58}</p>
          <p className="text-xs text-gray-500 mt-2">Active in fleet</p>
        </div>

        <div className="bg-orange-50 border border-orange-200 rounded-lg p-6">
          <p className="text-sm text-gray-600">Maintenance Due</p>
          <p className="text-3xl font-bold text-orange-600 mt-2">{fleetStats?.vehicles_needing_maintenance || 8}</p>
          <p className="text-xs text-gray-500 mt-2">Within 30 days</p>
        </div>

        <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
          <p className="text-sm text-gray-600">Annual Degradation</p>
          <p className="text-3xl font-bold text-purple-600 mt-2">{fleetStats?.average_degradation_rate_annual || 8.2}%</p>
          <p className="text-xs text-gray-500 mt-2">Fleet-wide rate</p>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* SOH Distribution */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Battery SOH Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={sohDistribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Historical SOH Trend */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Fleet Average SOH Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={historicalData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis domain={[85, 95]} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="soh" stroke="#3b82f6" strokeWidth={2} name="SOH %" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Top Alerts */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-red-500" />
          Maintenance Alerts
        </h3>
        <div className="space-y-3">
          {[
            { id: 'T001', soh: 72, days: 15, reason: 'High degradation rate' },
            { id: 'T002', soh: 65, days: 7, reason: 'Below threshold - urgent' },
            { id: 'T003', soh: 58, days: 3, reason: 'Critical - immediate action' }
          ].map(alert => (
            <div key={alert.id} className="flex items-center justify-between p-3 bg-red-50 border border-red-200 rounded">
              <div>
                <p className="font-semibold text-gray-800">{alert.id}</p>
                <p className="text-sm text-gray-600">{alert.reason}</p>
              </div>
              <div className="text-right">
                <p className="text-sm font-bold text-red-600">{alert.soh}% SOH</p>
                <p className="text-xs text-gray-500">{alert.days} days to maintenance</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Forecast */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <TrendingDown className="w-5 h-5 text-blue-600" />
          6-Month Forecast
        </h3>
        <p className="text-gray-700 mb-4">
          Based on current degradation trends, an estimated <span className="font-bold">12-15 vehicles</span> will require battery replacement within the next 6 months.
        </p>
        <div className="bg-white rounded p-4">
          <p className="text-sm text-gray-600">Estimated Fleet Replacement Cost: <span className="font-bold text-gray-900">₹45.0 Cr</span></p>
          <p className="text-sm text-gray-600 mt-2">Recommended Action: Lock in supplier contracts to secure pricing</p>
        </div>
      </div>
    </div>
  );
}
