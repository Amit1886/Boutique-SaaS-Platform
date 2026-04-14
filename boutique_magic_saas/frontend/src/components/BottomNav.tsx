import { NavLink } from "react-router-dom";

const items = [
  ["/", "Home"],
  ["/tryon-studio", "Studio"],
  ["/magic-mirror", "Mirror"],
  ["/outfit-builder", "Builder"],
  ["/saved-looks", "Looks"]
] as const;

export default function BottomNav() {
  return (
    <div className="md:hidden fixed bottom-3 left-0 right-0 z-50 px-3">
      <div className="glass rounded-2xl border border-base-300 grid grid-cols-5 overflow-hidden">
        {items.map(([to, label]) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `text-xs py-3 text-center ${isActive ? "bg-primary text-primary-content" : "opacity-80"}`
            }
          >
            {label}
          </NavLink>
        ))}
      </div>
    </div>
  );
}

