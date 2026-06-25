'use client';

import React from 'react';
import BatteryDashboard from '@/components/BatteryDashboard';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

export default function BatteryPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Link href="/" className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-4">
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Battery Health Dashboard</h1>
          <p className="text-gray-600 mt-2">Predictive battery SOH monitoring, degradation forecasting, and maintenance scheduling</p>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <BatteryDashboard />
      </div>

      {/* Info Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">How This Works</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="font-semibold text-gray-900 mb-2">1. Data Collection</p>
              <p className="text-sm text-gray-700">
                Real-time EV telematics collect voltage, current, temperature, and charge cycle data from battery management systems
              </p>
            </div>
            <div>
              <p className="font-semibold text-gray-900 mb-2">2. LSTM Prediction</p>
              <p className="text-sm text-gray-700">
                Advanced deep learning models forecast state-of-health degradation patterns and remaining useful life
              </p>
            </div>
            <div>
              <p className="font-semibold text-gray-900 mb-2">3. Actionable Insights</p>
              <p className="text-sm text-gray-700">
                Predictive maintenance recommendations, optimal charging schedules, and replacement planning
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
