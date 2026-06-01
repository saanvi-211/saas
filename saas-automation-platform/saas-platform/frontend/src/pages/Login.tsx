import { useState } from "react";

export default function Login({ onLogin }: { onLogin: (e: string, p: string) => Promise<any> }) {
  const [email, setEmail] = useState("admin@tenant1.com");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await onLogin(email, password);
    } catch {
      setError("Invalid credentials. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "#f1f5f9" }}>
      <div style={{ background: "#fff", padding: "2.5rem", borderRadius: 16, boxShadow: "0 4px 24px rgba(0,0,0,0.08)", width: 360 }}>
        <h1 style={{ fontSize: "1.5rem", marginBottom: "0.5rem" }}>SaaS Platform</h1>
        <p style={{ color: "#64748b", marginBottom: "2rem" }}>Sign in to your account</p>
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: "1rem" }}>
            <label style={{ display: "block", marginBottom: 4, fontSize: "0.9rem", fontWeight: 500 }}>Email</label>
            <input value={email} onChange={(e) => setEmail(e.target.value)}
              style={{ width: "100%", padding: "0.65rem", border: "1px solid #e2e8f0", borderRadius: 8, fontSize: "0.95rem", boxSizing: "border-box" }}
              type="email" required />
          </div>
          <div style={{ marginBottom: "1.5rem" }}>
            <label style={{ display: "block", marginBottom: 4, fontSize: "0.9rem", fontWeight: 500 }}>Password</label>
            <input value={password} onChange={(e) => setPassword(e.target.value)}
              style={{ width: "100%", padding: "0.65rem", border: "1px solid #e2e8f0", borderRadius: 8, fontSize: "0.95rem", boxSizing: "border-box" }}
              type="password" required />
          </div>
          {error && <p style={{ color: "#ef4444", fontSize: "0.85rem", marginBottom: "1rem" }}>{error}</p>}
          <button type="submit" disabled={loading}
            style={{ width: "100%", padding: "0.75rem", background: "#6366f1", color: "#fff", border: "none", borderRadius: 8, fontWeight: 600, fontSize: "1rem", cursor: "pointer" }}>
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
      </div>
    </div>
  );
}
