import { useSettingsStore } from "../stores/settingsStore";

export default function SettingsPage() {
  const lang = useSettingsStore((s) => s.lang);
  const setLang = useSettingsStore((s) => s.setLang);
  return (
    <div className="space-y-5 fade-in">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">Settings</div>
        <div className="mt-2 text-sm opacity-70">Language, caching, preferences.</div>
      </div>
      <div className="rounded-2xl border border-base-300 bg-base-100 p-6 max-w-md">
        <div className="text-sm opacity-70">Language</div>
        <div className="mt-3 flex gap-2">
          <button className={`btn btn-sm ${lang === "en" ? "btn-primary" : ""}`} onClick={() => setLang("en")}>
            English
          </button>
          <button className={`btn btn-sm ${lang === "hi" ? "btn-primary" : ""}`} onClick={() => setLang("hi")}>
            Hindi
          </button>
        </div>
      </div>
    </div>
  );
}

