import React, { useState } from "react";

export default function ApplicationForm() {
  const [name, setName] = useState("");
  const [amount, setAmount] = useState<number | "">("");
  const [purpose, setPurpose] = useState("");
  const [msg, setMsg] = useState<string | null>(null);

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    // pretend submit
    setMsg("Application submitted — sample flow (no backend configured).");
    setName("");
    setAmount("");
    setPurpose("");
    setTimeout(()=>setMsg(null), 4000);
  };

  return (
    <form onSubmit={submit} className="bg-white rounded-xl p-4 shadow">
      <h3 className="font-semibold mb-3">New application</h3>

      <label className="block text-sm">Applicant name</label>
      <input value={name} onChange={(e)=>setName(e.target.value)} required className="w-full p-2 border rounded mb-2"/>

      <label className="block text-sm">Amount (₹)</label>
      <input type="number" value={amount} onChange={(e)=>setAmount(e.target.value === "" ? "" : Number(e.target.value))} required className="w-full p-2 border rounded mb-2"/>

      <label className="block text-sm">Purpose</label>
      <input value={purpose} onChange={(e)=>setPurpose(e.target.value)} className="w-full p-2 border rounded mb-3"/>

      <button className="w-full bg-primary text-white py-2 rounded">Submit application</button>
      {msg && <div className="text-sm text-green-600 mt-3">{msg}</div>}
    </form>
  );
}
