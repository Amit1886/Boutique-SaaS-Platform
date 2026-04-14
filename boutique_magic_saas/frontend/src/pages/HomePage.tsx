import { useEffect } from "react";
import { Link } from "react-router-dom";
import Moodboard from "../components/Moodboard";
import { useCatalogStore } from "../store/useCatalogStore";
import { useTryOnStore } from "../store/useTryOnStore";
import TailorJinn from "../components/TailorJinn";
import { useAppStore } from "../store/useAppStore";

export default function HomePage() {
  const load = useCatalogStore((s) => s.load);
  const sarees = useCatalogStore((s) => s.sarees);
  const setSaree = useTryOnStore((s) => s.setSaree);
  const setMood = useAppStore((s) => s.setMood);
  const magicColor = useAppStore((s) => s.magicColor);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", "magic_light");
    document.documentElement.style.setProperty("--magic-color", magicColor);
  }, [magicColor]);

  useEffect(() => {
    load().catch(() => {});
  }, [load]);

  return (
    <div className="max-w-7xl mx-auto px-3 md:px-6 py-6 space-y-6">
      <div className="glass rounded-2xl border border-base-300 p-6 bloom is-blooming">
        <div className="text-xs opacity-70 uppercase tracking-wider">Boutique Magic</div>
        <div className="mt-1 text-3xl font-extrabold">Virtual Try-On Studio + Magic Mirror</div>
        <div className="mt-2 text-sm opacity-70">
          Cinematic effects: bloom, teleport, aura glow, ripple reveal, tilt gravity.
        </div>
        <div className="mt-4 flex flex-wrap gap-2">
          <Link className="btn btn-primary" to="/tryon-studio">Open Try-On Studio</Link>
          <Link className="btn" to="/magic-mirror">Magic Mirror</Link>
          <Link className="btn" to="/outfit-builder">Outfit Builder</Link>
          <Link className="btn" to="/mannequin-3d">3D Mannequin</Link>
          <Link className="btn" to="/draping-guide">Draping Guide</Link>
          <Link className="btn" to="/festival-themes">Festival Themes</Link>
        </div>
      </div>

      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-xl font-bold">Shopping Moodboard</div>
        <div className="mt-2 text-sm opacity-70">Pick a mood to change theme instantly.</div>
        <div className="mt-4">
          <Moodboard />
        </div>
      </div>

      <div className="flex items-center justify-between">
        <div className="text-xl font-bold">Saree Gallery</div>
        <div className="text-xs opacity-70">Tap to select</div>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {sarees.slice(0, 12).map((s) => (
          <button
            key={s.id}
            className="rounded-2xl border border-base-300 bg-base-100 overflow-hidden text-left transition hover:border-primary/60"
            onClick={() => {
              setSaree(s);
              setMood("festive", s.primary_color || "#db2777");
            }}
          >
            <div className="p-4">
              <div className="font-bold truncate">{s.name}</div>
              <div className="text-sm opacity-70">₹{s.price}</div>
              <div className="mt-3 flex items-center gap-2">
                <span className="w-3 h-3 rounded-full" style={{ background: s.primary_color || "#db2777" }} />
                <span className="text-xs opacity-70">{s.primary_color || ""}</span>
              </div>
            </div>
            <div className="p-4 pt-0">
              <div className="badge badge-primary">Select</div>
            </div>
          </button>
        ))}
        {!sarees.length ? <div className="opacity-70">No sarees yet. Add from Admin.</div> : null}
      </div>

      <TailorJinn eventKey={`${sarees.length}`} />
    </div>
  );
}
