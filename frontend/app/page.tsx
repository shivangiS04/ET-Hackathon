'use client';

import React from 'react';
import Link from 'next/link';
import { Battery, Zap, TrendingUp, AlertCircle, Menu } from 'lucide-react';

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
              <Link href="/battery" className="text-gray-700 hover:text-green-600 font-medium">Battery Health</Link>
              <Link href="/supply-chain" className="text-gray-700 hover:text-orange-600 font-medium">Supply Chain</Link>
              <Link href="/fleet" className="text-gray-700 hover:text-blue-600 font-medium">Fleet Readiness</Link>
              <Link href="/advanced-features" className="text-gray-700 hover:text-purple-600 font-medium">Advanced Features</Link>
              <Link href="/reports" className="text-gray-700 hover:text-indigo-600 font-medium">Reports</Link>
              <a href="http://localhost:8000/docs" target="_blank" className="text-gray-700 hover:text-slate-600 font-medium">API Docs</a>
            </nav>
          </div>

          {/* Mobile menu */}
          {mobileMenuOpen && (
            <nav className="md:hidden mt-4 space-y-2 pb-4">
              <Link href="/battery" className="block px-4 py-2 hover:bg-gray-100 rounded text-gray-700">Battery Health</Link>
              <Link href="/supply-chain" className="block px-4 py-2 hover:bg-gray-100 rounded text-gray-700">Supply Chain</Link>
              <Link href="/fleet" className="block px-4 py-2 hover:bg-gray-100 rounded text-gray-700">Fleet Readiness</Link>
              <Link href="/advanced-features" className="block px-4 py-2 hover:bg-gray-100 rounded text-gray-700">Advanced Features</Link>
              <Link href="/reports" className="block px-4 py-2 hover:bg-gray-100 rounded text-gray-700">Reports</Link>
              <a href="http://localhost:8000/docs" target="_blank" className="block px-4 py-2 hover:bg-gray-100 rounded text-gray-700">API Docs</a>
            </nav>
          )}
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold text-gray-900 mb-4">
            AI-Powered EV Intelligence Platform
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Accelerating India's EV transition through predictive battery management, supply chain visibility, and fleet electrification intelligence
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/battery"
              className="inline-block px-8 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition"
            >
              Explore Platform
            </Link>
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              className="inline-block px-8 py-3 bg-gray-200 text-gray-900 rounded-lg font-semibold hover:bg-gray-300 transition"
            >
              View API Docs
            </a>
          </div>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
          <div className="bg-white rounded-lg border border-gray-200 p-8 hover:shadow-lg transition">
            <div className="bg-green-100 rounded-lg p-3 w-12 h-12 flex items-center justify-center mb-4">
              <Battery className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Battery Health</h3>
            <p className="text-gray-600 text-sm">
              Predict battery state-of-health, degradation rates, and remaining useful life using advanced LSTM models
            </p>
            <Link href="/battery" className="text-green-600 font-medium mt-4 inline-block hover:underline">
              View Dashboard →
            </Link>
          </div>

          <div className="bg-white rounded-lg border border-gray-200 p-8 hover:shadow-lg transition">
            <div className="bg-orange-100 rounded-lg p-3 w-12 h-12 flex items-center justify-center mb-4">
              <AlertCircle className="w-6 h-6 text-orange-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Supply Chain Risk</h3>
            <p className="text-gray-600 text-sm">
              Real-time geopolitical risk monitoring, supplier concentration analysis, and material sourcing intelligence
            </p>
            <Link href="/supply-chain" className="text-orange-600 font-medium mt-4 inline-block hover:underline">
              View Analytics →
            </Link>
          </div>

          <div className="bg-white rounded-lg border border-gray-200 p-8 hover:shadow-lg transition">
            <div className="bg-purple-100 rounded-lg p-3 w-12 h-12 flex items-center justify-center mb-4">
              <Zap className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Advanced Intelligence</h3>
            <p className="text-gray-600 text-sm">
              Scenario simulation, anomaly detection, predictive alerts, and competitive benchmarking for strategic decision-making
            </p>
            <Link href="/advanced-features" className="text-purple-600 font-medium mt-4 inline-block hover:underline">
              Explore Features →
            </Link>
          </div>
        </div>

        {/* Stats Section */}
        <div className="bg-white rounded-lg border border-gray-200 p-12 mb-20">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">Platform Impact</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <p className="text-4xl font-bold text-green-600">58</p>
              <p className="text-gray-600 mt-2">Fleet Vehicles Tracked</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-orange-600">87.5%</p>
              <p className="text-gray-600 mt-2">Average Battery Health</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-blue-600">72.4%</p>
              <p className="text-gray-600 mt-2">EV Readiness Rate</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-purple-600">₹200Cr</p>
              <p className="text-gray-600 mt-2">Transition Investment</p>
            </div>
          </div>
        </div>

        {/* Quick Access */}
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-200 p-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-6">Quick Access</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Link
              href="/battery"
              className="block p-4 bg-white rounded-lg border border-green-200 hover:shadow-md transition"
            >
              <p className="font-semibold text-gray-900">Battery SOH Predictions</p>
              <p className="text-sm text-gray-600 mt-1">Analyze current health and forecast maintenance needs</p>
            </Link>
            <Link
              href="/supply-chain"
              className="block p-4 bg-white rounded-lg border border-orange-200 hover:shadow-md transition"
            >
              <p className="font-semibold text-gray-900">Supply Chain Heatmap</p>
              <p className="text-sm text-gray-600 mt-1">Monitor geopolitical and supplier risks in real-time</p>
            </Link>
            <Link
              href="/fleet"
              className="block p-4 bg-white rounded-lg border border-blue-200 hover:shadow-md transition"
            >
              <p className="font-semibold text-gray-900">Fleet Readiness Assessment</p>
              <p className="text-sm text-gray-600 mt-1">Get EV replacement recommendations and transition plans</p>
            </Link>
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              className="block p-4 bg-white rounded-lg border border-purple-200 hover:shadow-md transition"
            >
              <p className="font-semibold text-gray-900">API Documentation</p>
              <p className="text-sm text-gray-600 mt-1">Explore all endpoints and integrate with your systems</p>
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <p className="font-semibold mb-4">Platform</p>
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
                <li><a href="http://localhost:8000" target="_blank" className="hover:text-white">API Health</a></li>
              </ul>
            </div>
            <div>
              <p className="font-semibold mb-4">Technologies</p>
              <ul className="space-y-2 text-sm text-gray-400">
                <li>FastAPI + TensorFlow</li>
                <li>React 18 + Next.js</li>
                <li>MongoDB + Neo4j</li>
              </ul>
            </div>
            <div>
              <p className="font-semibold mb-4">ET AI Hackathon 2026</p>
              <p className="text-sm text-gray-400">
                Accelerating net zero through AI-powered industrial intelligence
              </p>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-center text-sm text-gray-400">
            <p>© 2026 EV Intelligence Platform. Built for the ET AI Hackathon.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
