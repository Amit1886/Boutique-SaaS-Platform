import { NavLink } from "react-router-dom";
import { useI18n } from "../i18n/i18n";

const links = [
  { to: "/", key: "nav.home" },
  { to: "/moodboard", key: "nav.moodboard" },
  { to: "/designer-flow/saree", key: "nav.designer" },
  { to: "/style-test", key: "nav.styleTest" },
  { to: "/trylist", key: "nav.trylist" },
  { to: "/profile", key: "nav.profile" },
  { to: "/settings", key: "nav.settings" }
];

export default function Sidebar() {
  const { t } = useI18n();
  return (
    <div className="glass rounded-2xl p-4 border border-base-300">
      <div className="text-xs uppercase tracking-wider opacity-60">Navigation</div>
      <div className="mt-3 flex flex-col gap-1">
        {links.map((l) => (
          <NavLink
            key={l.to}
            to={l.to}
            className={({ isActive }) =>
              `px-3 py-2 rounded-xl transition ${isActive ? "bg-primary text-primary-content" : "hover:bg-base-300/60"}`
            }
          >
            {t(l.key)}
          </NavLink>
        ))}
      </div>
    </div>
  );
}

