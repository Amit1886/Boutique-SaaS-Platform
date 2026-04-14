import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";
import { useAuthStore } from "../stores/authStore";

export default function ResultsPage() {
  const token = useAuthStore((s) => s.token);
  const [personality, setPersonality] = useState(sessionStorage.getItem("bvp.personality.latest") || "");

  useEffect(() => {
    if (!token) return;
    apiFetch<{ ok: true; personality: string }>("/style/personality", { method: "GET" })
      .then((r) => setPersonality(r.personality))
      .catch(() => {});
  }, [token]);

  return (
    <div className="space-y-5 fade-in">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">Results</div>
        <div className="mt-2 text-sm opacity-70">Your style profile will personalize the feed.</div>
      </div>
      <div className="rounded-2xl border border-base-300 bg-base-100 p-6">
        <div className="text-sm opacity-70">Personality</div>
        <div className="mt-1 text-2xl font-extrabold" style={{ color: "var(--bvp-primary)" }}>
          {personality || "—"}
        </div>
      </div>
    </div>
  );
}

