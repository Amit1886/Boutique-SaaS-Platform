import { useEffect } from "react";
import { useMoodStore } from "../stores/moodStore";
import { useAuthStore } from "../stores/authStore";

export default function MoodboardPage() {
  const moods = useMoodStore((s) => s.moods);
  const activeKey = useMoodStore((s) => s.activeKey);
  const loadMoods = useMoodStore((s) => s.loadMoods);
  const applyMood = useMoodStore((s) => s.applyMood);
  const token = useAuthStore((s) => s.token);

  useEffect(() => {
    loadMoods().catch(() => {});
  }, [loadMoods]);

  return (
    <div className="space-y-6 fade-in">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">Smart Moodboard</div>
        <div className="mt-2 opacity-70 text-sm">Select a mood and the UI theme + recommendations adapt instantly.</div>
      </div>

      {!token ? <div className="alert alert-warning">Login to save mood on server (UI still changes locally).</div> : null}

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {moods.map((m) => (
          <button
            key={m.key}
            className={`glass rounded-2xl border p-5 text-left transition ${
              activeKey === m.key ? "border-primary" : "border-base-300 hover:border-primary/50"
            }`}
            onClick={() => applyMood(m.key).catch(() => {})}
          >
            <div className="text-xs opacity-70 uppercase tracking-wider">Mood</div>
            <div className="mt-1 text-xl font-bold">{m.name_en}</div>
            <div className="mt-2 text-sm opacity-70">{m.banner}</div>
            <div className="mt-4 flex items-center gap-2">
              <span className="w-3 h-3 rounded-full" style={{ background: m.theme_color }} />
              <span className="text-xs opacity-70">{m.theme_color}</span>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

