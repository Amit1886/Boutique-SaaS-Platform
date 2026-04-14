import { NavLink } from "react-router-dom";

const items = [
  { to: "/", label: "Home" },
  { to: "/moodboard", label: "Mood" },
  { to: "/products", label: "Shop" },
  { to: "/designer-flow/saree", label: "Flow" },
  { to: "/trylist", label: "Try" }
];

export default function BottomNav() {
  return (
    <div className="md:hidden fixed bottom-3 left-0 right-0 z-40 px-3">
      <div className="glass rounded-2xl border border-base-300 grid grid-cols-5 overflow-hidden">
        {items.map((it) => (
          <NavLink
            key={it.to}
            to={it.to}
            className={({ isActive }) => `text-xs py-3 text-center ${isActive ? "bg-primary text-primary-content" : "opacity-80"}`}
          >
            {it.label}
          </NavLink>
        ))}
      </div>
    </div>
  );
}
