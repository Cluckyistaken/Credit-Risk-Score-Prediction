import React from "react";
import { short } from "../../utils/formatters";

const SAMPLE = [
  { id: "a1", name: "Micro Traders", amount: 150000, purpose: "Working capital", status: "Pending" },
  { id: "a2", name: "FreshFarms", amount: 90000, purpose: "Equipment", status: "Approved" },
];

export default function ApplicationList() {
  return (
    <div className="bg-white rounded-xl p-4 shadow">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold">Applications</h3>
        <span className="text-sm text-slate-600">{SAMPLE.length} items</span>
      </div>

      <ul className="space-y-3">
        {SAMPLE.map((a) => (
          <li key={a.id} className="p-3 border rounded flex items-center justify-between">
            <div>
              <div className="font-medium">{a.name}</div>
              <div className="text-sm text-slate-600">{short(a.purpose, 40)}</div>
            </div>
            <div className="text-right">
              <div className="font-semibold">₹{a.amount.toLocaleString()}</div>
              <div className={`text-xs mt-1 ${a.status === "Approved" ? "text-green-600" : "text-yellow-600"}`}>{a.status}</div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
