'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { ChevronRight, Battery, AlertCircle, Truck, CheckCircle, ArrowRight, Play, Zap } from 'lucide-react';

export default function OnboardingPage() {
  const [currentStep, setCurrentStep] = useState(0);

  const onboardingSteps = [
    {
      title: 'Welcome to EV Intelligence',
      subtitle: 'India\'s Most Comprehensive EV Supply Chain & Asset Platform',
      description: 'Supporting the national 30% EV adoption target by 2030 through AI-powered predictive analytics, real-time monitoring, and strategic decision support.',
      image: '⚡',
      cta: 'Next',
    },
    {
      title: 'Three Critical Challenges We Solve',
      subtitle: 'Battery Degradation | Supply Chain Risk | Fleet Readiness',
      description: 'India\'s hot climate, concentrated suppliers, and operational complexity create unique EV adoption challenges. Our platform tackles all three with advanced AI and physics-based models.',
      image: '🎯',
      cta: 'Continue',
    },
    {
      title: 'Battery Lifecycle Mastery',
      subtitle: 'Predict SOH, Degradation & Remaining Useful Life',
      description: 'Temperature-dependent degradation modeling using Arrhenius equation accounts for India\'s 35-50°C climate. LSTM predictions show 90%+ accuracy with confidence intervals.',
      image: '🔋',
      features: ['Arrhenius temperature modeling', 'Rainflow stress counting', 'RUL forecasting', 'Maintenance triggers'],
      cta: 'View Battery Dashboard',
      link: '/battery',
    },
    {
      title: 'Supply Chain Risk Intelligence',
      subtitle: 'Monitor Geopolitical & Supplier Risks in Real-Time',
      description: '60-70% of lithium/cobalt sourced from 3-5 countries. Multi-tier risk propagation with Herfindahl-Hirschman Index concentration analysis tracks real-time geopolitical events.',
      image: '🌍',
      features: ['HHI concentration tracking', 'Multi-tier risk propagation', 'Geopolitical event monitoring', 'Material forecasting'],
      cta: 'View Supply Chain Analytics',
      link: '/supply-chain',
    },
    {
      title: 'Fleet Electrification Planning',
      subtitle: 'Route Matching, TCO Analysis & Transition Planning',
      description: 'Match vehicle operations to EV capabilities with advanced route/payload algorithms. 8-year financial modeling shows ₹3.2L/vehicle/year savings and 4.2-year payback.',
      image: '🚗',
      features: ['Route & payload matching', 'TCO calculation', '8-year financial modeling', 'Phased transition plans'],
      cta: 'View Fleet Dashboard',
      link: '/fleet',
    },
    {
      title: 'Advanced Intelligence Features',
      subtitle: 'Scenario Simulation, Anomaly Detection, Predictive Alerts',
      description: 'Run what-if scenarios (lithium shortage, port closure). Detect anomalies with 70-95% confidence. Get 90-day forecasts with customizable thresholds.',
      image: '🔮',
      features: ['5 scenario presets', 'Z-score anomaly detection', '90-day predictions', 'Industry benchmarking'],
      cta: 'Explore Advanced Features',
      link: '/advanced-features',
    },
    {
      title: 'Real-Time Monitoring & Reports',
      subtitle: 'Live Dashboards, Export Reports, Carbon Tracking',
      description: 'Monitor fleet health in real-time. Generate compliance reports. Track carbon emissions with 2035 net-zero roadmap and 75% reduction potential.',
      image: '📊',
      features: ['Real-time metric cards', 'Executive reports', 'Data export (CSV/JSON)', 'Carbon tracker'],
      cta: 'View Reports & Analytics',
      link: '/reports',
    },
    {
      title: 'Ready to Get Started?',
      subtitle: 'Begin your EV Transition Intelligence Journey',
      description: 'Access comprehensive dashboards, run advanced analytics, and make data-driven decisions for India\'s EV future.',
      image: '🚀',
      cta: 'Enter Platform',
      link: '/',
    },
  ];

  const step = onboardingSteps[currentStep];
  const isLastStep = currentStep === onboardingSteps.length - 1;
  const isFirstStep = currentStep === 0;

  const handleNext = () => {
    if (!isLastStep) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrev = () => {
    if (!isFirstStep) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-green-50">
      {/* Skip Button */}
      <div className="fixed top-4 right-4 z-50">
        <Link href="/" className="px-4 py-2 text-gray-600 hover:text-gray-900 font-medium text-sm">
          Skip Tour
        </Link>
      </div>

      {/* Main Content */}
      <div className="min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl w-full">
          {/* Step Indicator */}
          <div className="mb-8 flex items-center justify-center gap-2">
            {onboardingSteps.map((_, index) => (
              <div
                key={index}
                className={`h-2 rounded-full transition-all ${
                  index === currentStep
                    ? 'w-8 bg-gradient-to-r from-green-600 to-emerald-600'
                    : index < currentStep
                    ? 'w-2 bg-green-600'
                    : 'w-2 bg-gray-300'
                }`}
              />
            ))}
          </div>

          {/* Card Content */}
          <div className="bg-white rounded-2xl shadow-xl border border-gray-200 overflow-hidden">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-0">
              {/* Left Side - Image/Icon */}
              <div className="hidden md:flex items-center justify-center bg-gradient-to-br from-green-50 to-blue-50 p-12">
                <div className="text-8xl">{step.image}</div>
              </div>

              {/* Right Side - Content */}
              <div className="p-12 flex flex-col justify-between">
                <div>
                  <h1 className="text-4xl font-bold text-gray-900 mb-4">{step.title}</h1>
                  <p className="text-xl text-green-600 font-semibold mb-6">{step.subtitle}</p>
                  <p className="text-lg text-gray-600 mb-8 leading-relaxed">{step.description}</p>

                  {/* Features List */}
                  {step.features && (
                    <div className="mb-8 space-y-3">
                      {step.features.map((feature, idx) => (
                        <div key={idx} className="flex items-start gap-3">
                          <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-1" />
                          <span className="text-gray-700">{feature}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* CTA Buttons */}
                <div className="flex gap-4">
                  <button
                    onClick={handlePrev}
                    disabled={isFirstStep}
                    className={`px-6 py-2 rounded-lg font-medium transition ${
                      isFirstStep
                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                        : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                    }`}
                  >
                    ← Back
                  </button>

                  {step.link ? (
                    <Link
                      href={step.link}
                      className="flex-1 px-6 py-2 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg font-medium hover:from-green-700 hover:to-emerald-700 transition flex items-center justify-center gap-2"
                    >
                      {step.cta}
                      <ArrowRight className="w-5 h-5" />
                    </Link>
                  ) : (
                    <button
                      onClick={handleNext}
                      className="flex-1 px-6 py-2 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg font-medium hover:from-green-700 hover:to-emerald-700 transition flex items-center justify-center gap-2"
                    >
                      {step.cta}
                      <ChevronRight className="w-5 h-5" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-4">
            <a href="http://localhost:8000/docs" target="_blank" className="p-4 bg-white rounded-lg border border-gray-200 hover:shadow-lg transition text-center">
              <Zap className="w-6 h-6 mx-auto mb-2 text-blue-600" />
              <p className="font-semibold text-gray-900">API Documentation</p>
              <p className="text-sm text-gray-600 mt-1">Full endpoint reference</p>
            </a>
            <Link href="/carbon-tracker" className="p-4 bg-white rounded-lg border border-gray-200 hover:shadow-lg transition text-center">
              <span className="text-3xl">🌱</span>
              <p className="font-semibold text-gray-900">Carbon Tracker</p>
              <p className="text-sm text-gray-600 mt-1">Net zero roadmap</p>
            </Link>
            <Link href="/reports" className="p-4 bg-white rounded-lg border border-gray-200 hover:shadow-lg transition text-center">
              <span className="text-3xl">📊</span>
              <p className="font-semibold text-gray-900">Reports</p>
              <p className="text-sm text-gray-600 mt-1">Export & compliance</p>
            </Link>
          </div>

          {/* Key Stats */}
          <div className="mt-12 bg-white rounded-xl border border-gray-200 p-8">
            <h3 className="text-xl font-bold text-gray-900 mb-8 text-center">Platform at a Glance</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
              <div>
                <p className="text-3xl font-bold text-green-600">156</p>
                <p className="text-sm text-gray-600 mt-2">Vehicles Tracked</p>
              </div>
              <div>
                <p className="text-3xl font-bold text-orange-600">92.3%</p>
                <p className="text-sm text-gray-600 mt-2">Avg Battery SOH</p>
              </div>
              <div>
                <p className="text-3xl font-bold text-blue-600">87.5%</p>
                <p className="text-sm text-gray-600 mt-2">EV Readiness</p>
              </div>
              <div>
                <p className="text-3xl font-bold text-purple-600">49.9 Cr</p>
                <p className="text-sm text-gray-600 mt-2">10Y ROI</p>
              </div>
            </div>
          </div>

          {/* Footer Note */}
          <div className="mt-12 text-center text-sm text-gray-600">
            <p>Built for ET AI Hackathon 2026 • Supporting India's 30% EV adoption target by 2030</p>
          </div>
        </div>
      </div>
    </div>
  );
}
