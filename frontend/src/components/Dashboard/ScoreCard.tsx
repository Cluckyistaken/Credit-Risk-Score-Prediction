import React from "react";
import { formatCurrency } from "../../utils/formatters";

export default function ScoreCard() {
  const sample = { score: 72, limit: 250000 };

  return (
    <div className="bg-white rounded-xl p-6 shadow">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-medium">Credit score</h3>
          <p className="text-sm text-slate-600">Estimated risk score for the selected application</p>
        </div>
        <div className="text-right">
          <div className="text-3xl font-bold text-primary">{sample.score}</div>
          <div className="text-sm text-slate-600">score (0 - 100)</div>
        </div>
      </div>

      <div className="mt-5 flex items-center gap-4">
        <div className="flex-1 h-2 bg-slate-200 rounded overflow-hidden">
          <div style={{ width: `${sample.score}%` }} className="h-full bg-gradient-to-r from-primary to-accent"></div>
        </div>
        <div className="text-sm text-slate-700">{formatCurrency(sample.limit)} limit</div>
      </div>
    </div>
  );
}
