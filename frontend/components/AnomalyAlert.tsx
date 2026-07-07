'use client';

export default function AnomalyAlert() {
  return (
    <div className="p-6 bg-white rounded-lg shadow">
      <h3 className="text-lg font-bold mb-4">Anomaly Detection</h3>
      <div className="p-4 bg-red-50 rounded">
        <p className="text-sm text-gray-700">Algorithm: LSTM + Isolation Forest</p>
      </div>
    </div>
  );
}
