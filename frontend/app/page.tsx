'use client';

import React from 'react';
import Link from 'next/link';
import { Battery, Zap, TrendingUp, AlertCircle, Menu, Leaf, Target, BarChart3 } from 'lucide-react';

export default function Home() {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-green-600 to-emerald-600 rounded-lg p-2">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">EV Intelligence</h1>
                <p className="text-xs text-gray-500">Supply Chain & Asset Intelligence</p>
              </div>
            </div>
            
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 hover:bg-gray-100 rounded"
            >
              <Menu className="w-6 h-6" />
            </button>

            <nav className="hidden md:flex items-center gap-8">
              <Link href="/onboarding" className="text-gray-700 hover:text-green-600 font-medium">Tour</Link>
              <Link href="/battery" className="text-gray-700 hover:text-green-600 font-medium">Battery</Link>
              <Link href="/supply-chain" className="text-gray-700 hover:text-orange-600 font-medium">Supply Chain</Link>
              <Link href="/fleet" className="text-gray-700 hover:text-blue-600 font-medium">Fleet</Link>
              <Link href="/advanced-features" className="text-gray-700 hover:text-purple-600 font-medium">Advanced</Link>
              <Link href="/reports" className="text-gray-700 hover:text-indigo-600 font-medium">Reports</Link>
              <a href="http://localhost:8000/docs" target="_blank" className="text-gray-700 hover:text-slate-600 font-medium">API</a>
            </nav>
          </div>

          {mobileMenuOpen && (
            <nav className="md:hidden mt-4 space-y-2 pb-4">
              <Link href="/onboarding" className="block px-4 py-2 hover:bg-gray-100 rounded text-gray-700">Tour</Link>
              <Link href="/battery" className="block px-4 py-2 hover:bg-gray-100 rounded text-gray-700">Battery</Link>
              <Link href="/supply-chain" className="block px-4 py-2 hover:bg-gray-100 rounded text-gray-700">Supply Chain</Link>
              <Link href="/fleet" className="block px-4 py-2 hover:bg-gray-100 rounded text-gray-700">Fleet</Link>
              <Link href="/advanced-features" className="block px-4 py-2 hover:bg-gray-100 rounded text-gray-700">Advanced</Link>
              <Link href="/reports" className="block px-4 py-2 hover:bg-gray-100 rounded text-gray-700">Reports</Link>
              <a href="http://localhost:8000/docs" target="_blank" className="block px-4 py-2 hover:bg-gray-100 rounded text-gray-700">API</a>
            </nav>
          )}
        </div>
      </header>

      {/* Hero Section - India Focused */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-green-50 border border-green-200 rounded-full mb-6">
            <Leaf className="w-4 h-4 text-green-600" />
            <span className="text-sm font-semibold text-green-700">India's Net-Zero 2070 Initiative</span>
          </div>
          
          <h2 className="text-5xl md:text-6xl font-bold text-gray-900 mb-4">
            Accelerating India's EV Transition
          </h2>
          <p className="text-xl text-gray-600 mb-2 max-w-4xl mx-auto">
            Supporting FAME-II and India's ambitious 30% EV adoption target by 2030
          </p>
          <p className="text-lg text-gray-500 max-w-4xl mx-auto mb-8">
            AI-powered supply chain visibility, battery lifecycle management, and fleet electrification for India's automotive industry
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/onboarding" className="inline-block px-8 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">
              Take a Tour
            </Link>
            <Link href="/battery" className="inline-block px-8 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition">
              Explore Platform
            </Link>
            <a href="http://localhost:8000/docs" target="_blank" className="inline-block px-8 py-3 bg-gray-200 text-gray-900 rounded-lg font-semibold hover:bg-gray-300 transition">
              View API Docs
            </a>
          </div>
        </div>

        {/* India-Specific Stats Section */}
        <div className="bg-gradient-to-r from-blue-50 to-green-50 rounded-lg border border-green-200 p-12 mb-20">
          <h3 className="text-2xl font-bold text-gray-900 text-center mb-12">India's EV Market Context (SIAM Data 2024)</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <p className="text-4xl font-bold text-green-600">30%</p>
              <p className="text-gray-600 mt-2">EV Adoption by 2030</p>
              <p className="text-xs text-gray-500 mt-1">FAME-II Target</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-blue-600">4.2M</p>
              <p className="text-gray-600 mt-2">Annual EV Sales 2030</p>
              <p className="text-xs text-gray-500 mt-1">SIAM Projection</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-orange-600">10K Cr</p>
              <p className="text-gray-600 mt-2">FAME-II Budget</p>
              <p className="text-xs text-gray-500 mt-1">Charging Infrastructure</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-purple-600">45%</p>
              <p className="text-gray-600 mt-2">Cost Reduction</p>
              <p className="text-xs text-gray-500 mt-1">By 2030</p>
            </div>
          </div>
        </div>

        {/* Three Critical Challenges */}
        <div className="mb-20">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">Three Critical Challenges for India's EV Industry</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white rounded-lg border border-gray-200 p-8 hover:shadow-lg transition">
              <div className="bg-green-100 rounded-lg p-3 w-12 h-12 flex items-center justify-center mb-4">
                <Battery className="w-6 h-6 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Challenge 1: Battery Lifecycle</h3>
              <p className="text-gray-600 text-sm mb-4">
                India's 35-50C climate accelerates degradation. Predict SOH, RUL using LSTM + Arrhenius equation.
              </p>
              <div className="bg-green-50 p-3 rounded mb-4 text-sm font-semibold text-green-900">
                Impact: 3.2L/vehicle/year savings
              </div>
              <Link href="/battery" className="text-green-600 font-medium inline-block hover:underline">
                View Dashboard →
              </Link>
            </div>

            <div className="bg-white rounded-lg border border-gray-200 p-8 hover:shadow-lg transition">
              <div className="bg-orange-100 rounded-lg p-3 w-12 h-12 flex items-center justify-center mb-4">
                <AlertCircle className="w-6 h-6 text-orange-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Challenge 2: Supply Chain Risk</h3>
              <p className="text-gray-600 text-sm mb-4">
                60-70% lithium/cobalt from 3-5 countries. Monitor HHI concentration & multi-tier risks.
              </p>
              <div className="bg-orange-50 p-3 rounded mb-4 text-sm font-semibold text-orange-900">
                Risk Score: 2,156-3,124 (High)
              </div>
              <Link href="/supply-chain" className="text-orange-600 font-medium inline-block hover:underline">
                View Analytics →
              </Link>
            </div>

            <div className="bg-white rounded-lg border border-gray-200 p-8 hover:shadow-lg transition">
              <div className="bg-purple-100 rounded-lg p-3 w-12 h-12 flex items-center justify-center mb-4">
                <Target className="w-6 h-6 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Challenge 3: Fleet Readiness</h3>
              <p className="text-gray-600 text-sm mb-4">
                Match operations to EV capabilities. TCO analysis with 4.2-year payback modeling.
              </p>
              <div className="bg-purple-50 p-3 rounded mb-4 text-sm font-semibold text-purple-900">
                Readiness: 87.5% avg score
              </div>
              <Link href="/fleet" className="text-purple-600 font-medium inline-block hover:underline">
                Explore Features →
              </Link>
            </div>
          </div>
        </div>

        {/* Platform Performance */}
        <div className="bg-white rounded-lg border border-gray-200 p-12 mb-20">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">Platform Performance</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <p className="text-4xl font-bold text-green-600">156</p>
              <p className="text-gray-600 mt-2">Vehicles Tracked</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-orange-600">92.3%</p>
              <p className="text-gray-600 mt-2">Avg Battery SOH</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-blue-600">87.5%</p>
              <p className="text-gray-600 mt-2">EV Readiness</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-purple-600">49.9 Cr</p>
              <p className="text-gray-600 mt-2">10-Year ROI</p>
            </div>
          </div>
        </div>

        {/* Advanced Features */}
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg border border-purple-200 p-8 mb-20">
          <h3 className="text-2xl font-bold text-gray-900 mb-6">Advanced Intelligence</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-10 w-10 rounded-md bg-purple-600 text-white">
                  <Zap className="w-5 h-5" />
                </div>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900">Scenario Simulation</h4>
                <p className="text-sm text-gray-600 mt-1">Lithium shortage, port closure modeling</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-10 w-10 rounded-md bg-pink-600 text-white">
                  <AlertCircle className="w-5 h-5" />
                </div>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900">Anomaly Detection</h4>
                <p className="text-sm text-gray-600 mt-1">Z-score based with 70-95% confidence</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-10 w-10 rounded-md bg-indigo-600 text-white">
                  <TrendingUp className="w-5 h-5" />
                </div>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900">Predictive Alerts</h4>
                <p className="text-sm text-gray-600 mt-1">90-day forecasts with confidence intervals</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-10 w-10 rounded-md bg-teal-600 text-white">
                  <BarChart3 className="w-5 h-5" />
                </div>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900">Benchmarking</h4>
                <p className="text-sm text-gray-600 mt-1">15+ metrics with industry comparison</p>
              </div>
            </div>
          </div>
          <Link href="/advanced-features" className="inline-block mt-6 px-6 py-2 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700">
            Explore More
          </Link>
        </div>

        {/* Quick Access */}
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-200 p-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6">Quick Access</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Link href="/battery" className="block p-4 bg-white rounded-lg border border-green-200 hover:shadow-md transition">
              <p className="font-semibold text-gray-900">Battery SOH Predictions</p>
              <p className="text-sm text-gray-600 mt-1">Arrhenius temperature modeling</p>
            </Link>
            <Link href="/supply-chain" className="block p-4 bg-white rounded-lg border border-orange-200 hover:shadow-md transition">
              <p className="font-semibold text-gray-900">Supply Chain Heatmap</p>
              <p className="text-sm text-gray-600 mt-1">HHI concentration analysis</p>
            </Link>
            <Link href="/fleet" className="block p-4 bg-white rounded-lg border border-blue-200 hover:shadow-md transition">
              <p className="font-semibold text-gray-900">Fleet Electrification</p>
              <p className="text-sm text-gray-600 mt-1">TCO & payback modeling</p>
            </Link>
            <Link href="/carbon-tracker" className="block p-4 bg-white rounded-lg border border-emerald-200 hover:shadow-md transition">
              <p className="font-semibold text-gray-900">Net Zero Tracker</p>
              <p className="text-sm text-gray-600 mt-1">Carbon reduction roadmap</p>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <p className="font-semibold mb-4">Modules</p>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><Link href="/battery" className="hover:text-white">Battery Health</Link></li>
                <li><Link href="/supply-chain" className="hover:text-white">Supply Chain</Link></li>
                <li><Link href="/fleet" className="hover:text-white">Fleet Readiness</Link></li>
              </ul>
            </div>
            <div>
              <p className="font-semibold mb-4">Resources</p>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="http://localhost:8000/docs" target="_blank" className="hover:text-white">API Docs</a></li>
                <li><Link href="/advanced-features" className="hover:text-white">Advanced</Link></li>
                <li><Link href="/reports" className="hover:text-white">Reports</Link></li>
              </ul>
            </div>
            <div>
              <p className="font-semibold mb-4">Tech Stack</p>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>FastAPI + TensorFlow</li>
                <li>React 18 + Next.js 14</li>
                <li>PostgreSQL + Redis</li>
              </ul>
            </div>
            <div>
              <p className="font-semibold mb-4">India Focus</p>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>FAME-II Compliant</li>
                <li>SIAM Data Integrated</li>
                <li>ET AI Hackathon 2026</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-center text-sm text-gray-400">
            <p>© 2026 EV Intelligence Platform. Supporting India's 30% EV target by 2030.</p>
            <p className="mt-2">Built for ET AI Hackathon 2026 - Accelerating India's Industrial Transition</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
