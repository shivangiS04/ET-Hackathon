'use client';

import React from 'react';
import SupplyChainMap from '@/components/SupplyChainMap';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

export default function SupplyChainPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Link href="/" className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-4">
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Supply Chain Risk Intelligence</h1>
          <p className="text-gray-600 mt-2">Geopolitical risk monitoring, supplier concentration analysis, and material sourcing intelligence</p>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <SupplyChainMap />
      </div>

      {/* Info Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-orange-50 border border-orange-200 rounded-lg p-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Risk Intelligence Framework</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="font-semibold text-gray-900 mb-2">🌍 Geopolitical Events</p>
              <p className="text-sm text-gray-700">
                Real-time monitoring of sanctions, trade restrictions, and geopolitical conflicts affecting critical material sourcing
              </p>
            </div>
            <div>
              <p className="font-semibold text-gray-900 mb-2">📊 Supplier Analytics</p>
              <p className="text-sm text-gray-700">
                Comprehensive risk profiling including concentration risk, quality deviations, and delivery performance tracking
              </p>
            </div>
            <div>
              <p className="font-semibold text-gray-900 mb-2">🎯 Procurement Intelligence</p>
              <p className="text-sm text-gray-700">
                Alternative sourcing recommendations, pricing forecasts, and supply diversification strategies
              </p>
            </div>
          </div>
        </div>

        {/* Material Insights */}
        <div className="mt-8 bg-white rounded-lg border border-gray-200 p-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Critical Battery Materials</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="p-4 border border-gray-200 rounded-lg">
              <p className="font-semibold text-gray-900">Lithium</p>
              <p className="text-2xl font-bold text-red-600 mt-2">78</p>
              <p className="text-xs text-gray-600 mt-1">Risk Score</p>
              <p className="text-xs text-gray-600 mt-2">45% China concentration</p>
            </div>
            <div className="p-4 border border-gray-200 rounded-lg">
              <p className="font-semibold text-gray-900">Cobalt</p>
              <p className="text-2xl font-bold text-red-600 mt-2">82</p>
              <p className="text-xs text-gray-600 mt-1">Risk Score</p>
              <p className="text-xs text-gray-600 mt-2">60% DR Congo concentration</p>
            </div>
            <div className="p-4 border border-gray-200 rounded-lg">
              <p className="font-semibold text-gray-900">Nickel</p>
              <p className="text-2xl font-bold text-yellow-600 mt-2">55</p>
              <p className="text-xs text-gray-600 mt-1">Risk Score</p>
              <p className="text-xs text-gray-600 mt-2">35% Indonesia concentration</p>
            </div>
            <div className="p-4 border border-gray-200 rounded-lg">
              <p className="font-semibold text-gray-900">NMC Cells</p>
              <p className="text-2xl font-bold text-orange-600 mt-2">65</p>
              <p className="text-xs text-gray-600 mt-1">Risk Score</p>
              <p className="text-xs text-gray-600 mt-2">40% China-based producers</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
