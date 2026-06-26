'use client';

import React, { useState, useEffect } from 'react';
import { AlertTriangle, AlertCircle, AlertOctagon, Info, CheckCircle, X } from 'lucide-react';

interface Anomaly {
  anomaly_id: string;
  type: string;
  severity: string;
  description: string;
  affected_count: number;
  zscore: number;
  confidence: number;
  recommended_action: string;
}

const AnomalyAlert: React.FC = () => {
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [dismissedIds, setDismissedIds] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState<string>('all');

  useEffect(() => {
    fetchAnomalies();
    const interval = setInterval(fetchAnomalies, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchAnomalies = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/v1/anomalies/active');
      const data = await response.json();
      setAnomalies(data.anomalies || []);
    } catch (error) {
      console.error('Error fetching anomalies:', error);
    } finally {
      setLoading(false);
    }
  };

  const dismissAnomaly = async (id: string) => {
    try {
      await fetch(`/api/v1/anomalies/${id}/acknowledge`, { method: 'PUT' });
      setDismissedIds(prev => new Set([...prev, id]));
      setAnomalies(anomalies.filter(a => a.anomaly_id !== id));
    } catch (error) {
      console.error('Error dismissing anomaly:', error);
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <AlertOctagon className="text-red-600" size={20} />;
      case 'high':
        return <AlertTriangle className="text-orange-600" size={20} />;
      case 'medium':
        return <AlertCircle className="text-yellow-600" size={20} />;
      default:
        return <Info className="text-blue-600" size={20} />;
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

  const getTypeLabel = (type: string): string => {
    const labels: Record<string, string> = {
      battery: 'Battery Health',
      supply_chain: 'Supply Chain',
      fleet: 'Fleet Management',
      infrastructure: 'Infrastructure',
    };
    return labels[type] || type;
  };

  const filteredAnomalies = filter === 'all' 
    ? anomalies 
    : anomalies.filter(a => a.severity === filter);

  const severityCounts = {
    critical: anomalies.filter(a => a.severity === 'critical').length,
    high: anomalies.filter(a => a.severity === 'high').length,
    medium: anomalies.filter(a => a.severity === 'medium').length,
    low: anomalies.filter(a => a.severity === 'low').length,
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-4 space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Anomaly Detection Center</h2>
        <p className="text-gray-600">Monitor unusual patterns in fleet and supply chain data</p>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="bg-red-50 rounded-lg p-3 border-l-4 border-red-600">
          <div className="text-2xl font-bold text-red-600">{severityCounts.critical}</div>
          <div className="text-xs text-gray-600">Critical</div>
        </div>
        <div className="bg-orange-50 rounded-lg p-3 border-l-4 border-orange-600">
          <div className="text-2xl font-bold text-orange-600">{severityCounts.high}</div>
          <div className="text-xs text-gray-600">High</div>
        </div>
        <div className="bg-yellow-50 rounded-lg p-3 border-l-4 border-yellow-600">
          <div className="text-2xl font-bold text-yellow-600">{severityCounts.medium}</div>
          <div className="text-xs text-gray-600">Medium</div>
        </div>
        <div className="bg-blue-50 rounded-lg p-3 border-l-4 border-blue-600">
          <div className="text-2xl font-bold text-blue-600">{severityCounts.low}</div>
          <div className="text-xs text-gray-600">Low</div>
        </div>
      </div>

      {/* Filter Buttons */}
      <div className="flex gap-2">
        {(['all', 'critical', 'high', 'medium', 'low'] as const).map(severity => (
          <button
            key={severity}
            onClick={() => setFilter(severity)}
            className={`px-4 py-2 rounded-lg font-medium text-sm transition ${
              filter === severity
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {severity.charAt(0).toUpperCase() + severity.slice(1)}
          </button>
        ))}
      </div>

      {/* Anomalies List */}
      <div className="space-y-3">
        {filteredAnomalies.length === 0 ? (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
            <CheckCircle className="mx-auto text-green-600 mb-2" size={32} />
            <h3 className="font-semibold text-gray-900 mb-1">No Anomalies Detected</h3>
            <p className="text-gray-600 text-sm">Your fleet and supply chain are operating normally</p>
            {loading && <p className="text-xs text-gray-500 mt-2">Checking for anomalies...</p>}
          </div>
        ) : (
          filteredAnomalies.map(anomaly => (
            <div key={anomaly.anomaly_id} className={`rounded-lg shadow-sm p-4 ${getSeverityColor(anomaly.severity)}`}>
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3 flex-1">
                  {getSeverityIcon(anomaly.severity)}
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-gray-900">{anomaly.description}</h3>
                      <span className="text-xs font-medium bg-white bg-opacity-60 px-2 py-0.5 rounded">
                        {getTypeLabel(anomaly.type)}
                      </span>
                    </div>
                    
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2 text-xs">
                      <div>
                        <span className="text-gray-600">Z-Score:</span>
                        <span className="font-semibold text-gray-900 ml-1">{anomaly.zscore.toFixed(1)}σ</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Confidence:</span>
                        <span className="font-semibold text-gray-900 ml-1">{(anomaly.confidence * 100).toFixed(0)}%</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Affected:</span>
                        <span className="font-semibold text-gray-900 ml-1">{anomaly.affected_count} items</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Severity:</span>
                        <span className="font-semibold text-gray-900 ml-1 capitalize">{anomaly.severity}</span>
                      </div>
                    </div>

                    <div className="mt-3 p-2 bg-white bg-opacity-60 rounded">
                      <p className="text-sm text-gray-900 font-medium mb-1">Recommended Action:</p>
                      <p className="text-sm text-gray-800">{anomaly.recommended_action}</p>
                    </div>
                  </div>
                </div>
                
                <button
                  onClick={() => dismissAnomaly(anomaly.anomaly_id)}
                  className="ml-3 text-gray-400 hover:text-gray-600 flex-shrink-0"
                  title="Dismiss alert"
                >
                  <X size={20} />
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Refresh Button */}
      <div className="flex justify-center">
        <button
          onClick={fetchAnomalies}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 font-medium text-sm"
        >
          {loading ? 'Refreshing...' : 'Refresh Now'}
        </button>
      </div>
    </div>
  );
};

export default AnomalyAlert;
