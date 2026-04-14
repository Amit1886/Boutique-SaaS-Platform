import { Link } from "react-router-dom";

const steps = [
  { to: "/designer-flow/saree", label: "Saree" },
  { to: "/designer-flow/blouse", label: "Blouse" },
  { to: "/designer-flow/accessories", label: "Accessories" },
  { to: "/designer-flow/jewelry", label: "Jewelry" },
  { to: "/final-preview", label: "Final" }
];

export default function DesignerFlowShell({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="space-y-5 fade-in">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="text-2xl font-extrabold">Outfit Flow Navigator</div>
        <div className="mt-1 opacity-70 text-sm">{title}</div>
        <div className="mt-4 flex flex-wrap gap-2">
          {steps.map((s) => (
            <Link key={s.to} to={s.to} className="btn btn-sm">
              {s.label}
            </Link>
          ))}
        </div>
      </div>
      {children}
    </div>
  );
}

