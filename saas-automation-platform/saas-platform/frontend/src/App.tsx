import { useAuth } from "./hooks/useAuth";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

export default function App() {
  const { user, loading, login, logout } = useAuth();

  if (loading) return <div style={{ padding: "2rem" }}>Loading...</div>;

  if (!user) return <Login onLogin={login} />;

  return (
    <div>
      <nav style={{ background: "#1e293b", color: "#fff", padding: "1rem 2rem", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontWeight: 700 }}>⚡ SaaS Platform</span>
        <button onClick={logout} style={{ background: "transparent", color: "#94a3b8", border: "1px solid #334155", borderRadius: 6, padding: "0.4rem 0.9rem", cursor: "pointer" }}>
          Logout
        </button>
      </nav>
      <Dashboard user={user} />
    </div>
  );
}
