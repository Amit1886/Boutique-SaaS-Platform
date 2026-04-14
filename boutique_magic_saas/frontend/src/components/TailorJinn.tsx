import { useEffect, useMemo, useState } from "react";

const lines = [
  "Madam, this saree suits your aura!",
  "Perfect pallu flow detected!",
  "Neon border glow engaged.",
  "Magic mirror ready — tilt for gravity!",
  "Tap fabric to reveal hidden patterns."
];

export default function TailorJinn({ eventKey }: { eventKey: string }) {
  const [open, setOpen] = useState(false);
  const line = useMemo(() => lines[Math.floor(Math.random() * lines.length)], [eventKey]);

  useEffect(() => {
    if (!eventKey) return;
    setOpen(true);
    const t = setTimeout(() => setOpen(false), 2600);
    return () => clearTimeout(t);
  }, [eventKey]);

  return (
    <div className="fixed bottom-24 right-4 z-50">
      <div className={`transition ${open ? "opacity-100 translate-y-0" : "opacity-0 translate-y-2 pointer-events-none"}`}>
        <div className="glass neon rounded-2xl border border-base-300 p-3 max-w-[240px]">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-2xl bg-primary text-primary-content flex items-center justify-center font-extrabold">
              J
            </div>
            <div>
              <div className="font-bold text-sm">Tailor Jinn</div>
              <div className="text-xs opacity-70">Virtual assistant</div>
            </div>
          </div>
          <div className="mt-2 text-sm">{line}</div>
        </div>
      </div>
    </div>
  );
}

