import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import Login from "./components/Auth/Login";
import Register from "./components/Auth/Register";
import ForgotPassword from "./components/Auth/ForgotPassword";
import ScoreCard from "./components/Dashboard/ScoreCard";
import ApplicationForm from "./components/Dashboard/ApplicationForm";
import ApplicationList from "./components/Dashboard/ApplicationList";
import ReviewApplications from "./components/Admin/ReviewApplications";
import AnalyticsDashboard from "./components/Admin/AnalyticsDashboard";
import { useAuth } from "./context/AuthContext";

const HomeShell: React.FC = () => {
  const { user, logout } = useAuth();
  return (
    <div className="min-h-screen bg-gradient-to-tr from-white to-card">
      <header className="flex items-center justify-between p-4 max-w-6xl mx-auto">
        <h1 className="text-2xl font-bold text-primary">CreditRisk — Dashboard</h1>
        <nav className="flex gap-3 items-center">
          <Link className="text-sm px-3 py-2 rounded-md hover:bg-slate-100" to="/">Home</Link>
          <Link className="text-sm px-3 py-2 rounded-md hover:bg-slate-100" to="/applications">Applications</Link>
          <Link className="text-sm px-3 py-2 rounded-md hover:bg-slate-100" to="/analytics">Analytics</Link>
          {user ? (
            <>
              <span className="text-sm text-slate-600">Hi, {user.name}</span>
              <button onClick={logout} className="text-sm bg-primary text-white px-3 py-1 rounded">Logout</button>
            </>
          ) : (
            <Link className="text-sm bg-primary text-white px-3 py-1 rounded" to="/login">Login</Link>
          )}
        </nav>
      </header>

      <main className="max-w-6xl mx-auto p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        <section className="md:col-span-2 space-y-6">
          <ScoreCard />
          <ApplicationList />
        </section>

        <aside className="space-y-6">
          <ApplicationForm />
          <div className="bg-white rounded-xl p-4 shadow">
            <h3 className="font-semibold mb-2">Admin</h3>
            <Link to="/admin/review" className="block text-sm text-primary underline">Review applications</Link>
          </div>
        </aside>
      </main>
    </div>
  );
};

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomeShell />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot" element={<ForgotPassword />} />
      <Route path="/admin/review" element={<ReviewApplications />} />
      <Route path="/analytics" element={<AnalyticsDashboard />} />
      <Route path="/applications" element={<ApplicationList />} />
    </Routes>
  );
}
