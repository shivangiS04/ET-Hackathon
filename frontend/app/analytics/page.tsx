'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { BarChart3, RefreshCw, Download, Settings } from 'lucide-react';
import AdvancedMetrics from '@/components/AdvancedMetrics';
import RealtimeMonitor from '@/components/RealtimeMonitor';

/**
 * Advanced Analytics Dashboard Page
 * Comprehensive view of all advanced metrics and real-time monitoring
 */

export default function AnalyticsDashboard() {
  const [activeView, setActiveView] = useState<'advanced' | 'realtime'>('advanced');
  const [autoRefresh, setAutoRefresh] = useState(true);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <BarChart3 className="w-6 h-6 text-purple-600" />
              <h1 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h1>
            </div>
            <div className="flex items-center gap-4">
              <label className="flex items-center gap-2 text-sm text-gray-700">
                <input
                  type="checkbox"
                  checked={autoRefresh}
                  onChange={(e) => setAutoRefresh(e.target.checked)}
                  className="rounded"
                />
                Auto Refresh
              </label>
              <button className="p-2 hover:bg-gray-100 rounded transition">
                <RefreshCw className="w-5 h-5 text-gray-600" />
              </button>
              <button className="p-2 hover:bg-gray-100 rounded transition">
                <Download className="w-5 h-5 text-gray-600" />
              </button>
              <button className="p-2 hover:bg-gray-100 rounded transition">
                <Settings className="w-5 h-5 text-gray-600" />
              </button>
            </div>
          </div>

          {/* View Tabs */}
          <div className="flex gap-4">
            <button
              onClick={() => setActiveView('advanced')}
              className={`px-4 py-2 rounded-lg font-semibold transition ${
                activeView === 'advanced'
                  ? 'bg-purple-100 text-purple-700'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              📊 Advanced Metrics
            </button>
            <button
              onClick={() => setActiveView('realtime')}
              className={`px-4 py-2 rounded-lg font-semibold transition ${
                activeView === 'realtime'
                  ? 'bg-purple-100 text-purple-700'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              📡 Real-time Monitor
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeView === 'advanced' ? (
          <div className="space-y-6">
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-2">
                Advanced Analytics & Insights
              </h2>
              <p className="text-gray-700">
                In-depth analysis with sophisticated visualizations for battery health predictions, supply chain network modeling, and fleet electrification readiness assessment.
              </p>
            </div>
            
            <AdvancedMetrics />
          </div>
        ) : (
          <div className="space-y-6">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-2">
                Real-time System Monitoring
              </h2>
              <p className="text-gray-700">
                Live metrics, active alerts, and system health status updated in real-time with configurable refresh rates.
              </p>
            </div>
            
            <RealtimeMonitor />
          </div>
        )}

        {/* Navigation Links */}
        <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            href="/battery"
            className="block p-4 bg-white rounded-lg border border-gray-200 hover:shadow-md transition"
          >
            <p className="font-semibold text-green-600">🔋 Battery Dashboard</p>
            <p className="text-sm text-gray-600 mt-2">View battery health metrics and maintenance alerts</p>
          </Link>
          <Link
            href="/supply-chain"
            className="block p-4 bg-white rounded-lg border border-gray-200 hover:shadow-md transition"
          >
            <p className="font-semibold text-orange-600">🌍 Supply Chain Map</p>
            <p className="text-sm text-gray-600 mt-2">Monitor supply chain risks and supplier health</p>
          </Link>
          <Link
            href="/fleet"
            className="block p-4 bg-white rounded-lg border border-gray-200 hover:shadow-md transition"
          >
            <p className="font-semibold text-blue-600">🚗 Fleet Readiness</p>
            <p className="text-sm text-gray-600 mt-2">Track EV transition progress and recommendations</p>
          </Link>
        </div>
      </main>
    </div>
  );
}
