'use client';

import React, { useState } from 'react';
import { Download, FileText, BarChart3, AlertCircle } from 'lucide-react';

interface ReportOption {
  type: string;
  description: string;
  icon: React.ReactNode;
}

interface ExportFormat {
  format: string;
  label: string;
  description: string;
}

const ReportsExport: React.FC = () => {
  const [selectedReport, setSelectedReport] = useState<string>('executive_summary');
  const [selectedFormat, setSelectedFormat] = useState<string>('json');
  const [dateRange, setDateRange] = useState<number>(30);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const reportOptions: ReportOption[] = [
    {
      type: 'executive_summary',
      description: '1-page executive overview with key metrics',
      icon: <FileText className="w-5 h-5" />,
    },
    {
      type: 'technical_detailed',
      description: 'Comprehensive technical analysis report',
      icon: <BarChart3 className="w-5 h-5" />,
    },
    {
      type: 'compliance',
      description: 'Regulatory compliance and audit status',
      icon: <AlertCircle className="w-5 h-5" />,
    },
    {
      type: 'financial_roi',
      description: 'ROI analysis and financial projections',
      icon: <FileText className="w-5 h-5" />,
    },
    {
      type: 'supply_chain_risk',
      description: 'Supply chain risk assessment',
      icon: <AlertCircle className="w-5 h-5" />,
    },
    {
      type: 'fleet_health',
      description: 'Fleet health and maintenance analysis',
      icon: <BarChart3 className="w-5 h-5" />,
    },
  ];

  const exportFormats: ExportFormat[] = [
    {
      format: 'json',
      label: 'JSON',
      description: 'Machine-readable format for integration',
    },
    {
      format: 'csv',
      label: 'CSV',
      description: 'Spreadsheet format for Excel',
    },
    {
      format: 'pdf',
      label: 'PDF',
      description: 'Professional printable format',
    },
    {
      format: 'xlsx',
      label: 'Excel',
      description: 'Excel workbook with multiple sheets',
    },
  ];

  const handleGenerateReport = async () => {
    setIsGenerating(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch(
        `/api/v1/reports/generate/${selectedReport}?format=${selectedFormat}&days=${dateRange}`,
        {
          method: 'POST',
        }
      );

      if (!response.ok) {
        throw new Error('Failed to generate report');
      }

      const data = await response.json();

      // Download the file
      const blob = new Blob(
        [selectedFormat === 'json' ? JSON.stringify(data.data, null, 2) : data.data],
        { type: selectedFormat === 'json' ? 'application/json' : 'text/csv' }
      );

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = data.filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      setSuccess(`Report generated and downloaded: ${data.filename}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExportData = async (exportType: 'vehicles' | 'supply-chain') => {
    setIsExporting(true);
    setError(null);
    setSuccess(null);

    try {
      const endpoint =
        exportType === 'vehicles'
          ? `/api/v1/reports/export/vehicles?format=${selectedFormat}`
          : `/api/v1/reports/export/supply-chain?format=${selectedFormat}`;

      const response = await fetch(endpoint, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Failed to export data');
      }

      const data = await response.json();

      // Download the file
      const blob = new Blob(
        [selectedFormat === 'json' ? JSON.stringify(data.data, null, 2) : data.data],
        { type: selectedFormat === 'json' ? 'application/json' : 'text/csv' }
      );

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = data.filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      setSuccess(`Data exported: ${data.filename} (${data.record_count} records)`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">Reports & Export</h1>
          <p className="text-slate-300">Generate and export comprehensive data reports</p>
        </div>

        {/* Alerts */}
        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/50 rounded-lg">
            <p className="text-red-200">{error}</p>
          </div>
        )}

        {success && (
          <div className="mb-6 p-4 bg-green-500/10 border border-green-500/50 rounded-lg">
            <p className="text-green-200">{success}</p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Export Settings */}
          <div className="lg:col-span-1">
            <div className="bg-slate-800 rounded-lg border border-slate-700 p-6 space-y-6">
              <div>
                <label className="block text-sm font-semibold text-white mb-3">
                  Export Format
                </label>
                <div className="space-y-2">
                  {exportFormats.map((fmt) => (
                    <label key={fmt.format} className="flex items-center p-3 cursor-pointer hover:bg-slate-700 rounded">
                      <input
                        type="radio"
                        name="format"
                        value={fmt.format}
                        checked={selectedFormat === fmt.format}
                        onChange={(e) => setSelectedFormat(e.target.value)}
                        className="mr-3"
                      />
                      <div>
                        <div className="text-sm font-medium text-white">{fmt.label}</div>
                        <div className="text-xs text-slate-400">{fmt.description}</div>
                      </div>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-white mb-3">
                  Date Range (Days)
                </label>
                <input
                  type="number"
                  min="1"
                  max="365"
                  value={dateRange}
                  onChange={(e) => setDateRange(parseInt(e.target.value))}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded text-white"
                />
                <p className="text-xs text-slate-400 mt-1">
                  Reports will include data from the last {dateRange} days
                </p>
              </div>
            </div>
          </div>

          {/* Reports Section */}
          <div className="lg:col-span-2">
            <h2 className="text-xl font-bold text-white mb-4">Available Reports</h2>

            <div className="space-y-3">
              {reportOptions.map((report) => (
                <div
                  key={report.type}
                  onClick={() => setSelectedReport(report.type)}
                  className={`p-4 rounded-lg border-2 cursor-pointer transition ${
                    selectedReport === report.type
                      ? 'border-blue-500 bg-blue-500/10'
                      : 'border-slate-700 bg-slate-800 hover:border-slate-600'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div className="text-blue-400 mt-1">{report.icon}</div>
                    <div className="flex-1">
                      <h3 className="font-semibold text-white capitalize">
                        {report.type.replace(/_/g, ' ')}
                      </h3>
                      <p className="text-sm text-slate-300">{report.description}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <button
              onClick={handleGenerateReport}
              disabled={isGenerating}
              className="w-full mt-6 px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white font-semibold rounded-lg flex items-center justify-center gap-2 transition"
            >
              <Download className="w-5 h-5" />
              {isGenerating ? 'Generating...' : 'Generate Report'}
            </button>
          </div>
        </div>

        {/* Data Export Section */}
        <div className="mt-12">
          <h2 className="text-xl font-bold text-white mb-4">Export Data</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button
              onClick={() => handleExportData('vehicles')}
              disabled={isExporting}
              className="p-6 bg-slate-800 border border-slate-700 rounded-lg hover:border-slate-600 transition text-left"
            >
              <div className="flex items-start gap-3">
                <BarChart3 className="w-6 h-6 text-green-400 mt-1" />
                <div className="flex-1">
                  <h3 className="font-semibold text-white">Export Fleet Data</h3>
                  <p className="text-sm text-slate-400 mt-1">
                    Download vehicle information, status, and health metrics
                  </p>
                  <p className="text-xs text-slate-500 mt-2">156 vehicles</p>
                </div>
              </div>
              <div className="mt-4 inline-flex items-center gap-2 px-3 py-2 bg-green-600/20 text-green-400 rounded text-sm">
                <Download className="w-4 h-4" />
                {isExporting ? 'Exporting...' : 'Export'}
              </div>
            </button>

            <button
              onClick={() => handleExportData('supply-chain')}
              disabled={isExporting}
              className="p-6 bg-slate-800 border border-slate-700 rounded-lg hover:border-slate-600 transition text-left"
            >
              <div className="flex items-start gap-3">
                <AlertCircle className="w-6 h-6 text-orange-400 mt-1" />
                <div className="flex-1">
                  <h3 className="font-semibold text-white">Export Supply Chain Data</h3>
                  <p className="text-sm text-slate-400 mt-1">
                    Download supplier information, risk scores, and lead times
                  </p>
                  <p className="text-xs text-slate-500 mt-2">28 suppliers</p>
                </div>
              </div>
              <div className="mt-4 inline-flex items-center gap-2 px-3 py-2 bg-orange-600/20 text-orange-400 rounded text-sm">
                <Download className="w-4 h-4" />
                {isExporting ? 'Exporting...' : 'Export'}
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ReportsExport;
