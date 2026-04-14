import { useEffect, useState } from "react";
import { apiFetch } from "../api/client";
import { useAuthStore } from "../stores/authStore";
import { useNavigate } from "react-router-dom";

type Q = { id: string; title_en: string; title_hi: string; choices: { key: string; label_en: string; label_hi: string }[] };

export default function StyleTestPage() {
  const token = useAuthStore((s) => s.token);
  const nav = useNavigate();
  const [qs, setQs] = useState<Q[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [err, setErr] = useState("");

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
      nav("/results");
    } catch (e: any) {
      setErr(e?.message || "Failed");
    }
  }

  return (
    <div className="space-y-5 fade-in">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">Style Personality Test</div>
        <div className="mt-2 text-sm opacity-70">7 quick questions; saves result to server.</div>
      </div>
      {err ? <div className="alert alert-error">{err}</div> : null}
      <div className="space-y-4">
        {qs.map((q) => (
          <div key={q.id} className="rounded-2xl border border-base-300 bg-base-100 p-4">
            <div className="font-semibold">{q.title_en}</div>
            <div className="mt-3 flex flex-wrap gap-2">
              {q.choices.map((c) => (
                <button
                  key={c.key}
                  className={`btn btn-sm ${answers[q.id] === c.key ? "btn-primary" : ""}`}
                  onClick={() => setAnswers((a) => ({ ...a, [q.id]: c.key }))}
                >
                  {c.label_en}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
      <button className="btn btn-primary" onClick={submit}>
        Submit
      </button>
    </div>
  );
}

