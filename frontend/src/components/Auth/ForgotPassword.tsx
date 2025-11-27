import React, { useState } from "react";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);

  const handle = (e: React.FormEvent) => {
    e.preventDefault();
    // pretend to send
    setTimeout(() => setSent(true), 500);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <form onSubmit={handle} className="w-full max-w-md bg-white p-6 rounded-xl shadow text-center">
        <h2 className="text-2xl font-semibold text-primary mb-4">Reset password</h2>
        {sent ? (
          <div className="text-slate-700">If that account exists, we sent reset steps to {email}.</div>
        ) : (
          <>
            <input placeholder="Your email" value={email} onChange={(e)=>setEmail(e.target.value)} required className="w-full p-2 border rounded mb-4" />
            <button type="submit" className="w-full bg-primary text-white py-2 rounded">Send reset link</button>
          </>
        )}
      </form>
    </div>
  );
}
