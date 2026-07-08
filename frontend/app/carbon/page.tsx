'use client';

import React from 'react';
import CarbonDashboard from '@/components/CarbonDashboard';

export default function CarbonPage() {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-950 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <CarbonDashboard />
      </div>
    </div>
  );
}
