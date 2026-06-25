'use client';

import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { AlertCircle, Globe } from 'lucide-react';

export default function SupplyChainMap() {
  const [riskData, setRiskData] = useState<any>(null);
  const [suppliers, setSuppliers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [riskRes, suppRes] = await Promise.all([
          fetch('http://localhost:8000/api/v1/supply-chain/risk-score'),
          fetch('http://localhost:8000/api/v1/supply-chain/suppliers')
        ]);
        
        const riskData = await riskRes.json();
        const suppData = await suppRes.json();
        
        setRiskData(riskData);
        setSuppliers(suppData.suppliers || []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching supply chain data:', error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading supply chain data...</p>
        </div>
      </div>
    );
  }

  const riskByCategory = [
    { name: 'Geopolitical', value: riskData?.risk_breakdown?.geopolitical || 0.75, color: '#ef4444' },
    { name: 'Supplier Concentration', value: riskData?.risk_breakdown?.supplier_concentration || 0.72, color: '#f97316' },
    { name: 'Quality Deviations', value: riskData?.risk_breakdown?.quality_deviations || 0.45, color: '#eab308' },
    { name: 'Logistics Delays', value: riskData?.risk_breakdown?.logistics_delays || 0.58, color: '#f59e0b' }
  ];

  const geoRisk = [
    { country: 'China', risk: 0.92, color: '#dc2626' },
    { country: 'DR Congo', risk: 0.85, color: '#ea580c' },
    { country: 'Indonesia', risk: 0.55, color: '#f59e0b' },
    { country: 'Australia', risk: 0.35, color: '#fbbf24' },
    { country: 'Chile', risk: 0.42, color: '#fcd34d' }
  ];

  const getRiskColor = (score: number) => {
    if (score >= 0.8) return 'bg-red-100 border-red-300 text-red-900';
    if (score >= 0.6) return 'bg-orange-100 border-orange-300 text-orange-900';
    if (score >= 0.4) return 'bg-yellow-100 border-yellow-300 text-yellow-900';
    return 'bg-green-100 border-green-300 text-green-900';
  };

  return (
    <div className="space-y-6">
      {/* Overall Risk Score */}
      <div className="bg-gradient-to-r from-red-50 to-orange-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600">Overall Supply Chain Risk</p>
            <p className="text-5xl font-bold text-red-600 mt-2">{(riskData?.overall_risk_score || 0.68).toFixed(2)}</p>
            <p className="text-lg text-red-700 font-semibold mt-2">{riskData?.risk_level}</p>
          </div>
          <div className="text-right">
            <p className="text-sm text-gray-600">Risk Level</p>
            <p className="text-3xl text-red-600 mt-2">⚠️</p>
            <p className="text-xs text-gray-500 mt-2">Requires immediate attention</p>
          </div>
        </div>
      </div>

      {/* Risk Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Risk Categories */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Risk Breakdown by Category</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={riskByCategory}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis domain={[0, 1]} />
              <Tooltip formatter={(value) => `${(value * 100).toFixed(0)}%`} />
              <Bar dataKey="value" fill="#ef4444" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Geographic Risk */}
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <Globe className="w-5 h-5 text-orange-600" />
            Geographic Risk Map
          </h3>
          <div className="space-y-2">
            {geoRisk.map((item) => (
              <div key={item.country} className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">{item.country}</span>
                <div className="flex items-center gap-2">
                  <div className="w-32 bg-gray-200 rounded-full h-2">
                    <div
                      className="h-2 rounded-full"
                      style={{
                        width: `${item.risk * 100}%`,
                        backgroundColor: item.color
                      }}
                    />
                  </div>
                  <span className="text-sm font-semibold text-gray-700 w-8">
                    {(item.risk * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Top Risk Factors */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <AlertCircle className="w-5 h-5 text-red-600" />
          Top Risk Factors
        </h3>
        <div className="space-y-3">
          {riskData?.top_risk_factors?.map((factor: any, idx: number) => (
            <div key={idx} className="border border-red-200 bg-red-50 rounded p-4">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <p className="font-semibold text-gray-900">{factor.factor}</p>
                  <p className="text-sm text-gray-700 mt-1">{factor.description}</p>
                </div>
                <div className="ml-4 text-right">
                  <p className="text-2xl font-bold text-red-600">{(factor.impact * 100).toFixed(0)}%</p>
                  <p className="text-xs text-gray-500">Impact Score</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Suppliers Risk Table */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Critical Supplier Risk Assessment</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-4 py-2 text-left font-semibold text-gray-700">Supplier</th>
                <th className="px-4 py-2 text-left font-semibold text-gray-700">Country</th>
                <th className="px-4 py-2 text-left font-semibold text-gray-700">Material</th>
                <th className="px-4 py-2 text-center font-semibold text-gray-700">Risk Score</th>
                <th className="px-4 py-2 text-center font-semibold text-gray-700">Concentration</th>
              </tr>
            </thead>
            <tbody>
              {suppliers.slice(0, 4).map((supplier) => (
                <tr key={supplier.supplier_id} className="border-b border-gray-200 hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium text-gray-900">{supplier.supplier_name}</td>
                  <td className="px-4 py-3 text-gray-700">{supplier.country}</td>
                  <td className="px-4 py-3 text-gray-700">{supplier.material}</td>
                  <td className="px-4 py-3 text-center">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getRiskColor(supplier.risk_score / 100)}`}>
                      {supplier.risk_score}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center text-gray-900 font-semibold">
                    {supplier.concentration_percentage}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recommendations */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-3">Strategic Recommendations</h3>
        <ul className="space-y-2">
          <li className="flex gap-3 text-gray-700">
            <span className="text-blue-600 font-bold">→</span>
            <span>Increase supplier diversification for cobalt (currently 60% concentrated)</span>
          </li>
          <li className="flex gap-3 text-gray-700">
            <span className="text-blue-600 font-bold">→</span>
            <span>Lock in long-term lithium contracts to hedge against price volatility</span>
          </li>
          <li className="flex gap-3 text-gray-700">
            <span className="text-blue-600 font-bold">→</span>
            <span>Develop alternative sourcing for China-dependent materials</span>
          </li>
        </ul>
      </div>
    </div>
  );
}
