import { useMemo } from "react";
import { useDesignerStore } from "../stores/designerStore";
import { useProductStore } from "../stores/productStore";

function pick(products: any[], id?: number) {
  if (!id) return null;
  return products.find((p) => p.id === id) || null;
}

export default function LivePreviewPanel() {
  const selected = useDesignerStore((s) => s.selected);
  const products = useProductStore((s) => s.products);

  const saree = useMemo(() => pick(products, selected.saree), [products, selected.saree]);
  const blouse = useMemo(() => pick(products, selected.blouse), [products, selected.blouse]);
  const accessories = useMemo(() => pick(products, selected.accessories), [products, selected.accessories]);
  const jewelry = useMemo(() => pick(products, selected.jewelry), [products, selected.jewelry]);

  return (
    <div className="glass rounded-2xl border border-base-300 p-4">
      <div className="text-xs uppercase tracking-wider opacity-60">Live Preview</div>
      <div className="mt-3 grid grid-cols-2 gap-3">
        <div className="rounded-xl border border-base-300 bg-base-100 p-3">
          <div className="text-xs opacity-60">Saree</div>
          <div className="font-semibold text-sm line-clamp-1">{saree?.name || "—"}</div>
        </div>
        <div className="rounded-xl border border-base-300 bg-base-100 p-3">
          <div className="text-xs opacity-60">Blouse</div>
          <div className="font-semibold text-sm line-clamp-1">{blouse?.name || "—"}</div>
        </div>
        <div className="rounded-xl border border-base-300 bg-base-100 p-3">
          <div className="text-xs opacity-60">Accessories</div>
          <div className="font-semibold text-sm line-clamp-1">{accessories?.name || "—"}</div>
        </div>
        <div className="rounded-xl border border-base-300 bg-base-100 p-3">
          <div className="text-xs opacity-60">Jewelry</div>
          <div className="font-semibold text-sm line-clamp-1">{jewelry?.name || "—"}</div>
        </div>
      </div>
      <div className="mt-3 text-xs opacity-60">Updates instantly as you pick items (no reload).</div>
    </div>
  );
}

