(function () {
  const overlay = document.getElementById("cmdk");
  const input = document.getElementById("cmdk-input");
  const list = document.getElementById("cmdk-list");
  const empty = document.getElementById("cmdk-empty");
  const sources = document.querySelectorAll("#cmd-sources [data-cmd]");
  if (!overlay || !input || !list || !empty || !sources.length) return;

  const items = Array.from(sources).map((el) => ({
    title: el.getAttribute("data-title") || "",
    url: el.getAttribute("data-url") || "/",
    desc: el.getAttribute("data-desc") || "",
    keywords: (el.getAttribute("data-keywords") || "").toLowerCase(),
  }));

  let open = false;
  let activeIndex = 0;
  let filtered = items.slice();

  function score(item, q) {
    if (!q) return 1;
    const t = (item.title + " " + item.desc + " " + item.keywords).toLowerCase();
    if (t.includes(q)) return 3;
    // very light fuzzy: all chars in order
    let i = 0;
    for (const ch of q) {
      i = t.indexOf(ch, i);
      if (i === -1) return 0;
      i += 1;
    }
    return 1;
  }

  function applyFilter() {
    const q = (input.value || "").trim().toLowerCase();
    filtered = items
      .map((it) => ({ it, s: score(it, q) }))
      .filter((x) => x.s > 0)
      .sort((a, b) => b.s - a.s)
      .map((x) => x.it);

    activeIndex = 0;
    render();
  }

  function render() {
    list.innerHTML = "";
    if (!filtered.length) {
      empty.classList.remove("hidden");
      return;
    }
    empty.classList.add("hidden");

    const show = filtered.slice(0, 10);
    show.forEach((it, idx) => {
      const li = document.createElement("button");
      li.type = "button";
      li.className =
        "w-full text-left rounded-xl px-3 py-2 border transition " +
        (idx === activeIndex
          ? "border-pink-300 bg-pink-50 dark:bg-white/10 dark:border-white/20"
          : "border-slate-200 bg-white/50 hover:bg-white dark:bg-white/5 dark:border-white/10");
      li.innerHTML =
        `<div class="font-semibold">${escapeHtml(it.title)}</div>` +
        `<div class="text-xs opacity-70 mt-0.5">${escapeHtml(it.desc || it.url)}</div>`;
      li.addEventListener("click", () => go(it.url));
      list.appendChild(li);
    });
  }

  function escapeHtml(s) {
    return String(s || "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;");
  }

  function setOpen(v) {
    open = v;
    overlay.classList.toggle("hidden", !open);
    document.body.classList.toggle("overflow-hidden", open);
    if (open) {
      input.value = "";
      applyFilter();
      setTimeout(() => input.focus(), 0);
    }
  }

  function go(url) {
    setOpen(false);
    window.location.href = url;
  }

  document.addEventListener("keydown", (e) => {
    const k = e.key.toLowerCase();
    const meta = e.metaKey || e.ctrlKey;

    if (meta && k === "k") {
      e.preventDefault();
      setOpen(!open);
      return;
    }
    if (!open) return;
    if (k === "escape") {
      e.preventDefault();
      setOpen(false);
      return;
    }
    if (k === "arrowdown") {
      e.preventDefault();
      activeIndex = Math.min(activeIndex + 1, Math.max(0, Math.min(filtered.length, 10) - 1));
      render();
      return;
    }
    if (k === "arrowup") {
      e.preventDefault();
      activeIndex = Math.max(activeIndex - 1, 0);
      render();
      return;
    }
    if (k === "enter") {
      e.preventDefault();
      const it = filtered[activeIndex];
      if (it) go(it.url);
    }
  });

  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) setOpen(false);
  });

  input.addEventListener("input", applyFilter);

  // Hint: open on "/" when not typing
  document.addEventListener("keydown", (e) => {
    if (open) return;
    if (e.key === "/" && !(e.target && (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA"))) {
      e.preventDefault();
      setOpen(true);
    }
  });
})();

