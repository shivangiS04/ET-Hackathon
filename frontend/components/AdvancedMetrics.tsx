'use client';

export default function AdvancedMetrics() {
  return (
    <div className="p-6 bg-white rounded-lg shadow">
      <h3 className="text-lg font-bold mb-4">Advanced Metrics</h3>
      <div className="grid grid-cols-4 gap-4">
        <div className="p-4 bg-blue-50 rounded"><div className="text-3xl font-bold">2.1%</div></div>
        <div className="p-4 bg-green-50 rounded"><div className="text-3xl font-bold">91.2%</div></div>
        <div className="p-4 bg-orange-50 rounded"><div className="text-3xl font-bold">3.2%</div></div>
        <div className="p-4 bg-purple-50 rounded"><div className="text-3xl font-bold">&lt;500ms</div></div>
      </div>
    </div>
  );
}
