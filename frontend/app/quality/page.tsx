'use client';

import React from 'react';
import QualityDashboard from '@/components/QualityDashboard';

export default function QualityPage() {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-950 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <QualityDashboard />
      </div>
    </div>
  );
}
