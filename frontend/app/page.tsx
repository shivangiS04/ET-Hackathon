'use client';

import React from 'react';
import Link from 'next/link';
import { Battery, Zap, TrendingUp, AlertCircle, Menu, Leaf, Target, BarChart3, X } from 'lucide-react';
import ThemeToggle from '@/components/ThemeToggle';

export default function Home() {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  return (
    <div className="min-h-screen gradient-bg">
      {/* Header */}
      <header className="header-bg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-green-600 to-emerald-600 rounded-lg p-2">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-primary">EV Intelligence</h1>
                <p className="text-xs text-secondary">Supply Chain & Asset Intelligence</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <ThemeToggle />
              
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="md:hidden p-2 hover:bg-gray-100 dark:hover:bg-dark-700 rounded"
              >
                {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
              </button>

              <nav className="hidden md:flex items-center gap-6">
                <Link href="/onboarding" className="text-secondary hover:text-green-600 dark:hover:text-green-400 font-medium">Tour</Link>
                <Link href="/battery" className="text-secondary hover:text-green-600 dark:hover:text-green-400 font-medium">Battery</Link>
                <Link href="/supply-chain" className="text-secondary hover:text-orange-600 dark:hover:text-orange-400 font-medium">Supply Chain</Link>
                <Link href="/fleet" className="text-secondary hover:text-blue-600 dark:hover:text-blue-400 font-medium">Fleet</Link>
                <Link href="/advanced-features" className="text-secondary hover:text-purple-600 dark:hover:text-purple-400 font-medium">Advanced</Link>
                <Link href="/reports" className="text-secondary hover:text-indigo-600 dark:hover:text-indigo-400 font-medium">Reports</Link>
              </nav>
            </div>
          </div>

          {mobileMenuOpen && (
            <nav className="md:hidden mt-4 space-y-2 pb-4">
              <Link href="/onboarding" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-dark-700 rounded text-secondary">Tour</Link>
              <Link href="/battery" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-dark-700 rounded text-secondary">Battery</Link>
              <Link href="/supply-chain" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-dark-700 rounded text-secondary">Supply Chain</Link>
              <Link href="/fleet" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-dark-700 rounded text-secondary">Fleet</Link>
              <Link href="/advanced-features" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-dark-700 rounded text-secondary">Advanced</Link>
              <Link href="/reports" className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-dark-700 rounded text-secondary">Reports</Link>
            </nav>
          )}
        </div>
      </header>

      {/* Hero Section - India Focused */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-4 py-2 badge badge-green mb-6">
            <Leaf className="w-4 h-4 text-green-600 dark:text-green-400" />
            <span>India's Net-Zero 2070 Initiative</span>
          </div>
          
          <h2 className="text-5xl md:text-6xl font-bold text-primary mb-4">
            Accelerating India's EV Transition
          </h2>
          <p className="text-xl text-secondary mb-2 max-w-4xl mx-auto">
            Supporting FAME-II and India's ambitious 30% EV adoption target by 2030
          </p>
          <p className="text-lg text-secondary max-w-4xl mx-auto mb-8">
            AI-powered supply chain visibility, battery lifecycle management, and fleet electrification for India's automotive industry
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/onboarding" className="btn-primary px-8 py-3">
              Take a Tour
            </Link>
            <Link href="/battery" className="bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 text-white rounded-lg font-semibold px-8 py-3 transition-colors">
              Explore Platform
            </Link>
            <a href="http://localhost:8000/docs" target="_blank" className="btn-secondary px-8 py-3">
              View API Docs
            </a>
          </div>
        </div>

        {/* India-Specific Stats Section */}
        <div className="section-gradient-blue rounded-lg p-12 mb-20">
          <h3 className="text-2xl font-bold text-primary text-center mb-12">India's EV Market Context (SIAM Data 2024)</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <p className="text-4xl font-bold text-green-600 dark:text-green-400">30%</p>
              <p className="text-secondary mt-2">EV Adoption by 2030</p>
              <p className="text-xs text-secondary mt-1">FAME-II Target</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-blue-600 dark:text-blue-400">4.2M</p>
              <p className="text-secondary mt-2">Annual EV Sales 2030</p>
              <p className="text-xs text-secondary mt-1">SIAM Projection</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-orange-600 dark:text-orange-400">10K Cr</p>
              <p className="text-secondary mt-2">FAME-II Budget</p>
              <p className="text-xs text-secondary mt-1">Charging Infrastructure</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-purple-600 dark:text-purple-400">45%</p>
              <p className="text-secondary mt-2">Cost Reduction</p>
              <p className="text-xs text-secondary mt-1">By 2030</p>
            </div>
          </div>
        </div>

        {/* Three Critical Challenges */}
        <div className="mb-20">
          <h2 className="text-3xl font-bold text-primary text-center mb-12">Three Critical Challenges for India's EV Industry</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="card-hover p-8">
              <div className="stat-green rounded-lg p-3 w-12 h-12 flex items-center justify-center mb-4">
                <Battery className="w-6 h-6 text-green-600 dark:text-green-400" />
              </div>
              <h3 className="text-lg font-semibold text-primary mb-3">Challenge 1: Battery Lifecycle</h3>
              <p className="text-secondary text-sm mb-4">
                India's 35-50C climate accelerates degradation. Predict SOH, RUL using LSTM + Arrhenius equation.
              </p>
              <div className="stat-green p-3 rounded mb-4 text-sm font-semibold text-green-900 dark:text-green-100">
                Impact: 3.2L/vehicle/year savings
              </div>
              <Link href="/battery" className="text-green-600 dark:text-green-400 font-medium inline-block hover:underline">
                View Dashboard →
              </Link>
            </div>

            <div className="card-hover p-8">
              <div className="stat-orange rounded-lg p-3 w-12 h-12 flex items-center justify-center mb-4">
                <AlertCircle className="w-6 h-6 text-orange-600 dark:text-orange-400" />
              </div>
              <h3 className="text-lg font-semibold text-primary mb-3">Challenge 2: Supply Chain Risk</h3>
              <p className="text-secondary text-sm mb-4">
                60-70% lithium/cobalt from 3-5 countries. Monitor HHI concentration & multi-tier risks.
              </p>
              <div className="stat-orange p-3 rounded mb-4 text-sm font-semibold text-orange-900 dark:text-orange-100">
                Risk Score: 2,156-3,124 (High)
              </div>
              <Link href="/supply-chain" className="text-orange-600 dark:text-orange-400 font-medium inline-block hover:underline">
                View Analytics →
              </Link>
            </div>

            <div className="card-hover p-8">
              <div className="stat-purple rounded-lg p-3 w-12 h-12 flex items-center justify-center mb-4">
                <Target className="w-6 h-6 text-purple-600 dark:text-purple-400" />
              </div>
              <h3 className="text-lg font-semibold text-primary mb-3">Challenge 3: Fleet Readiness</h3>
              <p className="text-secondary text-sm mb-4">
                Match operations to EV capabilities. TCO analysis with 4.2-year payback modeling.
              </p>
              <div className="stat-purple p-3 rounded mb-4 text-sm font-semibold text-purple-900 dark:text-purple-100">
                Readiness: 87.5% avg score
              </div>
              <Link href="/fleet" className="text-purple-600 dark:text-purple-400 font-medium inline-block hover:underline">
                Explore Features →
              </Link>
            </div>
          </div>
        </div>

        {/* Platform Performance */}
        <div className="card p-12 mb-20">
          <h2 className="text-3xl font-bold text-primary text-center mb-12">Platform Performance</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <p className="text-4xl font-bold text-green-600 dark:text-green-400">156</p>
              <p className="text-secondary mt-2">Vehicles Tracked</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-orange-600 dark:text-orange-400">92.3%</p>
              <p className="text-secondary mt-2">Avg Battery SOH</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-blue-600 dark:text-blue-400">87.5%</p>
              <p className="text-secondary mt-2">EV Readiness</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-purple-600 dark:text-purple-400">49.9 Cr</p>
              <p className="text-secondary mt-2">10-Year ROI</p>
            </div>
          </div>
        </div>

        {/* Advanced Features */}
        <div className="section-gradient-purple rounded-lg p-8 mb-20">
          <h3 className="text-2xl font-bold text-primary mb-6">Advanced Intelligence</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-10 w-10 rounded-md bg-purple-600 text-white">
                  <Zap className="w-5 h-5" />
                </div>
              </div>
              <div>
                <h4 className="font-semibold text-primary">Scenario Simulation</h4>
                <p className="text-sm text-secondary mt-1">Lithium shortage, port closure modeling</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-10 w-10 rounded-md bg-pink-600 text-white">
                  <AlertCircle className="w-5 h-5" />
                </div>
              </div>
              <div>
                <h4 className="font-semibold text-primary">Anomaly Detection</h4>
                <p className="text-sm text-secondary mt-1">Z-score based with 70-95% confidence</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-10 w-10 rounded-md bg-indigo-600 text-white">
                  <TrendingUp className="w-5 h-5" />
                </div>
              </div>
              <div>
                <h4 className="font-semibold text-primary">Predictive Alerts</h4>
                <p className="text-sm text-secondary mt-1">90-day forecasts with confidence intervals</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="flex-shrink-0">
                <div className="flex items-center justify-center h-10 w-10 rounded-md bg-teal-600 text-white">
                  <BarChart3 className="w-5 h-5" />
                </div>
              </div>
              <div>
                <h4 className="font-semibold text-primary">Benchmarking</h4>
                <p className="text-sm text-secondary mt-1">15+ metrics with industry comparison</p>
              </div>
            </div>
          </div>
          <Link href="/advanced-features" className="inline-block mt-6 px-6 py-2 bg-purple-600 hover:bg-purple-700 dark:bg-purple-500 dark:hover:bg-purple-600 text-white rounded-lg font-semibold transition-colors">
            Explore More
          </Link>
        </div>

        {/* Quick Access */}
        <div className="section-gradient-green rounded-lg p-8">
          <h3 className="text-2xl font-bold text-primary mb-6">Quick Access</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Link href="/battery" className="block p-4 card-hover">
              <p className="font-semibold text-primary">Battery SOH Predictions</p>
              <p className="text-sm text-secondary mt-1">Arrhenius temperature modeling</p>
            </Link>
            <Link href="/supply-chain" className="block p-4 card-hover">
              <p className="font-semibold text-primary">Supply Chain Heatmap</p>
              <p className="text-sm text-secondary mt-1">HHI concentration analysis</p>
            </Link>
            <Link href="/fleet" className="block p-4 card-hover">
              <p className="font-semibold text-primary">Fleet Electrification</p>
              <p className="text-sm text-secondary mt-1">TCO & payback modeling</p>
            </Link>
            <Link href="/carbon-tracker" className="block p-4 card-hover">
              <p className="font-semibold text-primary">Net Zero Tracker</p>
              <p className="text-sm text-secondary mt-1">Carbon reduction roadmap</p>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer-bg mt-20">
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
