'use client';

import React, { useState, useEffect } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell
} from 'recharts';
import {
  Zap,
  AlertCircle,
  CheckCircle,
  Clock,
  Cpu,
  TrendingUp,
  PlayCircle,
  RefreshCw,
  AlertTriangle,
  Info,
  ChevronRight
} from 'lucide-react';

interface AgentStatus {
  name: string;
  status: string;
  last_run: string | null;
  response_time_ms: number;
  insights_generated: number;
}

interface CrossAgentInsight {
  type: string;
  message: string;
  severity: string;
  affected_agents: string[];
  recommended_action: string;
  confidence: number;
}

interface OrchestrationResult {
  fleet_id: string;
  overall_fleet_health_score: number;
  cross_agent_insights: CrossAgentInsight[];
  agents_run: string[];
  execution_time_ms: number;
  insights_count: number;
  critical_insights_count: number;
  orchestration_timestamp: string;
  agent_results: Record<string, any>;
}

const AGENT_CONFIG = {
  battery: { label: 'Battery Health', color: '#3b82f6', icon: '🔋' },
  supply_chain: { label: 'Supply Chain', color: '#f97316', icon: '🚚' },
  fleet: { label: 'Fleet Readiness', color: '#8b5cf6', icon: '🚗' },
  anomaly: { label: 'Anomaly Detection', color: '#ef4444', icon: '⚠️' },
  quality: { label: 'Manufacturing', color: '#06b6d4', icon: '⚙️' },
  carbon: { label: 'Carbon Intel', color: '#10b981', icon: '🌱' }
};

