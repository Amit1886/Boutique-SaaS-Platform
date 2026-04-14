import { useAppStore, type MoodKey } from "../store/useAppStore";

const moods: { key: MoodKey; label: string; color: string }[] = [
  { key: "festive", label: "Festive", color: "#db2777" },
  { key: "wedding", label: "Wedding", color: "#ef4444" },
  { key: "bridal", label: "Bridal", color: "#f97316" },
  { key: "party", label: "Party", color: "#7c3aed" },
  { key: "traditional", label: "Traditional", color: "#f59e0b" }
];

export default function Moodboard() {
  const mood = useAppStore((s) => s.mood);
  const setMood = useAppStore((s) => s.setMood);
  return (
    <div className="grid sm:grid-cols-2 lg:grid-cols-5 gap-3">
      {moods.map((m) => (
        <button
          key={m.key}
          className={`glass rounded-2xl border p-4 text-left transition ${mood === m.key ? "border-primary neon" : "border-base-300 hover:border-primary/50"}`}
          onClick={() => {
            setMood(m.key, m.color);
            document.documentElement.style.setProperty("--magic-color", m.color);
          }}
        >
          <div className="text-xs opacity-70 uppercase tracking-wider">Mood</div>
          <div className="mt-1 font-bold">{m.label}</div>
          <div className="mt-3 flex items-center gap-2">
            <span className="w-3 h-3 rounded-full" style={{ background: m.color }} />
            <span className="text-xs opacity-70">{m.color}</span>
          </div>
        </button>
      ))}
    </div>
  );
}

