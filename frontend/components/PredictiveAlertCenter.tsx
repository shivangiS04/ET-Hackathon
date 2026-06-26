'use client';

import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Clock, TrendingDown, AlertTriangle, Zap } from 'lucide-react';

interface PredictiveAlert {
  alert_id: string;
  alert_type: string;
  severity: string;
  description: string;
  days_to_critical: number;
  current_value: number;
  forecast_90d: number;
  confidence: number;
  recommended_action: string;
}

const PredictiveAlertCenter: React.FC = () => {
  const [alerts, setAlerts] = useState<PredictiveAlert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 60000); // Refresh every minute
    return () => clearInterval(interval);
  }, []);

  const fetchAlerts = async () => {
    try {
      const response = await fetch('/api/v1/alerts/upcoming');
      const data = await response.json();
      setAlerts(data.alerts || []);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity: string): string => {
    switch (severity) {
      case 'critical':
        return 'bg-red-50 border-l-4 border-red-600';
      case 'high':
        return 'bg-orange-50 border-l-4 border-orange-600';
      case 'medium':
        return 'bg-yellow-50 border-l-4 border-yellow-600';
      default:
        return 'bg-blue-50 border-l-4 border-blue-600';
    }
  };

  const getSeverityBadgeColor = (severity: string): string => {
    switch (severity) {
      case 'critical':
        return 'bg-red-200 text-red-800';
      case 'high':
        return 'bg-orange-200 text-orange-800';
      case 'medium':
        return 'bg-yellow-200 text-yellow-800';
      default:
        return 'bg-blue-200 text-blue-800';
    }
  };

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'battery_ruf':
        return <Zap className="text-blue-600" size={20} />;
      case 'supply_risk':
        return <AlertTriangle className="text-orange-600" size={20} />;
      case 'fleet_readiness':
        return <TrendingDown className="text-purple-600" size={20} />;
      default:
        return <Clock className="text-gray-600" size={20} />;
    }
  };

  const getTypeLabel = (type: string): string => {
    const labels: Record<string, string> = {
      battery_ruf: 'Battery RUL Forecast',
      supply_risk: 'Supply Chain Risk',
      fleet_readiness: 'Fleet Readiness',
      cost: 'Cost Forecast',
    };
    return labels[type] || type;
  };

  const urgentAlerts = alerts.filter(a => a.days_to_critical <= 30);
  const warningAlerts = alerts.filter(a => a.days_to_critical > 30 && a.days_to_critical <= 90);
  const infoAlerts = alerts.filter(a => a.days_to_critical > 90);

  // Sample forecast data for timeline visualization
  const forecastData = [
    { day: 0, value: 65 },
    { day: 10, value: 63 },
    { day: 20, value: 61 },
    { day: 30, value: 59 },
    { day: 40, value: 57 },
    { day: 50, value: 54 },
    { day: 60, value: 51 },
    { day: 70, value: 48 },
    { day: 80, value: 45 },
    { day: 90, value: 42 },
  ];

  return (
    <div className="w-full max-w-6xl mx-auto p-4 space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Predictive Alert Center</h2>
        <p className="text-gray-600">Proactive forecasting and early warning system</p>
      </div>

      {/* Alert Timeline */}
      <div className="bg-white rounded-lg shadow-md p-4 space-y-4">
        <h3 className="font-semibold text-gray-900">Alert Timeline (Days to Critical)</h3>
        
        <div className="grid grid-cols-3 gap-3 mb-4">
          <div className="bg-red-50 rounded-lg p-3 border border-red-200">
            <div className="text-2xl font-bold text-red-600">{urgentAlerts.length}</div>
            <div className="text-xs text-gray-600">Urgent (≤30 days)</div>
          </div>
          <div className="bg-yellow-50 rounded-lg p-3 border border-yellow-200">
            <div className="text-2xl font-bold text-yellow-600">{warningAlerts.length}</div>
            <div className="text-xs text-gray-600">Warning (31-90 days)</div>
          </div>
          <div className="bg-blue-50 rounded-lg p-3 border border-blue-200">
            <div className="text-2xl font-bold text-blue-600">{infoAlerts.length}</div>
            <div className="text-xs text-gray-600">Monitor (>90 days)</div>
          </div>
        </div>

        {/* Forecast Chart */}
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={forecastData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="day" label={{ value: 'Days', position: 'insideBottomRight', offset: -5 }} />
            <YAxis label={{ value: 'Forecast Value', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="value" 
              stroke="#3b82f6" 
              dot={false}
              name="Metric Forecast"
              strokeWidth={2}
            />
            <Line 
              type="monotone" 
              dataKey={() => 50} 
              stroke="#ef4444" 
              strokeDasharray="5 5"
              dot={false}
              name="Critical Threshold"
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Detailed Alerts */}
      <div className="space-y-4">
        {/* Urgent Alerts */}
        {urgentAlerts.length > 0 && (
          <div className="space-y-3">
            <h3 className="font-semibold text-red-700 flex items-center gap-2">
              <AlertTriangle size={18} />
              Urgent Alerts - Action Required Now
            </h3>
            {urgentAlerts.map(alert => (
              <div key={alert.alert_id} className={`rounded-lg shadow-sm p-4 ${getSeverityColor(alert.severity)}`}>
                <div className="flex items-start gap-3">
                  {getAlertIcon(alert.alert_type)}
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-semibold text-gray-900">{alert.description}</h4>
                        <p className="text-xs text-gray-600 mt-1">{getTypeLabel(alert.alert_type)}</p>
                      </div>
                      <div className={`px-3 py-1 rounded-full font-semibold text-sm ${getSeverityBadgeColor(alert.severity)}`}>
                        {alert.days_to_critical}d
                      </div>
                    </div>

                    <div className="grid grid-cols-3 gap-2 mt-3 text-xs">
                      <div className="bg-white bg-opacity-60 p-2 rounded">
                        <span className="text-gray-600">Current:</span>
                        <span className="font-semibold text-gray-900 ml-1">{alert.current_value.toFixed(1)}</span>
                      </div>
                      <div className="bg-white bg-opacity-60 p-2 rounded">
                        <span className="text-gray-600">Forecast (90d):</span>
                        <span className="font-semibold text-gray-900 ml-1">{alert.forecast_90d.toFixed(1)}</span>
                      </div>
                      <div className="bg-white bg-opacity-60 p-2 rounded">
                        <span className="text-gray-600">Confidence:</span>
                        <span className="font-semibold text-gray-900 ml-1">{(alert.confidence * 100).toFixed(0)}%</span>
                      </div>
                    </div>

                    <div className="mt-3 p-3 bg-white bg-opacity-70 rounded-lg border-l-2 border-red-400">
                      <p className="text-sm font-medium text-gray-900 mb-1">📋 Recommended Action:</p>
                      <p className="text-sm text-gray-800">{alert.recommended_action}</p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Warning Alerts */}
        {warningAlerts.length > 0 && (
          <div className="space-y-3">
            <h3 className="font-semibold text-yellow-700 flex items-center gap-2">
              <Clock size={18} />
              Warnings - Plan Ahead
            </h3>
            {warningAlerts.map(alert => (
              <div key={alert.alert_id} className={`rounded-lg shadow-sm p-4 ${getSeverityColor(alert.severity)}`}>
                <div className="flex items-start gap-3">
                  {getAlertIcon(alert.alert_type)}
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h4 className="font-semibold text-gray-900">{alert.description}</h4>
                      <div className={`px-3 py-1 rounded-full font-semibold text-sm ${getSeverityBadgeColor(alert.severity)}`}>
                        {alert.days_to_critical}d
                      </div>
                    </div>
                    <p className="text-sm text-gray-700 mt-2">{alert.recommended_action}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Info Alerts */}
        {infoAlerts.length > 0 && (
          <div className="space-y-3">
            <h3 className="font-semibold text-blue-700">Monitoring - Low Priority</h3>
            <div className="bg-gray-50 rounded-lg p-3 space-y-2 max-h-32 overflow-y-auto">
              {infoAlerts.map(alert => (
                <div key={alert.alert_id} className="text-xs text-gray-600 border-b border-gray-200 pb-1 last:border-0">
                  <span className="font-medium">{alert.description}</span>
                  <span className="text-gray-500"> ({alert.days_to_critical} days)</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* No Alerts */}
        {alerts.length === 0 && !loading && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
            <Zap className="mx-auto text-green-600 mb-2" size={32} />
            <h3 className="font-semibold text-gray-900 mb-1">No Predictive Alerts</h3>
            <p className="text-gray-600 text-sm">All metrics are within normal ranges for the next 90 days</p>
          </div>
        )}
      </div>

      {/* Last Updated */}
      <div className="text-xs text-gray-500 text-center">
        {loading ? 'Loading alerts...' : `Last updated: ${new Date().toLocaleTimeString()}`}
      </div>
    </div>
  );
};

export default PredictiveAlertCenter;
