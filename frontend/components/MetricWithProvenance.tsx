'use client';

import React from 'react';
import { Info, CheckCircle, Clock, AlertCircle } from 'lucide-react';

interface MetricWithProvenanceProps {
  label: string;
  value: string | number;
  unit?: string;
  baseline?: {
    value: string;
    comparison: string; // e.g., "+28% better"
  };
  source: string;
  freshness?: {
    age_minutes: number;
    status: 'fresh' | 'stale' | 'old';
  };
  validation?: {
    rmse?: string;
    accuracy?: string;
    status: 'passed' | 'warning' | 'failed';
  };
}

export default function MetricWithProvenance({
  label,
  value,
  unit,
  baseline,
  source,
  freshness,
  validation
}: MetricWithProvenanceProps) {
  const [showTooltip, setShowTooltip] = React.useState(false);

  const freshnessColors = {
    fresh: 'text-green-600',
    stale: 'text-yellow-600',
    old: 'text-red-600'
  };

  const freshnessLabels = {
    fresh: 'Recently updated',
    stale: 'May be outdated',
    old: 'Needs refresh'
  };

  const validationColors = {
    passed: 'text-green-600 bg-green-50',
    warning: 'text-yellow-600 bg-yellow-50',
    failed: 'text-red-600 bg-red-50'
  };

  return (
    <div className="relative">
      <div 
        className="flex items-start gap-2 cursor-help"
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
      >
        <div className="flex-1">
          <div className="text-sm text-gray-600 mb-1 flex items-center gap-1">
            {label}
            <Info className="w-4 h-4 text-gray-400" />
          </div>
          <div className="flex items-baseline gap-1">
            <span className="text-3xl font-bold text-gray-900">{value}</span>
            {unit && <span className="text-lg text-gray-600">{unit}</span>}
            {baseline && (
              <span className="ml-2 px-2 py-0.5 bg-green-100 text-green-700 text-xs font-medium rounded-full">
                {baseline.comparison}
              </span>
            )}
          </div>
          {baseline && (
            <div className="text-xs text-gray-500 mt-1">
              vs {baseline.value} baseline
            </div>
          )}
        </div>
      </div>

      {showTooltip && (
        <div className="absolute z-50 left-0 top-full mt-2 w-72 bg-white rounded-lg shadow-xl border border-gray-200 p-4">
          <div className="space-y-3">
            {/* Source */}
            <div>
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Data Source</div>
              <div className="text-sm font-medium text-gray-900">{source}</div>
            </div>

            {/* Freshness */}
            {freshness && (
              <div>
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Data Freshness</div>
                <div className="flex items-center gap-2">
                  {freshness.status === 'fresh' && <CheckCircle className="w-4 h-4 text-green-600" />}
                  {freshness.status === 'stale' && <AlertCircle className="w-4 h-4 text-yellow-600" />}
                  {freshness.status === 'old' && <AlertCircle className="w-4 h-4 text-red-600" />}
                  <span className={`text-sm font-medium ${freshnessColors[freshness.status]}`}>
                    {freshnessLabels[freshness.status]}
                  </span>
                  <span className="text-xs text-gray-500">({freshness.age_minutes} min ago)</span>
                </div>
              </div>
            )}

            {/* Validation */}
            {validation && (
              <div>
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Model Validation</div>
                <div className={`inline-flex items-center gap-2 px-2 py-1 rounded text-sm font-medium ${validationColors[validation.status]}`}>
                  {validation.status === 'passed' && <CheckCircle className="w-4 h-4" />}
                  {validation.status === 'warning' && <AlertCircle className="w-4 h-4" />}
                  {validation.status === 'failed' && <AlertCircle className="w-4 h-4" />}
                  {validation.status === 'passed' ? 'Validated' : validation.status === 'warning' ? 'Review needed' : 'Failed'}
                </div>
                {validation.rmse && (
                  <div className="text-xs text-gray-600 mt-1">RMSE: {validation.rmse}</div>
                )}
                {validation.accuracy && (
                  <div className="text-xs text-gray-600 mt-1">Accuracy: {validation.accuracy}</div>
                )}
              </div>
            )}

            {/* Baseline Comparison */}
            {baseline && (
              <div>
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Baseline Comparison</div>
                <div className="text-sm text-gray-600">
                  Industry average: <span className="font-medium">{baseline.value}</span>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}