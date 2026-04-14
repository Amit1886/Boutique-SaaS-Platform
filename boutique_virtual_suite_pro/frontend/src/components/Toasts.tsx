import { useUIStore } from "../stores/uiStore";

export default function Toasts() {
  const toasts = useUIStore((s) => s.toasts);
  const dismiss = useUIStore((s) => s.dismiss);
  return (
    <div className="fixed top-16 right-3 z-[60] space-y-2 w-[92vw] sm:w-[360px]">
      {toasts.map((t) => (
        <div key={t.id} className={`alert shadow ${t.kind === "error" ? "alert-error" : t.kind === "success" ? "alert-success" : "alert-info"}`}>
          <div className="flex-1">
            <div className="font-semibold">{t.title}</div>
            {t.message ? <div className="text-xs opacity-80">{t.message}</div> : null}
          </div>
          <button className="btn btn-ghost btn-xs" onClick={() => dismiss(t.id)}>
            ✕
          </button>
        </div>
      ))}
    </div>
  );
}

