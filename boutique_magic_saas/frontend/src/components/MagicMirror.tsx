import { useEffect, useRef, useState } from "react";
import type { Saree } from "../store/useCatalogStore";

export default function MagicMirror({
  saree,
  shadowStrength = 0.25
}: {
  saree: Saree | null;
  shadowStrength?: number;
}) {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [on, setOn] = useState(false);
  const [err, setErr] = useState("");
  const [tilt, setTilt] = useState({ x: 0, y: 0 });

  useEffect(() => {
    function onMove(ev: DeviceOrientationEvent) {
      const gamma = Number(ev.gamma || 0); // left/right
      const beta = Number(ev.beta || 0); // forward/back
      setTilt({ x: Math.max(-12, Math.min(12, gamma / 4)), y: Math.max(-12, Math.min(12, beta / 8)) });
    }
    window.addEventListener("deviceorientation", onMove as any);
    return () => window.removeEventListener("deviceorientation", onMove as any);
  }, []);

  useEffect(() => {
    if (!on) return;
    let stream: MediaStream | null = null;
    (async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" }, audio: false });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          await videoRef.current.play();
        }
      } catch (e: any) {
        setErr(e?.message || "Camera error");
        setOn(false);
      }
    })();
    return () => {
      if (stream) stream.getTracks().forEach((t) => t.stop());
    };
  }, [on]);

  const palluTransform = `translate(${tilt.x}px, ${tilt.y}px) rotate(${tilt.x * 0.6}deg)`;

  return (
    <div className="rounded-2xl border border-base-300 bg-base-100 overflow-hidden relative bloom is-blooming">
      <div className="p-3 flex items-center justify-between">
        <div>
          <div className="font-bold">Magic Mirror Mode</div>
          <div className="text-xs opacity-70">Camera overlay + CSS blend + tilt gravity</div>
        </div>
        <button className={`btn btn-sm ${on ? "btn-primary" : ""}`} onClick={() => setOn((v) => !v)}>
          {on ? "Stop" : "Start"}
        </button>
      </div>
      {err ? <div className="px-3 pb-3 text-sm text-error">{err}</div> : null}

      <div className="relative aspect-[3/4] bg-black">
        <video ref={videoRef} playsInline className="absolute inset-0 w-full h-full object-cover scale-x-[-1]" />

        {/* Shadow sync (fake) */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            boxShadow: `inset 0 -80px 120px rgba(0,0,0,${shadowStrength})`
          }}
        />

        {/* Saree layers */}
        {saree?.layer_body_png ? (
          <img
            src={`${import.meta.env.VITE_UPLOAD_BASE_URL || ""}${saree.layer_body_png}`}
            className="absolute inset-0 w-full h-full object-contain teleport aura"
            style={{ mixBlendMode: "multiply", opacity: 0.92 }}
          />
        ) : null}
        {saree?.layer_border_png ? (
          <img
            src={`${import.meta.env.VITE_UPLOAD_BASE_URL || ""}${saree.layer_border_png}`}
            className="absolute inset-0 w-full h-full object-contain teleport aura"
            style={{ mixBlendMode: "screen", opacity: 0.9, filter: "drop-shadow(0 0 14px color-mix(in oklab, var(--magic-color) 55%, transparent))" }}
          />
        ) : null}
        {saree?.layer_pallu_png ? (
          <img
            src={`${import.meta.env.VITE_UPLOAD_BASE_URL || ""}${saree.layer_pallu_png}`}
            className="absolute inset-0 w-full h-full object-contain teleport aura"
            style={{ transform: palluTransform, mixBlendMode: "multiply", opacity: 0.92, transformOrigin: "40% 20%" }}
          />
        ) : null}
      </div>
    </div>
  );
}

