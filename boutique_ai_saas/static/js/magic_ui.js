(function () {
  const root = document.documentElement;
  const STORAGE_KEY = "boutique.theme";

  function setTheme(theme) {
    root.classList.toggle("dark", theme === "dark");
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch {}
  }

  function initTheme() {
    const saved = (() => {
      try {
        return localStorage.getItem(STORAGE_KEY);
      } catch {
        return null;
      }
    })();
    if (saved) return setTheme(saved);
    const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    setTheme(prefersDark ? "dark" : "light");
  }

  function addRipple(e) {
    // Ignore if user is selecting text / inputs
    const t = e.target;
    if (t && (t.closest("input,textarea,select,button,a") || t.tagName === "INPUT")) return;
    const el = document.createElement("span");
    el.className = "ripple";
    el.style.left = e.clientX + "px";
    el.style.top = e.clientY + "px";
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 700);
  }

  const LINES = [
    "Madam, aapki aura aaj pink sparkle maang rahi hai.",
    "Perfect pallu flow detected — cinematic mode ON.",
    "Aaj ka best: Wedding Season vibe + neon border.",
    "Tip: Magic Studio try karo — bilkul no-reload.",
    "Ek click me demo-flow se full testing ho jayegi.",
  ];

  function jinnSay(text) {
    let box = document.getElementById("jinn");
    if (!box) {
      box = document.createElement("div");
      box.id = "jinn";
      box.className = "jinn hide";
      box.innerHTML = `
        <div class="bubble neon-ring">
          <div style="display:flex; gap:10px; align-items:center;">
            <div style="width:42px;height:42px;border-radius:16px;background:var(--vendor-theme,#db2777);color:white;display:flex;align-items:center;justify-content:center;font-weight:900">J</div>
            <div>
              <div style="font-weight:900; letter-spacing:-0.01em">Tailor Jinn</div>
              <div style="font-size:12px; opacity:.75">Virtual assistant</div>
            </div>
          </div>
          <div id="jinnLine" style="margin-top:10px; font-size:14px; line-height:1.35"></div>
        </div>
      `;
      document.body.appendChild(box);
    }
    const line = box.querySelector("#jinnLine");
    if (line) line.textContent = text;
    box.classList.remove("hide");
    window.clearTimeout(window.__jinnTimer);
    window.__jinnTimer = window.setTimeout(() => box.classList.add("hide"), 2800);
  }

  function randomJinn() {
    const msg = LINES[Math.floor(Math.random() * LINES.length)];
    jinnSay(msg);
  }

  function initJinnTriggers() {
    document.addEventListener("click", (e) => {
      const el = e.target && e.target.closest ? e.target.closest("a,button") : null;
      if (!el) return;
      const txt = (el.textContent || "").trim().toLowerCase();
      if (txt.includes("try-on") || txt.includes("magic") || txt.includes("demo")) randomJinn();
    });
    // First nudge
    setTimeout(() => randomJinn(), 1200);
  }

  function initToggles() {
    const btn = document.querySelector("[data-theme-toggle]");
    if (!btn) return;
    btn.addEventListener("click", () => {
      const cur = root.classList.contains("dark") ? "dark" : "light";
      setTheme(cur === "dark" ? "light" : "dark");
      jinnSay(cur === "dark" ? "Light mode ON — showroom bright!" : "Dark mode ON — neon vibes!");
    });
  }

  function showLoader() {
    const el = document.getElementById("pageLoader");
    if (!el) return;
    el.classList.remove("hidden");
  }

  function hideLoader() {
    const el = document.getElementById("pageLoader");
    if (!el) return;
    el.classList.add("hidden");
  }

  function initLoader() {
    // Normal navigation
    document.addEventListener(
      "click",
      (e) => {
        const a = e.target && e.target.closest ? e.target.closest("a") : null;
        if (!a) return;
        const href = a.getAttribute("href") || "";
        if (!href || href.startsWith("#") || href.startsWith("javascript:")) return;
        if (a.getAttribute("target") === "_blank") return;
        // Only internal navigations
        if (href.startsWith("http") && !href.startsWith(window.location.origin)) return;
        showLoader();
      },
      { capture: true }
    );

    // Forms
    document.addEventListener(
      "submit",
      (e) => {
        const form = e.target;
        if (!form) return;
        showLoader();
      },
      { capture: true }
    );

    // HTMX
    document.body.addEventListener("htmx:beforeRequest", showLoader);
    document.body.addEventListener("htmx:afterRequest", hideLoader);
    document.body.addEventListener("htmx:responseError", hideLoader);
    document.body.addEventListener("htmx:sendError", hideLoader);

    window.addEventListener("pageshow", hideLoader);
  }

  initTheme();
  initToggles();
  document.addEventListener("click", addRipple, { passive: true });
  initJinnTriggers();
  initLoader();
})();
