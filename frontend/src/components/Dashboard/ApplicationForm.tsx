import React, { useState } from "react";

export default function ApplicationForm() {
  const [name, setName] = useState("");
  const [amount, setAmount] = useState<number | "">("");
  const [purpose, setPurpose] = useState("");
  const [age, setAge] = useState<number | "">("");
  const [duration, setDuration] = useState<number | "">("");
  const [msg, setMsg] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMsg(null);

    try {
      const payload = {
        "Credit amount": Number(amount),
        "Purpose": purpose,
        "Age": Number(age),
        "Duration": Number(duration)
      };

      const res = await fetch("/api/ml/score", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (res.ok) {
        const resultText = data.prediction === 1 ? "High Risk (Bad)" : "Low Risk (Good)";
        setMsg(`Result: ${resultText} (Score: ${data.risk_score?.toFixed(4)})`);
      } else {
        setMsg(`Error: ${data.error || "Unknown error"}`);
      }
    } catch (err) {
      setMsg("Error connecting to server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={submit} className="bg-white rounded-xl p-4 shadow">
      <h3 className="font-semibold mb-3">New application</h3>

      <label className="block text-sm">Applicant name</label>
      <input name="name" value={name} onChange={(e) => setName(e.target.value)} required className="w-full p-2 border rounded mb-2" />

      <label className="block text-sm">Age</label>
      <input name="age" type="number" value={age} onChange={(e) => setAge(e.target.value === "" ? "" : Number(e.target.value))} required className="w-full p-2 border rounded mb-2" />

      <label className="block text-sm">Amount (₹)</label>
      <input name="amount" type="number" value={amount} onChange={(e) => setAmount(e.target.value === "" ? "" : Number(e.target.value))} required className="w-full p-2 border rounded mb-2" />

      <label className="block text-sm">Duration (months)</label>
      <input name="duration" type="number" value={duration} onChange={(e) => setDuration(e.target.value === "" ? "" : Number(e.target.value))} required className="w-full p-2 border rounded mb-2" />

      <label className="block text-sm">Purpose</label>
      <input name="purpose" value={purpose} onChange={(e) => setPurpose(e.target.value)} className="w-full p-2 border rounded mb-3" />

      <button disabled={loading} className="w-full bg-primary text-white py-2 rounded disabled:opacity-50">
        {loading ? "Analyzing..." : "Submit application"}
      </button>
      {msg && <div className="text-sm font-semibold mt-3 p-2 bg-slate-100 rounded">{msg}</div>}
    </form>
  );
}
