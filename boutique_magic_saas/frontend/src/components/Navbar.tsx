import { Link, NavLink } from "react-router-dom";
import { useAppStore } from "../store/useAppStore";

export default function Navbar() {
  const userName = useAppStore((s) => s.userName);
  const setUserName = useAppStore((s) => s.setUserName);
  return (
    <div className="sticky top-0 z-50 backdrop-blur bg-base-100/70 border-b border-base-300">
      <div className="max-w-7xl mx-auto px-3 md:px-6 py-3 flex items-center justify-between gap-3">
        <Link to="/" className="font-extrabold tracking-tight text-lg">
          <span style={{ color: "var(--magic-color)" }}>Boutique</span> Magic
        </Link>
        <div className="hidden md:flex items-center gap-2">
          {[
            ["/tryon-studio", "Try-On Studio"],
            ["/outfit-builder", "Outfit Builder"],
            ["/magic-mirror", "Magic Mirror"],
            ["/mannequin-3d", "3D Mannequin"],
            ["/draping-guide", "Draping Guide"],
            ["/festival-themes", "Festival Themes"],
            ["/saved-looks", "Saved Looks"],
            ["/admin", "Admin"]
          ].map(([to, label]) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) => `btn btn-sm ${isActive ? "btn-primary" : "btn-ghost"}`}
            >
              {label}
            </NavLink>
          ))}
        </div>
        <div className="flex items-center gap-2">
          <input
            className="input input-bordered input-sm w-28"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
            placeholder="Your name"
          />
        </div>
      </div>
    </div>
  );
}
