'use client';

import React, { useState, useEffect } from 'react';
import { 
  LineChart, Line, AreaChart, Area, BarChart, Bar, 
  PieChart, Pie, Cell, ScatterChart, Scatter,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  ComposedChart
} from 'recharts';
import { TrendingUp, AlertCircle, CheckCircle, Clock } from 'lucide-react';

/**
 * Advanced Metrics Dashboard Component
 * Displays sophisticated visualizations for hackathon impact
 */

export default function AdvancedMetrics() {
  const [activeTab, setActiveTab] = useState<'battery' | 'supply' | 'fleet'>('battery');
  const [timeRange, setTimeRange] = useState<'7d' | '30d' | '90d' | '1y'>('30d');

  // BATTERY ANALYSIS DATA
  const degradationAnalysis = [
    { cycle: 0, soh: 100, predicted: 100, upper_ci: 100, lower_ci: 100 },
    { cycle: 250, soh: 98.1, predicted: 98.2, upper_ci: 98.5, lower_ci: 97.9 },
    { cycle: 500, soh: 96.2, predicted: 96.4, upper_ci: 96.9, lower_ci: 95.9 },
    { cycle: 750, soh: 94.5, predicted: 94.6, upper_ci: 95.2, lower_ci: 94.0 },
    { cycle: 1000, soh: 92.3, predicted: 92.8, upper_ci: 93.5, lower_ci: 92.1 },
    { cycle: 1250, soh: 90.1, predicted: 91.0, upper_ci: 91.8, lower_ci: 90.2 },
    { cycle: 1500, soh: 87.9, predicted: 89.2, upper_ci: 90.1, lower_ci: 88.3 }
  ];

  const temperatureStressMap = [
    { temp: -20, stress: 0.15, events: 3 },
    { temp: 0, stress: 0.08, events: 8 },
    { temp: 20, stress: 0.02, events: 45 },
    { temp: 35, stress: 0.12, events: 120 },
    { temp: 45, stress: 0.45, events: 65 },
    { temp: 55, stress: 0.78, events: 12 }
  ];

  const riskDistribution = [
    { name: 'Low Risk (SOH >80%)', value: 42, color: '#10b981' },
    { name: 'Medium Risk (60-80%)', value: 12, color: '#f59e0b' },
    { name: 'High Risk (40-60%)', value: 3, color: '#ef4444' },
    { name: 'Critical (<40%)', value: 1, color: '#7f1d1d' }
  ];

  // SUPPLY CHAIN ANALYSIS DATA
  const supplierRiskTimeline = [
    { week: 'W1', geopolitical: 0.45, concentration: 0.68, quality: 0.32, logistics: 0.28, total: 0.52 },
    { week: 'W2', geopolitical: 0.48, concentration: 0.67, quality: 0.35, logistics: 0.31, total: 0.55 },
    { week: 'W3', geopolitical: 0.52, concentration: 0.69, quality: 0.38, logistics: 0.35, total: 0.59 },
    { week: 'W4', geopolitical: 0.58, concentration: 0.72, quality: 0.42, logistics: 0.40, total: 0.65 },
  ];

  const countryRiskMatrix = [
    { country: 'China', concentration: 78, geopolitical: 92, size: 450 },
    { country: 'Australia', concentration: 45, geopolitical: 35, size: 280 },
    { country: 'Chile', concentration: 42, geopolitical: 42, size: 200 },
    { country: 'Indonesia', concentration: 35, geopolitical: 55, size: 150 },
    { country: 'DR Congo', concentration: 88, geopolitical: 85, size: 120 },
    { country: 'Japan', concentration: 32, geopolitical: 10, size: 100 }
  ];

  const tierRiskPropagation = [
    { tier: 'Tier 1', risk: 0.68, suppliers: 5, nodes: 5 },
    { tier: 'Tier 2', risk: 0.34, suppliers: 15, nodes: 15 },
    { tier: 'Tier 3', risk: 0.17, suppliers: 45, nodes: 45 }
  ];

  // FLEET ANALYSIS DATA
  const vehicleReadinessTrend = [
    { month: 'Jan', ready: 12, conditional: 8, not_ready: 38 },
    { month: 'Feb', ready: 14, conditional: 10, not_ready: 34 },
    { month: 'Mar', ready: 18, conditional: 12, not_ready: 28 },
    { month: 'Apr', ready: 22, conditional: 14, not_ready: 22 },
    { month: 'May', ready: 28, conditional: 16, not_ready: 14 }
  ];

  const tcoComparison = [
    { 
      vehicle: 'Urban T001', 
      diesel_tco: 28.5, 
      ev_tco: 24.2, 
      savings: 4.3,
      payback: 2.8,
      roi: 18.7
    },
    { 
      vehicle: 'Delivery T002', 
      diesel_tco: 32.1, 
      ev_tco: 27.9, 
      savings: 4.2,
      payback: 3.2,
      roi: 16.8
    },
    { 
      vehicle: 'Long-haul T003', 
      diesel_tco: 58.2, 
      ev_tco: 52.3, 
      savings: 5.9,
      payback: 4.1,
      roi: 14.2
    }
  ];

  const carbonReduction = [
    { phase: 'Phase 1 (Q1-Q2)', vehicles: 15, co2_reduction: 225, investment: 45 },
    { phase: 'Phase 2 (Q3-Q4)', vehicles: 20, co2_reduction: 380, investment: 60 },
    { phase: 'Phase 3 (2026)', vehicles: 15, co2_reduction: 285, investment: 45 }
  ];

  // CUSTOM TOOLTIP COMPONENTS
  const CustomBatteryTooltip = (props: any) => {
    const { active, payload } = props;
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-300 rounded shadow-lg">
          <p className="font-semibold">{`Cycle ${data.cycle}`}</p>
          <p className="text-blue-600">{`Measured: ${data.soh.toFixed(1)}%`}</p>
          <p className="text-purple-600">{`Predicted: ${data.predicted.toFixed(1)}%`}</p>
          <p className="text-green-600">{`Confidence: ±${((data.upper_ci - data.lower_ci) / 2).toFixed(1)}%`}</p>
        </div>
      );
    }
    return null;
  };

  const renderBatteryAnalysis = () => (
    <div className="space-y-6">
      {/* Degradation Prediction with Confidence Intervals */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Battery Degradation Prediction with Confidence Intervals
        </h3>
        <ResponsiveContainer width="100%" height={350}>
          <ComposedChart data={degradationAnalysis}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="cycle" label={{ value: 'Battery Cycles', position: 'insideBottomRight', offset: -5 }} />
            <YAxis label={{ value: 'SOH (%)', angle: -90, position: 'insideLeft' }} />
            <Tooltip content={<CustomBatteryTooltip />} />
            <Legend />
            <Area 
              type="monotone" 
              dataKey="upper_ci" 
              fill="#3b82f6" 
              stroke="none" 
              fillOpacity={0.1}
              name="95% CI Upper"
            />
            <Area 
              type="monotone" 
              dataKey="lower_ci" 
              fill="#3b82f6" 
              stroke="none" 
              fillOpacity={0.1}
              name="95% CI Lower"
            />
            <Line 
              type="monotone" 
              dataKey="predicted" 
              stroke="#3b82f6" 
              strokeWidth={2}
              name="Model Prediction"
              dot={{ r: 4 }}
            />
            <Line 
              type="monotone" 
              dataKey="soh" 
              stroke="#10b981" 
              strokeWidth={2}
              name="Actual SOH"
              dot={{ r: 5 }}
            />
          </ComposedChart>
        </ResponsiveContainer>
        <p className="text-sm text-gray-600 mt-4">
          <strong>Model Accuracy:</strong> RMSE &lt; 3% | <strong>Confidence Level:</strong> 95%
        </p>
      </div>

      {/* Temperature Stress Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Thermal Stress by Temperature
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={temperatureStressMap}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="temp" label={{ value: 'Temperature (°C)', position: 'insideBottomRight', offset: -5 }} />
              <YAxis label={{ value: 'Stress Factor', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Bar dataKey="stress" fill="#ef4444" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Risk Distribution
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={riskDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {riskDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );

  const renderSupplyChainAnalysis = () => (
    <div className="space-y-6">
      {/* Multi-Dimensional Risk Analysis */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Supply Chain Risk Evolution (Weekly)
        </h3>
        <ResponsiveContainer width="100%" height={350}>
          <ComposedChart data={supplierRiskTimeline}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="week" />
            <YAxis label={{ value: 'Risk Score (0-1)', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="geopolitical" stroke="#ef4444" strokeWidth={2} name="Geopolitical" />
            <Line type="monotone" dataKey="concentration" stroke="#f59e0b" strokeWidth={2} name="Concentration" />
            <Line type="monotone" dataKey="quality" stroke="#3b82f6" strokeWidth={2} name="Quality" />
            <Line type="monotone" dataKey="logistics" stroke="#8b5cf6" strokeWidth={2} name="Logistics" />
            <Line type="monotone" dataKey="total" stroke="#000" strokeWidth={3} name="Total Risk" strokeDasharray="5 5" />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {/* Country Risk Matrix */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Country Risk Matrix (Bubble Chart)
        </h3>
        <ResponsiveContainer width="100%" height={350}>
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              type="number" 
              dataKey="concentration" 
              name="Concentration Risk (%)"
              label={{ value: 'Supplier Concentration Risk (%)', position: 'insideBottomRight', offset: -5 }}
            />
            <YAxis 
              type="number" 
              dataKey="geopolitical" 
              name="Geopolitical Risk"
              label={{ value: 'Geopolitical Risk (0-100)', angle: -90, position: 'insideLeft' }}
            />
            <Tooltip cursor={{ strokeDasharray: '3 3' }} />
            <Scatter
              name="Countries"
              data={countryRiskMatrix}
              fill="#8884d8"
              shape="circle"
            >
              {countryRiskMatrix.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={`hsl(${Math.random() * 360}, 70%, 60%)`} />
              ))}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
        <p className="text-sm text-gray-600 mt-4">
          Bubble size represents material volume. High concentration + high geopolitical risk = critical focus areas.
        </p>
      </div>

      {/* Network Risk Propagation */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {tierRiskPropagation.map((tier) => (
          <div key={tier.tier} className="bg-white rounded-lg border border-gray-200 p-4">
            <h4 className="font-semibold text-gray-800 mb-3">{tier.tier}</h4>
            <div className="space-y-2">
              <div>
                <p className="text-sm text-gray-600">Risk Score</p>
                <div className="flex items-center gap-2 mt-1">
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-red-500 h-2 rounded-full" 
                      style={{ width: `${tier.risk * 100}%` }}
                    />
                  </div>
                  <p className="text-sm font-semibold">{(tier.risk * 100).toFixed(0)}%</p>
                </div>
              </div>
              <p className="text-sm text-gray-600 mt-2">
                Suppliers: <span className="font-semibold">{tier.suppliers}</span>
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderFleetAnalysis = () => (
    <div className="space-y-6">
      {/* Fleet Readiness Trend */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Fleet Electrification Readiness Trend
        </h3>
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={vehicleReadinessTrend}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis label={{ value: 'Number of Vehicles', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend />
            <Bar dataKey="ready" stackId="a" fill="#10b981" name="Ready (>85%)" />
            <Bar dataKey="conditional" stackId="a" fill="#f59e0b" name="Conditional (70-85%)" />
            <Bar dataKey="not_ready" stackId="a" fill="#ef4444" name="Not Ready (<70%)" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* TCO Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            TCO Savings Comparison (8-Year)
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={tcoComparison.slice(0, 2)}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="vehicle" />
              <YAxis label={{ value: 'Cost (₹ Lakhs)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="diesel_tco" fill="#ef4444" name="Diesel TCO" />
              <Bar dataKey="ev_tco" fill="#10b981" name="EV TCO" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Return on Investment (ROI %)
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={tcoComparison}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="vehicle" angle={-45} textAnchor="end" height={80} />
              <YAxis label={{ value: 'ROI (%)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Bar dataKey="roi" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Carbon Reduction Impact */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          Carbon Reduction Roadmap
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <ComposedChart data={carbonReduction}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="phase" />
            <YAxis yAxisId="left" label={{ value: 'Vehicles', angle: -90, position: 'insideLeft' }} />
            <YAxis yAxisId="right" orientation="right" label={{ value: 'CO₂ Reduction (tons)', angle: 90, position: 'insideRight' }} />
            <Tooltip />
            <Legend />
            <Bar yAxisId="left" dataKey="vehicles" fill="#3b82f6" name="Vehicles Converted" />
            <Line yAxisId="right" type="monotone" dataKey="co2_reduction" stroke="#10b981" strokeWidth={2} name="CO₂ Reduction (tons)" />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Tab Navigation */}
      <div className="flex gap-2 bg-white rounded-lg border border-gray-200 p-1">
        <button
          onClick={() => setActiveTab('battery')}
          className={`flex-1 px-4 py-2 rounded font-semibold transition ${
            activeTab === 'battery'
              ? 'bg-blue-500 text-white'
              : 'text-gray-700 hover:bg-gray-100'
          }`}
        >
          🔋 Battery Intelligence
        </button>
        <button
          onClick={() => setActiveTab('supply')}
          className={`flex-1 px-4 py-2 rounded font-semibold transition ${
            activeTab === 'supply'
              ? 'bg-blue-500 text-white'
              : 'text-gray-700 hover:bg-gray-100'
          }`}
        >
          🌍 Supply Chain
        </button>
        <button
          onClick={() => setActiveTab('fleet')}
          className={`flex-1 px-4 py-2 rounded font-semibold transition ${
            activeTab === 'fleet'
              ? 'bg-blue-500 text-white'
              : 'text-gray-700 hover:bg-gray-100'
          }`}
        >
          🚗 Fleet Readiness
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === 'battery' && renderBatteryAnalysis()}
      {activeTab === 'supply' && renderSupplyChainAnalysis()}
      {activeTab === 'fleet' && renderFleetAnalysis()}
    </div>
  );
}
