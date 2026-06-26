'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import ScenarioBuilder from '@/components/ScenarioBuilder';
import AnomalyAlert from '@/components/AnomalyAlert';
import PredictiveAlertCenter from '@/components/PredictiveAlertCenter';
import { ArrowLeft, Zap, AlertTriangle, TrendingDown, Trophy } from 'lucide-react';

export default function AdvancedFeaturesPage() {
  const [activeTab, setActiveTab] = useState<'scenarios' | 'anomalies' | 'alerts' | 'benchmarks'>('scenarios');

  const tabs = [
    {
      id: 'scenarios',
      label: 'Scenario Simulation',
      icon: <Zap size={18} />,
      description: 'Model "what-if" disruption scenarios',
    },
    {
      id: 'anomalies',
      label: 'Anomaly Detection',
      icon: <AlertTriangle size={18} />,
      description: 'Detect unusual patterns in real-time',
    },
    {
      id: 'alerts',
      label: 'Predictive Alerts',
      icon: <TrendingDown size={18} />,
      description: 'Get early warnings based on forecasts',
    },
    {
      id: 'benchmarks',
      label: 'Benchmarking',
      icon: <Trophy size={18} />,
      description: 'Compare your metrics to industry standards',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/" className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition">
                <ArrowLeft size={20} />
                <span className="text-sm font-medium">Back to Home</span>
              </Link>
              <div className="h-6 w-px bg-gray-300"></div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Advanced Features</h1>
                <p className="text-sm text-gray-600">Predictive intelligence & risk management tools</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Tab Navigation */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex gap-1 overflow-x-auto">
            {tabs.map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`px-4 py-4 font-medium text-sm border-b-2 transition flex items-center gap-2 whitespace-nowrap ${
                  activeTab === tab.id
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900'
                }`}
              >
                {tab.icon}
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Tab Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Scenario Simulation */}
        {activeTab === 'scenarios' && (
          <div className="space-y-4">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <h3 className="font-semibold text-gray-900 mb-2">How Scenario Simulation Works</h3>
              <p className="text-sm text-gray-600 mb-3">
                Model the impact of potential supply chain disruptions on your fleet and financial projections. 
                Run "what-if" scenarios to understand vulnerabilities and prepare mitigation strategies.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs text-gray-600">
                <div className="flex gap-2">
                  <span className="text-blue-600 font-semibold">✓</span>
                  <span>Test supply chain scenarios (lithium shortage, port closures, etc.)</span>
                </div>
                <div className="flex gap-2">
                  <span className="text-blue-600 font-semibold">✓</span>
                  <span>Calculate impact on costs, timeline, and fleet availability</span>
                </div>
                <div className="flex gap-2">
                  <span className="text-blue-600 font-semibold">✓</span>
                  <span>Get specific mitigation steps for each scenario</span>
                </div>
                <div className="flex gap-2">
                  <span className="text-blue-600 font-semibold">✓</span>
                  <span>Compare multiple scenarios side-by-side</span>
                </div>
              </div>
            </div>
            <ScenarioBuilder />
          </div>
        )}

        {/* Anomaly Detection */}
        {activeTab === 'anomalies' && (
          <div className="space-y-4">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <h3 className="font-semibold text-gray-900 mb-2">How Anomaly Detection Works</h3>
              <p className="text-sm text-gray-600 mb-3">
                Our AI system continuously monitors your fleet and supply chain for unusual patterns that may indicate problems. 
                Each anomaly includes statistical evidence and recommended actions.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs text-gray-600">
                <div className="flex gap-2">
                  <span className="text-blue-600 font-semibold">✓</span>
                  <span>Battery degradation accelerating unexpectedly</span>
                </div>
                <div className="flex gap-2">
                  <span className="text-blue-600 font-semibold">✓</span>
                  <span>Supply chain concentration spiking</span>
                </div>
                <div className="flex gap-2">
                  <span className="text-blue-600 font-semibold">✓</span>
                  <span>Regional fleet performance degrading</span>
                </div>
                <div className="flex gap-2">
                  <span className="text-blue-600 font-semibold">✓</span>
                  <span>Charging infrastructure bottlenecks forming</span>
                </div>
              </div>
            </div>
            <AnomalyAlert />
          </div>
        )}

        {/* Predictive Alerts */}
        {activeTab === 'alerts' && (
          <div className="space-y-4">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <h3 className="font-semibold text-gray-900 mb-2">How Predictive Alerts Work</h3>
              <p className="text-sm text-gray-600 mb-3">
                Our forecasting engine projects future states based on current trends and alerts you before problems become critical. 
                Get days of advance notice to plan maintenance, procurement, and operational changes.
              </p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs text-gray-600">
                <div className="flex gap-2">
                  <span className="text-blue-600 font-semibold">✓</span>
                  <span>Battery RUL projections (when replacement needed)</span>
                </div>
                <div className="flex gap-2">
                  <span className="text-blue-600 font-semibold">✓</span>
                  <span>Supply chain risk trajectory (when to activate backups)</span>
                </div>
                <div className="flex gap-2">
                  <span className="text-blue-600 font-semibold">✓</span>
                  <span>Fleet readiness trends (when capacity insufficient)</span>
                </div>
                <div className="flex gap-2">
                  <span className="text-blue-600 font-semibold">✓</span>
                  <span>Cost trajectory (when to lock in prices)</span>
                </div>
              </div>
            </div>
            <PredictiveAlertCenter />
          </div>
        )}

        {/* Benchmarking */}
        {activeTab === 'benchmarks' && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 space-y-6">
            <div>
              <h3 className="font-semibold text-gray-900 mb-2">How Benchmarking Works</h3>
              <p className="text-sm text-gray-600">
                Compare your fleet and supply chain performance to industry averages and best-in-class operators. 
                Identify improvement opportunities and learn from successful peers.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Your Position */}
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4 border border-blue-200">
                <h4 className="font-semibold text-gray-900 mb-3">Your Position</h4>
                <div className="space-y-2">
                  <div>
                    <p className="text-xs text-gray-600">Fleet Average SOH</p>
                    <p className="text-2xl font-bold text-blue-600">87.5%</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Readiness Score</p>
                    <p className="text-2xl font-bold text-blue-600">72</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">ROI Payback</p>
                    <p className="text-2xl font-bold text-blue-600">4.8y</p>
                  </div>
                </div>
              </div>

              {/* Industry Average */}
              <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg p-4 border border-gray-200">
                <h4 className="font-semibold text-gray-900 mb-3">Industry Average</h4>
                <div className="space-y-2">
                  <div>
                    <p className="text-xs text-gray-600">Fleet Average SOH</p>
                    <p className="text-2xl font-bold text-gray-600">85.2%</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Readiness Score</p>
                    <p className="text-2xl font-bold text-gray-600">72.5</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">ROI Payback</p>
                    <p className="text-2xl font-bold text-gray-600">5.2y</p>
                  </div>
                </div>
              </div>

              {/* Best in Class */}
              <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-4 border border-green-200">
                <h4 className="font-semibold text-gray-900 mb-3">Best in Class</h4>
                <div className="space-y-2">
                  <div>
                    <p className="text-xs text-gray-600">Fleet Average SOH</p>
                    <p className="text-2xl font-bold text-green-600">91.2%</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">Readiness Score</p>
                    <p className="text-2xl font-bold text-green-600">85</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-600">ROI Payback</p>
                    <p className="text-2xl font-bold text-green-600">3.8y</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Improvement Opportunities */}
            <div>
              <h4 className="font-semibold text-gray-900 mb-3">Improvement Opportunities</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                  <div className="flex items-start gap-2">
                    <span className="text-yellow-600 font-semibold">!</span>
                    <div>
                      <p className="font-medium text-gray-900 text-sm">Battery Performance</p>
                      <p className="text-xs text-gray-600 mt-1">Gap: 3.7% below industry best. Implement thermal management optimization.</p>
                    </div>
                  </div>
                </div>
                <div className="bg-orange-50 border border-orange-200 rounded-lg p-3">
                  <div className="flex items-start gap-2">
                    <span className="text-orange-600 font-semibold">!</span>
                    <div>
                      <p className="font-medium text-gray-900 text-sm">Supply Diversification</p>
                      <p className="text-xs text-gray-600 mt-1">Gap: 13% concentration risk. Qualify 2-3 additional suppliers per material.</p>
                    </div>
                  </div>
                </div>
                <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                  <div className="flex items-start gap-2">
                    <span className="text-red-600 font-semibold">!</span>
                    <div>
                      <p className="font-medium text-gray-900 text-sm">Charging Infrastructure</p>
                      <p className="text-xs text-gray-600 mt-1">Gap: 20% utilization. Add 8-10 new 50kW charging stations.</p>
                    </div>
                  </div>
                </div>
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                  <div className="flex items-start gap-2">
                    <span className="text-blue-600 font-semibold">!</span>
                    <div>
                      <p className="font-medium text-gray-900 text-sm">Regional Consistency</p>
                      <p className="text-xs text-gray-600 mt-1">Gap: 15% variance vs 10% avg. Investigate regional infrastructure.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
