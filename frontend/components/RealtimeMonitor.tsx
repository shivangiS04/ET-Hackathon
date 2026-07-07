'use client';

export default function RealtimeMonitor() {
  return (
    <div className="p-6 bg-white rounded-lg shadow">
      <h3 className="text-lg font-bold mb-4">Real-time Monitor</h3>
      <div className="space-y-2">
        <div className="flex justify-between p-2 bg-gray-50 rounded"><span>Battery</span><span>✅</span></div>
        <div className="flex justify-between p-2 bg-gray-50 rounded"><span>Supply Chain</span><span>⚠️</span></div>
        <div className="flex justify-between p-2 bg-gray-50 rounded"><span>Fleet</span><span>✅</span></div>
      </div>
    </div>
  );
}
