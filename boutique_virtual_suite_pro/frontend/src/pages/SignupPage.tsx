import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiFetch } from "../api/client";
import { useAuthStore } from "../stores/authStore";

export default function SignupPage() {
  const nav = useNavigate();
  const setAuth = useAuthStore((s) => s.setAuth);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");

  async function submit() {
    setErr("");
    try {
      const res = await apiFetch<any>("/auth/signup", { method: "POST", body: JSON.stringify({ name, email, password, language: "en" }) });
      setAuth(res.token, res.user);
      nav("/");
    } catch (e: any) {
      setErr(e?.message || "Failed");
    }
  }

  return (
    <div className="max-w-md">
      <div className="glass rounded-2xl border border-base-300 p-6 space-y-3">
        <div className="text-2xl font-extrabold">Sign up</div>
        {err ? <div className="alert alert-error">{err}</div> : null}
        <input className="input input-bordered w-full" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
        <input className="input input-bordered w-full" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="input input-bordered w-full" placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button className="btn btn-primary w-full" onClick={submit}>
          Create account
        </button>
        <div className="text-sm opacity-70">
          Already?{" "}
          <Link className="link" to="/login">
            Login
          </Link>
        </div>
      </div>
    </div>
  );
}

