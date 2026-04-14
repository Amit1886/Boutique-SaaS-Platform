import { useEffect, useState } from "react";
import { useAuthStore } from "../stores/authStore";
import { useFavoritesStore } from "../stores/favoritesStore";
import { useTrylistStore } from "../stores/trylistStore";
import { apiFetch } from "../api/client";

export default function DashboardPage() {
  const user = useAuthStore((s) => s.user);
  const token = useAuthStore((s) => s.token);
  const favRows = useFavoritesStore((s) => s.rows);
  const tryItems = useTrylistStore((s) => s.items);
  const [personality, setPersonality] = useState<string>("");

  useEffect(() => {
    if (!token) return;
    apiFetch<{ ok: true; personality: string }>("/style/personality", { method: "GET" })
      .then((r) => setPersonality(r.personality || ""))
      .catch(() => {});
  }, [token]);

  return (
    <div className="space-y-5">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">User Dashboard</div>
        <div className="mt-2 text-sm opacity-70">Progress, favorites, trylist, and style profile.</div>
      </div>
      {!token ? (
        <div className="alert alert-warning">Login to view your dashboard.</div>
      ) : (
        <div className="grid lg:grid-cols-3 gap-4 items-start">
          <div className="rounded-2xl border border-base-300 bg-base-100 p-5">
            <div className="text-xs uppercase tracking-wider opacity-60">Account</div>
            <div className="mt-2 font-semibold">{user?.email}</div>
            <div className="text-sm opacity-70">{user?.name}</div>
          </div>
          <div className="rounded-2xl border border-base-300 bg-base-100 p-5">
            <div className="text-xs uppercase tracking-wider opacity-60">Favorites</div>
            <div className="mt-2 text-3xl font-extrabold" style={{ color: "var(--bvp-primary)" }}>
              {favRows.length}
            </div>
            <div className="text-sm opacity-70">Saved items</div>
          </div>
          <div className="rounded-2xl border border-base-300 bg-base-100 p-5">
            <div className="text-xs uppercase tracking-wider opacity-60">Trylist</div>
            <div className="mt-2 text-3xl font-extrabold" style={{ color: "var(--bvp-primary)" }}>
              {tryItems.length}
            </div>
            <div className="text-sm opacity-70">Queued looks</div>
          </div>
          <div className="lg:col-span-3 rounded-2xl border border-base-300 bg-base-100 p-5">
            <div className="text-xs uppercase tracking-wider opacity-60">Style Personality</div>
            <div className="mt-2 text-xl font-extrabold">{personality || "Not taken yet"}</div>
            <div className="mt-1 text-sm opacity-70">Take the style test to personalize your feed.</div>
          </div>
        </div>
      )}
    </div>
  );
}

