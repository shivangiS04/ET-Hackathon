'use client';

import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, Clock, TrendingUp, Zap, Activity } from 'lucide-react';

/**
 * Real-time Monitoring Dashboard
 * Live metrics and alerts with status indicators
 */

interface Alert {
  id: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  title: string;
  description: string;
  timestamp: string;
  actionable: boolean;
}

interface MetricCard {
  title: string;
  value: string | number;
  unit?: string;
  status: 'good' | 'warning' | 'critical';
  trend?: 'up' | 'down' | 'stable';
  icon: React.ReactNode;
}

export default function RealtimeMonitor() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [metrics, setMetrics] = useState<MetricCard[]>([]);
  const [refreshRate, setRefreshRate] = useState<'realtime' | '5s' | '30s' | '1m'>('realtime');
  const [lastUpdate, setLastUpdate] = useState<string>(new Date().toLocaleTimeString());

  // Initialize with mock data
  useEffect(() => {
    updateMetrics();
    
    // Set up refresh interval
    const interval = setInterval(() => {
      updateMetrics();
    }, refreshRate === 'realtime' ? 1000 : refreshRate === '5s' ? 5000 : refreshRate === '30s' ? 30000 : 60000);
    
    return () => clearInterval(interval);
  }, [refreshRate]);

  const updateMetrics = () => {
    // Simulate real-time metric updates
    const newMetrics: MetricCard[] = [
      {
        title: 'Fleet Average SOH',
        value: (87.3 + Math.random() * 2 - 1).toFixed(1),
        unit: '%',
        status: 'good',
        trend: Math.random() > 0.5 ? 'down' : 'stable',
        icon: <Zap className="w-6 h-6 text-blue-600" />
      },
      {
        title: 'Supply Chain Risk',
        value: (0.65 + Math.random() * 0.1 - 0.05).toFixed(2),
        unit: '/1.0',
        status: 'warning',
        trend: 'up',
        icon: <AlertCircle className="w-6 h-6 text-orange-600" />
      },
      {
        title: 'EV Readiness %',
        value: (72.4 + Math.random() * 3).toFixed(1),
        unit: '%',
        status: 'good',
        trend: 'up',
        icon: <TrendingUp className="w-6 h-6 text-green-600" />
      },
      {
        title: 'Active Alerts',
        value: Math.floor(3 + Math.random() * 2),
        status: 'warning',
        trend: 'stable',
        icon: <Activity className="w-6 h-6 text-red-600" />
      },
      {
        title: 'API Health',
        value: (99.8 + Math.random() * 0.2).toFixed(2),
        unit: '%',
        status: 'good',
        trend: 'stable',
        icon: <CheckCircle className="w-6 h-6 text-green-600" />
      },
      {
        title: 'Avg Response Time',
        value: (87 + Math.random() * 20).toFixed(0),
        unit: 'ms',
        status: 'good',
        trend: 'down',
        icon: <Clock className="w-6 h-6 text-purple-600" />
      }
    ];
    
    setMetrics(newMetrics);
    setLastUpdate(new Date().toLocaleTimeString());
    
    // Update alerts
    const newAlerts: Alert[] = [
      {
        id: 'ALT_001',
        severity: 'critical',
        title: 'Vehicle T004 - Battery Critical',
        description: 'Long-haul vehicle battery SOH: 58% - requires immediate replacement',
        timestamp: new Date().toLocaleTimeString(),
        actionable: true
      },
      {
        id: 'ALT_002',
        severity: 'high',
        title: 'China Supply Disruption Risk',
        description: 'Geopolitical escalation detected - 45% lithium supply at risk',
        timestamp: new Date(Date.now() - 300000).toLocaleTimeString(),
        actionable: true
      },
      {
        id: 'ALT_003',
        severity: 'medium',
        title: 'Fleet Maintenance Due',
        description: 'T002 (Mum-Pune): Battery maintenance scheduled for next 15 days',
        timestamp: new Date(Date.now() - 600000).toLocaleTimeString(),
        actionable: false
      }
    ];
    
    setAlerts(newAlerts);
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-50 border-red-200 text-red-900';
      case 'high':
        return 'bg-orange-50 border-orange-200 text-orange-900';
      case 'medium':
        return 'bg-yellow-50 border-yellow-200 text-yellow-900';
      case 'low':
        return 'bg-blue-50 border-blue-200 text-blue-900';
      default:
        return 'bg-gray-50 border-gray-200 text-gray-900';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'good':
        return 'text-green-600 bg-green-50';
      case 'warning':
        return 'text-orange-600 bg-orange-50';
      case 'critical':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header with Controls */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Real-time Monitoring</h2>
            <p className="text-sm text-gray-600 mt-1">Last updated: {lastUpdate}</p>
          </div>
          <div className="flex gap-2">
            {['realtime', '5s', '30s', '1m'].map((rate) => (
              <button
                key={rate}
                onClick={() => setRefreshRate(rate as any)}
                className={`px-3 py-1 rounded text-sm font-semibold transition ${
                  refreshRate === rate
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {rate === 'realtime' ? 'Live' : rate}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {metrics.map((metric, idx) => (
          <div
            key={idx}
            className={`rounded-lg border p-6 transition ${
              metric.status === 'critical'
                ? 'bg-red-50 border-red-200'
                : metric.status === 'warning'
                ? 'bg-yellow-50 border-yellow-200'
                : 'bg-white border-gray-200'
            }`}
          >
            <div className="flex items-start justify-between mb-3">
              <h3 className="text-sm font-semibold text-gray-700">{metric.title}</h3>
              {metric.icon}
            </div>
            
            <div className="flex items-end gap-2">
              <div className="text-3xl font-bold text-gray-900">
                {metric.value}
              </div>
              {metric.unit && (
                <span className="text-sm text-gray-600 mb-1">{metric.unit}</span>
              )}
            </div>
            
            {metric.trend && (
              <div className="mt-3 flex items-center gap-1">
                {metric.trend === 'up' && (
                  <span className="text-green-600 font-semibold">↑</span>
                )}
                {metric.trend === 'down' && (
                  <span className="text-red-600 font-semibold">↓</span>
                )}
                {metric.trend === 'stable' && (
                  <span className="text-gray-600 font-semibold">→</span>
                )}
                <span className="text-xs text-gray-600">
                  {metric.trend === 'up' ? 'Increasing' : metric.trend === 'down' ? 'Decreasing' : 'Stable'}
                </span>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Alerts Section */}
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <AlertCircle className="w-6 h-6 text-red-600" />
          Active Alerts ({alerts.length})
        </h3>
        
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {alerts.length === 0 ? (
            <div className="text-center py-8">
              <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-2" />
              <p className="text-gray-600">No active alerts</p>
            </div>
          ) : (
            alerts.map((alert) => (
              <div
                key={alert.id}
                className={`rounded-lg border p-4 ${getSeverityColor(alert.severity)}`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="font-semibold">{alert.title}</p>
                    <p className="text-sm mt-1 opacity-90">{alert.description}</p>
                    <p className="text-xs mt-2 opacity-75">ID: {alert.id} | {alert.timestamp}</p>
                  </div>
                  {alert.actionable && (
                    <button className="px-3 py-1 bg-white bg-opacity-80 hover:bg-opacity-100 rounded text-sm font-semibold ml-4 transition">
                      Take Action →
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* System Health */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">System Health</h3>
          <div className="space-y-3">
            {[
              { name: 'API Server', status: 'healthy', uptime: '99.98%' },
              { name: 'Database', status: 'healthy', uptime: '99.95%' },
              { name: 'Cache Layer', status: 'healthy', uptime: '99.99%' },
              { name: 'Analytics', status: 'degraded', uptime: '98.5%' }
            ].map((service, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <span className="font-medium text-gray-800">{service.name}</span>
                <div className="flex items-center gap-3">
                  <div className={`w-2 h-2 rounded-full ${
                    service.status === 'healthy' ? 'bg-green-500' : 'bg-yellow-500'
                  }`} />
                  <span className="text-sm text-gray-600">{service.uptime}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Metrics</h3>
          <div className="space-y-3">
            {[
              { metric: 'Cache Hit Rate', value: '68.4%', target: '>50%', status: 'good' },
              { metric: 'P95 Latency', value: '145ms', target: '<500ms', status: 'good' },
              { metric: 'Error Rate', value: '0.2%', target: '<1%', status: 'good' },
              { metric: 'Memory Usage', value: '72%', target: '<80%', status: 'warning' }
            ].map((perf, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <div>
                  <p className="font-medium text-gray-800">{perf.metric}</p>
                  <p className="text-xs text-gray-500">Target: {perf.target}</p>
                </div>
                <p className={`font-semibold ${
                  perf.status === 'good' ? 'text-green-600' : 'text-orange-600'
                }`}>
                  {perf.value}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recommendation Box */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">🎯 Recommended Actions</h3>
        <ul className="space-y-2 text-sm text-gray-700">
          <li>✓ <strong>Battery T004 (Critical):</strong> Schedule immediate replacement - expected delivery in 3 days</li>
          <li>✓ <strong>Supply Chain Risk (High):</strong> Activate Australian lithium suppliers as backup</li>
          <li>✓ <strong>Fleet Readiness:</strong> Phase 2 vehicles show 91% avg readiness - proceed with Q3 conversions</li>
          <li>✓ <strong>Carbon Target:</strong> Current path achieves 42% reduction vs 30% target by 2030</li>
        </ul>
      </div>
    </div>
  );
}
