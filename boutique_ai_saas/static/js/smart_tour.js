(function () {
  const KEY = "boutique.tour.v1.done";

  function qs(sel) {
    return document.querySelector(sel);
  }

  function getSteps() {
    const path = window.location.pathname || "/";
    if (path === "/") {
      return [
        { sel: '[data-tour="brand"]', title: "Welcome!", body: "Ctrl+K dabao aur turbo navigation use karo." },
        { sel: '[data-tour="magic"]', title: "Magic Studio", body: "Cinematic try-on experience (no-build fallback bhi hai)." },
        { sel: '[data-tour="demo"]', title: "Demo Flow", body: "One-click checklist se full testing." },
        { sel: '[data-tour="search"]', title: "Live Search", body: "Vendor name type karo — grid live update (no reload)." },
        { sel: '[data-tour="theme"]', title: "Theme Toggle", body: "Dark/Light neon vibe." },
      ];
    }
    if (path.startsWith("/demo-flow/")) {
      return [
        { sel: '[data-tour="demo-seed"]', title: "Seed Demo", body: "Ek command se sab demo users + data ready." },
        { sel: '[data-tour="demo-links"]', title: "Quick Links", body: "Poora system flow yahi se test ho jayega." },
      ];
    }
    if (path.startsWith("/vendor/")) {
      return [
        { sel: '[data-tour="kpi"]', title: "KPI Cards", body: "Animated stats — instantly business pulse." },
        { sel: '[data-tour="quicklinks"]', title: "Quick Actions", body: "Inventory, POS, Tailor tasks, Admin." },
      ];
    }
    if (path.startsWith("/accounts/dashboard/")) {
      return [
        { sel: '[data-tour="kpi"]', title: "Your KPIs", body: "Wallet, orders, looks, favorites — all at a glance." },
      ];
    }
    if (path.startsWith("/tailor/")) {
      return [
        { sel: '[data-tour="kpi"]', title: "Task Status", body: "Pending / In progress / Done — live work view." },
      ];
    }
    return [];
  }

  function canShow() {
    try {
      return localStorage.getItem(KEY) !== "1";
    } catch {
      return true;
    }
  }

  function markDone() {
    try {
      localStorage.setItem(KEY, "1");
    } catch {}
  }

  function makeEl(tag, cls) {
    const el = document.createElement(tag);
    if (cls) el.className = cls;
    return el;
  }

  function showTour(opts) {
    const steps = getSteps().filter((s) => s.sel && qs(s.sel));
    if (!steps.length) return;

    let i = 0;
    const overlay = makeEl("div", "tour-overlay");
    const hole = makeEl("div", "tour-hole");
    const tip = makeEl("div", "tour-tip glass neon-ring");
    const title = makeEl("div", "tour-title");
    const body = makeEl("div", "tour-body");
    const actions = makeEl("div", "tour-actions");
    const btnPrev = makeEl("button", "btn-secondary btn-glow text-sm");
    const btnNext = makeEl("button", "btn-primary btn-glow text-sm");
    const btnSkip = makeEl("button", "btn-secondary btn-glow text-sm");

    btnPrev.type = "button";
    btnNext.type = "button";
    btnSkip.type = "button";
    btnPrev.textContent = "Back";
    btnNext.textContent = "Next";
    btnSkip.textContent = "Skip";

    actions.appendChild(btnPrev);
    actions.appendChild(btnNext);
    actions.appendChild(btnSkip);
    tip.appendChild(title);
    tip.appendChild(body);
    tip.appendChild(actions);
    overlay.appendChild(hole);
    overlay.appendChild(tip);

    function clamp(v, a, b) {
      return Math.max(a, Math.min(b, v));
    }

    function position() {
      const s = steps[i];
      const target = qs(s.sel);
      if (!target) return;

      target.scrollIntoView({ block: "center", behavior: "smooth" });
      const r = target.getBoundingClientRect();

      hole.style.left = r.left - 6 + "px";
      hole.style.top = r.top - 6 + "px";
      hole.style.width = r.width + 12 + "px";
      hole.style.height = r.height + 12 + "px";

      const vw = window.innerWidth;
      const vh = window.innerHeight;
      const tipW = Math.min(420, vw - 28);
      tip.style.width = tipW + "px";

      const preferBelow = r.top < vh * 0.45;
      const left = clamp(r.left, 14, vw - tipW - 14);
      const top = preferBelow ? r.bottom + 14 : r.top - 14;
      tip.style.left = left + "px";
      tip.style.top = (preferBelow ? top : Math.max(14, top - tip.offsetHeight)) + "px";

      title.textContent = s.title || "Tip";
      body.textContent = s.body || "";

      btnPrev.disabled = i === 0;
      btnPrev.style.opacity = i === 0 ? "0.6" : "1";
      btnNext.textContent = i === steps.length - 1 ? "Done" : "Next";
    }

    function close(done) {
      overlay.remove();
      window.removeEventListener("resize", position);
      window.removeEventListener("scroll", position, true);
      if (done) markDone();
    }

    btnPrev.addEventListener("click", () => {
      if (i > 0) i -= 1;
      position();
    });
    btnNext.addEventListener("click", () => {
      if (i < steps.length - 1) {
        i += 1;
        position();
      } else {
        close(true);
      }
    });
    btnSkip.addEventListener("click", () => close(true));

    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) close(true);
    });

    document.body.appendChild(overlay);
    window.addEventListener("resize", position);
    window.addEventListener("scroll", position, true);
    setTimeout(position, 50);

    if (opts && opts.force) {
      // don't mark done when forced open; mark only when user clicks done/skip
    }
  }

  // Auto show on first visit
  if (canShow()) {
    setTimeout(() => showTour({ force: false }), 900);
  }

  // Restart button
  document.addEventListener("click", (e) => {
    const btn = e.target && e.target.closest ? e.target.closest("[data-tour-restart]") : null;
    if (!btn) return;
    e.preventDefault();
    try {
      localStorage.removeItem(KEY);
    } catch {}
    showTour({ force: true });
  });
})();

