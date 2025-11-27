import React from "react";

export default function AnalyticsDashboard() {
  // small, static analytics snapshot — replace with charts when backend ready
  const stats = {
    totalApps: 152,
    avgScore: 68,
    totalExposure: 8200000
  };

  return (
    <div className="min-h-screen p-6 max-w-5xl mx-auto">
      <h2 className="text-2xl font-semibold text-primary mb-6">Analytics</h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-xl shadow text-center">
          <div className="text-sm text-slate-600">Applications</div>
          <div className="text-2xl font-bold mt-2">{stats.totalApps}</div>
        </div>

        <div className="bg-white p-4 rounded-xl shadow text-center">
          <div className="text-sm text-slate-600">Average credit score</div>
          <div className="text-2xl font-bold mt-2">{stats.avgScore}</div>
        </div>

        <div className="bg-white p-4 rounded-xl shadow text-center">
          <div className="text-sm text-slate-600">Total exposure</div>
          <div className="text-2xl font-bold mt-2">₹{stats.totalExposure.toLocaleString()}</div>
        </div>
      </div>

      <div className="mt-6 bg-white p-4 rounded-xl shadow">
        <h4 className="font-medium mb-2">Notes</h4>
        <p className="text-sm text-slate-600">Integrate charts (Recharts / Chart.js) later for time-series and breakdowns.</p>
      </div>
    </div>
  );
}
