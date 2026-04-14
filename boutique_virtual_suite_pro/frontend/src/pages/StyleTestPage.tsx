import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";
import { useAuthStore } from "../stores/authStore";
import { useNavigate } from "react-router-dom";
import { cacheSet } from "../lib/cache";
import { AnimatePresence, motion } from "framer-motion";
import StepProgressBar from "../components/StepProgressBar";

type Q = { id: string; title_en: string; title_hi: string; choices: { key: string; label_en: string; label_hi: string; image_url?: string }[] };

export default function StyleTestPage() {
  const token = useAuthStore((s) => s.token);
  const nav = useNavigate();
  const [qs, setQs] = useState<Q[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [err, setErr] = useState("");
  const [idx, setIdx] = useState(0);

  useEffect(() => {
    apiFetch<{ ok: true; questions: Q[] }>("/style/test/questions", { method: "GET" })
      .then((r) => setQs(r.questions))
      .catch((e) => setErr(e.message));
  }, []);

  async function submit() {
    if (!token) {
      setErr("Login required");
      return;
    }
    try {
      const res = await apiFetch<{ ok: true; result: { personality: string } }>("/style/test/submit", {
        method: "POST",
        body: JSON.stringify({ answers })
      });
      sessionStorage.setItem("bvp.personality.latest", res.result.personality);
      cacheSet("bvp.feed.personal", [], 1);
      nav("/results");
    } catch (e: any) {
      setErr(e?.message || "Failed");
    }
  }

  const q = qs[idx];
  const total = qs.length || 7;
  const step = Math.min(total, idx + 1);

  return (
    <div className="space-y-5 fade-in">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">Style Personality Test</div>
        <div className="mt-2 text-sm opacity-70">7 quick questions; saves result to server.</div>
        <div className="mt-4">
          <StepProgressBar step={step} total={total} labels={qs.map((x) => x.id)} />
        </div>
      </div>
      {err ? <div className="alert alert-error">{err}</div> : null}
      <div className="rounded-2xl border border-base-300 bg-base-100 p-5">
        {!q ? (
          <div className="opacity-70">Loading questions…</div>
        ) : (
          <AnimatePresence mode="wait">
            <motion.div
              key={q.id}
              initial={{ opacity: 0, x: 12 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -12 }}
              transition={{ duration: 0.18, ease: "easeOut" }}
            >
              <div className="font-semibold text-lg">{q.title_en}</div>
              <div className="mt-4 grid sm:grid-cols-3 gap-3">
                {q.choices.map((c) => (
                  <button
                    key={c.key}
                    className={`rounded-2xl border overflow-hidden text-left transition ${
                      answers[q.id] === c.key ? "border-primary" : "border-base-300 hover:border-primary/50"
                    }`}
                    onClick={() => setAnswers((a) => ({ ...a, [q.id]: c.key }))}
                  >
                    <div className="aspect-[4/3] bg-base-200">
                      {c.image_url ? <img src={c.image_url} className="w-full h-full object-cover" loading="lazy" /> : null}
                    </div>
                    <div className="p-3">
                      <div className="font-semibold">{c.label_en}</div>
                      <div className="text-xs opacity-70">Tap to select</div>
                    </div>
                  </button>
                ))}
              </div>
            </motion.div>
          </AnimatePresence>
        )}
      </div>

      <div className="flex items-center justify-between gap-3">
        <button className="btn" disabled={idx <= 0} onClick={() => setIdx((v) => Math.max(0, v - 1))}>
          Back
        </button>
        {idx < qs.length - 1 ? (
          <button className="btn btn-primary" disabled={!q || !answers[q.id]} onClick={() => setIdx((v) => Math.min(qs.length - 1, v + 1))}>
            Next
          </button>
        ) : (
          <button className="btn btn-primary" disabled={Object.keys(answers).length < Math.min(3, qs.length)} onClick={submit}>
            Submit
          </button>
        )}
      </div>
    </div>
  );
}
