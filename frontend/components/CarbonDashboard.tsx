'use client';

import React, { useState, useEffect } from 'react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  LineChart,
  Line
} from 'recharts';
import { TrendingDown, Leaf, Zap, Truck, AlertCircle, CheckCircle } from 'lucide-react';

interface RoadmapPhase {
  year: number;
  total_emissions_tonnes: number;
  ev_percentage: number;
  cumulative_savings_tonnes: number;
}

interface HighImpactVehicle {
  vehicle_id: string;
  vehicle_type: string;
  route_km_per_day: number;
  current_annual_emissions_tonnes: number;
  potential_annual_saving_tonnes: number;
  priority: string;
}

interface Supplier {
  supplier_id: string;
  country: string;
  annual_scope3_emissions_tonnes: number;
}

export default function CarbonDashboard() {
  const [roadmapData, setRoadmapData] = useState<RoadmapPhase[]>([]);
  const [highImpactVehicles, setHighImpactVehicles] = useState<HighImpactVehicle[]>([]);
  const [scopeData, setScopeData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch net-zero roadmap
        const roadmapResponse = await fetch(
          'http://localhost:8000/api/v1/carbon/net-zero-roadmap?total_vehicles=100&current_ev_count=15'
        );
        if (roadmapResponse.ok) {
          const roadmapResult = await roadmapResponse.json();
          setRoadmapData(roadmapResult.phases || []);
        }

        // Fetch high-impact targets
        const targetsResponse = await fetch('http://localhost:8000/api/v1/carbon/high-impact-targets', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify([])
        });
        if (targetsResponse.ok) {
          const targetsResult = await targetsResponse.json();
          setHighImpactVehicles(targetsResult.top_5_high_impact || []);
        }

        // Fetch scope3 analysis
        const scope3Response = await fetch('http://localhost:8000/api/v1/carbon/scope3-analysis', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify([])
        });
        if (scope3Response.ok) {
          const scope3Result = await scope3Response.json();
          setScopeData(scope3Result);
        }

        setLoading(false);
      } catch (err) {
        console.error('Error fetching carbon data:', err);
        setError('Failed to load carbon data');
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
          <p className="mt-4 text-gray-600 dark:text-gray-300">Loading carbon intelligence data...</p>
        </div>
      </div>
    );
  }

  // Prepare chart data for net-zero roadmap
  const roadmapChartData = roadmapData.map(phase => ({
    year: phase.year,
    baseline: phase.total_emissions_tonnes * 1.15, // Business as usual (15% higher)
    with_ev_transition: phase.total_emissions_tonnes,
    savings: phase.cumulative_savings_tonnes
  }));

  // Scope 1 vs Scope 3 data
  const scopeBreakdown = [
    { name: 'Scope 1\n(Direct)', value: 45, fill: '#ef4444' },
    { name: 'Scope 3\n(Supply Chain)', value: 55, fill: '#10b981' }
  ];

  // Priority distribution
  const priorityDistribution = highImpactVehicles.reduce(
    (acc, vehicle) => {
      const priority = vehicle.priority.toUpperCase();
      acc[priority] = (acc[priority] || 0) + 1;
      return acc;
    },
    {} as Record<string, number>
  );

  const totalCarbonSaved = roadmapData.length > 0 ? roadmapData[roadmapData.length - 1].cumulative_savings_tonnes : 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Carbon & Net Zero Intelligence</h2>
          <p className="text-gray-600 dark:text-gray-400 mt-1">Emissions tracking, EV transition planning & supply chain decarbonization</p>
        </div>
        <div className="flex items-center gap-2 bg-green-50 dark:bg-green-900/20 px-4 py-2 rounded-lg border border-green-200 dark:border-green-800">
          <Leaf className="w-5 h-5 text-green-600 dark:text-green-400" />
          <div>
            <p className="text-xs text-green-700 dark:text-green-300 uppercase">FAME-II Aligned</p>
            <p className="text-sm font-bold text-green-900 dark:text-green-200">30% EV Target</p>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 text-red-700 dark:text-red-400">
          {error}
        </div>
      )}

      {/* Hero Metric: CO2 Saved */}
      <div className="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/30 dark:to-emerald-900/30 border border-green-200 dark:border-green-800 rounded-lg p-8">
        <div className="flex items-end justify-between">
          <div>
            <p className="text-sm text-green-700 dark:text-green-300 uppercase tracking-wide font-semibold">Total CO₂ Saved This Year</p>
            <p className="text-5xl font-black text-green-600 dark:text-green-400 mt-2">{totalCarbonSaved.toFixed(0)}</p>
            <p className="text-green-700 dark:text-green-300 mt-1">tonnes CO₂ equivalent</p>
          </div>
          <div className="text-right">
            <div className="text-green-600 dark:text-green-400 text-sm mb-2">vs Business as Usual</div>
            <div className="flex items-center gap-2 text-green-700 dark:text-green-300">
              <TrendingDown className="w-5 h-5" />
              <span className="text-lg font-bold">-28.5%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Two Column: Roadmap Chart + Scope Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Net-Zero Roadmap Chart */}
        <div className="card">
          <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">Net-Zero Roadmap (FAME-II Aligned)</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={roadmapChartData}>
              <defs>
                <linearGradient id="colorBusiness" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0.1} />
                </linearGradient>
                <linearGradient id="colorEV" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0.1} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" className="dark:stroke-gray-700" />
              <XAxis dataKey="year" fontSize={12} stroke="#6b7280" className="dark:stroke-gray-500" />
              <YAxis fontSize={12} stroke="#6b7280" className="dark:stroke-gray-500" label={{ value: 'Tonnes CO₂', angle: -90, position: 'insideLeft' }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px'
                }}
              />
              <Legend />
              <Area
                type="monotone"
                dataKey="baseline"
                stackId="1"
                stroke="#ef4444"
                strokeDasharray="5 5"
                fill="url(#colorBusiness)"
                name="Business as Usual"
                isAnimationActive={true}
              />
              <Area
                type="monotone"
                dataKey="with_ev_transition"
                stackId="2"
                stroke="#10b981"
                fill="url(#colorEV)"
                name="With EV Transition"
              />
            </AreaChart>
          </ResponsiveContainer>
          <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <p className="text-xs text-gray-600 dark:text-gray-400">
              🎯 Target: 30% EV adoption by 2030 (FAME-II Policy)
              {roadmapData.length > 0 && (
                <>
                  <br />✅ Projected: {roadmapData[roadmapData.length - 1].ev_percentage.toFixed(1)}% EV by 2030
                </>
              )}
            </p>
          </div>
        </div>

        {/* Scope Breakdown Donut */}
        <div className="card">
          <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">Emissions by Scope</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={scopeBreakdown}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={2}
                dataKey="value"
                label={({ name, value }) => `${name} ${value}%`}
              >
                {scopeBreakdown.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px'
                }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="mt-4 space-y-2">
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <span className="text-gray-700 dark:text-gray-300">Scope 1: Direct Combustion</span>
              </div>
              <span className="font-bold text-gray-900 dark:text-white">45%</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span className="text-gray-700 dark:text-gray-300">Scope 3: Supply Chain</span>
              </div>
              <span className="font-bold text-gray-900 dark:text-white">55%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Top 5 High-Impact Vehicles Table */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-gray-900 dark:text-white">Top 5 High-Impact Vehicles for EV Transition</h3>
          <span className="text-xs bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300 px-3 py-1 rounded-full font-medium">
            {highImpactVehicles.length} vehicles analyzed
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="text-left py-3 px-4 font-semibold text-gray-900 dark:text-white">Vehicle ID</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900 dark:text-white">Type</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900 dark:text-white">Route (km/day)</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900 dark:text-white">Current Emissions</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900 dark:text-white">Potential Saving</th>
                <th className="text-left py-3 px-4 font-semibold text-gray-900 dark:text-white">Priority</th>
              </tr>
            </thead>
            <tbody>
              {highImpactVehicles.map((vehicle, idx) => (
                <tr key={idx} className="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition">
                  <td className="py-3 px-4 font-mono text-gray-900 dark:text-white">{vehicle.vehicle_id}</td>
                  <td className="py-3 px-4">
                    <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded text-xs font-medium">
                      {vehicle.vehicle_type}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-gray-700 dark:text-gray-300">{vehicle.route_km_per_day}</td>
                  <td className="py-3 px-4 font-bold text-gray-900 dark:text-white">
                    {vehicle.current_annual_emissions_tonnes.toFixed(1)} t
                  </td>
                  <td className="py-3 px-4 font-bold text-green-600 dark:text-green-400">
                    {vehicle.potential_annual_saving_tonnes.toFixed(1)} t
                  </td>
                  <td className="py-3 px-4">
                    {vehicle.priority === 'high' ? (
                      <span className="px-3 py-1 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-full text-xs font-bold flex items-center gap-1 w-fit">
                        <AlertCircle className="w-3 h-3" /> HIGH
                      </span>
                    ) : vehicle.priority === 'medium' ? (
                      <span className="px-3 py-1 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 rounded-full text-xs font-bold">
                        MEDIUM
                      </span>
                    ) : (
                      <span className="px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-full text-xs font-bold">
                        LOW
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {highImpactVehicles.length === 0 && (
          <div className="text-center py-8 text-gray-500 dark:text-gray-400">
            <Truck className="w-8 h-8 mx-auto mb-2 opacity-50" />
            <p>No high-impact vehicles data available</p>
          </div>
        )}
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <p className="text-xs text-blue-700 dark:text-blue-300 uppercase tracking-wide">Current EV %</p>
          <p className="text-2xl font-bold text-blue-600 dark:text-blue-400 mt-1">15%</p>
          <p className="text-xs text-blue-600 dark:text-blue-300 mt-1">15 of 100 vehicles</p>
        </div>

        <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
          <p className="text-xs text-green-700 dark:text-green-300 uppercase tracking-wide">2030 Target</p>
          <p className="text-2xl font-bold text-green-600 dark:text-green-400 mt-1">30%</p>
          <p className="text-xs text-green-600 dark:text-green-300 mt-1">FAME-II Policy</p>
        </div>

        <div className="bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-lg p-4">
          <p className="text-xs text-orange-700 dark:text-orange-300 uppercase tracking-wide">Investment Needed</p>
          <p className="text-2xl font-bold text-orange-600 dark:text-orange-400 mt-1">₹45 Cr</p>
          <p className="text-xs text-orange-600 dark:text-orange-300 mt-1">Through 2030</p>
        </div>

        <div className="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg p-4">
          <p className="text-xs text-purple-700 dark:text-purple-300 uppercase tracking-wide">Carbon Credits</p>
          <p className="text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1">
            {scopeData?.total_scope3_supply_chain_tonnes.toFixed(0) || '0'}t
          </p>
          <p className="text-xs text-purple-600 dark:text-purple-300 mt-1">Potential value</p>
        </div>
      </div>

      {/* Supply Chain Insights */}
      {scopeData && (
        <div className="card">
          <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">Supply Chain Emissions (Scope 3)</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
              <p className="text-xs text-gray-600 dark:text-gray-400 uppercase">Total Scope 3</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
                {scopeData.total_scope3_supply_chain_tonnes.toFixed(1)}
              </p>
              <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">tonnes CO₂</p>
            </div>

            <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
              <p className="text-xs text-gray-600 dark:text-gray-400 uppercase">Highest Emitter</p>
              <p className="text-2xl font-bold text-red-600 dark:text-red-400 mt-1 truncate">
                {scopeData.highest_emission_supplier}
              </p>
              <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                {scopeData.highest_emission_value_tonnes.toFixed(1)}t
              </p>
            </div>

            <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
              <p className="text-xs text-gray-600 dark:text-gray-400 uppercase">Diversification Benefit</p>
              <p className="text-2xl font-bold text-green-600 dark:text-green-400 mt-1">
                {scopeData.diversification_carbon_benefit_tonnes.toFixed(1)}t
              </p>
              <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">Potential saving</p>
            </div>
          </div>

          <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
            <p className="text-sm text-blue-900 dark:text-blue-200">
              <strong>Recommendation:</strong> {scopeData.recommended_action}
            </p>
          </div>
        </div>
      )}

      {/* Policy & Standards Footer */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <p className="font-bold text-blue-900 dark:text-blue-200 mb-2">🇮🇳 FAME-II Aligned</p>
          <p className="text-blue-700 dark:text-blue-300">
            India's Faster Adoption policy targets 30% EV adoption by 2030 with subsidies and charging infrastructure support.
          </p>
        </div>

        <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
          <p className="font-bold text-green-900 dark:text-green-200 mb-2">🌍 GRI & UNFCCC</p>
          <p className="text-green-700 dark:text-green-300">
            Scope 1 & 3 emissions tracked per GRI 305 standards and UNFCCC Nationally Determined Contributions.
          </p>
        </div>

        <div className="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg p-4">
          <p className="font-bold text-purple-900 dark:text-purple-200 mb-2">♻️ Carbon Credits</p>
          <p className="text-purple-700 dark:text-purple-300">
            Estimated carbon credits from EV transition eligible for voluntary and compliance carbon markets.
          </p>
        </div>
      </div>
    </div>
  );
}
