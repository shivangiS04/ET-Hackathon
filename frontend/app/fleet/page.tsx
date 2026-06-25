'use client';

import React from 'react';
import FleetTable from '@/components/FleetTable';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';

export default function FleetPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Link href="/" className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-4">
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Fleet Electrification Readiness</h1>
          <p className="text-gray-600 mt-2">EV procurement intelligence, transition roadmaps, and net-zero progress tracking</p>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <FleetTable />
      </div>

      {/* Info Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-green-50 border border-green-200 rounded-lg p-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Electrification Strategy</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="font-semibold text-gray-900 mb-2">🎯 Phase 1: Q1 2025</p>
              <p className="text-sm text-gray-700">
                Start with 15 high-readiness urban and delivery vehicles. Establish charging infrastructure foundation. Investment: ₹45 Cr
              </p>
            </div>
            <div>
              <p className="font-semibold text-gray-900 mb-2">📈 Phase 2: Q2-Q3 2025</p>
              <p className="text-sm text-gray-700">
                Scale to 20 mixed-duty vehicles. Expand charging network and secure long-term battery supply contracts. Investment: ₹60 Cr
              </p>
            </div>
            <div>
              <p className="font-semibold text-gray-900 mb-2">🚀 Phase 3: Q4 2025</p>
              <p className="text-sm text-gray-700">
                Convert final 15 long-haul and mining vehicles. Achieve full fleet transition. Total investment: ₹45 Cr
              </p>
            </div>
          </div>
        </div>

        {/* Government Support */}
        <div className="mt-8 bg-purple-50 border border-purple-200 rounded-lg p-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Funding & Government Support</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <p className="font-semibold text-gray-900 mb-2">FAME-II Subsidy</p>
              <p className="text-2xl font-bold text-purple-600">₹40 Cr</p>
              <p className="text-sm text-gray-700 mt-2">
                Government incentives available for electric vehicle procurement under Phase-II of FAME scheme
              </p>
            </div>
            <div>
              <p className="font-semibold text-gray-900 mb-2">Tax Benefits</p>
              <p className="text-2xl font-bold text-purple-600">15-20%</p>
              <p className="text-sm text-gray-700 mt-2">
                GST exemption and income tax deductions for EV purchases. Road tax reductions in many states
              </p>
            </div>
          </div>
        </div>

        {/* Success Metrics */}
        <div className="mt-8 bg-white rounded-lg border border-gray-200 p-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Expected Outcomes</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center p-4">
              <p className="text-3xl font-bold text-green-600">50</p>
              <p className="text-sm text-gray-700 mt-2">EVs by end 2025</p>
              <p className="text-xs text-gray-600">(86% of fleet)</p>
            </div>
            <div className="text-center p-4">
              <p className="text-3xl font-bold text-green-600">1,250</p>
              <p className="text-sm text-gray-700 mt-2">Tons CO₂ reduction</p>
              <p className="text-xs text-gray-600">annually</p>
            </div>
            <div className="text-center p-4">
              <p className="text-3xl font-bold text-green-600">₹43Cr</p>
              <p className="text-sm text-gray-700 mt-2">Annual savings</p>
              <p className="text-xs text-gray-600">fuel + maintenance</p>
            </div>
            <div className="text-center p-4">
              <p className="text-3xl font-bold text-green-600">4.8yr</p>
              <p className="text-sm text-gray-700 mt-2">Payback period</p>
              <p className="text-xs text-gray-600">NPV positive</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
