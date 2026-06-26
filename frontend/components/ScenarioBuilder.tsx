'use client';

import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { AlertTriangle, Play, Download } from 'lucide-react';

interface ScenarioResult {
  scenario_id: string;
  scenario_name: string;
  severity: number;
  days_to_shortage: number;
  cost_impact_percent: number;
  affected_vehicles: number;
  timeline_delay_months: number;
  mitigation_steps: string[];
  confidence_score: number;
}

interface ScenarioTemplate {
  id: string;
  name: string;
  description: string;
  parameters: Record<string, any>;
  impact_areas: string[];
  severity: string;
}

const ScenarioBuilder: React.FC = () => {
  const [scenarios, setScenarios] = useState<ScenarioTemplate[]>([]);
  const [selectedScenario, setSelectedScenario] = useState<string>('');
  const [parameters, setParameters] = useState<Record<string, number>>({});
  const [results, setResults] = useState<ScenarioResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [comparisonResults, setComparisonResults] = useState<any>(null);

  React.useEffect(() => {
    fetchScenarioTemplates();
  }, []);

  const fetchScenarioTemplates = async () => {
    try {
      const response = await fetch('/api/v1/scenarios/templates');
      const data = await response.json();
      setScenarios(data.scenarios || []);
    } catch (error) {
      console.error('Error fetching scenarios:', error);
    }
  };

  const handleScenarioSelect = (id: string) => {
    setSelectedScenario(id);
    const scenario = scenarios.find(s => s.id === id);
    if (scenario) {
      // Initialize parameters with defaults
      const defaultParams: Record<string, number> = {};
      Object.entries(scenario.parameters).forEach(([key, value]: [string, any]) => {
        defaultParams[key] = value.default || value;
      });
      setParameters(defaultParams);
    }
  };

  const handleParameterChange = (param: string, value: number) => {
    setParameters(prev => ({ ...prev, [param]: value }));
  };

  const runScenario = async () => {
    if (!selectedScenario) return;
    
    setLoading(true);
    try {
      const response = await fetch('/api/v1/scenarios/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scenario_id: selectedScenario,
          parameters
        })
      });
      const data = await response.json();
      setResults(data);
    } catch (error) {
      console.error('Error running scenario:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSeverityColor = (severity: number): string => {
    if (severity > 0.8) return 'text-red-600';
    if (severity > 0.6) return 'text-orange-600';
    if (severity > 0.4) return 'text-yellow-600';
    return 'text-green-600';
  };

  const getSeverityBg = (severity: number): string => {
    if (severity > 0.8) return 'bg-red-50 border-l-4 border-red-600';
    if (severity > 0.6) return 'bg-orange-50 border-l-4 border-orange-600';
    if (severity > 0.4) return 'bg-yellow-50 border-l-4 border-yellow-600';
    return 'bg-green-50 border-l-4 border-green-600';
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-4 space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Scenario Simulation Engine</h2>
        <p className="text-gray-600">Model "what-if" disruption scenarios for your supply chain and fleet</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Scenario Selector */}
        <div className="lg:col-span-1 space-y-4">
          <div className="bg-white rounded-lg shadow-md p-4 space-y-3">
            <h3 className="font-semibold text-gray-900">Select Scenario</h3>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {scenarios.map(scenario => (
                <button
                  key={scenario.id}
                  onClick={() => handleScenarioSelect(scenario.id)}
                  className={`w-full text-left p-3 rounded-lg border-2 transition ${
                    selectedScenario === scenario.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="font-medium text-sm text-gray-900">{scenario.name}</div>
                  <div className="text-xs text-gray-500 mt-1">{scenario.description}</div>
                  <div className="mt-2 flex flex-wrap gap-1">
                    {scenario.impact_areas.map(area => (
                      <span key={area} className="text-xs bg-gray-100 px-2 py-0.5 rounded">
                        {area}
                      </span>
                    ))}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Parameters & Results */}
        <div className="lg:col-span-2 space-y-4">
          {selectedScenario && scenarios.find(s => s.id === selectedScenario) && (
            <div className="bg-white rounded-lg shadow-md p-4 space-y-4">
              <h3 className="font-semibold text-gray-900">Adjust Parameters</h3>
              
              <div className="space-y-4">
                {Object.entries(scenarios.find(s => s.id === selectedScenario)?.parameters || {}).map(
                  ([paramKey, paramConfig]: [string, any]) => (
                    <div key={paramKey}>
                      <label className="block text-sm font-medium text-gray-700 mb-1 capitalize">
                        {paramKey.replace(/_/g, ' ')}
                      </label>
                      
                      {paramConfig.min !== undefined ? (
                        <div className="flex items-center gap-3">
                          <input
                            type="range"
                            min={paramConfig.min}
                            max={paramConfig.max}
                            step={1}
                            value={parameters[paramKey] || paramConfig.default}
                            onChange={e => handleParameterChange(paramKey, parseFloat(e.target.value))}
                            className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                          />
                          <span className="font-semibold text-gray-900 w-16 text-right">
                            {parameters[paramKey] || paramConfig.default}
                          </span>
                        </div>
                      ) : (
                        <select
                          value={parameters[paramKey] || paramConfig.default}
                          onChange={e => handleParameterChange(paramKey, e.target.value as any)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                          {paramConfig.options?.map((opt: string) => (
                            <option key={opt} value={opt}>{opt}</option>
                          ))}
                        </select>
                      )}
                    </div>
                  )
                )}
              </div>

              <button
                onClick={runScenario}
                disabled={loading}
                className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 flex items-center justify-center gap-2 font-medium"
              >
                <Play size={18} />
                {loading ? 'Running...' : 'Run Simulation'}
              </button>
            </div>
          )}

          {results && (
            <div className={`rounded-lg shadow-md p-4 space-y-3 ${getSeverityBg(results.severity)}`}>
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-semibold text-gray-900 text-lg">{results.scenario_name}</h3>
                  <div className="flex items-center gap-2 mt-1">
                    <div className={`text-2xl font-bold ${getSeverityColor(results.severity)}`}>
                      {(results.severity * 100).toFixed(0)}%
                    </div>
                    <span className="text-sm text-gray-600">Severity</span>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-gray-600">Confidence</div>
                  <div className="text-lg font-semibold text-gray-900">{(results.confidence_score * 100).toFixed(0)}%</div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="bg-white bg-opacity-60 p-2 rounded">
                  <div className="text-xs text-gray-600">Days to Shortage</div>
                  <div className="text-xl font-bold text-gray-900">{results.days_to_shortage}</div>
                </div>
                <div className="bg-white bg-opacity-60 p-2 rounded">
                  <div className="text-xs text-gray-600">Cost Impact</div>
                  <div className="text-xl font-bold text-gray-900">{results.cost_impact_percent.toFixed(1)}%</div>
                </div>
                <div className="bg-white bg-opacity-60 p-2 rounded">
                  <div className="text-xs text-gray-600">Affected Vehicles</div>
                  <div className="text-xl font-bold text-gray-900">{results.affected_vehicles}</div>
                </div>
                <div className="bg-white bg-opacity-60 p-2 rounded">
                  <div className="text-xs text-gray-600">Timeline Delay</div>
                  <div className="text-xl font-bold text-gray-900">{results.timeline_delay_months}mo</div>
                </div>
              </div>

              <div>
                <h4 className="font-semibold text-gray-900 mb-2 flex items-center gap-2">
                  <AlertTriangle size={18} />
                  Mitigation Steps
                </h4>
                <ol className="space-y-1 list-decimal list-inside">
                  {results.mitigation_steps.map((step, i) => (
                    <li key={i} className="text-sm text-gray-800">{step}</li>
                  ))}
                </ol>
              </div>

              <button className="w-full bg-white text-gray-700 py-1 rounded flex items-center justify-center gap-2 border border-gray-300 hover:bg-gray-50 text-sm font-medium">
                <Download size={16} />
                Export Results
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ScenarioBuilder;
