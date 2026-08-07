"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password);
      router.push("/");
    } catch (err: any) {
      console.error("Login error:", err);
      let detail = "Login failed.";
      if (err?.response) {
        detail = `Server error ${err.response.status}: ${JSON.stringify(err.response.data)}`;
      } else if (err?.request) {
        detail = `Network error: request never got a response (likely CORS or the server is unreachable). ${err.message}`;
      } else {
        detail = `Error: ${err.message}`;
      }
      setError(detail);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <Link href="/" className="auth-logo">amazon</Link>
      <div className="auth-card">
        <h1>Sign in</h1>
        <form onSubmit={handleSubmit}>
          <label>Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />

          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />

          {error && <p className="auth-error">{error}</p>}

          <button type="submit" disabled={loading}>
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </form>
        <p className="auth-switch">
          New to Amazon Clone? <Link href="/register">Create your account</Link>
        </p>
      </div>
    </div>
  );
}
