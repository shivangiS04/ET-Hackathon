'use client';

import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';
import { AlertTriangle, CheckCircle, TrendingUp, Zap, Package, Truck } from 'lucide-react';

interface SPCMetrics {
  line_id: string;
  cpk: number;
  cp: number;
  defects_per_million: number;
  yield_rate: number;
  last_10_readings: number[];
  ucl: number;
  lcl: number;
  mean: number;
  std_dev: number;
  control_status: string;
  capability_rating: string;
  timestamp: string;
}

interface DefectTrace {
  cell_id: string;
  pack_id: string;
  vehicle_id: string;
  manufacturing_date: string;
  batch_number: string;
  supplier_id: string;
  defect_chain: any[];
  affected_vehicles: string[];
  quality_score: number;
  recommendation: string;
}

interface QualityDriftResult {
  quality_drift_detected: boolean;
  defect_risk_score: number;
  severity: string;
  recommended_action: string;
  control_chart_signal: string;
  confidence: number;
  timestamp: string;
  process_summary: any;
}

export default function QualityDashboard() {
  const [spcMetrics, setSpcMetrics] = useState<SPCMetrics | null>(null);
  const [qualityDrift, setQualityDrift] = useState<QualityDriftResult | null>(null);
  const [defectTrace, setDefectTrace] = useState<DefectTrace | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [runningQualityCheck, setRunningQualityCheck] = useState(false);

  // Fetch SPC metrics and run initial quality check
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch SPC metrics
        const spcResponse = await fetch('http://localhost:8000/api/v1/quality/spc-metrics/LINE_01');
        if (spcResponse.ok) {
          const spcData = await spcResponse.json();
          setSpcMetrics(spcData);
        }

        // Fetch defect trace for a sample cell
        const traceResponse = await fetch('http://localhost:8000/api/v1/quality/trace/CELL_001_A1');
        if (traceResponse.ok) {
          const traceData = await traceResponse.json();
          setDefectTrace(traceData);
        }

        // Run initial quality check
        const driftResponse = await fetch('http://localhost:8000/api/v1/quality/detect-drift', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            voltage_mean: 4.2,
            voltage_std: 0.03,
            temperature_mean: 35,
            temperature_std: 3,
            cycle_count: 500,
            capacity_fade_rate: 0.001
          })
        });
        if (driftResponse.ok) {
          const driftData = await driftResponse.json();
          setQualityDrift(driftData);
        }

        setLoading(false);
      } catch (err) {
        console.error('Error fetching quality data:', err);
        setError('Failed to load quality data');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Handle manual quality check
  const handleRunQualityCheck = async () => {
    try {
      setRunningQualityCheck(true);
      const response = await fetch('http://localhost:8000/api/v1/quality/detect-drift', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          voltage_mean: 4.2 + (Math.random() - 0.5) * 0.1,
          voltage_std: 0.03 + (Math.random() - 0.5) * 0.01,
          temperature_mean: 35 + (Math.random() - 0.5) * 5,
          temperature_std: 3 + (Math.random() - 0.5) * 1,
          cycle_count: 500 + Math.floor(Math.random() * 100),
          capacity_fade_rate: 0.001 + (Math.random() - 0.5) * 0.0005
        })
      });

      if (response.ok) {
        const data = await response.json();
        setQualityDrift(data);
      }
    } catch (err) {
      console.error('Error running quality check:', err);
      setError('Failed to run quality check');
    } finally {
      setRunningQualityCheck(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 dark:text-gray-300">Loading quality data...</p>
        </div>
      </div>
    );
  }

  // Prepare chart data from SPC metrics
  const chartData = spcMetrics?.last_10_readings.map((reading, idx) => ({
    batch: `Batch ${idx + 1}`,
    voltage: reading,
    ucl: spcMetrics.ucl,
    lcl: spcMetrics.lcl,
    mean: spcMetrics.mean
  })) || [];

  // Get severity color
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800';
      case 'high':
        return 'text-orange-600 dark:text-orange-400 bg-orange-50 dark:bg-orange-900/20 border-orange-200 dark:border-orange-800';
      case 'medium':
        return 'text-yellow-600 dark:text-yellow-400 bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800';
      case 'low':
        return 'text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800';
      default:
        return 'text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-800 border-gray-200 dark:border-gray-700';
    }
  };

  // Get control status icon
  const getControlStatusIcon = (status: string) => {
    return status === 'IN_CONTROL' ? (
      <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400" />
    ) : (
      <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400" />
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Manufacturing Quality Intelligence</h2>
          <p className="text-gray-600 dark:text-gray-400 mt-1">AI-powered quality control and predictive maintenance</p>
        </div>
        <button
          onClick={handleRunQualityCheck}
          disabled={runningQualityCheck}
          className="bg-blue-600 hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-medium transition disabled:opacity-50"
        >
          {runningQualityCheck ? 'Running...' : 'Run Quality Check'}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 text-red-700 dark:text-red-400">
          {error}
        </div>
      )}

      {/* Quality Drift Alert */}
      {qualityDrift && (
        <div className={`border rounded-lg p-6 ${getSeverityColor(qualityDrift.severity)}`}>
          <div className="flex items-start justify-between">
            <div>
              <h3 className="text-lg font-bold mb-2">Quality Drift Detection</h3>
              <div className="space-y-2 text-sm">
                <p>
                  <strong>Status:</strong>{' '}
                  {qualityDrift.quality_drift_detected ? (
                    <span className="text-red-600 dark:text-red-400">⚠️ Drift Detected</span>
                  ) : (
                    <span className="text-green-600 dark:text-green-400">✅ Normal Operation</span>
                  )}
                </p>
                <p>
                  <strong>Risk Score:</strong> {(qualityDrift.defect_risk_score * 100).toFixed(1)}%
                </p>
                <p>
                  <strong>Severity:</strong> {qualityDrift.severity.toUpperCase()}
                </p>
                <p>
                  <strong>Control Signal:</strong> {qualityDrift.control_chart_signal}
                </p>
                <p className="mt-3">
                  <strong>Recommendation:</strong> {qualityDrift.recommended_action}
                </p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold">
                {(qualityDrift.defect_risk_score * 100).toFixed(1)}%
              </div>
              <p className="text-xs mt-1">Defect Risk</p>
            </div>
          </div>
        </div>
      )}

      {/* Three Column Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* 1. SPC Control Chart */}
        <div className="md:col-span-1 card">
          <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">SPC Control Chart</h3>
          {spcMetrics ? (
            <div className="space-y-4">
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" className="dark:stroke-gray-700" />
                  <XAxis dataKey="batch" fontSize={12} stroke="#6b7280" className="dark:stroke-gray-500" />
                  <YAxis fontSize={12} stroke="#6b7280" className="dark:stroke-gray-500" domain={[3.9, 4.5]} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#fff',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px'
                    }}
                  />
                  <Legend />
                  <ReferenceLine
                    y={spcMetrics.ucl}
                    stroke="#ef4444"
                    strokeDasharray="5 5"
                    label={{ value: `UCL: ${spcMetrics.ucl}V`, position: 'right', fill: '#ef4444' }}
                  />
                  <ReferenceLine
                    y={spcMetrics.lcl}
                    stroke="#ef4444"
                    strokeDasharray="5 5"
                    label={{ value: `LCL: ${spcMetrics.lcl}V`, position: 'right', fill: '#ef4444' }}
                  />
                  <ReferenceLine
                    y={spcMetrics.mean}
                    stroke="#3b82f6"
                    strokeDasharray="3 3"
                    label={{ value: `Mean: ${spcMetrics.mean}V`, position: 'right', fill: '#3b82f6' }}
                  />
                  <Line type="monotone" dataKey="voltage" stroke="#3b82f6" dot={{ fill: '#3b82f6', r: 4 }} name="Voltage (V)" />
                </LineChart>
              </ResponsiveContainer>

              {/* SPC Metrics */}
              <div className="bg-gray-50 dark:bg-gray-800 rounded p-3 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">Cpk (Capability):</span>
                  <span className="font-bold text-gray-900 dark:text-white">{spcMetrics.cpk.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">DPM:</span>
                  <span className="font-bold text-gray-900 dark:text-white">{spcMetrics.defects_per_million}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">Yield Rate:</span>
                  <span className="font-bold text-gray-900 dark:text-white">{(spcMetrics.yield_rate * 100).toFixed(2)}%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">Rating:</span>
                  <span className="font-bold text-gray-900 dark:text-white">{spcMetrics.capability_rating}</span>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-gray-600 dark:text-gray-400">Loading SPC metrics...</p>
          )}
        </div>

        {/* 2. Defect Risk Gauge */}
        <div className="md:col-span-1 card">
          <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">Defect Risk Gauge</h3>
          {qualityDrift ? (
            <div className="space-y-4">
              {/* Progress bar */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Risk Level</span>
                  <span className="text-sm font-bold text-gray-900 dark:text-white">
                    {(qualityDrift.defect_risk_score * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4 overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all ${
                      qualityDrift.defect_risk_score < 0.3
                        ? 'bg-green-500'
                        : qualityDrift.defect_risk_score < 0.6
                        ? 'bg-yellow-500'
                        : 'bg-red-500'
                    }`}
                    style={{ width: `${qualityDrift.defect_risk_score * 100}%` }}
                  />
                </div>
              </div>

              {/* Severity indicator */}
              <div className="bg-gray-50 dark:bg-gray-800 rounded p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Severity</span>
                  <span
                    className={`px-3 py-1 rounded text-sm font-bold ${
                      qualityDrift.severity === 'critical'
                        ? 'bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-400'
                        : qualityDrift.severity === 'high'
                        ? 'bg-orange-100 dark:bg-orange-900 text-orange-700 dark:text-orange-400'
                        : qualityDrift.severity === 'medium'
                        ? 'bg-yellow-100 dark:bg-yellow-900 text-yellow-700 dark:text-yellow-400'
                        : 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-400'
                    }`}
                  >
                    {qualityDrift.severity.toUpperCase()}
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Control Status</span>
                  <div className="flex items-center gap-2">
                    {getControlStatusIcon(qualityDrift.control_chart_signal)}
                    <span className="text-sm font-bold text-gray-900 dark:text-white">
                      {qualityDrift.control_chart_signal}
                    </span>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Confidence</span>
                  <span className="text-sm font-bold text-gray-900 dark:text-white">
                    {(qualityDrift.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-gray-600 dark:text-gray-400">Loading risk metrics...</p>
          )}
        </div>

        {/* 3. Traceability Chain */}
        <div className="md:col-span-1 card">
          <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">Traceability Chain</h3>
          {defectTrace ? (
            <div className="space-y-4">
              {/* Chain visualization */}
              <div className="space-y-3">
                {/* Cell */}
                <div className="flex items-center gap-2">
                  <div className="bg-blue-100 dark:bg-blue-900 rounded-lg p-3 flex-1 border border-blue-300 dark:border-blue-700">
                    <div className="text-xs font-bold text-blue-900 dark:text-blue-200">CELL</div>
                    <div className="text-sm font-mono text-blue-700 dark:text-blue-300">{defectTrace.cell_id}</div>
                  </div>
                  <Zap className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                </div>

                {/* Pack */}
                <div className="flex items-center gap-2">
                  <div className="bg-purple-100 dark:bg-purple-900 rounded-lg p-3 flex-1 border border-purple-300 dark:border-purple-700">
                    <div className="text-xs font-bold text-purple-900 dark:text-purple-200">PACK</div>
                    <div className="text-sm font-mono text-purple-700 dark:text-purple-300">{defectTrace.pack_id}</div>
                  </div>
                  <Package className="w-5 h-5 text-purple-600 dark:text-purple-400" />
                </div>

                {/* Vehicle */}
                <div className="flex items-center gap-2">
                  <div className="bg-green-100 dark:bg-green-900 rounded-lg p-3 flex-1 border border-green-300 dark:border-green-700">
                    <div className="text-xs font-bold text-green-900 dark:text-green-200">VEHICLE</div>
                    <div className="text-sm font-mono text-green-700 dark:text-green-300">{defectTrace.vehicle_id}</div>
                  </div>
                  <Truck className="w-5 h-5 text-green-600 dark:text-green-400" />
                </div>
              </div>

              {/* Quality info */}
              <div className="bg-gray-50 dark:bg-gray-800 rounded p-3 space-y-2 border-t border-gray-200 dark:border-gray-700 pt-4">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">Quality Score</span>
                  <span className="font-bold text-gray-900 dark:text-white">{(defectTrace.quality_score * 100).toFixed(0)}%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">Batch</span>
                  <span className="text-xs font-mono text-gray-900 dark:text-white">{defectTrace.batch_number}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600 dark:text-gray-400">Supplier</span>
                  <span className="font-bold text-gray-900 dark:text-white">{defectTrace.supplier_id}</span>
                </div>
                <div className="text-xs mt-2 p-2 bg-blue-50 dark:bg-blue-900/20 rounded text-blue-700 dark:text-blue-300">
                  {defectTrace.recommendation}
                </div>
              </div>
            </div>
          ) : (
            <p className="text-gray-600 dark:text-gray-400">Loading traceability data...</p>
          )}
        </div>
      </div>

      {/* Detailed Metrics Summary */}
      {spcMetrics && qualityDrift && (
        <div className="card">
          <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">Process Summary</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-gray-50 dark:bg-gray-800 rounded p-4">
              <p className="text-xs text-gray-600 dark:text-gray-400 uppercase tracking-wide">Voltage Status</p>
              <p className="text-lg font-bold text-gray-900 dark:text-white mt-1">
                {qualityDrift.process_summary?.voltage_status}
              </p>
            </div>
            <div className="bg-gray-50 dark:bg-gray-800 rounded p-4">
              <p className="text-xs text-gray-600 dark:text-gray-400 uppercase tracking-wide">Temperature Status</p>
              <p className="text-lg font-bold text-gray-900 dark:text-white mt-1">
                {qualityDrift.process_summary?.temperature_status}
              </p>
            </div>
            <div className="bg-gray-50 dark:bg-gray-800 rounded p-4">
              <p className="text-xs text-gray-600 dark:text-gray-400 uppercase tracking-wide">Capacity Fade Rate</p>
              <p className="text-lg font-bold text-gray-900 dark:text-white mt-1">
                {(qualityDrift.process_summary?.capacity_fade_rate * 1000).toFixed(2)}‰
              </p>
            </div>
            <div className="bg-gray-50 dark:bg-gray-800 rounded p-4">
              <p className="text-xs text-gray-600 dark:text-gray-400 uppercase tracking-wide">Line Status</p>
              <p className="text-lg font-bold text-gray-900 dark:text-white mt-1">
                {spcMetrics.control_status}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
