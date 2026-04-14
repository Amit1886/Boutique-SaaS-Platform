import { useTrylistStore } from "../stores/trylistStore";
import DesignerFlowShell from "./designer/DesignerFlowShell";
import LivePreviewPanel from "../components/LivePreviewPanel";
import ImageCompareSlider from "../components/ImageCompareSlider";
import { useDesignerStore } from "../stores/designerStore";
import { useProductStore } from "../stores/productStore";

export default function FinalPreviewPage() {
  const items = useTrylistStore((s) => s.items).slice().sort((a, b) => a.position - b.position);
  const selected = useDesignerStore((s) => s.selected);
  const products = useProductStore((s) => s.products);
  const saree = products.find((p) => p.id === selected.saree);
  const beforeUrl = saree?.image_url || (items[0]?.product?.image_url || "https://picsum.photos/seed/bvp_before/800/1000");
  const afterUrl = saree?.image_url || (items[0]?.product?.image_url || "https://picsum.photos/seed/bvp_after/800/1000");
  return (
    <DesignerFlowShell title="Final Preview" activeStep={5}>
      <div className="grid lg:grid-cols-[1fr_360px] gap-4 items-start">
        <div className="glass rounded-2xl border border-base-300 p-6">
          <div className="font-bold">Your selected items</div>
          <div className="mt-4 grid md:grid-cols-2 gap-4">
            <ImageCompareSlider beforeUrl={beforeUrl} afterUrl={afterUrl} />
            <div className="rounded-2xl border border-base-300 bg-base-100 p-4">
              <div className="text-xs uppercase tracking-wider opacity-60">Preview</div>
              <div className="mt-2 text-sm opacity-70">Use the slider to compare before/after.</div>
              <div className="mt-4 text-xs opacity-70">Tip: favorites + trylist update instantly.</div>
            </div>
          </div>
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
        <LivePreviewPanel />
      </div>
    </DesignerFlowShell>
  );
}
