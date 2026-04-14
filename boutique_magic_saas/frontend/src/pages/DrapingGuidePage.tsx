import { AnimatePresence, motion } from "framer-motion";
import { useMemo, useState } from "react";
import TailorJinn from "../components/TailorJinn";

const steps = [
  { key: "tuck", title: "Tuck", desc: "Tuck saree into the waist band smoothly.", seed: "tuck" },
  { key: "pleat", title: "Pleat", desc: "Make neat pleats with rhythmic motion.", seed: "pleat" },
  { key: "wrap", title: "Wrap", desc: "Wrap around with even tension for a clean fall.", seed: "wrap" },
  { key: "pallu", title: "Pallu", desc: "Drape pallu and let gravity add flow.", seed: "pallu" },
  { key: "pin", title: "Pin", desc: "Pin discreetly for confidence.", seed: "pin" }
];

export default function DrapingGuidePage() {
  const [idx, setIdx] = useState(0);
  const step = steps[idx];
  const img = useMemo(() => `https://picsum.photos/seed/magic_${step.seed}/900/1200`, [step.seed]);

  return (
    <div className="max-w-7xl mx-auto px-3 md:px-6 py-6 space-y-6">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">Interactive Saree Draping Guide</div>
        <div className="mt-2 text-sm opacity-70">Step-by-step visual animations (non-AI).</div>
      </div>

      <div className="grid lg:grid-cols-[1fr_360px] gap-4 items-start">
        <div className="rounded-2xl border border-base-300 bg-base-100 overflow-hidden">
          <AnimatePresence mode="wait">
            <motion.div
              key={step.key}
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.98 }}
              transition={{ duration: 0.22 }}
              className="relative aspect-[3/4]"
            >
              <img src={img} className="absolute inset-0 w-full h-full object-cover" />
              <motion.div
                className="absolute inset-0 pointer-events-none"
                animate={{ backgroundPosition: ["0% 0%", "100% 100%"] }}
                transition={{ duration: 1.8, repeat: Infinity, ease: "linear" }}
                style={{
                  backgroundImage:
                    "radial-gradient(circle at 30% 20%, color-mix(in oklab, var(--magic-color) 25%, transparent) 0%, transparent 55%)",
                  opacity: 0.65
                }}
              />
              <div className="absolute top-3 left-3 badge badge-primary">{step.title}</div>
            </motion.div>
          </AnimatePresence>
          <div className="p-4">
            <div className="font-bold">{step.title}</div>
            <div className="mt-1 text-sm opacity-70">{step.desc}</div>
          </div>
        </div>

        <div className="glass rounded-2xl border border-base-300 p-4">
          <div className="font-bold">Steps</div>
          <div className="mt-3 space-y-2">
            {steps.map((s, i) => (
              <button key={s.key} className={`btn btn-sm w-full ${i === idx ? "btn-primary" : "btn-ghost"}`} onClick={() => setIdx(i)}>
                {i + 1}. {s.title}
              </button>
            ))}
          </div>
          <div className="mt-4 flex gap-2">
            <button className="btn" disabled={idx === 0} onClick={() => setIdx((v) => Math.max(0, v - 1))}>
              Back
            </button>
            <button className="btn btn-primary" disabled={idx === steps.length - 1} onClick={() => setIdx((v) => Math.min(steps.length - 1, v + 1))}>
              Next
            </button>
          </div>
        </div>
      </div>

      <TailorJinn eventKey={`guide-${idx}`} />
    </div>
  );
}

