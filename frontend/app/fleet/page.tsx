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
        {/* Financial Hero Metrics - PROMINENT */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <div className="bg-gradient-to-br from-green-600 to-emerald-600 rounded-lg p-8 text-white shadow-lg">
            <p className="text-sm font-semibold opacity-90 mb-2">Annual Savings Per Vehicle</p>
            <p className="text-5xl font-bold mb-2">₹3.2L</p>
            <p className="text-sm opacity-80">Diesel: ₹6.0L vs EV: ₹2.8L</p>
            <div className="mt-4 pt-4 border-t border-white border-opacity-20">
              <p className="text-xs font-semibold">Fleet-wide: ₹50L/year (50 vehicles)</p>
            </div>
          </div>

          <div className="bg-gradient-to-br from-blue-600 to-cyan-600 rounded-lg p-8 text-white shadow-lg">
            <p className="text-sm font-semibold opacity-90 mb-2">5-Year ROI</p>
            <p className="text-5xl font-bold mb-2">₹160Cr</p>
            <p className="text-sm opacity-80">Total cumulative savings across fleet</p>
            <div className="mt-4 pt-4 border-t border-white border-opacity-20">
              <p className="text-xs font-semibold">Year 1: ₹25Cr | Year 5: ₹160Cr</p>
            </div>
          </div>

          <div className="bg-gradient-to-br from-orange-600 to-amber-600 rounded-lg p-8 text-white shadow-lg">
            <p className="text-sm font-semibold opacity-90 mb-2">Payback Period</p>
            <p className="text-5xl font-bold mb-2">4.2 yrs</p>
            <p className="text-sm opacity-80">Investment: ₹17.5Cr | Infrastructure: ₹3.5Cr</p>
            <div className="mt-4 pt-4 border-t border-white border-opacity-20">
              <p className="text-xs font-semibold">NPV (10yr): ₹49.9Cr @ 12% discount</p>
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-600 to-pink-600 rounded-lg p-8 text-white shadow-lg">
            <p className="text-sm font-semibold opacity-90 mb-2">Total Fleet Investment</p>
            <p className="text-5xl font-bold mb-2">₹21Cr</p>
            <p className="text-sm opacity-80">50 EVs @ ₹35L + Infrastructure</p>
            <div className="mt-4 pt-4 border-t border-white border-opacity-20">
              <p className="text-xs font-semibold">FAME subsidy covers: ₹5.5Cr (26%)</p>
            </div>
          </div>
        </div>

        {/* Financial Breakdown Table */}
        <div className="bg-white rounded-lg border border-gray-200 p-8 mb-12 shadow">
          <h3 className="text-2xl font-bold text-gray-900 mb-6">Financial Impact Summary</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="px-6 py-4 text-left font-semibold text-gray-900">Metric</th>
                  <th className="px-6 py-4 text-center font-semibold text-red-600">Diesel Baseline (56 vehicles)</th>
                  <th className="px-6 py-4 text-center font-semibold text-green-600">EV Fleet (50 vehicles)</th>
                  <th className="px-6 py-4 text-center font-semibold text-blue-600">Annual Benefit</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                <tr>
                  <td className="px-6 py-3 text-gray-900 font-medium">Fuel Cost</td>
                  <td className="px-6 py-3 text-center text-red-600 font-semibold">₹3.36Cr/yr</td>
                  <td className="px-6 py-3 text-center text-green-600 font-semibold">₹1.40Cr/yr</td>
                  <td className="px-6 py-3 text-center text-blue-600 font-bold">₹1.96Cr</td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="px-6 py-3 text-gray-900 font-medium">Maintenance Cost</td>
                  <td className="px-6 py-3 text-center text-red-600 font-semibold">₹84L/yr</td>
                  <td className="px-6 py-3 text-center text-green-600 font-semibold">₹20L/yr</td>
                  <td className="px-6 py-3 text-center text-blue-600 font-bold">₹64L</td>
                </tr>
                <tr>
                  <td className="px-6 py-3 text-gray-900 font-medium">Vehicle Insurance</td>
                  <td className="px-6 py-3 text-center text-red-600 font-semibold">₹56L/yr</td>
                  <td className="px-6 py-3 text-center text-green-600 font-semibold">₹40L/yr</td>
                  <td className="px-6 py-3 text-center text-blue-600 font-bold">₹16L</td>
                </tr>
                <tr className="bg-gray-50">
                  <td className="px-6 py-3 text-gray-900 font-medium">Road Tax & Permit</td>
                  <td className="px-6 py-3 text-center text-red-600 font-semibold">₹28L/yr</td>
                  <td className="px-6 py-3 text-center text-green-600 font-semibold">₹4L/yr</td>
                  <td className="px-6 py-3 text-center text-blue-600 font-bold">₹24L</td>
                </tr>
                <tr>
                  <td className="px-6 py-3 text-gray-900 font-medium bold-text">TOTAL ANNUAL COST</td>
                  <td className="px-6 py-3 text-center text-red-600 font-bold text-lg">₹4.64Cr</td>
                  <td className="px-6 py-3 text-center text-green-600 font-bold text-lg">₹2.04Cr</td>
                  <td className="px-6 py-3 text-center text-blue-600 font-bold text-lg">₹2.60Cr</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

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
          <h3 className="text-lg font-semibold text-gray-900 mb-6">Financial Roadmap & Milestones</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg">
              <p className="text-3xl font-bold text-green-600">Year 1</p>
              <p className="text-sm text-gray-700 mt-2 font-semibold">₹25Cr Savings</p>
              <p className="text-xs text-gray-600 mt-1">15 EVs deployed | Payback starts</p>
            </div>
            <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-lg">
              <p className="text-3xl font-bold text-blue-600">Year 2</p>
              <p className="text-sm text-gray-700 mt-2 font-semibold">₹60Cr Cumulative</p>
              <p className="text-xs text-gray-600 mt-1">35 EVs | 59% payback achieved</p>
            </div>
            <div className="text-center p-4 bg-gradient-to-br from-orange-50 to-amber-50 rounded-lg">
              <p className="text-3xl font-bold text-orange-600">Year 3</p>
              <p className="text-sm text-gray-700 mt-2 font-semibold">₹100Cr Cumulative</p>
              <p className="text-xs text-gray-600 mt-1">50 EVs | 59% payback + FAME subsidy</p>
            </div>
            <div className="text-center p-4 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg">
              <p className="text-3xl font-bold text-purple-600">Year 5+</p>
              <p className="text-sm text-gray-700 mt-2 font-semibold">₹160Cr+ Savings</p>
              <p className="text-xs text-gray-600 mt-1">Pure profit phase | ROI maximized</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
