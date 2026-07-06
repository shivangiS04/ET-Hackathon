'use client';

import React from 'react';
import { Building2, TrendingUp, Scale, IndianRupee } from 'lucide-react';

interface PolicyImpactBannerProps {
  className?: string;
}

export default function PolicyImpactBanner({ className = '' }: PolicyImpactBannerProps) {
  const policies = [
    {
      icon: <Building2 className="w-8 h-8" />,
      title: 'FAME-II Subsidy',
      value: '₹24,000 Cr',
      description: 'Total allocated for EV adoption',
      color: 'blue'
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: '2030 Target',
      value: '30%',
      description: 'Electric vehicle penetration target',
      color: 'green'
    },
    {
      icon: <Scale className="w-8 h-8" />,
      title: 'Carbon Reduction',
      value: '10 Cr tonnes',
      description: 'Projected annual CO₂ reduction by 2030',
      color: 'emerald'
    },
    {
      icon: <IndianRupee className="w-8 h-8" />,
      title: 'TCO Savings',
      value: '₹3.2L/vehicle',
      description: 'Annual fuel cost savings per EV',
      color: 'orange'
    }
  ];

  const colorClasses: Record<string, { bg: string; text: string; border: string }> = {
    blue: { bg: 'bg-blue-50', text: 'text-blue-700', border: 'border-blue-200' },
    green: { bg: 'bg-green-50', text: 'text-green-700', border: 'border-green-200' },
    emerald: { bg: 'bg-emerald-50', text: 'text-emerald-700', border: 'border-emerald-200' },
    orange: { bg: 'bg-orange-50', text: 'text-orange-700', border: 'border-orange-200' }
  };

  return (
    <div className={`bg-white rounded-xl border border-gray-200 p-6 ${className}`}>
      <div className="flex items-center gap-3 mb-6">
        <div className="bg-gradient-to-r from-orange-500 to-amber-500 rounded-lg p-2">
          <TrendingUp className="w-6 h-6 text-white" />
        </div>
        <div>
          <h3 className="text-xl font-bold text-gray-900">India EV Policy Impact</h3>
          <p className="text-sm text-gray-600">Government initiatives driving EV transition</p>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {policies.map((policy, idx) => (
          <div 
            key={idx} 
            className={`${colorClasses[policy.color].bg} rounded-lg p-4 border ${colorClasses[policy.color].border}`}
          >
            <div className={`${colorClasses[policy.color].text} mb-2`}>
              {policy.icon}
            </div>
            <div className="text-2xl font-bold text-gray-900 mb-1">
              {policy.value}
            </div>
            <div className="text-sm font-medium text-gray-900 mb-1">
              {policy.title}
            </div>
            <div className="text-xs text-gray-600">
              {policy.description}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-sm text-gray-600">
          <span className="font-medium">Platform Advantage:</span> Our AI models help fleet operators 
          leverage these policies optimally, calculating ROI and identifying the best time to transition 
          based on battery health predictions and supply chain risk analysis.
        </p>
      </div>
    </div>
  );
}