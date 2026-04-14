import { useEffect, useMemo } from "react";
import DesignerFlowShell from "./DesignerFlowShell";
import { useProductStore } from "../../stores/productStore";
import ProductCard from "../../components/ProductCard";

export default function DesignerAccessoriesPage() {
  const loadAll = useProductStore((s) => s.loadAll);
  const products = useProductStore((s) => s.products);
  useEffect(() => {
    loadAll().catch(() => {});
  }, [loadAll]);
  const accessories = useMemo(() => products.filter((p) => p.category === "accessories").slice(0, 12), [products]);
  return (
    <DesignerFlowShell title="Step 3: Accessories selection">
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {accessories.map((p) => (
          <ProductCard key={p.id} p={p} />
        ))}
      </div>
    </DesignerFlowShell>
  );
}

