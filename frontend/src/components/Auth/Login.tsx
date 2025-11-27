import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    setLoading(true);
    try {
      await login(email, password);
      nav("/");
    } catch (e: any) {
      setErr(e.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <form onSubmit={submit} className="w-full max-w-md bg-white p-6 rounded-xl shadow">
        <h2 className="text-2xl font-semibold text-primary mb-4">Welcome back</h2>
        {err && <div className="text-sm text-red-600 mb-3">{err}</div>}

        <label className="block mb-2 text-sm">Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} required className="w-full p-2 border rounded mb-3"/>

        <label className="block mb-2 text-sm">Password</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required className="w-full p-2 border rounded mb-4"/>

        <button disabled={loading} className="w-full bg-primary text-white py-2 rounded mb-3">
          {loading ? "Logging in…" : "Login"}
        </button>

        <div className="flex justify-between text-sm">
          <Link to="/forgot" className="text-slate-600">Forgot?</Link>
          <Link to="/register" className="text-primary">Create account</Link>
        </div>
      </form>
    </div>
  );
}
