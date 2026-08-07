"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

export default function RegisterPage() {
  const { register } = useAuth();
  const router = useRouter();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await register(email, password, firstName, lastName);
      router.push("/");
    } catch (err: any) {
      console.error("Register error:", err);
      let detail = "Registration failed.";
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
        <h1>Create account</h1>
        <form onSubmit={handleSubmit}>
          <label>First name</label>
          <input value={firstName} onChange={(e) => setFirstName(e.target.value)} required />

          <label>Last name</label>
          <input value={lastName} onChange={(e) => setLastName(e.target.value)} required />

          <label>Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />

          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required minLength={8} />
          <p className="hint">At least 8 characters</p>

          {error && <p className="auth-error">{error}</p>}

          <button type="submit" disabled={loading}>
            {loading ? "Creating account..." : "Create your Amazon Clone account"}
          </button>
        </form>
        <p className="auth-switch">
          Already have an account? <Link href="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
