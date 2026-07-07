'use client';

export default function PredictiveAlertCenter() {
  return (
    <div className="p-6 bg-white rounded-lg shadow">
      <h3 className="text-lg font-bold mb-4">Predictive Alerts</h3>
      <div className="p-4 bg-blue-50 rounded">
        <p className="text-sm text-gray-700">90-day forecast (RMSE &lt;3%)</p>
      </div>
    </div>
  );
}
