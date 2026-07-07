'use client';

import React from 'react';

const AnomalyAlert: React.FC = () => {
  return (
    <div className="p-6 bg-white rounded-lg shadow">
      <h3 className="text-lg font-bold mb-4">Anomaly Detection</h3>
      <p className="text-sm text-gray-700">LSTM + Isolation Forest</p>
    </div>
  );
};

export default AnomalyAlert;
