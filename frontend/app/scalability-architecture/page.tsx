'use client';

import React from 'react';
import Link from 'next/link';
import { 
  Zap, Server, Database, Cpu, Network, Cloud, 
  Shield, TrendingUp, Users, Gauge, Activity
} from 'lucide-react';

export default function ScalabilityArchitecture() {
  const scalePhases = [
    {
      phase: "Phase 1",
      vehicles: "156",
      title: "Current Production",
      icon: <Gauge className="w-8 h-8" />,
      color: "blue",
      details: {
        infrastructure: "Single server with PostgreSQL + Redis",
        database: "Single PostgreSQL instance",
        cache: "Single Redis instance",
        ml_inference: "In-process",
        cost_per_vehicle: "₹12,500/year"
      },
      metrics: {
        avg_response_time: "87ms",
        uptime: "99.8%",
        max_concurrent: "200 users"
      }
    },
    {
      phase: "Phase 2",
      vehicles: "10,000",
      title: "Growth Scale",
      icon: <TrendingUp className="w-8 h-8" />,
      color: "green",
      details: {
        infrastructure: "Load-balanced 3-server cluster",
        database: "PostgreSQL with read replicas",
        cache: "Redis Cluster (6 nodes)",
        ml_inference: "GPU-accelerated batch processing",
        cost_per_vehicle: "₹8,200/year"
      },
      metrics: {
        avg_response_time: "95ms",
        uptime: "99.9%",
        max_concurrent: "2,000 users"
      }
    },
    {
      phase: "Phase 3",
      vehicles: "50,000",
      title: "Enterprise Scale",
      icon: <Users className="w-8 h-8" />,
      color: "orange",
      details: {
        infrastructure: "Kubernetes cluster (12 nodes)",
        database: "PostgreSQL sharded + read replicas",
        cache: "Redis Cluster (12 nodes)",
        ml_inference: "Dedicated ML inference server",
        cost_per_vehicle: "₹5,400/year"
      },
      metrics: {
        avg_response_time: "120ms",
        uptime: "99.95%",
        max_concurrent: "10,000 users"
      }
    },
    {
      phase: "Phase 4",
      vehicles: "1,000,000",
      title: "National Scale",
      icon: <Cloud className="w-8 h-8" />,
      color: "purple",
      details: {
        infrastructure: "Multi-region Kubernetes + CDN",
        database: "Distributed sharded PostgreSQL + Neo4j",
        cache: "Global Redis distributed cache",
        ml_inference: "Edge ML inference + centralized training",
        cost_per_vehicle: "₹3,100/year"
      },
      metrics: {
        avg_response_time: "180ms",
        uptime: "99.99%",
        max_concurrent: "100,000 users"
      }
    }
  ];

  const shardingStrategy = [
    { component: "MongoDB", strategy: "Sharding by vehicle_id", shards: "64", rationale: "Even distribution of vehicle data" },
    { component: "Neo4j", strategy: "Graph partitioning", shards: "8", rationale: "Supplier relationship clustering" },
    { component: "PostgreSQL", strategy: "Tenant-based sharding", shards: "16", rationale: "Geographic data isolation" },
    { component: "Redis", strategy: "Key-based partitioning", shards: "12", rationale: "Session & cache distribution" }
  ];

  const costBreakdown = [
    { scale: "156 vehicles", infrastructure: "₹19.5L", ml_compute: "₹3L", total: "₹22.5L", per_vehicle: "₹12,500" },
    { scale: "10,000 vehicles", infrastructure: "₹45L", ml_compute: "₹18L", total: "₹63L", per_vehicle: "₹8,200" },
    { scale: "50,000 vehicles", infrastructure: "₹120L", ml_compute: "₹65L", total: "₹185L", per_vehicle: "₹5,400" },
    { scale: "100,000 vehicles", infrastructure: "₹180L", ml_compute: "₹85L", total: "₹265L", per_vehicle: "₹4,100" }
  ];

  const colorClasses: Record<string, { bg: string; border: string; text: string }> = {
    blue: { bg: 'bg-blue-50', border: 'border-blue-200', text: 'text-blue-600' },
    green: { bg: 'bg-green-50', border: 'border-green-200', text: 'text-green-600' },
    orange: { bg: 'bg-orange-50', border: 'border-orange-200', text: 'text-orange-600' },
    purple: { bg: 'bg-purple-50', border: 'border-purple-200', text: 'text-purple-600' }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-3">
            <Link href="/" className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-cyan-600 to-blue-600 rounded-lg p-2">
                <Network className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Scalability Architecture</h1>
                <p className="text-xs text-gray-500">From 156 to 1,000,000 vehicles</p>
              </div>
            </Link>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero */}
        <div className="bg-gradient-to-r from-cyan-600 to-blue-600 rounded-xl p-8 text-white mb-8">
          <div className="flex items-center gap-4 mb-4">
            <Server className="w-12 h-12" />
            <div>
              <h2 className="text-3xl font-bold">Built for Scale</h2>
              <p className="text-cyan-100 mt-1">Architecture designed to handle India's EV transition at national scale</p>
            </div>
          </div>
          <div className="grid grid-cols-4 gap-6 mt-6">
            <div>
              <div className="text-4xl font-bold">1M+</div>
              <div className="text-cyan-200 text-sm">Vehicles Supported</div>
            </div>
            <div>
              <div className="text-4xl font-bold">99.99%</div>
              <div className="text-cyan-200 text-sm">Target Uptime</div>
            </div>
            <div>
              <div className="text-4xl font-bold">100K</div>
              <div className="text-cyan-200 text-sm">Concurrent Users</div>
            </div>
            <div>
              <div className="text-4xl font-bold">₹3,100</div>
              <div className="text-cyan-200 text-sm">Cost per Vehicle/year</div>
            </div>
          </div>
        </div>

        {/* Scale Phases */}
        <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <Activity className="w-7 h-7 text-cyan-600" />
          Scale Phases
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {scalePhases.map((phase, idx) => (
            <div key={idx} className={`bg-white rounded-xl border-2 ${colorClasses[phase.color].border} p-6`}>
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm font-medium text-gray-500">{phase.phase}</span>
                <div className={`${colorClasses[phase.color].text}`}>
                  {phase.icon}
                </div>
              </div>
              
              <div className="text-3xl font-bold text-gray-900 mb-1">
                {phase.vehicles}
              </div>
              <div className="text-sm font-medium text-gray-700 mb-4">
                {phase.title}
              </div>

              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">Response:</span>
                  <span className="font-medium">{phase.metrics.avg_response_time}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Uptime:</span>
                  <span className="font-medium">{phase.metrics.uptime}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Max Users:</span>
                  <span className="font-medium">{phase.metrics.max_concurrent}</span>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="text-xs text-gray-500 mb-2">Infrastructure</div>
                <div className="text-sm font-medium text-gray-900">
                  {phase.details.infrastructure}
                </div>
                <div className="mt-2 text-xs text-green-600 font-medium">
                  ₹{phase.details.cost_per_vehicle}/vehicle/yr
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Database Sharding */}
        <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <Database className="w-7 h-7 text-cyan-600" />
          Database Sharding Strategy
        </h3>

        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 text-gray-600 font-medium">Component</th>
                  <th className="text-left py-3 px-4 text-gray-600 font-medium">Strategy</th>
                  <th className="text-right py-3 px-4 text-gray-600 font-medium">Shards</th>
                  <th className="text-left py-3 px-4 text-gray-600 font-medium">Rationale</th>
                </tr>
              </thead>
              <tbody>
                {shardingStrategy.map((item, idx) => (
                  <tr key={idx} className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">{item.component}</td>
                    <td className="py-3 px-4 text-gray-600">{item.strategy}</td>
                    <td className="py-3 px-4 text-right font-mono">{item.shards}</td>
                    <td className="py-3 px-4 text-gray-600">{item.rationale}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Cost Analysis */}
        <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <Cpu className="w-7 h-7 text-cyan-600" />
          Cost Analysis at Scale
        </h3>

        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 text-gray-600 font-medium">Scale</th>
                  <th className="text-right py-3 px-4 text-gray-600 font-medium">Infrastructure</th>
                  <th className="text-right py-3 px-4 text-gray-600 font-medium">ML Compute</th>
                  <th className="text-right py-3 px-4 text-gray-600 font-medium">Total Cost</th>
                  <th className="text-right py-3 px-4 text-gray-600 font-medium">Per Vehicle</th>
                </tr>
              </thead>
              <tbody>
                {costBreakdown.map((row, idx) => (
                  <tr key={idx} className="border-b border-gray-100">
                    <td className="py-3 px-4 font-medium text-gray-900">{row.scale}</td>
                    <td className="py-3 px-4 text-right text-gray-600">{row.infrastructure}</td>
                    <td className="py-3 px-4 text-right text-gray-600">{row.ml_compute}</td>
                    <td className="py-3 px-4 text-right font-medium text-gray-900">{row.total}</td>
                    <td className="py-3 px-4 text-right font-bold text-green-600">{row.per_vehicle}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-4 text-sm text-gray-600">
            * Costs calculated at ₹75/kWh for ML compute, ₹2L/server/year for infrastructure
          </p>
        </div>

        {/* ML Inference Scaling */}
        <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <Shield className="w-7 h-7 text-cyan-600" />
          ML Inference at Scale
        </h3>

        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-4">
              <div className="text-3xl font-bold text-gray-900 mb-2">{'<'}10ms</div>
              <div className="text-sm text-gray-600 mb-1">Battery SOH Prediction</div>
              <div className="text-xs text-gray-500">Per vehicle inference</div>
            </div>
            <div className="text-center p-4">
              <div className="text-3xl font-bold text-gray-900 mb-2">{'<'}5ms</div>
              <div className="text-sm text-gray-600 mb-1">Supply Chain Risk</div>
              <div className="text-xs text-gray-500">Per supplier query</div>
            </div>
            <div className="text-center p-4">
              <div className="text-3xl font-bold text-gray-900 mb-2">{'<'}8ms</div>
              <div className="text-sm text-gray-600 mb-1">Fleet Readiness</div>
              <div className="text-xs text-gray-500">Per vehicle analysis</div>
            </div>
          </div>
          
          <div className="mt-6 pt-6 border-t border-gray-200">
            <h4 className="font-bold text-gray-900 mb-3">Inference Optimization Strategy</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-start gap-3">
                <div className="bg-green-100 rounded-lg p-2">
                  <Shield className="w-5 h-5 text-green-600" />
                </div>
                <div>
                  <div className="font-medium text-gray-900">Model Quantization</div>
                  <div className="text-sm text-gray-600">INT8 quantization reduces inference time by 4x</div>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-blue-100 rounded-lg p-2">
                  <Server className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <div className="font-medium text-gray-900">Batch Processing</div>
                  <div className="text-sm text-gray-600">Process 100+ vehicles simultaneously</div>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-purple-100 rounded-lg p-2">
                  <Cloud className="w-5 h-5 text-purple-600" />
                </div>
                <div>
                  <div className="font-medium text-gray-900">Edge Caching</div>
                  <div className="text-sm text-gray-600">Pre-compute predictions for frequent queries</div>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="bg-orange-100 rounded-lg p-2">
                  <Activity className="w-5 h-5 text-orange-600" />
                </div>
                <div>
                  <div className="font-medium text-gray-900">Async Processing</div>
                  <div className="text-sm text-gray-600">Background ML jobs for bulk analysis</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}