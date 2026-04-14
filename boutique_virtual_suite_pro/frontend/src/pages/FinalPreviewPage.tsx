import { useTrylistStore } from "../stores/trylistStore";
import DesignerFlowShell from "./designer/DesignerFlowShell";

export default function FinalPreviewPage() {
  const items = useTrylistStore((s) => s.items).slice().sort((a, b) => a.position - b.position);
  return (
    <DesignerFlowShell title="Final Preview">
      <div className="glass rounded-2xl border border-base-300 p-6">
        <div className="font-bold">Your selected items</div>
        <div className="mt-4 grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {items.map((it) => (
            <div key={it.product_id} className="rounded-2xl border border-base-300 bg-base-100 overflow-hidden">
              {it.product?.image_url ? <img src={it.product.image_url} className="w-full h-44 object-cover" /> : null}
              <div className="p-4">
                <div className="font-semibold">{it.product?.name || `#${it.product_id}`}</div>
                <div className="text-xs opacity-70">{it.product?.category}</div>
              </div>
            </div>
          ))}
          {!items.length ? <div className="opacity-70">Trylist empty.</div> : null}
        </div>
      </div>
    </DesignerFlowShell>
  );
}