export default function AgentOrchestrator() {
  const [agentStatuses, setAgentStatuses] = useState<AgentStatus[]>([]);
  const [orchestrationResult, setOrchestrationResult] = useState<OrchestrationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [runningAllAgents, setRunningAllAgents] = useState(false);

  // Fetch agent statuses on mount
  useEffect(() => {
    fetchAgentStatus();
  }, []);

  const fetchAgentStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/agents/status');
      if (response.ok) {
        const data = await response.json();
        setAgentStatuses(data.agents || []);
      }
    } catch (err) {
      console.error('Error fetching agent status:', err);
    }
  };

  const handleRunAllAgents = async () => {
    try {
      setRunningAllAgents(true);
      setError(null);
      setLoading(true);

      const response = await fetch(
        'http://localhost:8000/api/v1/agents/orchestrate?fleet_id=FLEET_001&vehicle_count=100&run_parallel=false'
      );

      if (response.ok) {
        const data = await response.json();
        setOrchestrationResult(data);
        await fetchAgentStatus();
      } else {
        setError('Failed to run orchestration');
      }
    } catch (err) {
      setError('Error running orchestration');
      console.error(err);
    } finally {
      setLoading(false);
      setRunningAllAgents(false);
    }
  };

  const getHealthColor = (score: number) => {
    if (score >= 80) return '#10b981'; // green
    if (score >= 60) return '#f59e0b'; // amber
    return '#ef4444'; // red
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800 text-red-700 dark:text-red-400';
      case 'high':
        return 'bg-orange-50 dark:bg-orange-900/20 border-orange-200 dark:border-orange-800 text-orange-700 dark:text-orange-400';
      case 'medium':
        return 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800 text-yellow-700 dark:text-yellow-400';
      default:
        return 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800 text-blue-700 dark:text-blue-400';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <AlertTriangle className="w-5 h-5" />;
      case 'high':
        return <AlertCircle className="w-5 h-5" />;
      case 'medium':
        return <Info className="w-5 h-5" />;
      default:
        return <Info className="w-5 h-5" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'operational':
        return 'bg-green-500';
      case 'running':
        return 'bg-blue-500 animate-pulse';
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-gray-400';
    }
  };

  // Prepare response timeline data
  const timelineData = agentStatuses.map((agent) => ({
    name: AGENT_CONFIG[agent.name as keyof typeof AGENT_CONFIG]?.label || agent.name,
    time: agent.response_time_ms || 0,
    fill: AGENT_CONFIG[agent.name as keyof typeof AGENT_CONFIG]?.color || '#6b7280'
  }));

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Agent Command Center</h2>
          <p className="text-gray-600 dark:text-gray-400 mt-1">Coordinated multi-agent fleet intelligence</p>
        </div>
        <button
          onClick={handleRunAllAgents}
          disabled={runningAllAgents || loading}
          className="flex items-center gap-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 dark:from-purple-700 dark:to-blue-700 dark:hover:from-purple-600 dark:hover:to-blue-600 text-white px-6 py-3 rounded-lg font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {runningAllAgents ? (
            <>
              <RefreshCw className="w-5 h-5 animate-spin" />
              Running Agents...
            </>
          ) : (
            <>
              <PlayCircle className="w-5 h-5" />
              Run All Agents
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 text-red-700 dark:text-red-400">
          {error}
        </div>
      )}

      {/* 6-Agent Status Grid (3x2) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Object.entries(AGENT_CONFIG).map(([agentKey, agentConfig]) => {
          const agent = agentStatuses.find((a) => a.name === agentKey);
          return (
            <div
              key={agentKey}
              className="card border-l-4"
              style={{ borderLeftColor: agentConfig.color }}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{agentConfig.icon}</span>
                  <div>
                    <h3 className="font-bold text-gray-900 dark:text-white">{agentConfig.label}</h3>
                    <p className="text-xs text-gray-500 dark:text-gray-400">{agentKey}</p>
                  </div>
                </div>
                <div
                  className={`w-3 h-3 rounded-full ${
                    agent ? getStatusColor(agent.status) : 'bg-gray-400'
                  }`}
                />
              </div>

              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Status</span>
                  <span className="font-semibold text-gray-900 dark:text-white capitalize">
                    {agent?.status || 'idle'}
                  </span>
                </div>

                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Response Time</span>
                  <span className="font-mono text-gray-900 dark:text-white">{agent?.response_time_ms.toFixed(0) || 0}ms</span>
                </div>

                <div className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">Insights</span>
                  <span className="font-semibold text-gray-900 dark:text-white">{agent?.insights_generated || 0}</span>
                </div>

                {agent?.last_run && (
                  <div className="flex justify-between pt-2 border-t border-gray-200 dark:border-gray-700">
                    <span className="text-gray-600 dark:text-gray-400 text-xs">Last Run</span>
                    <span className="text-xs text-gray-700 dark:text-gray-300">
                      {new Date(agent.last_run).toLocaleTimeString()}
                    </span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Overall Health Score */}
      {orchestrationResult && (
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">Overall Fleet Health</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Composite score from 6 agents + cross-agent insights
              </p>
            </div>

            {/* Circular Gauge */}
            <div className="relative w-32 h-32">
              <svg className="w-full h-full" viewBox="0 0 120 120">
                {/* Background circle */}
                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  fill="none"
                  stroke="#e5e7eb"
                  strokeWidth="8"
                  className="dark:stroke-gray-700"
                />
                {/* Progress circle */}
                <circle
                  cx="60"
                  cy="60"
                  r="50"
                  fill="none"
                  stroke={getHealthColor(orchestrationResult.overall_fleet_health_score)}
                  strokeWidth="8"
                  strokeDasharray={`${(orchestrationResult.overall_fleet_health_score / 100) * 314} 314`}
                  strokeLinecap="round"
                  className="transition-all"
                  style={{ transform: 'rotate(-90deg)', transformOrigin: '60px 60px' }}
                />
              </svg>
              {/* Score text */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <div
                    className="text-3xl font-black"
                    style={{ color: getHealthColor(orchestrationResult.overall_fleet_health_score) }}
                  >
                    {orchestrationResult.overall_fleet_health_score.toFixed(1)}
                  </div>
                  <div className="text-xs text-gray-600 dark:text-gray-400">/100</div>
                </div>
              </div>
            </div>
          </div>

          {/* Health interpretation */}
          <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <p className="text-sm">
              {orchestrationResult.overall_fleet_health_score >= 80 && (
                <span className="text-green-700 dark:text-green-400">
                  ✅ Excellent health - All systems optimal
                </span>
              )}
              {orchestrationResult.overall_fleet_health_score >= 60 &&
                orchestrationResult.overall_fleet_health_score < 80 && (
                  <span className="text-yellow-700 dark:text-yellow-400">
                    ⚠️ Good health - Minor issues to address
                  </span>
                )}
              {orchestrationResult.overall_fleet_health_score < 60 && (
                <span className="text-red-700 dark:text-red-400">
                  🔴 Needs attention - Critical issues detected
                </span>
              )}
            </p>
          </div>
        </div>
      )}

      {/* Cross-Agent Insights Panel */}
      {orchestrationResult && orchestrationResult.cross_agent_insights.length > 0 && (
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white">Cross-Agent Insights</h3>
            <span className="px-3 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 rounded-full text-sm font-semibold">
              {orchestrationResult.cross_agent_insights.length} detected
            </span>
          </div>

          <div className="space-y-3">
            {orchestrationResult.cross_agent_insights.map((insight, idx) => (
              <div
                key={idx}
                className={`border rounded-lg p-4 ${getSeverityColor(insight.severity)}`}
              >
                <div className="flex gap-3">
                  <div className="flex-shrink-0 mt-1">{getSeverityIcon(insight.severity)}</div>
                  <div className="flex-1">
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="font-bold capitalize">{insight.type}</h4>
                        <p className="text-sm mt-1">{insight.message}</p>
                      </div>
                      <span className="text-xs font-mono bg-white dark:bg-gray-800 px-2 py-1 rounded opacity-75">
                        {(insight.confidence * 100).toFixed(0)}%
                      </span>
                    </div>

                    {/* Affected agents */}
                    <div className="flex flex-wrap gap-2 mt-3">
                      {insight.affected_agents.map((agent) => (
                        <span
                          key={agent}
                          className="px-2 py-1 bg-white dark:bg-gray-800 rounded text-xs font-medium opacity-75"
                        >
                          {AGENT_CONFIG[agent as keyof typeof AGENT_CONFIG]?.label || agent}
                        </span>
                      ))}
                    </div>

                    {/* Recommended action */}
                    <div className="mt-3 p-3 bg-white dark:bg-gray-800/50 rounded border-l-2 border-white dark:border-gray-700">
                      <p className="text-xs font-semibold opacity-75 mb-1">Recommended Action:</p>
                      <p className="text-sm">{insight.recommended_action}</p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Agent Response Timeline */}
      {timelineData.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-bold mb-4 text-gray-900 dark:text-white">Agent Response Timeline</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={timelineData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" className="dark:stroke-gray-700" />
              <XAxis dataKey="name" fontSize={12} stroke="#6b7280" className="dark:stroke-gray-500" />
              <YAxis
                fontSize={12}
                stroke="#6b7280"
                className="dark:stroke-gray-500"
                label={{ value: 'Response Time (ms)', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#fff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px'
                }}
              />
              <Bar dataKey="time" name="Response Time (ms)" radius={[8, 8, 0, 0]}>
                {timelineData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Execution Summary */}
      {orchestrationResult && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="card">
            <p className="text-xs text-gray-600 dark:text-gray-400 uppercase">Agents Run</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
              {orchestrationResult.agents_run.length}
            </p>
            <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">of 6</p>
          </div>

          <div className="card">
            <p className="text-xs text-gray-600 dark:text-gray-400 uppercase">Total Insights</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
              {orchestrationResult.insights_count}
            </p>
          </div>

          <div className="card">
            <p className="text-xs text-gray-600 dark:text-gray-400 uppercase">Critical</p>
            <p className={`text-2xl font-bold mt-1 ${
              orchestrationResult.critical_insights_count > 0 ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400'
            }`}>
              {orchestrationResult.critical_insights_count}
            </p>
          </div>

          <div className="card">
            <p className="text-xs text-gray-600 dark:text-gray-400 uppercase">Execution Time</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
              {orchestrationResult.execution_time_ms.toFixed(0)}ms
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
