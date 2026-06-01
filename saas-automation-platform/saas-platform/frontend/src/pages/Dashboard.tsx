import { useEffect, useState } from "react";
import { analyticsApi, workflowApi } from "../utils/api";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

interface Stats {
  total_workflows: number;
  total_runs: number;
  success_rate: number;
  daily_runs: { _id: string; count: number }[];
}

export default function Dashboard({ user }: { user: any }) {
  const [stats, setStats] = useState<Stats | null>(null);
  const [workflows, setWorkflows] = useState<any[]>([]);

  useEffect(() => {
    analyticsApi.dashboard().then((r) => setStats(r.data));
    workflowApi.list().then((r) => setWorkflows(r.data));
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "system-ui, sans-serif", maxWidth: 1100, margin: "0 auto" }}>
      <h1 style={{ fontSize: "1.8rem", marginBottom: "0.5rem" }}>
        Welcome back, {user?.full_name} 👋
      </h1>
      <p style={{ color: "#64748b", marginBottom: "2rem" }}>
        Tenant: <strong>{user?.tenant_id}</strong> · Role: <strong>{user?.role}</strong>
      </p>

      {/* KPI Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "1rem", marginBottom: "2rem" }}>
        {[
          { label: "Total Workflows", value: stats?.total_workflows ?? "—" },
          { label: "Total Runs", value: stats?.total_runs ?? "—" },
          { label: "Success Rate", value: stats ? `${stats.success_rate}%` : "—" },
        ].map((kpi) => (
          <div key={kpi.label} style={{ background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: 12, padding: "1.5rem" }}>
            <div style={{ fontSize: "2rem", fontWeight: 700 }}>{kpi.value}</div>
            <div style={{ color: "#64748b", marginTop: "0.25rem" }}>{kpi.label}</div>
          </div>
        ))}
      </div>

      {/* Chart */}
      {stats?.daily_runs && stats.daily_runs.length > 0 && (
        <div style={{ background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: 12, padding: "1.5rem", marginBottom: "2rem" }}>
          <h2 style={{ fontSize: "1rem", marginBottom: "1rem" }}>Workflow Runs – Last 7 Days</h2>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={stats.daily_runs}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="_id" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="count" stroke="#6366f1" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Workflow List */}
      <div style={{ background: "#f8fafc", border: "1px solid #e2e8f0", borderRadius: 12, padding: "1.5rem" }}>
        <h2 style={{ fontSize: "1rem", marginBottom: "1rem" }}>Your Workflows</h2>
        {workflows.length === 0 ? (
          <p style={{ color: "#94a3b8" }}>No workflows yet. Create your first workflow via the API.</p>
        ) : (
          workflows.map((wf) => (
            <div key={wf.id} style={{ display: "flex", justifyContent: "space-between", padding: "0.75rem 0", borderBottom: "1px solid #e2e8f0" }}>
              <div>
                <strong>{wf.name}</strong>
                <div style={{ fontSize: "0.85rem", color: "#64748b" }}>{wf.description}</div>
              </div>
              <div style={{ textAlign: "right", fontSize: "0.85rem", color: "#64748b" }}>
                <div>Runs: {wf.run_count}</div>
                <div style={{ color: wf.is_active ? "#22c55e" : "#ef4444" }}>
                  {wf.is_active ? "Active" : "Inactive"}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
