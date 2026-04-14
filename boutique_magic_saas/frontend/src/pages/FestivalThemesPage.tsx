import { useEffect, useState } from "react";
import { apiGet } from "../api/client";

type Festival = { id: number; name: string; start_date: string; end_date: string; theme_color: string; banner_text: string };

export default function FestivalThemesPage() {
  const [active, setActive] = useState<Festival | null>(null);
  const [all, setAll] = useState<Festival[]>([]);

  useEffect(() => {
    apiGet<{ ok: true; active: Festival | null; all: Festival[] }>("/theme/festival")
      .then((r) => {
        setActive(r.active);
        setAll(r.all || []);
        if (r.active?.theme_color) {
          document.documentElement.style.setProperty("--magic-color", r.active.theme_color);
        }
      })
      .catch(() => {});
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-3 md:px-6 py-6 space-y-6">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">Festival Themes</div>
        <div className="mt-2 text-sm opacity-70">Auto theme based on date.</div>
      </div>

      {active ? (
        <div className="glass rounded-2xl border border-base-300 p-6 neon">
          <div className="text-xs opacity-70 uppercase tracking-wider">Active</div>
          <div className="mt-1 text-2xl font-extrabold">{active.name}</div>
          <div className="mt-2 text-sm opacity-70">{active.banner_text}</div>
          <div className="mt-3 badge badge-primary">{active.theme_color}</div>
        </div>
      ) : (
        <div className="alert">No active festival today.</div>
      )}

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {all.map((f) => (
          <div key={f.id} className="rounded-2xl border border-base-300 bg-base-100 p-5">
            <div className="font-bold">{f.name}</div>
            <div className="mt-2 text-sm opacity-70">{f.start_date} → {f.end_date}</div>
            <div className="mt-3 flex items-center gap-2">
              <span className="w-3 h-3 rounded-full" style={{ background: f.theme_color }} />
              <span className="text-xs opacity-70">{f.theme_color}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

