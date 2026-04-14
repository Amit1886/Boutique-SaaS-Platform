import { useEffect, useMemo, useState } from "react";
import { apiGet } from "../api/client";
import { useTryOnStore } from "../store/useTryOnStore";
import Mannequin3D from "../components/Mannequin3D";
import TailorJinn from "../components/TailorJinn";

type Body = { key: string; label: string; scale: number };

export default function MannequinPage() {
  const saree = useTryOnStore((s) => s.selectedSaree);
  const [bodies, setBodies] = useState<Body[]>([]);
  const [active, setActive] = useState<Body | null>(null);
  const [jinnKey, setJinnKey] = useState("mannequin");

  useEffect(() => {
    apiGet<{ ok: true; bodies: Body[] }>("/3d/mannequin")
      .then((r) => {
        setBodies(r.bodies || []);
        setActive((r.bodies || [])[1] || null);
      })
      .catch(() => {});
  }, []);

  const textureUrl = useMemo(() => {
    if (!saree?.layer_body_png) return null;
    return `${import.meta.env.VITE_UPLOAD_BASE_URL || ""}${saree.layer_body_png}`;
  }, [saree?.layer_body_png]);

  return (
    <div className="max-w-7xl mx-auto px-3 md:px-6 py-6 space-y-6">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">3D Body Reconstruction (Simple)</div>
        <div className="mt-2 text-sm opacity-70">Dummy mannequin + 360° rotate + saree wrap.</div>
      </div>

      <div className="grid lg:grid-cols-[1fr_360px] gap-4 items-start">
        <Mannequin3D textureUrl={textureUrl} bodyScale={active?.scale || 1.0} />
        <div className="glass rounded-2xl border border-base-300 p-4">
          <div className="font-bold">Multi-Body Preview</div>
          <div className="mt-3 grid grid-cols-2 gap-2">
            {bodies.map((b) => (
              <button
                key={b.key}
                className={`btn btn-sm ${active?.key === b.key ? "btn-primary" : "btn-ghost"}`}
                onClick={() => {
                  setActive(b);
                  setJinnKey(`body-${b.key}`);
                }}
              >
                {b.label}
              </button>
            ))}
          </div>
          <div className="mt-4 text-xs opacity-70">Tip: select a saree in Studio to texture-wrap it here.</div>
        </div>
      </div>

      <TailorJinn eventKey={jinnKey} />
    </div>
  );
}

