import { useEffect, useMemo } from "react";
import DesignerFlowShell from "./DesignerFlowShell";
import { useProductStore } from "../../stores/productStore";
import ProductCard from "../../components/ProductCard";
import LivePreviewPanel from "../../components/LivePreviewPanel";
import { useDesignerStore } from "../../stores/designerStore";

export default function DesignerSareePage() {
  const loadAll = useProductStore((s) => s.loadAll);
  const products = useProductStore((s) => s.products);
  const setSelected = useDesignerStore((s) => s.setSelected);
  useEffect(() => {
    loadAll().catch(() => {});
  }, [loadAll]);
  const sarees = useMemo(() => products.filter((p) => p.category === "saree").slice(0, 12), [products]);
  return (
    <DesignerFlowShell title="Step 1: Saree selection" activeStep={1}>
      <div className="grid lg:grid-cols-[1fr_360px] gap-4 items-start">
        <div className="grid sm:grid-cols-2 lg:grid-cols-2 gap-4">
          {sarees.map((p) => (
            <div key={p.id} className="relative">
              <ProductCard p={p} />
              <button className="btn btn-sm btn-secondary absolute bottom-3 left-3" onClick={() => setSelected("saree", p.id)}>
                Select for Flow
              </button>
            </div>
          ))}
        </div>
        <LivePreviewPanel />
      </div>
    </DesignerFlowShell>
  );
}
