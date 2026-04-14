import { useEffect, useState } from "react";
import { useCatalogStore } from "../store/useCatalogStore";
import { useTryOnStore } from "../store/useTryOnStore";
import MagicMirror from "../components/MagicMirror";
import TailorJinn from "../components/TailorJinn";
import { useUxStore } from "../store/useUxStore";

export default function MagicMirrorPage() {
  const load = useCatalogStore((s) => s.load);
  const sarees = useCatalogStore((s) => s.sarees);
  const setSaree = useTryOnStore((s) => s.setSaree);
  const saree = useTryOnStore((s) => s.selectedSaree);
  const [jinnKey, setJinnKey] = useState("mirror");
  const isOn = useUxStore((s) => s.isOn);
  const on = isOn("magic_mirror");

  useEffect(() => {
    load().catch(() => {});
  }, [load]);

  return (
    <div className="max-w-7xl mx-auto px-3 md:px-6 py-6 space-y-6">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">Magic Mirror</div>
        <div className="mt-2 text-sm opacity-70">Camera ON + overlay saree layers with blend modes.</div>
      </div>

      <div className="grid lg:grid-cols-[1fr_360px] gap-4 items-start">
        {on ? <MagicMirror saree={saree} /> : <div className="alert alert-warning">Magic Mirror is OFF (admin flag).</div>}
        <div className="glass rounded-2xl border border-base-300 p-4">
          <div className="font-bold">Choose Saree</div>
          <div className="mt-3 grid grid-cols-2 gap-2">
            {sarees.slice(0, 12).map((s) => (
              <button
                key={s.id}
                className={`btn btn-sm ${saree?.id === s.id ? "btn-primary" : "btn-ghost"}`}
                onClick={() => {
                  setSaree(s);
                  setJinnKey(`mirror-${s.id}`);
                }}
              >
                {s.name.slice(0, 12)}
              </button>
            ))}
          </div>
          <div className="mt-4 text-xs opacity-70">
            Pallu gravity uses device tilt (works on mobile browsers).
          </div>
        </div>
      </div>

      <TailorJinn eventKey={jinnKey} />
    </div>
  );
}
