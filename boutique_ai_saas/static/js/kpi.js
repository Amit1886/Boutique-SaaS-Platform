(function () {
  function fmt(n) {
    const s = Math.round(n).toString();
    return s.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  function animate(el) {
    if (el.__kpiDone) return;
    el.__kpiDone = true;

    const target = Number(el.getAttribute("data-kpi") || "0");
    const prefix = el.getAttribute("data-prefix") || "";
    const suffix = el.getAttribute("data-suffix") || "";
    const dur = Math.max(420, Math.min(1200, Number(el.getAttribute("data-dur") || "900")));

    const start = performance.now();
    const from = 0;
    function tick(t) {
      const p = Math.min(1, (t - start) / dur);
      const eased = 1 - Math.pow(1 - p, 3);
      const v = from + (target - from) * eased;
      el.textContent = prefix + fmt(v) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  const els = Array.from(document.querySelectorAll("[data-kpi]"));
  if (!els.length) return;

  const io = new IntersectionObserver(
    (entries) => {
      for (const e of entries) {
        if (e.isIntersecting) animate(e.target);
      }
    },
    { threshold: 0.35 }
  );
  els.forEach((el) => io.observe(el));
})();

