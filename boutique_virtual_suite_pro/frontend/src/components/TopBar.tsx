import { Link } from "react-router-dom";
import { useSettingsStore } from "../stores/settingsStore";
import { useAuthStore } from "../stores/authStore";
import { useI18n } from "../i18n/i18n";
import { useTrylistStore } from "../stores/trylistStore";

export default function TopBar() {
  const { t } = useI18n();
  const theme = useSettingsStore((s) => s.theme);
  const setTheme = useSettingsStore((s) => s.setTheme);
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const setOpen = useTrylistStore((s) => s.setOpen);

  return (
    <div className="sticky top-0 z-30 backdrop-blur bg-base-100/70 border-b border-base-300">
      <div className="max-w-7xl mx-auto px-3 md:px-6 py-3 flex items-center justify-between gap-3">
        <Link to="/" className="font-extrabold tracking-tight text-lg">
          <span style={{ color: "var(--bvp-primary)" }}>Boutique</span> Virtual Suite Pro
        </Link>
        <div className="flex items-center gap-2">
          <button className="btn btn-ghost btn-sm" onClick={() => setOpen(true)}>
            {t("nav.trylist")}
          </button>
          <label className="btn btn-ghost btn-sm gap-2">
            <span className="text-xs">Dark</span>
            <input
              type="checkbox"
              className="toggle toggle-sm"
              checked={theme === "dark"}
              onChange={(e) => setTheme(e.target.checked ? "dark" : "bvp_light")}
            />
          </label>
          {user ? (
            <button className="btn btn-ghost btn-sm" onClick={logout}>
              Logout
            </button>
          ) : (
            <Link className="btn btn-primary btn-sm" to="/login">
              {t("auth.login")}
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}

