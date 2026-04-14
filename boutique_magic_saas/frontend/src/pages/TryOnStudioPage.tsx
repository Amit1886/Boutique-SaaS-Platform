import { useEffect, useMemo, useRef, useState } from "react";
import { useCatalogStore } from "../store/useCatalogStore";
import { useTryOnStore } from "../store/useTryOnStore";
import TailorJinn from "../components/TailorJinn";
import ImageCompareSlider from "../components/ImageCompareSlider";
import { useUxStore } from "../store/useUxStore";

export default function TryOnStudioPage() {
  const load = useCatalogStore((s) => s.load);
  const sarees = useCatalogStore((s) => s.sarees);
  const blouses = useCatalogStore((s) => s.blouses);
  const accessories = useCatalogStore((s) => s.accessories);

  const saree = useTryOnStore((s) => s.selectedSaree);
  const blouse = useTryOnStore((s) => s.selectedBlouse);
  const selectedAccessories = useTryOnStore((s) => s.selectedAccessories);
  const setSaree = useTryOnStore((s) => s.setSaree);
  const setBlouse = useTryOnStore((s) => s.setBlouse);
  const toggleAccessory = useTryOnStore((s) => s.toggleAccessory);

  const [jinnKey, setJinnKey] = useState("studio");
  const [bloom, setBloom] = useState(false);
  const [ripple, setRipple] = useState<{ x: number; y: number; px: string; py: string; k: number } | null>(null);
  const stageRef = useRef<HTMLDivElement | null>(null);
  const isOn = useUxStore((s) => s.isOn);
  const colorBloomOn = isOn("color_bloom");
  const rippleOn = isOn("ripple_reveal");
  const [hue, setHue] = useState(0);
  const [scrollFx, setScrollFx] = useState(0);
  const [sparkleKey, setSparkleKey] = useState(0);

  useEffect(() => {
    load().catch(() => {});
  }, [load]);

  useEffect(() => {
    const onScroll = () => {
      const v = Math.max(-1, Math.min(1, (window.scrollY || 0) / 600));
      setScrollFx(v);
    };
    window.addEventListener("scroll", onScroll, { passive: true } as any);
    onScroll();
    return () => window.removeEventListener("scroll", onScroll as any);
  }, []);

  useEffect(() => {
    const c = saree?.primary_color || "#db2777";
    document.documentElement.style.setProperty("--magic-color", c);
    if (colorBloomOn) {
      setBloom(true);
      const t = setTimeout(() => setBloom(false), 420);
      return () => clearTimeout(t);
    }
  }, [saree?.id, colorBloomOn]);

  useEffect(() => {
    if (!saree?.id) return;
    setSparkleKey(Date.now());
  }, [saree?.id]);

  const afterUrl = useMemo(() => {
    // In this system, "after" is just composited in the browser (no AI).
    return "https://picsum.photos/seed/magic_after/900/1200";
  }, [saree?.id, blouse?.id, selectedAccessories.length]);

  function onTap(e: React.MouseEvent) {
    if (!rippleOn) return;
    const el = stageRef.current;
    if (!el) return;
    const r = el.getBoundingClientRect();
    const x = e.clientX - r.left;
    const y = e.clientY - r.top;
    const px = `${Math.max(0, Math.min(100, (x / r.width) * 100)).toFixed(2)}%`;
    const py = `${Math.max(0, Math.min(100, (y / r.height) * 100)).toFixed(2)}%`;
    setRipple({ x, y, px, py, k: Date.now() });
    setJinnKey(`tap-${Date.now()}`);
  }

  return (
    <div className="max-w-7xl mx-auto px-3 md:px-6 py-6 space-y-6">
      <div className={`glass rounded-2xl border border-base-300 p-6 bloom ${bloom ? "is-blooming" : ""}`}>
        <div className="text-2xl font-extrabold">Try-On Studio</div>
        <div className="mt-2 text-sm opacity-70">
          Real-time preview (no reload): CSS blend layers + aura glow + ripple reveal + teleport effect.
        </div>
      </div>

      <div className="grid lg:grid-cols-[1fr_360px] gap-4 items-start">
        <div className="space-y-4">
          <div className="rounded-2xl border border-base-300 bg-base-100 overflow-hidden">
            <div className="p-3 flex items-center justify-between">
              <div>
                <div className="font-bold">Live Preview</div>
                <div className="text-xs opacity-70">Tap stage for ripple reveal</div>
              </div>
              <div className="badge badge-primary">Teleport</div>
            </div>
            <div ref={stageRef} onClick={onTap} className="relative aspect-[3/4] bg-base-200 overflow-hidden">
              <img src="https://picsum.photos/seed/magic_user/900/1200" className="absolute inset-0 w-full h-full object-cover" />
              <div key={sparkleKey} className="sparkle-overlay" />
              {/* Saree overlays */}
              {saree?.layer_body_png ? (
                <img
                  src={`${import.meta.env.VITE_UPLOAD_BASE_URL || ""}${saree.layer_body_png}`}
                  className="absolute inset-0 w-full h-full object-contain teleport aura"
                  style={{ mixBlendMode: "multiply", opacity: 0.92, filter: `hue-rotate(${hue}deg) saturate(1.15)` }}
                />
              ) : null}
              {/* Pattern reveal (zoom) */}
              {rippleOn && ripple && saree?.layer_body_png ? (
                <img
                  key={`reveal-${ripple.k}`}
                  src={`${import.meta.env.VITE_UPLOAD_BASE_URL || ""}${saree.layer_body_png}`}
                  className="absolute inset-0 w-full h-full object-contain pattern-reveal"
                  style={
                    {
                      mixBlendMode: "multiply",
                      opacity: 0.95,
                      transform: "scale(1.18)",
                      filter: `hue-rotate(${hue}deg) saturate(1.35) contrast(1.08)`,
                      ["--reveal-x" as any]: ripple.px,
                      ["--reveal-y" as any]: ripple.py
                    } as any
                  }
                />
              ) : null}
              {saree?.layer_border_png ? (
                <img
                  src={`${import.meta.env.VITE_UPLOAD_BASE_URL || ""}${saree.layer_border_png}`}
                  className="absolute inset-0 w-full h-full object-contain teleport aura"
                  style={{ mixBlendMode: "screen", opacity: 0.92, filter: `hue-rotate(${hue}deg) saturate(1.2)` }}
                />
              ) : null}
              {saree?.layer_pallu_png ? (
                <img
                  src={`${import.meta.env.VITE_UPLOAD_BASE_URL || ""}${saree.layer_pallu_png}`}
                  className="absolute inset-0 w-full h-full object-contain teleport aura"
                  style={{
                    mixBlendMode: "multiply",
                    opacity: 0.92,
                    transform: `translate(1%, ${-1 + scrollFx * 1.2}%) skewX(${scrollFx * 1.5}deg)`,
                    filter: `hue-rotate(${hue}deg) saturate(1.15)`
                  }}
                />
              ) : null}
              {/* Blouse template */}
              {blouse?.template_png ? (
                <img
                  src={`${import.meta.env.VITE_UPLOAD_BASE_URL || ""}${blouse.template_png}`}
                  className="absolute inset-0 w-full h-full object-contain teleport aura"
                  style={{ mixBlendMode: "screen", opacity: 0.92 }}
                />
              ) : null}
              {/* Accessories */}
              {selectedAccessories.map((a, i) =>
                a.image_png ? (
                  <img
                    key={a.id}
                    src={`${import.meta.env.VITE_UPLOAD_BASE_URL || ""}${a.image_png}`}
                    className="absolute inset-0 w-full h-full object-contain teleport aura"
                    style={{ mixBlendMode: "screen", opacity: 0.92, transform: `translate(${i * 3 - 4}%, ${i * 2 - 2}%) scale(0.75)` }}
                  />
                ) : null
              )}

              {rippleOn && ripple ? <span key={ripple.k} className="ripple" style={{ left: ripple.x, top: ripple.y }} /> : null}
            </div>
          </div>

          <ImageCompareSlider beforeUrl="https://picsum.photos/seed/magic_user/900/1200" afterUrl={afterUrl} />
        </div>

        <div className="glass rounded-2xl border border-base-300 p-4 space-y-4">
          <div>
            <div className="font-bold">Sarees</div>
            <div className="mt-2 flex items-center gap-2">
              <div className="text-xs opacity-70">Live Color</div>
              <input className="range range-primary range-xs" type="range" min={-45} max={45} value={hue} onChange={(e) => setHue(Number(e.target.value))} />
            </div>
            <div className="mt-2 grid grid-cols-2 gap-2">
              {sarees.slice(0, 8).map((s) => (
                <button
                  key={s.id}
                  className={`btn btn-sm ${saree?.id === s.id ? "btn-primary" : ""}`}
                  onClick={() => {
                    setSaree(s);
                    setJinnKey(`saree-${s.id}`);
                  }}
                >
                  {s.name.slice(0, 12)}
                </button>
              ))}
            </div>
          </div>

          <div>
            <div className="font-bold">Blouses (Auto-match)</div>
            <div className="mt-2 grid grid-cols-2 gap-2">
              {blouses.slice(0, 10).map((b) => (
                <button
                  key={b.id}
                  className={`btn btn-sm ${blouse?.id === b.id ? "btn-secondary" : "btn-ghost"}`}
                  onClick={() => {
                    setBlouse(b);
                    setJinnKey(`blouse-${b.id}`);
                  }}
                >
                  {b.name.slice(0, 12)}
                </button>
              ))}
            </div>
          </div>

          <div>
            <div className="font-bold">Accessories</div>
            <div className="mt-2 grid grid-cols-2 gap-2">
              {accessories.slice(0, 10).map((a) => (
                <button
                  key={a.id}
                  className={`btn btn-sm ${
                    selectedAccessories.some((x) => x.id === a.id) ? "btn-accent" : "btn-ghost"
                  }`}
                  onClick={() => {
                    toggleAccessory(a);
                    setJinnKey(`acc-${a.id}`);
                  }}
                >
                  {a.name.slice(0, 12)}
                </button>
              ))}
            </div>
          </div>

          <div className="text-xs opacity-70">Tip: Add layer PNGs from Admin for full magic overlay.</div>
        </div>
      </div>

      <TailorJinn eventKey={jinnKey} />
    </div>
  );
}
